#!/usr/bin/env python3
"""Ad 1 layout assets — two style variants.
V1 = J2 tactical (BG 13,14,11 / OLIVE 140,152,88 / Impact + Copperplate eyebrows / Manrope URL)
V2 = MadMuscles modern (near-black / white Arial Bold / red accent)
Outputs to assets_v1/ and assets_v2/.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os

BG = (13, 14, 11); OLIVE = (140, 152, 88); RED = (226, 34, 34)
W, H = 1920, 1080
F = lambda p, s: ImageFont.truetype(p, s)
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
ARIALB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MANROPE = os.path.expanduser("~/Library/Fonts/Manrope.ttf")
COPPER = "/System/Library/Fonts/Copperplate.ttc"

A = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
GOAL = f"{A}/Media/example pictures/dan by pool.png"
BEFORE = f"{A}/Media/ad-assets/ad2-nutritionist/full/03_before_picture.png"
SHOTS = [
    f"{A}/photos/finalized social media photos/photo-180_FINAL_PRIMARY copy.png",   # landscape
    f"{A}/photos/finalized social media photos/Dan-flag-FINAL.jpg",                 # landscape
    f"{A}/photos/finalized social media photos/dan-pool-shoot-towel-smile-retouched-final.jpg",  # portrait
    f"{A}/photos/finalized social media photos/photo-137_FINAL_PRIMARY.jpg",        # portrait
]
APP_ASSESS = f"{A}/Media/ad-assets/batch1-ads/full/app_trainer_assessment.png"
APP_WORKOUT = f"{A}/Media/ad-assets/batch1-ads/full/app_trainer_workout.png"
APP_NUTRI = f"{A}/Media/ad-assets/ad2-nutritionist/full/09_app_nutrition_plan.png"

def spaced(s, n=2):
    return (" " * n).join(list(s.replace(" ", "  ")))

def tag_png(variant, path, text="AI-GENERATED"):
    """Small tag pill, transparent PNG."""
    if variant == 1:
        f = F(COPPER, 34)
        t = text  # Copperplate is small-caps; text is all-caps by design
        im = Image.new("RGBA", (10, 10))
        d = ImageDraw.Draw(im)
        tw = d.textlength(t, font=f)
        im = Image.new("RGBA", (int(tw) + 44, 56), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, im.width - 1, 55], fill=(13, 14, 11, 225), outline=OLIVE, width=2)
        d.text((22, 9), t, font=f, fill=(235, 235, 230, 255))
    else:
        f = F(ARIALB, 34)
        im = Image.new("RGBA", (10, 10))
        d = ImageDraw.Draw(im)
        tw = d.textlength(text, font=f)
        im = Image.new("RGBA", (int(tw) + 44, 56), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, im.width - 1, 55], radius=14, fill=(200, 24, 24, 235))
        d.text((22, 8), text, font=f, fill=(255, 255, 255, 255))
    im.save(path)

def panel_bg(variant):
    im = Image.new("RGB", (W, H), BG if variant == 1 else (8, 8, 10))
    if variant == 1:
        d = ImageDraw.Draw(im)
        d.rectangle([24, 24, W - 25, H - 25], outline=(40, 43, 34), width=2)
    return im

def blur_bg(img):
    """MadMuscles-style: blurred cover of the image itself."""
    bg = ImageOps.fit(img.convert("RGB"), (W, H))
    return bg.filter(ImageFilter.GaussianBlur(40)).point(lambda p: int(p * 0.45))

def compose_panel(variant, src, out, tag=None, mode="fit", crop_top=None, zoom_pad=False):
    img = Image.open(src).convert("RGB")
    if crop_top:
        img = img.crop((0, 0, img.width, min(img.height, crop_top)))
    if mode == "cover":
        base = ImageOps.fit(img, (W, H))
        canvas = base
    else:
        canvas = panel_bg(variant) if variant == 1 else blur_bg(img)
        h = H - (96 if variant == 1 else 0)
        w = int(img.width * h / img.height)
        if w > W - 100:
            w = W - 100; h = int(img.height * w / img.width)
        img = img.resize((w, h), Image.LANCZOS)
        canvas.paste(img, ((W - w) // 2, (H - h) // 2))
        if variant == 2:
            d = ImageDraw.Draw(canvas)
            x0, y0 = (W - w) // 2, (H - h) // 2
            d.rectangle([x0 - 2, y0 - 2, x0 + w + 1, y0 + h + 1], outline=(255, 255, 255), width=2)
    if tag:
        t = Image.open(tag).convert("RGBA")
        canvas.paste(t, (W // 2 - t.width // 2, 40), t)
    canvas.save(out, quality=92)

def cta_bar(variant, path):
    """Persistent lower-third CTA bar, transparent PNG, full width."""
    im = Image.new("RGBA", (W, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if variant == 1:
        d.rectangle([0, 0, W, 96], fill=(13, 14, 11, 215))
        d.rectangle([0, 0, W, 4], fill=OLIVE + (255,))
        f1 = F(IMPACT, 46); f2 = F(MANROPE, 40)
        t1 = "TAP THE BUTTON BELOW"; t2 = "or go to AbsByAI.com"
        w1 = d.textlength(t1, font=f1); w2 = d.textlength(t2, font=f2)
        gap = 48
        x = (W - w1 - w2 - gap) / 2
        d.text((x, 22), t1, font=f1, fill=(255, 255, 255, 255))
        d.text((x + w1 + gap, 26), t2, font=f2, fill=OLIVE + (255,))
    else:
        # red pill centered
        f1 = F(ARIALB, 44)
        t1 = "Tap below — or go to AbsByAI.com"
        w1 = d.textlength(t1, font=f1)
        pw = int(w1) + 80
        x0 = (W - pw) // 2
        d.rounded_rectangle([x0, 8, x0 + pw, 88], radius=40, fill=(200, 24, 24, 240))
        d.text((x0 + 40, 24), t1, font=f1, fill=(255, 255, 255, 255))
    im.save(path)

def end_card(variant, path):
    img = Image.open(GOAL).convert("RGB")
    if variant == 1:
        canvas = panel_bg(1)
    else:
        canvas = blur_bg(img)
    h = 820; w = int(img.width * h / img.height)
    img = img.resize((w, h), Image.LANCZOS)
    x = W // 2 - w // 2
    canvas.paste(img, (x, 70))
    d = ImageDraw.Draw(canvas)
    if variant == 2:
        d.rectangle([x - 2, 68, x + w + 1, 70 + h + 1], outline=(255, 255, 255), width=2)
    # tag on image
    tagf = f"assets_v{variant}/tag.png"
    t = Image.open(tagf).convert("RGBA")
    canvas.paste(t, (W // 2 - t.width // 2, 84), t)
    if variant == 1:
        f1 = F(IMPACT, 64); f2 = F(MANROPE, 44)
        t1 = "SEE YOURSELF WITH ABS"; t2 = "Tap below  ·  AbsByAI.com"
        d.text(((W - d.textlength(t1, font=f1)) / 2, 908), t1, font=f1, fill=(255, 255, 255))
        d.text(((W - d.textlength(t2, font=f2)) / 2, 992), t2, font=f2, fill=OLIVE)
    else:
        f1 = F(ARIALB, 60)
        t1 = "See yourself with abs — free"
        d.text(((W - d.textlength(t1, font=f1)) / 2, 916), t1, font=f1, fill=(255, 255, 255))
        f2 = F(ARIALB, 44)
        t2 = "Tap below — or go to AbsByAI.com"
        d.text(((W - d.textlength(t2, font=f2)) / 2, 1000), t2, font=f2, fill=(255, 90, 90))
    canvas.save(path, quality=92)

for v in (1, 2):
    os.makedirs(f"assets_v{v}", exist_ok=True)
    tag_png(v, f"assets_v{v}/tag.png")
    # goal image panel (opener + mid inserts)
    compose_panel(v, GOAL, f"assets_v{v}/p_goal.jpg", tag=f"assets_v{v}/tag.png")
    compose_panel(v, BEFORE, f"assets_v{v}/p_before.jpg")
    # shoot photos: landscape full-bleed, portrait panel
    compose_panel(v, SHOTS[0], f"assets_v{v}/p_shot1.jpg", mode="cover")
    compose_panel(v, SHOTS[1], f"assets_v{v}/p_shot2.jpg", mode="cover")
    compose_panel(v, SHOTS[2], f"assets_v{v}/p_shot3.jpg")
    compose_panel(v, SHOTS[3], f"assets_v{v}/p_shot4.jpg")
    # app screens: top crop to ~16:10 of the 900-wide capture
    compose_panel(v, APP_ASSESS, f"assets_v{v}/p_app_assess.jpg", crop_top=1500)
    compose_panel(v, APP_WORKOUT, f"assets_v{v}/p_app_workout.jpg", crop_top=1500)
    compose_panel(v, APP_NUTRI, f"assets_v{v}/p_app_nutri.jpg", crop_top=1500)
    # panel BG for video inserts (phone clip / app clip)
    panel_bg(v).save(f"assets_v{v}/p_vidbg.jpg", quality=92)
    cta_bar(v, f"assets_v{v}/cta_bar.png")
    end_card(v, f"assets_v{v}/end_card.jpg")
print("assets done")
