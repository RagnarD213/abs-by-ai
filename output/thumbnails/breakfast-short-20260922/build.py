#!/usr/bin/env python3
"""Build two review thumbnails for Why I Skip Breakfast Every Day.

The pool image and studio subject are real finalized photos. Only the
background behind the studio subject was generated.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
W, H = 1080, 1920
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
WHITE = (255, 255, 248)
YELLOW = (255, 218, 0)


def fit_text(draw, text, max_width, initial, stroke=0):
    for size in range(initial, 50, -2):
        font = ImageFont.truetype(IMPACT, size)
        bb = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bb[2] - bb[0] <= max_width:
            return font
    raise ValueError(text)


def draw_copy(im, label, outlined=False):
    d = ImageDraw.Draw(im)
    if outlined:
        d.rounded_rectangle((25, 25, W-25, H-25), radius=28,
                            outline=(255, 255, 255, 245), width=5)
    badge = ImageFont.truetype(ARIAL, 49)
    bb = d.textbbox((0, 0), label, font=badge)
    badge_w = bb[2] - bb[0] + 48
    d.rounded_rectangle((57, 53, 57+badge_w, 122), radius=15, fill=(251, 48, 45))
    d.text((81, 58), label, font=badge, fill=WHITE)
    for text, y, color in [
        ("WHY I SKIP", 166, WHITE),
        ("BREAKFAST", 330, YELLOW),
    ]:
        font = fit_text(d, text, 965, 174, 5)
        bb = d.textbbox((0, 0), text, font=font, stroke_width=5)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        d.text((x, y), text, font=font, fill=color,
               stroke_width=5, stroke_fill=(15, 12, 9))
    return im


def pool():
    source = PROJECT / "photos/pool shoot | 7-31-26 | dan | mindi/top-10-social/edited/photo-247_FINAL_PRIMARY.jpg"
    with Image.open(source) as original:
        original = ImageOps.exif_transpose(original).convert("RGB")
        photo = original.resize((W, round(original.height * W / original.width)), Image.Resampling.LANCZOS)
        # The dark header gives the headline clear space above his hair.
        im = Image.new("RGB", (W, H), (14, 17, 17))
        layer = Image.new("RGBA", (W, H))
        layer.paste(photo.convert("RGBA"), (0, 460))
        alpha = Image.new("L", (W, H))
        alpha.paste(255, (0, 460, W, H))
        grad = Image.new("L", (W, 180))
        gp = grad.load()
        for y in range(180):
            a = int(255 * (y / 180) ** 1.2)
            for x in range(W):
                gp[x, y] = a
        alpha.paste(grad, (0, 460))
        im.paste(layer, (0, 0), alpha)
        # Lightly darken the lower edges so the face and abs stay the focus.
        shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        sd.rectangle((0, 1630, W, H), fill=(0, 0, 0, 38))
        im = Image.alpha_composite(im.convert("RGBA"), shade)
        im = draw_copy(im, "EVERY DAY")
        im.convert("RGB").save(ROOT / "A-pool-shoot.jpg", quality=94, subsampling=0)


def studio():
    with Image.open(ROOT / "studio-breakfast-background.png") as bg:
        im = ImageOps.fit(bg.convert("RGB"), (W, H), method=Image.Resampling.LANCZOS).convert("RGBA")
    with Image.open(PROJECT / "photos/finalized social media photos/_cutouts/studio-gray-67_CUTOUT.png") as original:
        person = original.convert("RGBA")
        # Keep the original studio portrait pixels. The cutout already has alpha.
        person = person.resize((round(person.width * 0.365), round(person.height * 0.365)),
                               Image.Resampling.LANCZOS)
    x, y = -62, 397
    alpha = Image.new("L", (W, H))
    alpha.paste(person.getchannel("A"), (x, y))
    outline = alpha.filter(ImageFilter.MaxFilter(17))
    white = Image.new("RGBA", (W, H), (250, 248, 240, 0))
    white.putalpha(outline)
    im = Image.alpha_composite(im, white)
    fg = Image.new("RGBA", (W, H))
    fg.paste(person, (x, y))
    im = Image.alpha_composite(im, fg)
    im = draw_copy(im, "EVERY DAY", outlined=True)
    im.convert("RGB").save(ROOT / "B-studio-design.jpg", quality=94, subsampling=0)


if __name__ == "__main__":
    pool()
    studio()
    a = Image.open(ROOT / "A-pool-shoot.jpg")
    b = Image.open(ROOT / "B-studio-design.jpg")
    preview = Image.new("RGB", (540, 480), (16, 16, 16))
    preview.paste(a.resize((270, 480), Image.Resampling.LANCZOS), (0, 0))
    preview.paste(b.resize((270, 480), Image.Resampling.LANCZOS), (270, 0))
    preview.save(ROOT / "phone-size-comparison.jpg", quality=92)
