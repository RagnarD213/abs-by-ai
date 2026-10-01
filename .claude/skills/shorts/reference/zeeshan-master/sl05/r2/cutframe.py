#!/usr/bin/env python3
"""cutframe.py: for every shot start in the manifest that is a SOURCE picture cut (not a piece start, not our own
switch inside continuous footage), find the exact first frame of the new shot (max frame difference within +-3
frames), versus round(absStart*FPS). Accurate seek: frames returned start at the first pts >= X."""
import json, subprocess, math, numpy as np
B = '/Volumes/Extreme/_edit_work/sl05/build'; FPS = 30000 / 1001
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').SRC))"], cwd=B).decode())
cuts = sorted({round(t, 3) for s in json.load(open(f'{B}/work/shots_all.json')) for t in s[1:]})
for t in cuts:
    n = round(t * FPS); X = (n - 4 - 0.4) / FPS
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{X:.5f}', '-i', SRC, '-frames:v', '9', '-vf', 'scale=320:180:in_color_matrix=bt709:in_range=tv,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 180, 320).astype(float)
    first = math.ceil(X * FPS)
    d = [np.abs(fr[k] - fr[k - 1]).mean() for k in range(1, len(fr))]
    k = int(np.argmax(d)) + 1
    print(f'{t:8.3f} round {n} true {first + k} ({(first+k)/FPS:.4f}) diff {d[k-1]:5.1f} next {sorted(d)[-2]:5.1f} {"OK" if first + k == n else "OFF " + str(first + k - n)}')
