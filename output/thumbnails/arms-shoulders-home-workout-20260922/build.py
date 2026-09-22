from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PHOTOS = ROOT / "photos/finalized social media photos"
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_SMALL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
W, H = 1280, 720
NAVY = (8, 19, 32)
YELLOW = (255, 215, 54)
WHITE = (255, 255, 250)


def cover(im):
    ratio = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.Resampling.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def title(draw, xy, txt, size, fill=WHITE, stroke=5):
    draw.text(xy, txt, font=ImageFont.truetype(FONT, size), fill=fill,
              stroke_width=stroke, stroke_fill=NAVY)


def subtitle(draw, xy, txt, size=43):
    draw.text(xy, txt, font=ImageFont.truetype(FONT_SMALL, size), fill=WHITE,
              stroke_width=3, stroke_fill=NAVY)


def darken_left(im, strength=220, width=660):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = overlay.load()
    for x in range(width):
        a = round(strength * (1 - x / width) ** 1.65)
        for y in range(H):
            px[x, y] = (3, 14, 24, a)
    return Image.alpha_composite(im.convert("RGBA"), overlay)


def save(im, name):
    im.convert("RGB").save(OUT / name, "JPEG", quality=93, optimize=True, subsampling=0)


def person_cutout(name, target_h):
    im = Image.open(PHOTOS / "_cutouts" / name).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * target_h / im.height), target_h), Image.Resampling.LANCZOS)


# 1. Real pool photo, front double biceps.
im = cover(Image.open(PHOTOS / "photo-122_FINAL_PRIMARY.jpg").convert("RGB"))
im = ImageEnhance.Contrast(im).enhance(1.08)
im = darken_left(im, 195, 560)
d = ImageDraw.Draw(im)
title(d, (42, 18), "2 Min Home", 94, YELLOW)
title(d, (42, 117), "Arm Workout", 94, YELLOW)
save(im, "01-pool-double-biceps.jpg")

# 2. Studio triceps pose, with a clear text column.
im = Image.new("RGBA", (W, H), NAVY + (255,))
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 742, H), fill=(10, 28, 44, 255))
d.polygon([(650, 0), (780, 0), (590, H), (460, H)], fill=(14, 66, 80, 255))
d.rectangle((0, 646, W, H), fill=(231, 190, 43, 255))
person = person_cutout("studio-blue-89_CUTOUT.png", 820)
im.alpha_composite(person, (810, 0))
d = ImageDraw.Draw(im)
title(d, (54, 83), "ARMS +", 120, YELLOW)
title(d, (54, 214), "SHOULDERS", 96)
subtitle(d, (61, 535), "HOME WORKOUT", 45)
save(im, "02-studio-triceps.jpg")

# 3. Retouched curl frame from the actual final video.
source = OUT / "retouched-curl-frame.png"
im = cover(Image.open(source).convert("RGB"))
im = darken_left(im, 215, 620)
d = ImageDraw.Draw(im)
title(d, (55, 376), "2-6 MIN", 105, YELLOW)
title(d, (55, 497), "ARM WORKOUT", 82)
save(im, "03-video-curl-retouched.jpg")

# 4. Studio double biceps with a clean, simple no-gym promise.
im = Image.new("RGBA", (W, H), NAVY + (255,))
d = ImageDraw.Draw(im)
d.polygon([(0, 0), (W, 0), (W, H), (560, H)], fill=(11, 62, 76, 255))
d.ellipse((745, -150, 1450, 555), fill=(17, 83, 96, 255))
person = person_cutout("studio-blue-66_CUTOUT.png", 720)
im.alpha_composite(person, (545, 0))
d = ImageDraw.Draw(im)
title(d, (52, 113), "NO GYM", 122, YELLOW)
title(d, (52, 261), "BIG ARMS", 112)
subtitle(d, (61, 571), "DUMBBELLS ONLY", 38)
save(im, "04-studio-no-gym.jpg")

# Review sheet.
sheet = Image.new("RGB", (W * 2, H * 2), "white")
for i, name in enumerate([
    "01-pool-double-biceps.jpg", "02-studio-triceps.jpg",
    "03-video-curl-retouched.jpg", "04-studio-no-gym.jpg",
]):
    sheet.paste(Image.open(OUT / name), ((i % 2) * W, (i // 2) * H))
sheet.save(OUT / "comparison.jpg", "JPEG", quality=90, optimize=True)
