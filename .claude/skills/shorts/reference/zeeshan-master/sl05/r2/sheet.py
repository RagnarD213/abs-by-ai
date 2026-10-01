#!/usr/bin/env python3
"""sheet.py S [video]: (1) every shot boundary as the -1|0 frame pair, (2) each shot's middle frame; exact frame
indices by sequential decode of the rendered short. -> r2/look/<S>_joins.jpg, <S>_mids.jpg"""
import sys, json, subprocess, numpy as np
from PIL import Image, ImageDraw
B = '/Volumes/Extreme/_edit_work/sl05/build'; FPS = 30000 / 1001
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
S = sys.argv[1]
segs = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./segments.js').SEGMENTS))"], cwd=B))
slug = next(s['slug'] for s in segs if s['id'] == S)
V = sys.argv[2] if len(sys.argv) > 2 else f'{B}/out/{S.lower()}_{slug}.mp4'
man = [m for m in json.load(open(f'{B}/shots/manifest.json')) if m['seg'] == S]
w, h = 270, 480
raw = subprocess.run([FF, '-v', 'error', '-i', V, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
starts = []; f = 0
for m in man: starts.append(f); f += m['frames']
def lab(im, t):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 120, 16], fill=(0, 0, 0)); d.text((2, 2), t, fill=(255, 255, 0)); return im
pairs = []
for i, n in enumerate(starts[1:], 1):
    a = lab(Image.fromarray(fr[n - 1].copy()), f'{man[i]["name"]} -1 {(n-1)/FPS:.2f}'); b = lab(Image.fromarray(fr[n].copy()), f'0 {n/FPS:.2f}')
    pairs.append((a, b))
cols = 4
g = Image.new('RGB', (cols * 2 * w + (cols - 1) * 10, ((len(pairs) + cols - 1) // cols) * h), (60, 0, 0))
for k, (a, b) in enumerate(pairs):
    x = (k % cols) * (2 * w + 10); y = (k // cols) * h; g.paste(a, (x, y)); g.paste(b, (x + w, y))
g.save(f'{B}/r2/look/{S}_joins.jpg', quality=85)
mids = [lab(Image.fromarray(fr[s + m['frames'] // 2].copy()), f'{m["name"]} {m["t"]} {(s + m["frames"]//2)/FPS:.1f}') for s, m in zip(starts, man)]
cols = 6
g = Image.new('RGB', (cols * w, ((len(mids) + cols - 1) // cols) * h))
for k, im in enumerate(mids): g.paste(im, ((k % cols) * w, (k // cols) * h))
g.save(f'{B}/r2/look/{S}_mids.jpg', quality=85)
print(len(fr), 'frames decoded; plan', sum(m['frames'] for m in man))
