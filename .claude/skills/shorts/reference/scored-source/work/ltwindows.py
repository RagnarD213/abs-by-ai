#!/usr/bin/env python3
"""When is a burned lower third actually on screen?

Treating a whole 12s or 27s shot as "carries a lower third" costs the stage 168px of height
for the entire shot when the graphic is only up for three seconds of it. Measure the real
window at 10 fps so the shot can be split.

Detection is on the lower-third BAND only (rows 700-1010) and needs a wide, flat, horizontal
run of either the olive fill or the near-white pill - a sky or a pool never produces one.
"""
import subprocess, sys, json
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Organic Videos/Daniel Organic Video -The $17 Ab Wheel Beats Every Crunch-v2 HD.mp4"
W, H = 480, 270
R0, R1 = (round(0/1080*H), round(230/1080*H)) if len(sys.argv)>2 else (round(700/1080*H), round(1010/1080*H))

def windows(t0, dur, fps=10):
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{t0:.2f}", "-i", SRC,
                        "-t", f"{dur:.2f}", "-vf", f"fps={fps},scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (W * H * 3)
    a = a[:n * W * H * 3].reshape(n, H, W, 3).astype(np.int16)[:, R0:R1]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    olive = (abs(r - 120) < 40) & (abs(g - 138) < 40) & (abs(b - 68) < 46)
    white = (r > 218) & (g > 218) & (b > 205) & (abs(r - b) < 34)
    fill = olive | white
    # THE DISCRIMINATOR. A bright sky fills the top band with near-white just as a pill does,
    # which made the first version report a graphic across every outdoor shot. A pill also
    # carries TEXT: dark or olive glyphs inside the same rows as the fill. Require both.
    luma = (r * 299 + g * 587 + b * 114) // 1000
    ink = (luma < 150) & ~olive
    rowhit = (fill.sum(2) >= W * 0.35) & (ink.sum(2) >= W * 0.02) & (ink.sum(2) <= W * 0.55)
    on = rowhit.sum(1) >= 6
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= 2: out.append([round(t0 + s / fps, 2), round(t0 + i / fps, 2)])
            s = None
    if s is not None: out.append([round(t0 + s / fps, 2), round(t0 + len(on) / fps, 2)])
    return out

for name, t0, dur in json.load(open(sys.argv[1])):
    print(f"{name:12s} {t0:7.2f}+{dur:5.1f}  ->  {windows(t0, dur)}")
