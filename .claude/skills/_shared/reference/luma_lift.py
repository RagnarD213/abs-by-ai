#!/usr/bin/env python3
"""THE TALKING-HEAD BRIGHTNESS, matched to Muhammad's by measurement, not by eye.

He is ~6 luma brighter on the talking head than our grades (picture.json `talking_head_luma`: his Ad 1 66.2,
Ad 2 72.0 on the watch scan's frame-mean gray; the handoff measured ours at ~55). This tool closes that gap with
a SHADOW LIFT appended after the grade -- a curve pinned at 0/0 and 1/1 (true black stays black, white does not
move) that raises the quarter-tones most, the mids less and the highlights least -- sized by measurement:

  1. sample frames of the graded talking head (the 16:9 base, the same frame the reference was measured on);
  2. find the lift d whose result puts the median frame-mean luma on HIS centre (the mean of his two edits),
     never past his `hi` (overshooting a reference is a warning, not a win: memory audio-never-over-strip);
  3. do-no-harm: refuse a lift that grows the clipped-highlight share (>= 250) by more than 1 point;
  4. verify the chosen filter through ffmpeg itself and write the record.

  python3 luma_lift.py measure --src base.mp4 [--grade grade.py] [--span 0,60] [--edl edl.json]
  python3 luma_lift.py solve   --src RAW --grade grade.py [--edl edl.json | --span t0,t1] [--out lift.json]
  -> prints the filter to append:  <grade>,curves=all='0/0 0.25/0.3 0.5/0.535 0.75/0.768 1/1'

Instrument: the watch scan's (`checks/picture.py`, 160x90 gray, frame mean), median over the sampled frames.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
sys.path.insert(0, os.path.join(HERE, "..", "cut"))
from piccuts import grade_filter, load_edl  # noqa: E402

W, H = 160, 90
SHAPE = (0.25, 1.0), (0.5, 0.7), (0.75, 0.35)         # knot x, share of d: the quarter-tones lift most
D_MAX = 0.15
CLIP_GROWTH_MAX = 0.01


def ref_band():
    ref = json.load(open(os.path.join(HERE, "picture.json")))["numbers"]["talking_head_luma"]
    return dict(centre=round((ref["ad1"] + ref["ad2"]) / 2, 2), lo=ref["lo"], hi=ref["hi"], his=[ref["ad1"], ref["ad2"]])


def lift_filter(d):
    pts = " ".join(f"{x}/{min(1.0, x + s * d):.4f}" for x, s in SHAPE)
    return f"curves=all='0/0 {pts} 1/1'"


def times_for(src, span=None, edl=None, n=48):
    if edl:
        E = load_edl(edl)
        tot = sum(s["src_out"] - s["src_in"] for s in E)
        ts, acc, step = [], 0.0, tot / n
        for s in E:
            d = s["src_out"] - s["src_in"]
            q = (step / 2 - acc) % step
            while q < d:
                ts.append((s.get("roll"), s["src_in"] + q))
                q += step
            acc += d
        return ts
    t0, t1 = span
    return [(None, t0 + (i + 0.5) * (t1 - t0) / n) for i in range(n)]


def frames(src, ts, vf, rolls=None):
    """One RGB frame per sample time (frame-snapped seek), through vf, at 160x90."""
    out = []
    for roll, t in ts:
        s = (rolls or {}).get(roll, src) if roll else src
        t = round(t * 30000 / 1001) / (30000 / 1001)
        cmd = [FF, "-nostdin", "-v", "error", "-ss", f"{t:.4f}", "-i", s, "-frames:v", "1",
               "-vf", f"{vf + ',' if vf else ''}scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        b = subprocess.run(cmd, capture_output=True).stdout
        if len(b) == W * H * 3:
            out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    return np.array(out)


def luma(rgb):
    """ffmpeg's rgb24 -> gray (BT.601 weights), frame mean, median over frames; and the clipped share."""
    y = rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114
    return float(np.median(y.reshape(len(y), -1).mean(1))), float((y >= 250).mean())


def lut(d):
    """The lift curve as a 256-entry LUT (natural cubic spline, ffmpeg curves' default interpolation)."""
    from scipy.interpolate import CubicSpline
    xs = [0.0] + [x for x, _ in SHAPE] + [1.0]
    ys = [0.0] + [min(1.0, x + s * d) for x, s in SHAPE] + [1.0]
    cs = CubicSpline(xs, ys, bc_type="natural")
    return np.clip(np.round(cs(np.arange(256) / 255.0) * 255), 0, 255).astype(np.uint8)


def solve(src, grade, ts, rolls=None, log=print):
    band = ref_band()
    base = frames(src, ts, grade, rolls)
    if not len(base):
        raise SystemExit("no frames sampled")
    l0, c0 = luma(base)
    log(f"graded talking head: luma {l0:.1f} (his {band['his'][0]:.1f} / {band['his'][1]:.1f}, band {band['lo']:.1f}-"
        f"{band['hi']:.1f}); clipped {c0:.2%}")
    rec = dict(before=dict(luma=round(l0, 2), clipped=round(c0, 4)), reference=band, frames=len(base))
    if l0 >= band["centre"]:
        rec.update(d=0.0, filter=None, verdict="no lift: already at or above his centre (never darken toward it here)")
        log(rec["verdict"])
        return rec
    lo, hi = 0.0, D_MAX
    for _ in range(14):
        mid = (lo + hi) / 2
        l, _ = luma(lut(mid)[base])
        lo, hi = (mid, hi) if l < band["centre"] else (lo, mid)
    d = round(lo, 4)
    lf, cf = luma(lut(d)[base])
    if cf - c0 > CLIP_GROWTH_MAX:                        # do no harm: back off until the highlights hold
        while d > 0 and luma(lut(d)[base])[1] - c0 > CLIP_GROWTH_MAX:
            d = round(d - 0.005, 4)
    f = lift_filter(d)
    real = frames(src, ts, f"{grade},{f}" if grade else f, rolls)
    lr, cr = luma(real)
    over = lr > band["hi"]
    rec.update(d=d, filter=f, after=dict(luma=round(lr, 2), clipped=round(cr, 4), simulated=round(lf, 2)),
               verdict=("OVERSHOOT -- do not use" if over else
                        "PASS" if band["lo"] <= lr <= band["hi"] else "SHORT -- lift capped (D_MAX or highlights)"))
    log(f"lift d={d}: luma {l0:.1f} -> {lr:.1f} (target {band['centre']}), clipped {c0:.2%} -> {cr:.2%}  {rec['verdict']}")
    log(f"append to the grade:  {f}")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("measure", "solve"):
        p = sub.add_parser(name)
        p.add_argument("--src", required=True)
        p.add_argument("--rolls")
        p.add_argument("--grade")
        p.add_argument("--span", help="t0,t1 seconds")
        p.add_argument("--edl")
        p.add_argument("--n", type=int, default=48)
        p.add_argument("--out")
    a = ap.parse_args()
    rolls = json.load(open(a.rolls)) if a.rolls else None
    span = tuple(float(x) for x in a.span.split(",")) if a.span else None
    if not span and not a.edl:
        span = (0.0, float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                                           "format=duration", "-of", "csv=p=0", a.src], capture_output=True, text=True).stdout))
    ts = times_for(a.src, span, a.edl, a.n)
    g = grade_filter(a.grade)
    if a.cmd == "measure":
        l, c = luma(frames(a.src, ts, g, rolls))
        rec = dict(luma=round(l, 2), clipped=round(c, 4), reference=ref_band())
        print(json.dumps(rec))
    else:
        rec = solve(a.src, g, ts, rolls)
    if a.out:
        json.dump(rec, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
