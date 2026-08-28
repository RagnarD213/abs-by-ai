#!/usr/bin/env python3
"""THE WATCH PASS for longform — the delivery gate the metrics cannot fake.

`qc_style.py` measures the finished file and still cannot see a black frame at a splice,
a segment that froze, a graphic that rendered but never composited, or an animation that
plays at the wrong time. The ad pipeline learned this the expensive way: attempt 2 passed
15/15 and Dan found 13 problems, eight of which a human sees in one viewing.

Three things, all on the EXACT file being delivered:

  1. FULL-FRAME SCAN, every frame, streamed (a 53-minute programme is 96k frames — held
     as an array that is 2 GB, so it is computed incrementally instead): black frames,
     frozen runs, and frame-to-frame jumps far above the file's own noise level that do
     not sit at a boundary the plan knows about.
  2. GRAPHIC PRESENCE, at full resolution: for every declared graphic window, is the
     picture actually different from the same timecode in the pre-graphics source? A
     graphic that renders to an .mov and never reaches the picture is invisible to every
     other check. This is the check that would have caught the ad pipeline's
     "all 7 lower thirds, all 3 CTA pills and all 11 flashes were invisible".
  3. BOUNDARY STRIPS: consecutive frames spanning each change, written as contact sheets
     so a jump cut, a frozen beat or a mistimed animation is visible by eye.

usage:
  watch_longform.py FINAL.mp4 [--base NO-GRAPHICS.mp4] [--spec spec.py-importable]
                    [--out watch] [--strips N]
"""
import argparse, json, math, os, subprocess, sys
from pathlib import Path
import numpy as np

FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")
SW, SH = 96, 54


def probe_fps_dur(v):
    r = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=r_frame_rate", "-of", "csv=p=0", v],
                       capture_output=True, text=True).stdout.strip()
    num, den = r.split("/")
    fps = int(num) / int(den)
    dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", v], capture_output=True,
                               text=True).stdout.strip())
    return fps, dur


def scan(video, fps):
    """Stream every frame at 96x54 grey. Returns (n, diffs, lums)."""
    p = subprocess.Popen([FF, "-v", "error", "-i", video, "-vf",
                          f"scale={SW}:{SH},format=gray", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE, bufsize=SW * SH * 64)
    n = SW * SH
    prev, diffs, lums, k = None, [], [], 0
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n: break
        f = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        lums.append(float(f.mean()))
        if prev is not None: diffs.append(float(np.abs(f - prev).mean()))
        prev = f; k += 1
    p.stdout.close(); p.wait()
    return k, np.array(diffs), np.array(lums)


def analyse(nfr, d, lum, fps, known, frozen_min=1.2):
    med = float(np.median(d)) if len(d) else 0.0
    mad = float(np.median(np.abs(d - med))) or 0.05
    frozen, i = [], 0
    while i < len(d):
        if d[i] < 0.05:
            j = i
            while j < len(d) and d[j] < 0.05: j += 1
            if (j - i) / fps >= frozen_min: frozen.append([round(i / fps, 2), round((j - i) / fps, 2)])
            i = j
        else: i += 1
    black = [round(k / fps, 2) for k, v in enumerate(lum) if v < 3.0]
    kn = set()
    for t in known:
        kn.update(range(int((t - 0.30) * fps), int((t + 0.30) * fps) + 1))
    thr = max(med + 10 * mad, med * 8)
    hits = sorted(k for k in range(len(d)) if d[k] > thr and k not in kn)
    # merge consecutive frames into ONE event: a dissolve, a wipe-on graphic and a fast
    # motion passage all trip the threshold on every frame they last, and eighty
    # "unexplained jumps" that are really one 0.4 s animation is noise, not a finding.
    jumps, run = [], []
    for k in hits:
        if run and k - run[-1] <= max(2, int(0.40 * fps)): run.append(k)
        else:
            if run: jumps.append([round(run[0] / fps, 2), round(float(max(d[j] for j in run)), 2),
                                  round((run[-1] - run[0] + 1) / fps, 2)])
            run = [k]
    if run: jumps.append([round(run[0] / fps, 2), round(float(max(d[j] for j in run)), 2),
                          round((run[-1] - run[0] + 1) / fps, 2)])
    return dict(frames=nfr, median_diff=round(med, 3), threshold=round(thr, 3),
                frozen=frozen, black_frames=len(black),
                black_times=black[:40], jumps=sorted(jumps)[:80])


def graphic_presence(final, base, windows, fps):
    """At full resolution, is the graphic actually IN the picture?"""
    out = []
    for (key, a, b) in windows:
        t = a + (b - a) * 0.62
        fa = grab(final, t); fb = grab(base, t)
        if fa is None or fb is None:
            out.append({"key": key, "t": round(t, 2), "delta": None, "present": False}); continue
        delta = float(np.abs(fa.astype(float) - fb.astype(float)).mean())
        out.append({"key": key, "t": round(t, 2), "delta": round(delta, 3),
                    "present": bool(delta > 0.5)})
    return out


def grab(v, t, w=480, h=270):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1",
                          "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    if len(raw) < w * h: return None
    return np.frombuffer(raw[:w * h], dtype=np.uint8).reshape(h, w)


def strips(video, times, outdir, fps, n=8):
    """A strip of CONSECUTIVE frames spanning each boundary — the only thing that
    exposes a jump cut or a frozen beat by eye."""
    from PIL import Image
    outdir.mkdir(parents=True, exist_ok=True)
    made = []
    for t in times:
        ss = max(0.0, t - (n // 2) / fps)
        raw = subprocess.run([FF, "-v", "error", "-ss", f"{ss:.3f}", "-i", video,
                              "-frames:v", str(n), "-vf", "scale=320:180",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        k = 320 * 180 * 3
        got = len(raw) // k
        if got < 2: continue
        sheet = Image.new("RGB", (320 * got, 180))
        for i in range(got):
            sheet.paste(Image.frombytes("RGB", (320, 180), raw[i * k:(i + 1) * k]), (320 * i, 0))
        p = outdir / f"b_{t:08.2f}.jpg"
        sheet.save(p, quality=88)
        made.append(str(p))
    return made


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--base", help="the pre-graphics picture, for the presence check")
    ap.add_argument("--windows", help="json [[key,a,b],...] of declared graphic windows")
    ap.add_argument("--known", help="json [t,...] of boundaries the plan knows about")
    ap.add_argument("--out", default="watch")
    ap.add_argument("--strips", type=int, default=40)
    A = ap.parse_args()

    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    fps, dur = probe_fps_dur(A.video)
    known = json.load(open(A.known)) if A.known else []
    print(f"scanning {dur:.1f}s at {fps:.3f} fps ...")
    nfr, d, lum = scan(A.video, fps)
    rep = analyse(nfr, d, lum, fps, known)
    print(f"  {rep['frames']} frames  median diff {rep['median_diff']}  "
          f"threshold {rep['threshold']}")
    print(f"  black frames {rep['black_frames']}   frozen runs >=1.2s: {len(rep['frozen'])}")
    for f in rep["frozen"][:12]: print(f"     frozen {f[0]:.2f}s for {f[1]:.2f}s")
    print(f"  unexplained jumps: {len(rep['jumps'])}")
    for j in rep["jumps"][:16]: print(f"     jump {j[0]:.2f}s  peak {j[1]}  lasts {j[2]}s")

    if A.windows and not known:
        known = [w[1] for w in json.load(open(A.windows))] + \
                [w[2] for w in json.load(open(A.windows))]
        rep = analyse(nfr, d, lum, fps, known)
        print(f"  re-analysed with {len(known)} declared graphic boundaries: "
              f"{len(rep['jumps'])} jump events remain")
    if A.base and A.windows:
        W = json.load(open(A.windows))
        pres = graphic_presence(A.video, A.base, W, fps)
        rep["graphics"] = pres
        missing = [p for p in pres if not p["present"]]
        print(f"  graphics present {len(pres)-len(missing)}/{len(pres)}")
        for m in missing: print(f"     MISSING {m['key']} at {m['t']}s delta={m['delta']}")

    # strips at the biggest changes plus every declared boundary
    ts = sorted(set([j[0] for j in rep["jumps"][:A.strips]] +
                    [round(t, 2) for t in known][:A.strips]))
    rep["strips"] = strips(A.video, ts, out / "strips", fps)
    print(f"  wrote {len(rep['strips'])} boundary strips -> {out/'strips'}")
    json.dump(rep, open(out / "watch_pass.json", "w"), indent=1)
    print("->", out / "watch_pass.json")
