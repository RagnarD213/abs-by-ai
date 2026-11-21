#!/usr/bin/env python3
"""Labelled contact sheets of every detected shot, grouped by segment, with the 9:16
centre-crop window drawn on so it is obvious what a blind vertical crop would lose."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
man = json.load(open(os.path.join(SHOTS, 'manifest.json')))

COLS, TW = 4, 420
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
except OSError:
    font = ImageFont.load_default()

by_seg = {}
for m in man:
    by_seg.setdefault(m['seg'], []).append(m)

for seg, items in by_seg.items():
    items.sort(key=lambda m: (m['piece'], m['shot']))
    thumbs = []
    for m in items:
        im = Image.open(os.path.join(SHOTS, m['name'] + '.jpg')).convert('RGB')
        im = im.resize((TW, round(TW * im.height / im.width)), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        # 9:16 centre-crop window on a 16:9 frame = 31.6% of the width, centred
        cw = im.width * 9 / 16 * (im.height / im.width)
        x0 = (im.width - cw) / 2
        d.rectangle([x0, 0, x0 + cw, im.height - 1], outline=(255, 40, 40), width=3)
        # label bar
        bar = 30
        out = Image.new('RGB', (im.width, im.height + bar), (16, 16, 16))
        out.paste(im, (0, 0))
        ImageDraw.Draw(out).text(
            (8, im.height + 5),
            f"{m['name']}  @{m['absStart']:.1f}s  {m['dur']:.1f}s", font=font, fill=(255, 255, 255))
        thumbs.append(out)

    rows = (len(thumbs) + COLS - 1) // COLS
    w, h = thumbs[0].width, thumbs[0].height
    sheet = Image.new('RGB', (COLS * w + (COLS + 1) * 10, rows * h + (rows + 1) * 10), (8, 8, 8))
    for i, t in enumerate(thumbs):
        r, c = divmod(i, COLS)
        sheet.paste(t, (10 + c * (w + 10), 10 + r * (h + 10)))
    p = os.path.join(SHOTS, f'sheet-{seg}.jpg')
    sheet.save(p, quality=88)
    print(f'{seg}: {len(thumbs)} shots -> {os.path.basename(p)} ({sheet.width}x{sheet.height})')
