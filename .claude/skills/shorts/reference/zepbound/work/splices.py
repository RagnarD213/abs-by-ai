#!/usr/bin/env python3
"""Frame-accurate picture-splice table for the clean master.

The EDL cumsum is systematically EARLY by a monotonically growing amount (+0.036s at the
first cut, +1.137s at the last) - render.py rounds every one of the 62 segments to whole
frames and the error accumulates, which is exactly the trap the skill records from the
spray-tan build. It totals the 1.149s by which the EDL undershoots the master.

So each boundary is MEASURED, not predicted: a full-frame-rate frame-difference peak inside
a window around the prediction. The window is half the shorter neighbouring range so a
short beat cannot capture its neighbour's cut (ginger-b did exactly that at +/-2.5s).
"""
import json, subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"
FPS = 30000 / 1001
W, H = 320, 180

def peak(t, win):
    t0 = max(0.0, t - win)
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{t0:.3f}", "-i", SRC,
                        "-t", f"{2*win:.3f}", "-vf", f"scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (W * H)
    a = a[:n*W*H].reshape(n, H, W).astype(np.float32)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    k = int(np.argmax(d))
    return t0 + (k + 1) / FPS, float(d[k]) / max(0.05, float(np.median(d)))

rows = json.load(open('work/edl_splices.json'))
out = []
prev_m = 0.0
for i, r in enumerate(rows):
    if i == 0:
        out.append({**r, 'cut': 0.0, 'ratio': None}); prev_m = 0.0; continue
    lo = rows[i-1]['dur']; hi = r['dur']
    win = max(0.6, min(2.5, 0.45 * min(lo, hi)))
    m, ratio = peak(r['outFrame'], win)
    if m <= prev_m + 0.2:                       # captured the previous cut - retry tighter
        m, ratio = peak(r['outFrame'], 0.6)
    out.append({**r, 'cut': round(m, 3), 'ratio': round(ratio, 1)})
    prev_m = m

# The correction must be monotonic: a later cut can never precede an earlier one, and the
# rounding error only ever grows. Assert it rather than eyeball the column.
d = [o['cut'] - o['outFrame'] for o in out[1:]]
assert all(d[i] >= d[i-1] - 0.05 for i in range(1, len(d))), 'offset is not monotonic'
weak = [o['beat'] for o in out[1:] if o['ratio'] < 3.0]
json.dump(out, open('work/splices.json', 'w'), indent=1)
print(f"{len(out)} cuts. offset {d[0]:+.3f} -> {d[-1]:+.3f}s, monotonic. "
      f"weakest peak {min(o['ratio'] for o in out[1:]):.1f}x. "
      f"{'weak: ' + ', '.join(weak) if weak else 'no weak boundaries'}")
