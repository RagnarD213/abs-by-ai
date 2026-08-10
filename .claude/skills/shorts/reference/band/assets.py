#!/usr/bin/env python3
"""Band assets for the short1 rebuild: tactical background, persistent header,
the four muscle chips (one per reveal), and the wordmark."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets'); os.makedirs(OUT, exist_ok=True)
L = json.load(open(os.path.join(HERE, 'layout.json')))
CHIPS = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./plan.js').CHIPS))"], cwd=HERE).decode())

W, H = L['canvas']
BG = (13, 14, 11); OLIVE = (140, 152, 88); GRID = (27, 30, 19); INSET = 28
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'


def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + gap
    return x


def tactical_bg():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    for x in range(0, W, 90): d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 90): d.line([(0, y), (W, y)], fill=GRID)
    d.rectangle([INSET, INSET, W - INSET - 1, H - INSET - 1], outline=OLIVE, width=3)
    for x in range(INSET + 60, W - INSET - 40, 60):
        n = 18 if (x // 60) % 3 == 0 else 9
        d.line([(x, INSET + 3), (x, INSET + 3 + n)], fill=OLIVE, width=2)
        d.line([(x, H - INSET - 4), (x, H - INSET - 4 - n)], fill=OLIVE, width=2)
    for y in range(INSET + 60, H - INSET - 40, 60):
        n = 18 if (y // 60) % 3 == 0 else 9
        d.line([(INSET + 3, y), (INSET + 3 + n, y)], fill=OLIVE, width=2)
        d.line([(W - INSET - 4, y), (W - INSET - 4 - n, y)], fill=OLIVE, width=2)
    for (cx, cy, sx, sy) in [(INSET, INSET, 1, 1), (W - INSET, INSET, -1, 1),
                             (INSET, H - INSET, 1, -1), (W - INSET, H - INSET, -1, -1)]:
        d.rectangle([min(cx, cx + sx * 74), min(cy, cy + sy * 6),
                     max(cx, cx + sx * 74), max(cy, cy + sy * 6)], fill=(255, 255, 255))
        d.rectangle([min(cx, cx + sx * 6), min(cy, cy + sy * 74),
                     max(cx, cx + sx * 6), max(cy, cy + sy * 74)], fill=(255, 255, 255))
    p = os.path.join(OUT, 'bg.png'); im.save(p); return p


def header():
    """Small persistent title inside the band — it never touches Dan, so it can stay up."""
    im = Image.new('RGBA', (W, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    spaced(d, (56, 6), 'THE 4 AB MUSCLES', ImageFont.truetype(COPPER, 34), OLIVE + (255,), 6)
    p = os.path.join(OUT, 'header.png'); im.save(p); return p


def chip(c):
    b = L['band']
    im = Image.new('RGBA', (b['chipW'], b['chipH'] + 54), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    spaced(d, (2, 0), f"MUSCLE {c['n']} OF 4", ImageFont.truetype(COPPER, 28), OLIVE + (255,), 5)
    top = 54
    d.rectangle([0, top, b['chipW'] - 1, top + b['chipH'] - 1],
                fill=BG + (238,), outline=OLIVE + (255,), width=3)
    f1 = ImageFont.truetype(IMPACT, 62)
    d.text((26, top + 20), c['title'], font=f1, fill=(255, 255, 255, 255))
    spaced(d, (28, top + 98), c['sub'], ImageFont.truetype(COPPER, 24), OLIVE + (255,), 3)
    p = os.path.join(OUT, f"chip-{c['key']}.png"); im.save(p); return p


def wordmark():
    im = Image.new('RGBA', (420, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(COPPER, 30)
    d.text((3, 15), 'AbsByAI.com', font=f, fill=(0, 0, 0, 150))
    d.text((0, 12), 'AbsByAI.com', font=f, fill=(255, 255, 255, 165))
    p = os.path.join(OUT, 'wordmark.png'); im.save(p); return p


print(tactical_bg()); print(header()); print(wordmark())
for c in CHIPS:
    p = chip(c)
    ink = Image.open(p).split()[-1].getbbox()
    assert ink[2] <= L['band']['chipW'], f"{c['title']} overflows the chip ({ink[2]}px)"
    print(p)
# the chip block must fit inside the band
b = L['band']
assert b['chipY'] + b['chipH'] <= b['h'] - 10, 'chip runs past the band'
print(f"band {b['h']}px: header@{b['headerY']} counter@{b['counterY']} "
      f"chip {b['chipY']}..{b['chipY']+b['chipH']}  OK")
