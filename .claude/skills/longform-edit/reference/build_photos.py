#!/usr/bin/env python3
"""REV1 items 1 + 3: before/after photo panels, J2-framed, cropped tight to Dan.

Dan's note: "crop this so that it only shows me, and eliminate all that
unnecessary space on the sides and the top". Every crop below is head-to-
mid-thigh so the two halves of a pair are framed the SAME - a comparison
only reads if the framing matches.
usage: build_photos.py [check]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

B = Path("/Volumes/Extreme/_edit_work/spraytan")
P = B / "photos"; OUT = B / "gfx"; OUT.mkdir(exist_ok=True)
W, H = 1920, 1080
BG = (13, 14, 11); OLIVE = (140, 152, 88); WHITE = (255, 255, 255)
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'

# crop = (x0, y0, x1, y1) as PERCENT of the EXIF-corrected image
# crop = (x0, y0, x1, y1) as PERCENT of the EXIF-corrected image
#
# REV2 (Dan): "make sure they're all centered within the frame you use. Some of
# them are not centered, and some are going off the side." Every crop is now
# centred on his BODY CENTRE with a real margin on both sides, so no fist, elbow
# or hip touches an edge. The three that were actually broken: tan_a and tan_b
# had the crop's right edge cutting through his arm, and tan_intro's left fist
# sat on the frame line. The double-biceps frames (pale_intro, pale_c, tan_c)
# were centred but had only ~2-5% margin, which reads as "going off the side"
# once an olive frame is drawn around it.
# Measuring this automatically does not work here: a torso-band skin mask finds
# the torso, not the raised arms, and sunlit limestone is also r>g>b at the same
# saturation. Set by eye against a centre-line overlay, then verified.
CROPS = {
 "pale_intro": (17.5, 20, 75.5, 87),  # 844C5D19  double biceps, poolside (Dan's pick)
 "tan_intro":  (28.0,  6, 85.0, 100), # photo-103 double biceps  -> pairs with pale_intro
 "pale_a":     (26.0,  9, 67.0, 74),  # 1654FF4C  standing front, arms down
 "tan_a":      (20.0, 10, 95.0, 96),  # photo-138 standing front, arms down
 "pale_b":     (29.0, 10, 67.0, 72),  # 4A3E7A35  standing, hands at hips
 "tan_b":      (26.0, 12, 85.5, 94),  # photo-13  standing, hand at hip (shorts, to match)
 "pale_c":     (21.5, 18, 81.5, 86),  # 2263A1D9  double biceps, wide
 "tan_c":      ( 7.0, 20, 97.0, 100), # photo-125 double biceps
}
SRC = {k: (P / (k + (".png" if k.startswith("pale") else ".jpg"))) for k in CROPS}

def load(key):
    im = ImageOps.exif_transpose(Image.open(SRC[key])).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = CROPS[key]
    return im.crop((int(w*x0/100), int(h*y0/100), int(w*x1/100), int(h*y1/100)))

def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + gap
    return x - gap - xy[0]

def panel(im, base, x_off, label):
    """Draw one 960x1080 half: photo fitted in an olive frame + eyebrow label."""
    d = ImageDraw.Draw(base)
    d.rectangle([x_off, 0, x_off+959, H], fill=BG+(255,))
    BOXW, BOXH, TOP = 872, 880, 76
    fit = im.copy(); fit.thumbnail((BOXW, BOXH), Image.LANCZOS)
    px = x_off + (960 - fit.width)//2
    py = TOP + (BOXH - fit.height)//2
    base.paste(fit, (px, py))
    d.rectangle([px-3, py-3, px+fit.width+2, py+fit.height+2], outline=OLIVE+(255,), width=3)
    f = ImageFont.truetype(COPPER, 30)
    tw = sum(f.getlength(c)+6 for c in label)
    lx = x_off + (960 - tw)//2
    ly = TOP + BOXH + 26
    d.rectangle([lx-16, ly-8, lx+tw+8, ly+40], fill=BG+(235,))
    spaced(d, (lx, ly), label, f, OLIVE+(255,), 6)

def two_up(key_l, key_r, name, left_only=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    panel(load(key_l), im, 0, "BEFORE")
    if not left_only:
        panel(load(key_r), im, 960, "AFTER")
        ImageDraw.Draw(im).rectangle([957, 60, 962, H-60], fill=OLIVE+(255,))
    p = OUT / f"photo_{name}.png"; im.save(p); print("  ", p.name, im.size)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # contact sheet of every crop, to eyeball the framing before compositing
        ims = []
        for k in CROPS:
            c = load(k); c.thumbnail((360, 460), Image.LANCZOS)
            pad = Image.new("RGB", (360, 460), (32, 32, 32))
            pad.paste(c, ((360-c.width)//2, (460-c.height)//2))
            dd = ImageDraw.Draw(pad)
            dd.text((6, 6), k, fill=(255, 230, 0),
                    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20))
            ims.append(pad)
        sheet = Image.new("RGB", (360*4, 460*2))
        for i, m in enumerate(ims): sheet.paste(m, (360*(i % 4), 460*(i//4)))
        sheet.save(B/"photos"/"CROPCHECK.png"); print("wrote CROPCHECK.png")
    else:
        two_up("pale_intro", "tan_intro", "intro_left", left_only=True)
        two_up("pale_intro", "tan_intro", "intro_both")
        two_up("pale_a", "tan_a", "pair_a")
        two_up("pale_b", "tan_b", "pair_b")
        two_up("pale_c", "tan_c", "pair_c")
