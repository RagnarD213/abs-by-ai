#!/usr/bin/env python3
"""sharp.py T0 T1: per-frame Laplacian variance (480x270 grey, BT.709) with source frame times."""
import sys, subprocess, json, numpy as np
from scipy import ndimage
B = '/Volumes/Extreme/_edit_work/sl05/build'
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').SRC))"], cwd=B).decode())
t0, t1 = float(sys.argv[1]), float(sys.argv[2]); FPS = 30000 / 1001
raw = subprocess.run([FF, '-v', 'error', '-ss', f'{t0-2:.3f}', '-i', SRC, '-ss', '2', '-t', f'{t1-t0:.3f}', '-vf', 'scale=480:270:in_color_matrix=bt709:in_range=tv,format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 270, 480).astype(float)
n0 = round(t0 * FPS)
prev = None
for k, f in enumerate(fr):
    d = np.abs(f - prev).mean() if prev is not None else 0
    print(f'{(n0+k)/FPS:8.3f} lap {ndimage.laplace(f).var():7.1f} diff {d:5.1f}'); prev = f
