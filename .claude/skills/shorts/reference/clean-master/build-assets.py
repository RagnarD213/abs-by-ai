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


def fit_head(meta):
    """Largest Impact size at which BOTH headline lines fit, down to a floor.

    Rev 2: Dan's wording for M - "Why test boosters are the least important supplement" -
    measures 1352px on one line at the batch's 98pt against a 976px limit. The options were to
    change his words, drop to three lines (which would push the title into the picture and
    break the standing rule), or fit the type. Fitting the type is the only one that costs
    nothing, so the size is chosen per short instead of being fixed.
    """
    for size in range(98, 63, -2):
        f = ImageFont.truetype(IMPACT, size)
        if all(64 + f.getlength(l) < W - 60 for l in meta['title'].split('\n')):
            return size, f
    raise AssertionError(f"headline will not fit even at 64pt: {meta['title']!r}")


def title_overlay(seg, meta):
    """Big overlaid title with a drop shadow — no static intro card (Dan's rule)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # The stage now starts at y=170, so the title sits ON the picture for its 3.2s. Bake a
    # soft top scrim into the same PNG: it fades out with the title, costs no extra ffmpeg
    # input, and keeps white Impact legible over a bright pool deck.
    scrim = Image.new('RGBA', (W, SCRIM_H), (0, 0, 0, 0))
    sp = scrim.load()
    for y in range(SCRIM_H):
        f = 1.0 - (y / SCRIM_H) ** 1.5
        a = int(196 * f)
        for x in range(W):
            sp[x, y] = (6, 7, 5, a)
    im.alpha_composite(scrim, (0, 0))
    d = ImageDraw.Draw(im)
    eyebrow = ImageFont.truetype(COPPER, 36)
    size, head = fit_head(meta)
    lh = int(round(size * 0.96))

    y = 40
    # eyebrow, letter-spaced olive
    ex = 64
    for ch in meta['eyebrow']:
        d.text((ex + 2, y + 2), ch, font=eyebrow, fill=(0, 0, 0, 170))
        d.text((ex, y), ch, font=eyebrow, fill=OLIVE + (255,))
        ex += d.textlength(ch, font=eyebrow) + 6
    y += 58

    for line in meta['title'].split('\n'):
        for dx, dy in ((5, 6), (3, 4)):
            d.text((64 + dx, y + dy), line, font=head, fill=(0, 0, 0, 190))
        d.text((64, y), line, font=head, fill=(255, 255, 255, 255))
        y += lh
    p = os.path.join(OUT, f'title-{seg}.png')
    im.save(p)
    return p


def header_overlay(seg, meta):
    """The eyebrow alone. It persists for the whole short: with the picture dropped to y=310
    the title band would otherwise sit empty once the headline fades at 3.2s."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(COPPER, 36)
    ex, y = 64, 40
    for ch in meta['eyebrow']:
        d.text((ex + 2, y + 2), ch, font=f, fill=(0, 0, 0, 170))
        d.text((ex, y), ch, font=f, fill=OLIVE + (255,))
        ex += d.textlength(ch, font=f) + 6
    assert ex < W - 40, f'eyebrow for {seg} is {ex}px wide, runs off the frame'
    p = os.path.join(OUT, f'header-{seg}.png')
    im.save(p)
    return p


def ai_label():
    """Small AI GENERATED tag for the generated cover clips.

    Standing rule: AI imagery is labelled. Kept small and low-contrast so it reads as a
    disclosure rather than a graphic, and placed high-left where neither the title band
    (above y=310) nor the caption band (from ~y1015) sits.
    """
    f = ImageFont.truetype(COPPER, 26)
    txt = 'AI GENERATED'
    pad = 18
    tw = sum(f.getlength(c) + 4 for c in txt)
    w_, h_ = int(tw + pad * 2), 46
    im = Image.new('RGBA', (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w_ - 1, h_ - 1], fill=BG + (170,), outline=OLIVE + (210,), width=2)
    x = pad
    for c in txt:
        d.text((x, h_ // 2 - 14), c, font=f, fill=(255, 255, 255, 205))
        x += f.getlength(c) + 4
    p = os.path.join(OUT, 'ai-label.png')
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


def check_width(seg, meta):
    size, head = fit_head(meta)
    for line in meta['title'].split('\n'):
        w = head.getlength(line)
        assert 64 + w < W - 40, f'title-{seg} line {line!r} is {w:.0f}px wide, runs off the frame'
    if size != 98:
        print(f'  title-{seg}: headline set at {size}pt to fit the frame')


L = json.load(open(os.path.join(HERE, 'layout.json')))
SCRIM_H = L['titleScrimH']
print(tactical_bg())
print(wordmark())
print(ai_label())
for seg, meta in META.items():
    check_width(seg, meta)
    print(title_overlay(seg, meta))
    print(header_overlay(seg, meta))

for shot, label in L['card']['labels'].items():
    print(chip(shot, label, L['card']['w'], L['card']['chipH']))

# The stage now runs the full canvas width with its top edge at y=310, so NO title may
# reach it - not just the ones that open on a card. Two hard checks, both measured off the
# rendered PNG rather than estimated from the font metrics.
for seg, meta in META.items():
    lines = meta['title'].split('\n')
    assert len(lines) <= L['titleMaxLines'], f'title-{seg} has {len(lines)} lines, max is {L["titleMaxLines"]}'
    # STANDING RULE: the title may not reach the picture. On a full-bleed shot the picture
    # starts at dropTop; assert against that, not against the scrim.
    top = L['dropTop']
    ink = Image.open(os.path.join(OUT, f'title-{seg}.png')).crop((0, top, W, H))
    assert ink.split()[-1].getbbox() is None, (
        f'title-{seg} ink reaches into the picture below y={top} - shorten the headline')
print(f'title clears the picture top (y={L["dropTop"]}) on all {len(META)} shorts')
