#!/usr/bin/env python3
"""Pick the source-crop x for each shot: centre it on Dan (the non-green mass), then
clamp so it never includes the source's own left-hand overlay."""
import json, os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(HERE, '../../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg')
SRC = os.path.join(HERE, '../../V4 - The Ultimate 1 Minute Ab Workout(2).mp4 - READY FOR UPLOAD.mp4')
L = json.load(open(os.path.join(HERE, 'layout.json')))
shots = json.load(open(os.path.join(HERE, 'shots.json')))
SW, SH = 1920, 1080
blockW, blockH = L['block']['w'], L['block']['h']
CROP_W = round(SH * blockW / blockH)          # source-space width that fills the block


def subject_center(times, ignore_left=0):
    """Centre of Dan's SILHOUETTE, not the centre of mass of non-green pixels.
    A centroid is biased by whatever is excluded: counting the source overlay drags it
    left, excluding that strip drags it right. Instead find the first and last column
    that is substantially non-green and take the midpoint of those bounds."""
    cs = []
    for t in times:
        p = f'/tmp/v4crop_{t:.2f}.png'
        subprocess.run([FF, '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
                        '-ss', f'{t:.2f}', '-i', SRC, '-frames:v', '1', '-vf', 'scale=480:-1', p],
                       check=True)
        im = Image.open(p).convert('RGB'); W, H = im.size; px = im.load()
        x_lo = int(ignore_left / SW * W)
        y0, y1 = int(H * 0.20), int(H * 0.92)
        rows = len(range(y0, y1, 3))
        cols = []
        for x in range(x_lo, W):
            n = 0
            for y in range(y0, y1, 3):
                r, g, b = px[x, y]
                if not (g > r + 8 and g > b + 8):
                    n += 1
            if n > rows * 0.45:                 # this column is mostly subject
                cols.append(x)
        if len(cols) > 6:
            cs.append((cols[0] + cols[-1]) / 2 / W)
    return sum(cs) / len(cs) if cs else 0.5


out = {}
for s in shots:
    spec = L['shots'][str(s['i'])]
    if spec['t'] == 'fitcard':
        out[str(s['i'])] = None
        print(f"shot{s['i']}: fitcard (whole frame into the block)")
        continue
    ts = [s['absStart'] + s['dur'] * f for f in (0.25, 0.5, 0.75)]
    c = subject_center(ts, spec.get('minX0', 0))
    x0 = round(c * SW - CROP_W / 2)
    lo = spec.get('minX0', 0)
    x0c = min(max(x0, lo), SW - CROP_W)
    out[str(s['i'])] = x0c
    flag = '  <- clamped off the source overlay' if x0c != x0 else ''
    print(f"shot{s['i']}: subject at {c:.3f} -> x0={x0} clamped {x0c}"
          f"  (subject sits {(c*SW-x0c)/CROP_W:.2f} across the block){flag}")

json.dump({'cropW': CROP_W, 'x0': out}, open(os.path.join(HERE, 'crops.json'), 'w'), indent=1)
print(f'\ncrop width {CROP_W}px of {SW} -> block {blockW}x{blockH} (upscale {blockW/CROP_W:.2f}x)')
