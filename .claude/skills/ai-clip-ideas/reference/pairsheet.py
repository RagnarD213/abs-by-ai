#!/usr/bin/env python3
"""Build START|END review sheets for AI clip idea frame pairs.
Usage: python3 pairsheet.py <dir> <key1>:<TITLE 1> <key2>:<TITLE 2> ...
Expects <dir>/<key>-start.jpg and <dir>/<key>-end.jpg; writes <dir>/PAIR-<key>.jpg
"""
import sys
from PIL import Image, ImageDraw, ImageFont

d = sys.argv[1]
W = 1400
for spec in sys.argv[2:]:
    key, title = spec.split(":", 1)
    a = Image.open(f"{d}/{key}-start.jpg"); b = Image.open(f"{d}/{key}-end.jpg")
    a = a.resize((W, int(a.height * W / a.width)))
    b = b.resize((W, int(b.height * W / b.width)))
    hh = max(a.height, b.height)
    sheet = Image.new("RGB", (W * 2 + 30, hh + 90), (10, 10, 10))
    sheet.paste(a, (0, 90)); sheet.paste(b, (W + 30, 90))
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        f2 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except OSError:
        f = f2 = None
    dr.text((20, 18), title, fill=(255, 255, 255), font=f)
    dr.text((20, hh + 30), "START FRAME", fill=(120, 255, 120), font=f2)
    dr.text((W + 50, hh + 30), "END FRAME", fill=(120, 180, 255), font=f2)
    sheet.save(f"{d}/PAIR-{key}.jpg", quality=90)
    print(f"PAIR-{key}.jpg", sheet.size)
