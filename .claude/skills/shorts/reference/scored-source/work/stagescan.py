#!/usr/bin/env python3
"""Scan every frame of every delivered short for a picture-less frame.

blackdetect only catches a WHOLE black frame; this batch's failure mode is subtler - the
stage goes empty while the title, captions and wordmark still draw, so the frame is not
black and the gate passes. Measure the stage rectangle itself, at full frame rate.
"""
import json, subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
L = json.load(open('layout.json'))
Y0, Y1 = L['card']['y'], L['card']['y'] + L['card']['h']
W, H = 96, 171                     # downscaled probe; stage rows scale with it
sy0, sy1 = round(Y0 / 1920 * H), round(Y1 / 1920 * H)
bad = 0
for seg in json.loads(subprocess.check_output(
        ['node', '-e', "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"],
        stderr=subprocess.DEVNULL).decode()):
    sid, slug = seg
    src = f'out/{sid.lower()}_{slug}.mp4'
    p = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H}',
                        '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8).reshape(-1, H, W).astype(float)
    band = a[:, sy0:sy1, :]
    # the J2 field is near-black with a faint grid: a real picture has both level and variance
    m = band.reshape(len(band), -1)
    empty = (m.mean(1) < 12) & (m.std(1) < 9)
    idx = np.where(empty)[0]
    fps = 30000 / 1001
    if len(idx):
        runs = np.split(idx, np.where(np.diff(idx) != 1)[0] + 1)
        for r in runs:
            print(f"  {sid} EMPTY STAGE frames {r[0]}-{r[-1]} ({r[0]/fps:.2f}-{(r[-1]+1)/fps:.2f}s)")
        bad += len(runs)
    print(f"{sid} {len(a)} frames, stage mean {band.mean():.1f}, "
          f"{'CLEAN' if not len(idx) else str(len(idx))+' empty frames'}")
print('\n' + ('stage scan PASS' if bad == 0 else f'stage scan: {bad} empty run(s)'))
sys.exit(0 if bad == 0 else 1)
