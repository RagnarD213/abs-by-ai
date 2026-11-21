#!/usr/bin/env python3
"""Measure Muhammad's LEFT-EDGE muscle pills exactly.

They typewrite in and stack, so a single frame gives a box that is too narrow - which is how
`minX0: 540` was set and why the right edge of a pill was showing at the left edge of our crop
at 0:10 and 0:19. Scan the whole shot at 5fps and take the union.
The pill is a near-WHITE rounded rect carrying OLIVE text, on an outdoor scene.
"""
import json, subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"]).decode())['SRC']
W, H = 480, 270

def pills(t0, dur, fps=5):
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{t0:.2f}", "-i", SRC,
                        "-t", f"{dur:.2f}", "-vf", f"fps={fps},scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (W * H * 3)
    a = a[:n * W * H * 3].reshape(n, H, W, 3).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    white = (r > 232) & (g > 232) & (b > 225) & (abs(r - b) < 22) & (abs(r - g) < 14)
    olive = (abs(r - 120) < 46) & (abs(g - 140) < 46) & (abs(b - 70) < 50) & (g > b + 24)
    box = None
    for i in range(n):
        m = white[i] | olive[i]
        # a pill is a solid horizontal run in the LEFT half; sky is white but has no olive text
        rows = np.where((m[:, :W // 2].sum(1) >= 26) & (olive[i][:, :W // 2].sum(1) >= 2))[0]
        if len(rows) < 4: continue
        cols = np.where(m[np.ix_(rows, range(W // 2))].sum(0) >= max(3, len(rows) * 0.30))[0]
        if len(cols) < 12: continue
        bb = (cols[0] / W, cols[-1] / W, rows[0] / H, rows[-1] / H)
        box = bb if box is None else (min(box[0], bb[0]), max(box[1], bb[1]),
                                      min(box[2], bb[2]), max(box[3], bb[3]))
    return box

man = json.load(open('shots/manifest.json'))
for m in man:
    if not m['name'].startswith('B-p0-s0'): continue
    b = pills(m['absStart'], m['dur'])
    if not b: print(f"{m['name']:12s} {m['absStart']:7.2f}+{m['dur']:5.1f}  no left pill"); continue
    print(f"{m['name']:12s} {m['absStart']:7.2f}+{m['dur']:5.1f}  pill x {b[0]:.3f}-{b[1]:.3f} "
          f"({b[0]*1920:.0f}-{b[1]*1920:.0f}px)  y {b[2]:.3f}-{b[3]:.3f}")
