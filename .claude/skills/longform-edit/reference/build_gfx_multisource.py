#!/usr/bin/env python3
"""J2 tactical chips + AbsByAI.com watermark for a longform cut.
Constants verbatim from .claude/skills/shorts/reference/band/assets.py.
Chip times are given in SOURCE seconds and mapped to OUTPUT time via edl.json,
so a revision to the cut only needs a re-run of this script.
usage: build_gfx.py <slug> <chips.py>"""
from PIL import Image, ImageDraw, ImageFont
import json, sys, importlib.util
from pathlib import Path

slug, chips_file = sys.argv[1], sys.argv[2]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
OUT = BASE / "gfx"; OUT.mkdir(exist_ok=True)
W, H = 1920, 1080
BG = (13, 14, 11); OLIVE = (140, 152, 88); WHITE = (255, 255, 255)
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'

spec = importlib.util.spec_from_file_location("c", chips_file)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CHIPS = mod.CHIPS

ranges = json.load(open(BASE / "edl.json"))["ranges"]

def src_to_out(src, t):
    off = 0.0
    for r in ranges:
        d = round(r["end"] - r["start"], 3)
        if r["source"] == src and r["start"] <= t < r["end"]:
            return round(off + (t - r["start"]), 2)
        off = round(off + d, 3)
    return None

def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + gap
    return x

def chip(key, eyebrow, title, x=120, y=800):
    f_eye = ImageFont.truetype(COPPER, 26)
    size = 58
    while size > 34:
        f_ttl = ImageFont.truetype(IMPACT, size)
        if ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(title, font=f_ttl) <= 1500: break
        size -= 2
    f_ttl = ImageFont.truetype(IMPACT, size)
    pad_x, pad_y = 26, 16
    tw = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(title, font=f_ttl))
    ew = sum(f_eye.getlength(c) + 5 for c in eyebrow)
    boxw = int(max(tw + pad_x * 2, ew + pad_x * 2)); boxh = size + pad_y * 2
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ebh = 36
    d.rectangle([x, y - 4, x + int(ew) + pad_x, y - 4 + ebh], fill=BG + (225,))
    spaced(d, (x + 10, y), eyebrow, f_eye, OLIVE + (255,), 5)
    top = y + 40
    d.rectangle([x, top, x + boxw, top + boxh], fill=BG + (238,), outline=OLIVE + (255,), width=3)
    d.text((x + pad_x, top + pad_y - 6), title, font=f_ttl, fill=WHITE + (255,))
    p = OUT / f"chip_{key}.png"; im.save(p); return p

def watermark():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(MANROPE, 30)          # Manrope: Copperplate is small-caps
    txt = "AbsByAI.com"
    wid = f.getlength(txt)
    x0, y0 = W - wid - 46, H - 62
    d.text((x0 + 2, y0 + 2), txt, font=f, fill=(0, 0, 0, 150))
    d.text((x0, y0), txt, font=f, fill=(255, 255, 255, 205))
    p = OUT / "wm.png"; im.save(p); return p

DUR = 6.4
timings, missed = [], []
for key, src, src_t, eye, ttl in CHIPS:
    out_t = src_to_out(src, src_t)
    if out_t is None:
        missed.append((key, f"{src} {src_t}")); continue
    chip(key, eye, ttl)
    timings.append({"key": key, "start": out_t, "end": round(out_t + DUR, 2)})
timings.sort(key=lambda c: c["start"])
for a, b in zip(timings, timings[1:]):
    if b["start"] < a["end"] + 0.3:
        print(f"WARN overlap: {a['key']} ({a['start']}-{a['end']}) vs {b['key']} ({b['start']})")
watermark()
json.dump(timings, open(BASE / "chip_timings.json", "w"), indent=1)
for k, t in missed: print(f"WARN: chip {k} src {t} not inside any kept range")
print(f"{len(timings)} chips + watermark -> {OUT}")
for c in timings: print(f"  {c['key']:26s} out {c['start']:8.2f}")
