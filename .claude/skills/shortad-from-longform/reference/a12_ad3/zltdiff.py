#!/usr/bin/env python3
"""Prove that a re-render changed ONLY the lower-third windows.

After a graphics-only fix the picture must be identical everywhere else. This walks both renders
frame by frame and reports every frame whose pixels differ, then checks that each differing frame
falls inside one of the beat sheet's `lt` windows (plus its fade-out tail).

Why it matters: the watch pass is the gate, and the gate has to be done on the EXACT delivered file.
If the only changed frames are the lower-third windows, re-watching those boundaries is a complete
watch pass for the new file; if anything else moved, the whole pass has to be redone.

    python3 zltdiff.py old.mp4 new.mp4
"""
import subprocess, sys, numpy as np
sys.path.insert(0, ".")
from beats import OVERLAYS as OV, FPS                     # the beat sheet is the authority on the windows

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W, H = 1080, 1920
CHUNK = 40


def reader(path):
    p = subprocess.Popen([FF, "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         stdout=subprocess.PIPE)
    need = W * H
    while True:
        buf = p.stdout.read(need * CHUNK)
        if not buf:
            break
        n = len(buf) // need
        if n == 0:
            raise RuntimeError(f"short read from {path}: {len(buf)} bytes")
        yield np.frombuffer(buf[:n * need], dtype=np.uint8).reshape(n, H, W)
    p.stdout.close(); p.wait()


def main(old, new):
    windows, why = [], {}
    for o in OV:
        if o.get('kind') == 'lt':
            w = (o['n0'] - 2, o['n1'] + 6)                   # + the 3-frame fade-out and a margin
            windows.append(w); why[w] = 'lower third'
    from beats import T as BEATS
    for b in BEATS:                                          # the other two fixes, from the beat sheet itself
        if b[0] == 'photoseq':
            w = (b[1] - 2, b[2] + 2); windows.append(w); why[w] = 'photo-shoot stills (real-picture label)'
        if b[0] == 'phonecard' and b[1] == 5278:
            w = (b[1] - 2, b[2] + 2); windows.append(w); why[w] = 'app-upload card (stranger photo)'
    changed, maxdiff = [], {}
    n = 0
    for a, b in zip(reader(old), reader(new)):
        m = min(len(a), len(b))
        d = np.abs(a[:m].astype(np.int16) - b[:m].astype(np.int16)).max(axis=(1, 2))
        for i in range(m):
            if d[i] > 0:
                changed.append(n + i); maxdiff[n + i] = int(d[i])
        n += m
    print(f"frames compared     : {n}")
    print(f"frames that changed : {len(changed)}")
    if not changed:
        print("NOTHING CHANGED -- the fix did not reach the render."); return 1
    outside = [f for f in changed
               if not any(w0 <= f <= w1 for w0, w1 in windows)]
    lo, hi = min(changed), max(changed)
    print(f"changed range       : {lo} ({lo/FPS:.2f}s) .. {hi} ({hi/FPS:.2f}s)")
    per = []
    for w in sorted(windows):
        w0, w1 = w
        c = [f for f in changed if w0 <= f <= w1]
        per.append(f"  {w0+2:5d}-{w1:5d} ({(w0+2)/FPS:7.2f}s) {why[w]:38s}: {len(c):4d} frames changed, "
                   f"peak |diff| {max([maxdiff[f] for f in c], default=0)}")
    print("per expected window:"); print("\n".join(per))
    if outside:
        print(f"\nFAIL  {len(outside)} changed frames OUTSIDE every expected window -- "
              f"the picture moved, re-watch the whole file")
        print("      first 20:", [f"{f} ({f/FPS:.2f}s)" for f in outside[:20]])
        return 1
    print("\nPASS  every changed frame is inside an expected window; "
          "re-watching those boundaries covers the new file")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
