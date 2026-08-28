#!/usr/bin/env python3
"""Verify every shot boundary against a full-frame-rate frame-difference peak.

detect-shots.js downscales to 320x180 and thresholds `scene`, which is cheap and finds the
right cuts but can land one up to ~0.6s early when the outgoing shot is already changing
(a push-in, a whip). That matters here because the treatment is per SHOT: a boundary 0.6s
early gave 18 frames of GYM B-ROLL a talking-head crop. Measured, not assumed.
"""
import json, subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"]).decode())['SRC']
FPS = 30000 / 1001
man = json.load(open('shots/manifest.json'))

def cuts_near(t, win=1.2):
    a0 = max(0, t - win)
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{a0:.3f}", "-i", SRC,
                        "-t", f"{2*win:.3f}", "-vf", "scale=64:36", "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (64 * 36)
    a = a[:n * 64 * 36].reshape(n, 36, 64).astype(float)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    if not len(d): return []
    thr = max(8.0, 4.0 * np.median(d))
    return [(a0 + (i + 1) / FPS, float(d[i])) for i in np.where(d > thr)[0]]

bad = 0
prev = None
for m in man:
    if prev is None or prev['seg'] != m['seg'] or prev['piece'] != m['piece']:
        prev = m; continue
    t = m['absStart']
    c = cuts_near(t)
    if not c:
        print(f"  {prev['name']} -> {m['name']} at {t:7.2f}: no measured cut within 1.2s "
              f"(likely a same-shot split)")
        prev = m; continue
    best = min(c, key=lambda x: abs(x[0] - t))
    err = best[0] - t
    flag = ''
    if abs(err) > 0.10:
        flag = '   <-- BOUNDARY OFF'; bad += 1
    print(f"  {prev['name']} -> {m['name']} at {t:7.2f}: nearest real cut {best[0]:7.2f} "
          f"({err:+.2f}s, diff {best[1]:.0f}){flag}")
    prev = m
print(f"\n{bad} boundary(ies) more than 0.10s from a measured cut")
