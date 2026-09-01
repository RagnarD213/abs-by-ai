#!/usr/bin/env python3
"""If we cut a pause out, does the picture jump?

A pause is dead air, but the cut still joins two moments in time. How visible that join is
depends entirely on how much Dan MOVES during the pause - and he is on a locked tripod, so
the answer might be "not at all". Measure it: compare the frame just before the pause with
the frame just after it, and score that against the file's own frame-to-frame baseline.

Reference points, measured the same way:
  * an inherited SOURCE SPLICE, which is a real take change and is what "awkward cut" means
  * two ADJACENT frames, which is what "no jump at all" looks like
"""
import json, subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"
def frame(t):
    p = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', SRC, '-frames:v', '1',
                        '-vf', 'crop=644:960:1029:120,scale=322:480', '-f', 'rawvideo',
                        '-pix_fmt', 'gray', '-'], capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(480, 322).astype(np.float32)
def mad(a, b): return float(np.abs(a - b).mean())

GAPS = json.load(open('work/gaps.json'))
segs = json.loads(subprocess.check_output(
    ['node', '-e', "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS))"]).decode())
SPL = [s['cut'] for s in json.load(open('work/splices.json'))]

base = np.median([mad(frame(t), frame(t + 1/29.97)) for t in (700.0, 1000.0, 1250.0, 430.0)])
sp = np.median([mad(frame(c - 0.08), frame(c + 0.08)) for c in (446.68, 946.31, 1272.87, 699.63)])
print(f"BASELINE  adjacent frames        : {base:.2f}")
print(f"REFERENCE inherited source splice: {sp:.2f}  <- what an 'awkward cut' scores\n")
print(f"{'short':6s} {'out':>7s} {'len':>6s} {'jump':>6s}   verdict")
for s in segs:
    off = 0.0
    for p in s['pieces']:
        for g0, g1 in GAPS:
            if g0 < p['start'] + 0.05 or g1 > p['end'] - 0.05: continue
            if g1 - g0 < 0.55: continue
            j = mad(frame(g0 - 0.05), frame(g1 + 0.05))
            r = j / sp
            v = 'invisible' if r < 0.35 else ('mild - punch it' if r < 0.7 else 'real jump - punch it')
            print(f"{s['id']:6s} {off+g0-p['start']:7.2f} {g1-g0:6.2f} {j:6.2f}   {v} ({r:.2f}x a splice)")
        off += p['end'] - p['start']
