#!/usr/bin/env python3
"""Short 2's replacement pill in ZEESHAN'S style, rebuilt from his frame (source 105.0, pill/z105.png):
olive fill (77,86,49), text (230,237,216), rows 804-907 (103 px), text inset 40 px, cap height 46 px.
Delivered on the F-s01 card at 1080/1517 = 0.712x, so every measure is scaled by 0.712. Manrope SemiBold
at 44 px matches his cap height (46 x 0.712 = 33 px). Dan's text, 2026-09-25, centred on the canvas."""
from PIL import Image, ImageDraw, ImageFont
import os
K = 1080 / 1517
FONT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/ad-factory/the-upload/assembly/fonts/Manrope.ttf'
f = ImageFont.truetype(FONT, 44); f.set_variation_by_name(b'SemiBold')
lines = ['Use this 2-minute workout', 'to pump up before a photo shoot']
padx, pady, lh, rad = round(40 * K), round(22 * K), 56, round(10 * K)
tw = max(f.getlength(l) for l in lines)
w, h = round(tw + 2 * padx), round(2 * pady + lh * len(lines))
im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle([0, 0, w - 1, h - 1], rad, fill=(77, 86, 49, 255))
cap = f.getbbox('H')
for i, l in enumerate(lines):
    lw = f.getlength(l)
    y = pady + i * lh + (lh - (cap[3] - cap[1])) / 2 - cap[1]
    d.text(((w - lw) / 2, y), l, font=f, fill=(230, 237, 216, 255))
out = os.path.join(os.path.dirname(__file__), '..', 'assets', 'pill-F.png')
im.save(out); print(out, im.size)
