#!/usr/bin/env python3
"""J2 tactical chips for 'Why You Should Invest More In Your Health'.
Constants verbatim from the shorts J2 system (via longform-edit reference).
Chip times are given in SOURCE seconds and mapped to OUTPUT time via edl.json,
so a revision to the cut only needs a re-run of this script."""
from PIL import Image, ImageDraw, ImageFont
import json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "gfx"; OUT.mkdir(exist_ok=True)
W, H = 1920, 1080
BG = (13, 14, 11); OLIVE = (140, 152, 88); WHITE = (255, 255, 255)
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'

edl = json.load(open(HERE / "edl.json"))
ranges = edl["ranges"]

def src_to_out(t):
    off = 0.0
    for r in ranges:
        d = round(r["end"] - r["start"], 3)
        if r["start"] <= t < r["end"]:
            return round(off + (t - r["start"]), 2)
        off = round(off + d, 3)
    return None

def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + gap
    return x

def chip(key, eyebrow, title, x=120, y=800):
    f_eye = ImageFont.truetype(COPPER, 26); f_ttl = ImageFont.truetype(IMPACT, 58)
    pad_x, pad_y = 26, 16
    tw = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(title, font=f_ttl))
    ew = sum(f_eye.getlength(c) + 5 for c in eyebrow)
    boxw = int(max(tw + pad_x * 2, ew + pad_x * 2)); boxh = 58 + pad_y * 2
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
    f = ImageFont.truetype(MANROPE, 30)
    txt = "AbsByAI.com"
    wid = f.getlength(txt)
    x0, y0 = W - wid - 46, H - 62
    d.text((x0 + 2, y0 + 2), txt, font=f, fill=(0, 0, 0, 150))
    d.text((x0, y0), txt, font=f, fill=(255, 255, 255, 205))
    p = OUT / "wm.png"; im.save(p); return p

# (key, src_time, eyebrow, title)
CHIPS = [
    ("title",   3.0,    "ABS BY AI // DAN ROSE",            "INVEST MORE IN YOUR HEALTH"),
    ("r1",      9.6,    "REASON 01",                        "THE HALO EFFECT"),
    ("r2",      392.7,  "REASON 02",                        "PRODUCTIVITY"),
    ("r3",      628.3,  "REASON 03",                        "MENTAL HEALTH"),
    ("r4",      742.5,  "REASON 04",                        "BAD HEALTH IS EXPENSIVE"),
    ("dead",    931.5,  "REMEMBER",                         "MONEY IS NO GOOD IF YOU'RE DEAD"),
    ("nocut",   1233.5, "NEVER CUT",                        "FOOD - MATTRESS - SHELTER"),
    ("cut1",    1346.8, "CUT 01",                           "BARS & CLUBS"),
    ("cut2",    1464.9, "CUT 02",                           "RESTAURANTS"),
    ("cut3",    1570.8, "CUT 03",                           "JUNK FOOD"),
    ("cut4",    1612.4, "CUT 04",                           "VACATIONS"),
    ("cut5",    1699.6, "CUT 05 // NOT MEDICAL ADVICE",     "THERAPY & PSYCH MEDS"),
    ("t1a",     1858.3, "TIER 01 // IF YOU'RE BROKE",       "HOME WORKOUT SETUP - UNDER $100"),
    ("t1b",     1979.0, "TIER 01 // IF YOU'RE BROKE",       "BASIC HEALTHY FOOD"),
    ("t2a",     2105.5, "TIER 02 // MIDDLE CLASS",          "PREMIUM PROTEIN"),
    ("t2b",     2270.0, "TIER 02 // MIDDLE CLASS",          "A GREAT MATTRESS"),
    ("t2c",     2499.0, "TIER 02 // MIDDLE CLASS",          "GYM MEMBERSHIP"),
    ("t2d",     2664.5, "TIER 02 // MIDDLE CLASS",          "SLEEP TRACKER"),
    ("t2e",     2789.0, "TIER 02 // MIDDLE CLASS",          "WEIGHT LOSS MEDICATION"),
    ("t2f",     2967.3, "TIER 02 // MIDDLE CLASS",          "TRT"),
    ("t2g",     3078.0, "TIER 02 // MIDDLE CLASS",          "FISH OIL - VITAMIN D - MAGNESIUM"),
    ("t3a",     3258.5, "TIER 03 // $10K+ PER MONTH",       "HOME GYM"),
    ("t3b",     3419.7, "TIER 03 // $10K+ PER MONTH",       "MEAL PREP OR PERSONAL CHEF"),
    ("t3c",     3547.2, "TIER 03 // $10K+ PER MONTH",       "OUTSOURCE YOUR CHORES"),
    ("t3d",     3597.0, "TIER 03 // $10K+ PER MONTH",       "TRAINER & NUTRITIONIST"),
    ("beyond",  3799.0, "BEYOND THE LIST",                  "THE BRYAN JOHNSON TIER"),
    ("cta",     4066.0, "GET STARTED FREE",                 "ABSBYAI.COM"),
]

DUR = 6.4
timings = []
for key, src_t, eye, ttl in CHIPS:
    out_t = src_to_out(src_t)
    if out_t is None:
        print(f"WARN: chip {key} src {src_t} not inside any kept range")
        continue
    chip(key, eye, ttl)
    timings.append({"key": key, "start": out_t, "end": round(out_t + DUR, 2)})
    print(f"chip {key:8s} src {src_t:8.1f} -> out {out_t:8.2f}")

# no overlapping chips
for a, b in zip(timings, timings[1:]):
    if b["start"] < a["end"] + 0.3:
        print(f"WARN: chips {a['key']} and {b['key']} overlap/too close")

watermark()
json.dump(timings, open(HERE / "chip_timings.json", "w"), indent=1)
print(f"{len(timings)} chips + watermark -> {OUT}")
