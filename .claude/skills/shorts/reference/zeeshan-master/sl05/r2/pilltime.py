#!/usr/bin/env python3
"""pilltime.py T0 T1 [T0 T1 ...]: per-frame olive-pixel count in rows 760-960 (source), 960x540 decode. Prints on/off frames."""
import sys, subprocess, json, numpy as np
B = '/Volumes/Extreme/_edit_work/sl05/build'
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').SRC))"], cwd=B).decode())
FPS = 30000 / 1001
a = sys.argv[1:]
for i in range(0, len(a), 2):
    t0, t1 = float(a[i]), float(a[i + 1])
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{max(0,t0-2):.3f}', '-i', SRC, '-ss', f'{min(2,t0):.3f}', '-t', f'{t1-t0:.3f}',
                          '-vf', 'scale=960:540:in_color_matrix=bt709:in_range=tv,format=rgb24,crop=960:100:0:380', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 100, 960, 3).astype(int)
    ol = np.array([77, 86, 49]); txt = np.array([230, 237, 216])
    cnt = [int((np.abs(f - ol).sum(2) < 30).sum()) for f in fr]
    n0 = round(t0 * FPS); full = max(cnt)
    on = [k for k, c in enumerate(cnt) if c > 0.05 * full]
    s = ' '.join(f'{(n0+k)/FPS:.2f}:{c}' for k, c in enumerate(cnt) if k % 3 == 0)
    print(f'[{t0}-{t1}] max {full} first>5% {(n0+on[0])/FPS:.3f} last>5% {(n0+on[-1])/FPS:.3f}  first>50% {(n0+[k for k,c in enumerate(cnt) if c>0.5*full][0])/FPS:.3f} last>50% {(n0+[k for k,c in enumerate(cnt) if c>0.5*full][-1])/FPS:.3f}')
