#!/usr/bin/env python3
"""Generate the fixed overlay assets for the V2 Shorts: the locked 'J2 tactical'
background used by card/pip shots, the AbsByAI.com wordmark, and one title overlay
per short (Impact headline + Copperplate eyebrow, drop-shadowed)."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets')
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
BG = (13, 14, 11)             # #0D0E0B
OLIVE = (140, 152, 88)        # #8C9858
GRID = (27, 30, 19)
INSET = 28

IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'

META = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./plan.js').META))"], cwd=HERE).decode())


def tactical_bg():
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 90):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

    d.rectangle([INSET, INSET, W - INSET - 1, H - INSET - 1], outline=OLIVE, width=3)

    # rangefinder ticks along all four edges
    for x in range(INSET + 60, W - INSET - 40, 60):
        long = (x // 60) % 3 == 0
        n = 18 if long else 9
        d.line([(x, INSET + 3), (x, INSET + 3 + n)], fill=OLIVE, width=2)
        d.line([(x, H - INSET - 4), (x, H - INSET - 4 - n)], fill=OLIVE, width=2)
    for y in range(INSET + 60, H - INSET - 40, 60):
        long = (y // 60) % 3 == 0
        n = 18 if long else 9
        d.line([(INSET + 3, y), (INSET + 3 + n, y)], fill=OLIVE, width=2)
        d.line([(W - INSET - 4, y), (W - INSET - 4 - n, y)], fill=OLIVE, width=2)

    # white corner brackets
    L, T = 74, 6
    for (cx, cy, sx, sy) in [(INSET, INSET, 1, 1), (W - INSET, INSET, -1, 1),
                             (INSET, H - INSET, 1, -1), (W - INSET, H - INSET, -1, -1)]:
        d.rectangle([min(cx, cx + sx * L), min(cy, cy + sy * T),
                     max(cx, cx + sx * L), max(cy, cy + sy * T)], fill=(255, 255, 255))
        d.rectangle([min(cx, cx + sx * T), min(cy, cy + sy * L),
                     max(cx, cx + sx * T), max(cy, cy + sy * L)], fill=(255, 255, 255))
    p = os.path.join(OUT, 'j2-bg.png')
    im.save(p)
    return p


def wordmark():
    """Small, muted AbsByAI.com — camel case, on every short from video #1 (rip protection)."""
    im = Image.new('RGBA', (420, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(COPPER, 30)
    txt = 'AbsByAI.com'
    d.text((3, 15), txt, font=f, fill=(0, 0, 0, 150))
    d.text((0, 12), txt, font=f, fill=(255, 255, 255, 165))
    p = os.path.join(OUT, 'wordmark.png')
    im.save(p)
    return p


def title_overlay(seg, meta):
    """Big overlaid title with a drop shadow — no static intro card (Dan's rule)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Sized so a 3-line headline ends by ~y=440. Dan's eyes sit around y=560 on the
    # locked kitchen camera, and at 118/112 the last line landed straight across them.
    eyebrow = ImageFont.truetype(COPPER, 38)
    head = ImageFont.truetype(IMPACT, 106)

    y = 72
    # eyebrow, letter-spaced olive
    ex = 64
    for ch in meta['eyebrow']:
        d.text((ex + 2, y + 2), ch, font=eyebrow, fill=(0, 0, 0, 170))
        d.text((ex, y), ch, font=eyebrow, fill=OLIVE + (255,))
        ex += d.textlength(ch, font=eyebrow) + 6
    y += 64

    for line in meta['title'].split('\n'):
        for dx, dy in ((5, 6), (3, 4)):
            d.text((64 + dx, y + dy), line, font=head, fill=(0, 0, 0, 190))
        d.text((64, y), line, font=head, fill=(255, 255, 255, 255))
        y += 102
    p = os.path.join(OUT, f'title-{seg}.png')
    im.save(p)
    return p


def chip(shot, label, w, h):
    """Square-cornered olive-bordered mission chip, per the locked type system."""
    f = ImageFont.truetype(COPPER, 30)
    pad = 30
    tw = sum(f.getlength(c) + 5 for c in label)
    cw = round(tw + pad * 2)
    im = Image.new('RGBA', (cw, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, cw - 1, h - 1], fill=BG + (235,), outline=OLIVE + (255,), width=2)
    x = pad
    for c in label:
        d.text((x, h // 2 - 18), c, font=f, fill=OLIVE + (255,))
        x += f.getlength(c) + 5
    p = os.path.join(OUT, f'chip-{shot}.png')
    im.save(p)
    return p


print(tactical_bg())
print(wordmark())
for seg, meta in META.items():
    print(title_overlay(seg, meta))

L = json.load(open(os.path.join(HERE, 'layout.json')))
for shot, label in L['card']['labels'].items():
    print(chip(shot, label, L['card']['w'], L['card']['chipH']))

# Any short that OPENS on a card shot must have a title short enough to clear the card's
# top edge, or the headline sits on the artwork. Assert it rather than trusting the copy.
CARD_OPENERS = json.loads(subprocess.check_output(
    ['node', '-e', """
const {loadShots, SEGMENTS} = require('./plan.js');
const L = require('./layout.json');
const out = [];
for (const seg of SEGMENTS) {
  const first = loadShots().filter((s) => s.seg === seg.id)[0];
  if (first && first.t === 'card') out.push(seg.id);
}
console.log(JSON.stringify(out));
"""], cwd=HERE).decode())
for seg in CARD_OPENERS:
    bbox = Image.open(os.path.join(OUT, f'title-{seg}.png')).split()[-1].getbbox()
    assert bbox[3] < L['card']['y'], (
        f'title-{seg} ink reaches y={bbox[3]} but its opening card starts at '
        f"y={L['card']['y']} — shorten the headline")
print(f'checked title clearance on card-opening shorts: {CARD_OPENERS}')
