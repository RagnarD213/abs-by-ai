#!/usr/bin/env python3
"""v3 inserts: Oura / Whoop product cards, the SUPPLEMENTS card that covers the
recut supplements joint, and the Bryan Johnson PiP window (frame + attribution).
J2 constants identical to build_gfx.py. All cards are full-frame 1920x1080 RGBA
so composite.py can overlay them at 0:0 like the chips."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / "gfx"; OUT.mkdir(exist_ok=True)
SRC = Path("/tmp/ihv3/prod")
W, H = 1920, 1080
BG = (13, 14, 11); OLIVE = (140, 152, 88); WHITE = (255, 255, 255)
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'

def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + gap
    return x

# ---------- product card: J2 frame, light product well, name plate ----------
# Sits viewer-left over the pantry door. The 10% zoom pulls the door's right
# edge in to ~x=560, so the card is kept inside x=[55, 495] to clear Dan.
CARD_X, CARD_Y, CARD_W, CARD_H = 55, 225, 440, 520
WELL_PAD = 18
PLATE_H = 118

def product_card(key, img_path, alpha_crop, eyebrow, title, bgcolor=(246, 246, 242)):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, y, cw, ch = CARD_X, CARD_Y, CARD_W, CARD_H
    d.rectangle([x, y, x + cw, y + ch], fill=BG + (238,), outline=OLIVE + (255,), width=3)
    well = [x + WELL_PAD, y + WELL_PAD, x + cw - WELL_PAD, y + ch - PLATE_H]
    d.rectangle(well, fill=bgcolor + (255,))

    p = Image.open(img_path).convert('RGBA')
    if alpha_crop:
        bb = p.getchannel('A').getbbox()
        if bb: p = p.crop(bb)
    else:
        p = p.crop(alpha_crop) if isinstance(alpha_crop, tuple) else p
    ww = well[2] - well[0] - 34; wh = well[3] - well[1] - 34
    sc = min(ww / p.width, wh / p.height)
    p = p.resize((int(p.width * sc), int(p.height * sc)), Image.LANCZOS)
    px = well[0] + (well[2] - well[0] - p.width) // 2
    py = well[1] + (well[3] - well[1] - p.height) // 2
    im.alpha_composite(p, (px, py))

    f_eye = ImageFont.truetype(COPPER, 22); f_ttl = ImageFont.truetype(IMPACT, 46)
    ty = well[3] + 16
    spaced(d, (x + 20, ty), eyebrow, f_eye, OLIVE + (255,), 4)
    d.text((x + 20, ty + 34), title, font=f_ttl, fill=WHITE + (255,))
    im.save(OUT / f"{key}.png"); print("wrote", key, "->", OUT / f"{key}.png")

def crop_card(key, img_path, box, eyebrow, title):
    """same card, but the source is an opaque photo cropped to `box`."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, y, cw, ch = CARD_X, CARD_Y, CARD_W, CARD_H
    d.rectangle([x, y, x + cw, y + ch], fill=BG + (238,), outline=OLIVE + (255,), width=3)
    well = [x + WELL_PAD, y + WELL_PAD, x + cw - WELL_PAD, y + ch - PLATE_H]
    p = Image.open(img_path).convert('RGB').crop(box)
    tw, th = well[2] - well[0], well[3] - well[1]
    sc = max(tw / p.width, th / p.height)
    p = p.resize((int(p.width * sc) + 1, int(p.height * sc) + 1), Image.LANCZOS)
    p = p.crop(((p.width - tw) // 2, (p.height - th) // 2,
                (p.width - tw) // 2 + tw, (p.height - th) // 2 + th))
    im.paste(p, (well[0], well[1]))
    d.rectangle(well, outline=OLIVE + (160,), width=2)
    f_eye = ImageFont.truetype(COPPER, 22); f_ttl = ImageFont.truetype(IMPACT, 46)
    ty = well[3] + 16
    spaced(d, (x + 20, ty), eyebrow, f_eye, OLIVE + (255,), 4)
    d.text((x + 20, ty + 34), title, font=f_ttl, fill=WHITE + (255,))
    im.save(OUT / f"{key}.png"); print("wrote", key)

# 1. Oura Ring 4 — official product render (ouraring.com), beige backdrop kept
crop_card("prod_oura", SRC / "oura_black-v2.png", (300, 170, 960, 800),
          "SLEEP TRACKER", "OURA RING 4")

# 2. WHOOP 5.0 — official transparent band render (shop.whoop.com)
product_card("prod_whoop", SRC / "whoop_band.png", True,
             "SLEEP TRACKER", "WHOOP 5.0")

# 3. SUPPLEMENTS card — covers the 39:54 recut joint. J2 card, no photo:
#    no usable supplement-bottle photography exists in the repo (the only
#    candidate, ad-assets/.../hero_robot_supplements.png, is dominated by the
#    ad's robot arm and is off-tone for the longform).
def supplements_card():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, y, cw, ch = 55, 360, 560, 300
    d.rectangle([x, y, x + cw, y + ch], fill=BG + (238,), outline=OLIVE + (255,), width=3)
    f_eye = ImageFont.truetype(COPPER, 24); f_ttl = ImageFont.truetype(IMPACT, 72)
    f_sub = ImageFont.truetype(MANROPE, 26)
    spaced(d, (x + 26, y + 34), "TIER 02 // MIDDLE CLASS", f_eye, OLIVE + (255,), 5)
    d.text((x + 26, y + 84), "SUPPLEMENTS", font=f_ttl, fill=WHITE + (255,))
    d.text((x + 28, y + 186), "Fish oil  -  Vitamin D  -  Magnesium", font=f_sub,
           fill=(215, 215, 210, 255))
    d.line([x + 26, y + 232, x + cw - 26, y + 232], fill=OLIVE + (200,), width=3)
    d.text((x + 28, y + 244), "the cheap ones that actually matter", font=f_sub,
           fill=(160, 168, 120, 255))
    im.save(OUT / "supp_card.png"); print("wrote supp_card")
supplements_card()

# 4. Bryan Johnson PiP frame + attribution (the video itself is scaled by ffmpeg)
BJ_X, BJ_Y, BJ_W, BJ_H = 60, 330, 600, 338
def bj_frame():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([BJ_X - 4, BJ_Y - 4, BJ_X + BJ_W + 4, BJ_Y + BJ_H + 4],
                outline=OLIVE + (255,), width=4)
    bar_h = 46
    d.rectangle([BJ_X - 4, BJ_Y + BJ_H + 4, BJ_X + BJ_W + 4, BJ_Y + BJ_H + 4 + bar_h],
                fill=BG + (235,))
    f = ImageFont.truetype(MANROPE, 24)
    d.text((BJ_X + 14, BJ_Y + BJ_H + 15), "Bryan Johnson / YouTube", font=f,
           fill=(235, 235, 230, 255))
    im.save(OUT / "bj_frame.png"); print("wrote bj_frame", BJ_X, BJ_Y, BJ_W, BJ_H)
bj_frame()
