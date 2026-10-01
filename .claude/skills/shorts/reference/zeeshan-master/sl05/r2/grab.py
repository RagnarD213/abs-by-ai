#!/usr/bin/env python3
"""grab.py OUT.jpg COLS t1 t2 ... : exact source frames (BT.709 decode) in a labelled grid, 480 px wide each."""
import sys, subprocess, json, os
from PIL import Image, ImageDraw, ImageFont
B = '/Volumes/Extreme/_edit_work/sl05/build'
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').SRC))"], cwd=B).decode())
out, cols, ts = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
W, H = 480, 270; ims = []
for t in ts:
    p = f'/tmp/sl05g_{t}.png'
    subprocess.run([FF, '-v', 'error', '-y', '-ss', str(max(0, float(t) - 1)), '-i', SRC, '-ss', str(min(1, float(t))), '-frames:v', '1',
                    '-vf', f'scale={W}:{H}:in_color_matrix=bt709:in_range=tv', p], check=True)
    im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im); d.rectangle([0, 0, 90, 18], fill=(0, 0, 0)); d.text((3, 3), t, fill=(255, 255, 0)); ims.append(im)
rows = (len(ims) + cols - 1) // cols
g = Image.new('RGB', (cols * W, rows * H))
for i, im in enumerate(ims): g.paste(im, ((i % cols) * W, (i // cols) * H))
g.save(out, quality=85); print(out)
