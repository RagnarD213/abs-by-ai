#!/usr/bin/env python3
"""/ad-setup step 4 — waist ruler sheet for thumbnail photos.

The clean-look thumbnail crops Dan at a fraction of his cutout's height (`waist`). It must be MEASURED per photo —
0.60 cut through the abs on Ad 5. This draws lines at 0.50–0.80 of the cutout bounding box over each photo.
Read the fraction where the top of the waistband sits and use that + 0.03 as `waist` in the thumbnail build.

  python3 .claude/skills/ad-setup/ruler.py studio-gray-87 studio-white-57 [--out sheet.jpg]
"""
import os, sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
PH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../photos/finalized social media photos/')

args = sys.argv[1:]
out = args[args.index('--out') + 1] if '--out' in args else '/tmp/adsetup_ruler.jpg'
names = [a for a in args if not a.startswith('--') and a != out]
tiles = []
for n in names:
    cut = Image.open(PH + '_cutouts/' + n + '_CUTOUT.png'); bb = cut.getchannel('A').getbbox()
    ph = Image.open(PH + n + '_FINAL_PRIMARY.jpg').convert('RGB').crop(bb)
    ph = ph.resize((int(ph.width * 900 / ph.height), 900)); d = ImageDraw.Draw(ph)
    for i in range(50, 81):
        y = int(i / 100 * 900)
        d.line([(0, y), (ph.width, y)], fill=(255, 0, 0) if i % 5 == 0 else (255, 200, 0), width=1)
        if i % 5 == 0: d.text((4, y - 10), f'{i / 100:.2f}', fill=(255, 0, 0))
    d.text((4, 4), n, fill=(255, 0, 0)); tiles.append(ph)
sheet = Image.new('RGB', (sum(t.width + 20 for t in tiles), 900), 'white'); x = 0
for t in tiles: sheet.paste(t, (x, 0)); x += t.width + 20
sheet.save(out, quality=88); print(out)
