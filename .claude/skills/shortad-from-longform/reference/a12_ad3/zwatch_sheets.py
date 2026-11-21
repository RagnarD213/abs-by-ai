#!/usr/bin/env python3
"""Tile the watch pass's consecutive-frame strips (watch/strip/*.png, -4/-2/-1/0/+1/+2/+4/+8 frames around every
boundary) into sheets of SIX strips, labelled with the boundary time, so every boundary can actually be looked at.
  python3 zwatch_sheets.py <outdir>      -> <outdir>/watch_sheet_NN.jpg"""
import glob, os, sys
from PIL import Image, ImageDraw
out = sys.argv[1] if len(sys.argv) > 1 else 'watch'
fs = sorted(glob.glob('watch/strip/*.png'))
os.makedirs(out, exist_ok=True)
for k in range(0, len(fs), 6):
    ims = [Image.open(f) for f in fs[k:k+6]]
    W = max(i.width for i in ims); H = sum(i.height + 22 for i in ims)
    sh = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(sh); y = 0
    for f, im in zip(fs[k:k+6], ims):
        d.text((4, y + 4), os.path.basename(f)[1:-4] + ' s', fill=(255, 255, 0)); sh.paste(im, (0, y + 22)); y += im.height + 22
    sh.save(f'{out}/watch_sheet_{k//6:02d}.jpg', quality=85)
print(len(fs), 'strips ->', (len(fs) + 5)//6, 'sheets in', out)
