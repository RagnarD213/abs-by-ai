#!/usr/bin/env python3
"""DEAD AIR TO ~ZERO, EVERY REMOVAL PAIRED WITH A PICTURE CUT. Shared by every video skill.

Dan: "Remove every pause longer than ~0.3 s. Zero dead air (reference edit had none)." His reference cuts and
Waleed's round 1 measure zero dead air; the spray-tan long-form shipped 36 % against a 23 % target.

Two counter-measurements this tool honours:
  * A pause removal is itself as visible as the fault it fixes: 4.97-12.46 against a 1.30 adjacent-frame
    baseline (shorts/.../pausejump.py). So every removal becomes a splice that `piccuts.py` decides like any
    other: the picture cuts on the head-matched frame within +-15, and a join whose head still jumps past the
    calibrated bound is flagged `cover` + `watch` for the render's push or an insert. No removal ships bare.
  * 0.55-0.65 s is breathing rhythm, not dead air (shorts/SKILL.md Step 4.5). The shorts preset never touches
    a pause under 0.66 s. Nothing is removed outright: every pause keeps a tail after the outgoing word and a
    head before the incoming one (a soft onset is protected).

Silence is the 5 ms RMS envelope of the REAL audio, never Whisper's word times (ad-edit lesson 20).

Presets (measured where each pipeline already runs):
  ad       min 0.22 s, keep 0.055 + 0.100   ad-edit/reference/modern60/tight.py
  website  min 0.30 s, keep 0.12 + 0.18     website-video/reference/recipe/tight.py (the trust cut, calmer)
  shorts   min 0.66 s, keep 0.12 + 0.18     shorts Step 4.5: 0.55-0.65 s is breath, leave it

  python3 deadair.py --edl edl.json --raw ROLL [--rolls rolls.json] [--astream 0:a:0] [--pan mean|c0|c1]
                     --preset ad|website|shorts --out DIR [--pair --grade grade.py] [--hook-safe 3.0]
  -> DIR/edl_tight.json (the audio EDL, every pause removal a new splice marked join: "deadair"),
     DIR/deadair_report.json (dead air before/after, every removal),
     with --pair: DIR/piccuts.json + DIR/edl_picture.json (piccuts decided on the new joins only)
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import piccuts  # noqa: E402

FF = piccuts.FF
FPS = piccuts.FPS
SR = 16000
HOP = 0.005
SIL_DB = -40.0
DEAD_MIN = 0.30                                        # what counts as dead air in the report (Dan's ~0.3 s)
PRESETS = dict(ad=dict(min_sil=0.22, keep_tail=0.055, keep_head=0.100, min_remove=0.06),
               website=dict(min_sil=0.30, keep_tail=0.12, keep_head=0.18, min_remove=0.08),
               shorts=dict(min_sil=0.66, keep_tail=0.12, keep_head=0.18, min_remove=0.08))


def snap(t):
    return round(t * FPS) / FPS


def envelope(src, t0, t1, astream="0:a:0", pan="mean"):
    """5 ms RMS in dBFS over [t0, t1) of the source audio."""
    ch = {"mean": "pan=mono|c0=0.5*c0+0.5*c1", "c0": "pan=mono|c0=c0", "c1": "pan=mono|c0=c1"}[pan]
    cmd = [FF, "-nostdin", "-v", "error", "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", src, "-map", astream,
           "-af", ch, "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
    if pan == "mean" and not len(x):                    # a mono stream: pan to c1 fails, read it straight
        cmd[cmd.index("-af") + 1] = "anull"
        x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
    h = int(SR * HOP)
    n = len(x) // h
    rms = np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms)


def runs_below(db, thr, min_len):
    out, cur = [], None
    for i, v in enumerate(db):
        if v < thr:
            cur = (cur[0], i) if cur else (i, i)
        elif cur:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return [(a * HOP, (b + 1) * HOP) for a, b in out if (b - a + 1) * HOP >= min_len]


def tighten(E, raw, rolls=None, astream="0:a:0", pan="mean", preset="ad", hook_safe=0.0, log=print):
    """Split every segment at its internal pauses. Returns (new EDL, removals, dead-air stats)."""
    P = PRESETS[preset]
    rolls = rolls or {}
    out, removals = [], []
    dead_before = dead_after = total_before = 0.0
    for seg in E:
        src = rolls.get(seg.get("roll"), raw) if seg.get("roll") else raw
        a, b = seg["src_in"], seg["src_out"]
        db = envelope(src, a, b, astream, pan)
        total_before += b - a
        dead = [(x, y) for x, y in runs_below(db, SIL_DB, DEAD_MIN) if x > 0 and y < (b - a) - HOP]   # internal only
        dead_before += sum(y - x for x, y in dead)
        cuts = []
        for s0, s1 in runs_below(db, SIL_DB, P["min_sil"]):
            if s0 <= 0 or s1 >= (b - a) - HOP:          # a pause touching the segment edge is the EDL's business
                continue
            ci, co = snap(a + s0 + P["keep_tail"]), snap(a + s1 - P["keep_head"])
            if co - ci < P["min_remove"] or seg["cut_in"] + (ci - a) < hook_safe:
                continue
            cuts.append((ci, co))
        # the kept pieces of this segment
        pieces, t = [], a
        for ci, co in cuts:
            pieces.append((t, ci))
            removals.append(dict(roll=seg.get("roll"), src_out=round(ci, 4), src_in=round(co, 4), removed=round(co - ci, 3)))
            t = co
        pieces.append((t, b))
        for j, (x, y) in enumerate(pieces):
            out.append(dict(src_in=x, src_out=y, roll=seg.get("roll"), join="deadair" if j > 0 else seg.get("join")))
        # dead air left after the cut: every removed pause keeps keep_tail + keep_head
        for x, y in dead:
            ax, ay = a + x, a + y
            kept = ay - ax - sum(max(0.0, min(ay, co) - max(ax, ci)) for ci, co in cuts)
            if kept >= DEAD_MIN:
                dead_after += kept
    t = 0.0
    for i, s in enumerate(out):
        d = snap(s["src_out"]) - snap(s["src_in"])
        s.update(i=i, cut_in=round(t, 6), cut_out=round(t + d, 6))
        t += d
    stats = dict(preset=preset, params=P, removals=len(removals), removed_s=round(sum(r["removed"] for r in removals), 2),
                 dur_before=round(total_before, 2), dur_after=round(t, 2),
                 dead_air_before=round(dead_before / max(total_before, 1e-6), 4),
                 dead_air_after=round(dead_after / max(t, 1e-6), 4),
                 dead_air_rule=f"internal silence runs >= {DEAD_MIN} s below {SIL_DB} dBFS (5 ms RMS), share of runtime")
    log(f"{len(removals)} pauses shortened ({stats['removed_s']} s); dead air {stats['dead_air_before']:.1%} -> "
        f"{stats['dead_air_after']:.1%}; {stats['dur_before']} s -> {stats['dur_after']} s")
    return out, removals, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--edl", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--rolls")
    ap.add_argument("--astream", default="0:a:0")
    ap.add_argument("--pan", default="mean", choices=["mean", "c0", "c1"])
    ap.add_argument("--preset", required=True, choices=sorted(PRESETS))
    ap.add_argument("--hook-safe", type=float, default=0.0, help="no pause cut before this programme time (s)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pair", action="store_true", help="decide the picture cut of every new join (piccuts.py)")
    ap.add_argument("--grade")
    ap.add_argument("--cover-below", type=float, default=0.44)
    a = ap.parse_args()
    E = piccuts.load_edl(a.edl)
    rolls = json.load(open(a.rolls)) if a.rolls else {}
    os.makedirs(a.out, exist_ok=True)
    T, removals, stats = tighten(E, a.raw, rolls, a.astream, a.pan, a.preset, a.hook_safe,
                                 log=lambda s: print(s, flush=True))
    json.dump(T, open(os.path.join(a.out, "edl_tight.json"), "w"), indent=1)
    rep = dict(stats=stats, removals=removals)
    if a.pair:
        new = {s["i"] for s in T if s.get("join") == "deadair"}
        dec = piccuts.decide(T, None, raw=a.raw, rolls=rolls, grade=piccuts.grade_filter(a.grade), mode="raw",
                             cover_below=a.cover_below, only=new, log=lambda s: print(s, flush=True))
        json.dump(dec, open(os.path.join(a.out, "piccuts.json"), "w"), indent=1)
        json.dump(piccuts.picture_edl(T, dec), open(os.path.join(a.out, "edl_picture.json"), "w"), indent=1)
        rep["paired"] = dict(joins=len(new), decided=len(dec), moved=sum(1 for r in dec if r["k"]),
                             cover=sum(1 for r in dec if r.get("cover")),
                             head_at_0_median=float(np.median([r["head_at_0"] for r in dec if r.get("head_at_0") is not None] or [np.nan])),
                             head_at_k_median=float(np.median([r["head_at_k"] for r in dec if r.get("head_at_k") is not None] or [np.nan])))
        print(f"paired: {len(dec)} of {len(new)} new joins decided, {rep['paired']['moved']} moved off the audio, "
              f"{rep['paired']['cover']} flagged cover + watch", flush=True)
    json.dump(rep, open(os.path.join(a.out, "deadair_report.json"), "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
