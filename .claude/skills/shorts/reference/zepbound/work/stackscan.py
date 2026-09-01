#!/usr/bin/env python3
"""Does the supplement stack on the counter EVER change?

The layout decision for the whole batch turns on this. If Dan picks products up, the
counter is payload and a band layout (whole 16:9 frame preserved) earns its cost. If the
stack is static set dressing, the band shrinks him to a third of the height to show a row
of packaging nobody is looking at.

Measure, don't eyeball: sample 1 fps at 320x180, take the TEMPORAL MEDIAN of the counter
region as "the stack at rest", and report every second whose counter region departs from
it. Dan's hands crossing the region will fire too, so the region is split into a LEFT box
(the stack he never stands in front of) and a CENTRE box (the white tubs, right under his
hands) - the left box is the clean signal.
"""
import subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"
W, H = 320, 180
p = subprocess.run([FF, "-nostdin", "-v", "error", "-i", SRC, "-vf", f"fps=1,scale={W}:{H}",
                    "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
a = np.frombuffer(p.stdout, dtype=np.uint8)
n = len(a) // (W * H)
a = a[:n * W * H].reshape(n, H, W).astype(np.float32)
print(f"{n} frames sampled at 1 fps")

# counter band, measured off the frame grabs: products occupy y 0.40-0.78 of frame height
y0, y1 = int(0.40 * H), int(0.78 * H)
BOXES = {
    "left-stack  x0.00-0.28": (0.00, 0.28),
    "mid-left    x0.28-0.45": (0.28, 0.45),
    "centre-tubs x0.45-0.68": (0.45, 0.68),
    "right-AG1   x0.72-0.98": (0.72, 0.98),
}
for name, (fx0, fx1) in BOXES.items():
    box = a[:, y0:y1, int(fx0 * W):int(fx1 * W)]
    med = np.median(box, axis=0)
    d = np.abs(box - med).mean(axis=(1, 2))
    hot = np.where(d > max(3.0, np.percentile(d, 99.5)))[0]
    runs = []
    if len(hot):
        for r in np.split(hot, np.where(np.diff(hot) > 2)[0] + 1):
            runs.append(f"{r[0]}-{r[-1]}s")
    print(f"{name}: mean dev {d.mean():5.2f}  p99 {np.percentile(d,99):5.2f}  max {d.max():5.2f}"
          f"  hot: {', '.join(runs[:12]) if runs else 'none'}")
