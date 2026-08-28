#!/usr/bin/env python3
"""Measure the bounding box of Muhammad's burned olive graphics in a shot.

His lower thirds and top pills are drawn in the brand olive (~(140,152,88)) with white
text, and they TYPEWRITE in, so the box is only at full width part-way through the shot.
Sampling one frame gives a box that is too narrow and the crop then slices it. Scan the
whole shot at 4 fps and take the UNION.
"""
import subprocess, sys, json
import numpy as np
from PIL import Image
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "../mrepro/ref_hd.mp4"

def boxes(t0, dur, fps=4):
    n = max(1, int(dur * fps))
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{t0:.2f}", "-i", SRC,
                        "-t", f"{dur:.2f}", "-vf", f"fps={fps},scale=480:270",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    a = a[:(len(a) // (480 * 270 * 3)) * 480 * 270 * 3].reshape(-1, 270, 480, 3).astype(np.int16)
    # brand olive, generous tolerance; his boxes are semi-transparent over the scene
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (abs(r - 140) < 46) & (abs(g - 152) < 46) & (abs(b - 88) < 52) & (g > r) & (g > b + 28)
    # also the near-white pill background used on the top pills
    m |= (r > 225) & (g > 225) & (b > 218) & (abs(r - b) < 26)
    out = []
    for i in range(m.shape[0]):
        mi = m[i]
        # a graphic is a wide horizontal run; require >=90 of 480 px on a row
        rows = np.where(mi.sum(1) >= 90)[0]
        if len(rows) < 6: out.append(None); continue
        cols = np.where(mi[rows].sum(0) >= max(4, len(rows) * 0.35))[0]
        if len(cols) < 40: out.append(None); continue
        out.append((cols[0] / 480, cols[-1] / 480, rows[0] / 270, rows[-1] / 270))
    return out

for name, t0, dur in json.load(open(sys.argv[1])):
    bs = [b for b in boxes(t0, dur) if b]
    if not bs:
        print(f"{name:12s} {t0:7.1f}+{dur:5.1f}  no burned graphic"); continue
    x0 = min(b[0] for b in bs); x1 = max(b[1] for b in bs)
    y0 = min(b[2] for b in bs); y1 = max(b[3] for b in bs)
    print(f"{name:12s} {t0:7.1f}+{dur:5.1f}  x {x0:.3f}-{x1:.3f}  y {y0:.3f}-{y1:.3f}"
          f"   ({len(bs)} of {len(boxes(t0,dur))} sampled frames)")
