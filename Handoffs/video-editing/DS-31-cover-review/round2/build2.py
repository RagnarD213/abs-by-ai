#!/usr/bin/env python3
"""DS-31 cover round 2 (Dan, 2026-10-20): a ripped college student works out while a robot
does his homework on a laptop. Three unique designs: A is a younger AI Dan, B and C are other people.
Top text "Make Time To Work Out", bottom text "Let AI Do Your Homework". Images: Codex
gpt-6.1-sol high (A age-down edit pass once). Type set here. YouTube full cover + Instagram 3:4 grid layout.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = Path(__file__).resolve().parent
PROJECT = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
OUT = PROJECT / 'Short-form video content/AI Homework - DS-31/covers/round2'
ASSETS = OUT / 'assets'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
TOP, BOT = 'Make Time To Work Out', 'Let AI Do Your Homework'
IG_TOP, IG_BOT = 240, 1680          # Instagram grid shows rows 240-1680 of the 1080x1920 cover
records = []

PLATES = {'A': 'generated-A2.png', 'B': 'generated-B.png', 'C': 'generated-C.png'}
# Measured on each plate (fractions of width/height): faces, and the rows the IG panel must keep.
FACES = {'A': (0.60, 0.18, 0.76, 0.31), 'B': (0.23, 0.18, 0.36, 0.28), 'C': (0.64, 0.245, 0.79, 0.36)}
KEEP = {'A': (0.165, 0.76), 'B': (0.17, 0.79), 'C': (0.23, 0.75)}


def font(name, size, index=0):
    return ImageFont.truetype(str(SUP / name), size, index=index)


def fit(d, copy, name, size, maxwidth, index=0):
    f = font(name, size, index)
    while d.textbbox((0, 0), copy, font=f)[2] > maxwidth:
        size -= 2
        f = font(name, size, index)
    return f


def put(im, copy, x, y, name, size, color, maxwidth, align='center', index=0, shadow=None):
    d = ImageDraw.Draw(im)
    f = fit(d, copy, name, size, maxwidth, index)
    b = d.textbbox((0, 0), copy, font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    if align == 'center':
        x -= w // 2
    if shadow:
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((x - b[0] + 4, y - b[1] + 6), copy, font=f, fill=shadow)
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((x - b[0], y - b[1]), copy, font=f, fill=color)
    box = [x, y, x + w, y + h]
    assert box[0] >= 24 and box[2] <= W - 24, (copy, box)
    return box


def plate(k):
    im = Image.open(ASSETS / PLATES[k]).convert('RGB')
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2)).convert('RGBA')


def scrim(im, top, bottom, alpha, reverse=False, color=(5, 10, 16)):
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    for y in range(max(0, top), min(H, bottom)):
        t = (y - top) / max(1, bottom - top)
        d.line((0, y, W, y), fill=int(alpha * (t if reverse else 1 - t)))
    layer = Image.new('RGBA', (W, H), color + (0,))
    layer.putalpha(mask)
    return Image.alpha_composite(im, layer)


def face_box(k, place):
    """Face box on the final canvas; place maps plate coords to canvas (scale, dx, dy)."""
    s, dx, dy = place
    x0, y0, x1, y1 = FACES[k]
    return [round(x0 * W * s + dx), round(y0 * H * s + dy), round(x1 * W * s + dx), round(y1 * H * s + dy)]


def ig_panel(k, bg, band_top, band_bot, frame=None):
    """Instagram: the people/robot rows as a framed panel between two solid text bands."""
    src = plate(k)
    r0, r1 = round(KEEP[k][0] * H), round(KEEP[k][1] * H)
    avail = band_bot - band_top
    s = min(1.0, avail / (r1 - r0))
    crop = src.crop((0, r0, W, r1)).resize((round(W * s), round((r1 - r0) * s)), Image.Resampling.LANCZOS)
    im = Image.new('RGBA', (W, H), bg + (255,))
    dx = (W - crop.width) // 2
    dy = band_top + (avail - crop.height) // 2
    if frame:
        ImageDraw.Draw(im).rectangle((dx - 6, dy - 6, dx + crop.width + 5, dy + crop.height + 5), fill=frame)
    im.alpha_composite(crop, (dx, dy))
    return im, (s, dx, dy - r0 * s)


def design_a(ig):
    """Young AI Dan, blue campus gym. Tall DIN Condensed, white top line, sky-blue bottom, centred."""
    blue, navy = (110, 205, 255), (9, 22, 38)
    if ig:
        im, place = ig_panel('A', navy, 430, 1488)
        b1 = put(im, TOP, 540, 286, 'DIN Condensed Bold.ttf', 150, (255, 255, 255), 1000)
        b2 = put(im, BOT, 540, 1532, 'DIN Condensed Bold.ttf', 150, blue, 1000)
        return im, [b1, b2], face_box('A', place)
    im = scrim(plate('A'), 0, 420, 150, color=navy)
    im = scrim(im, 1380, H, 245, reverse=True, color=navy)
    b1 = put(im, TOP, 540, 120, 'DIN Condensed Bold.ttf', 200, (255, 255, 255), 1010, shadow=(0, 0, 0, 160))
    b2 = put(im, 'Let AI Do', 540, 1566, 'DIN Condensed Bold.ttf', 160, blue, 900, shadow=(0, 0, 0, 200))
    b2b = put(im, 'Your Homework', 540, b2[3] + 12, 'DIN Condensed Bold.ttf', 160, blue, 1000, shadow=(0, 0, 0, 200))
    return im, [b1, b2, b2b], face_box('A', (1, 0, 0))


def banner(im, box, fill, pad=(30, 22), outline=None):
    x0, y0, x1, y1 = box
    ImageDraw.Draw(im).rectangle((x0 - pad[0], y0 - pad[1], x1 + pad[0], y1 + pad[1]), fill=fill, outline=outline, width=6 if outline else 0)


def design_b(ig):
    """Other student, pull-ups in a dark amber gym. Impact on full-width banners: amber top, black bottom."""
    amber, ink = (255, 168, 38), (12, 10, 8)
    if ig:
        im, place = ig_panel('B', ink, 444, 1476, frame=amber)
        ty, by = 290, 1528
    else:
        im = plate('B')
        im = scrim(im, 1480, H, 200, reverse=True, color=(0, 0, 0))
        place, ty, by = (1, 0, 0), 120, 1640
    d = ImageDraw.Draw(im)
    f = fit(d, TOP, 'Impact.ttf', 120, 960)
    tmp = Image.new('RGBA', (W, H))
    bt = put(tmp, TOP, 540, ty, 'Impact.ttf', f.size, ink, 960)
    d.rectangle((0, bt[1] - 26, W, bt[3] + 26), fill=amber)
    bt = put(im, TOP, 540, ty, 'Impact.ttf', f.size, ink, 960)
    bb = put(tmp, BOT, 540, by, 'Impact.ttf', 120, (255, 255, 255), 960)
    d.rectangle((0, bb[1] - 26, W, bb[3] + 26), fill=ink, outline=amber, width=6)
    bb = put(im, BOT, 540, by, 'Impact.ttf', 120, (255, 255, 255), 960)
    boxes = [[0, bt[1] - 26, W, bt[3] + 26], [0, bb[1] - 26, W, bb[3] + 26]]
    return im, boxes, face_box('B', place)


def design_c(ig):
    """Other student, kettlebell in a bright daylight campus gym. Futura Condensed ExtraBold, left-aligned,
    red over navy with a red rule."""
    red, navy = (214, 40, 40), (16, 28, 52)
    if ig:
        im, place = ig_panel('C', (246, 244, 239), 470, 1452)
        b1 = put(im, 'Make Time To Work Out', 64, 290, 'Futura.ttc', 150, red, 950, 'left', index=4)
        ImageDraw.Draw(im).rectangle((66, b1[3] + 24, 330, b1[3] + 36), fill=red)
        b2 = put(im, 'Let AI Do Your Homework', 64, 1500, 'Futura.ttc', 150, navy, 950, 'left', index=4)
        return im, [b1, b2], face_box('C', place)
    im = scrim(plate('C'), 1500, H, 120, reverse=True, color=(246, 244, 239))
    b1 = put(im, 'Make Time', 64, 96, 'Futura.ttc', 168, red, 900, 'left', index=4)
    b1b = put(im, 'To Work Out', 64, b1[3] + 18, 'Futura.ttc', 168, red, 900, 'left', index=4)
    ImageDraw.Draw(im).rectangle((68, b1b[3] + 30, 340, b1b[3] + 44), fill=red)
    b2 = put(im, 'Let AI Do', 64, 1560, 'Futura.ttc', 150, navy, 900, 'left', index=4)
    b2b = put(im, 'Your Homework', 64, b2[3] + 16, 'Futura.ttc', 150, navy, 950, 'left', index=4)
    return im, [b1, b1b, b2, b2b], face_box('C', (1, 0, 0))


BUILDERS = {'A': design_a, 'B': design_b, 'C': design_c}
LABELS = {'A': 'Younger Me, Blue Gym', 'B': 'Pull-Ups, Amber Banners', 'C': 'Kettlebell, Bright Daylight'}
DESIGNS = {
    'A': 'Younger AI Dan curls a dumbbell beside a white robot typing on a laptop with textbooks; blue campus gym; tall DIN Condensed, white top, sky-blue bottom, centred',
    'B': 'A different student does pull-ups while a black robot types on a laptop on a stack of textbooks; dark amber gym; Impact on full-width banners, amber top, black bottom',
    'C': 'A different student swings a kettlebell while a white robot works at a study desk with laptop, textbook and backpack; bright daylight gym; Futura Condensed ExtraBold left-aligned, red top with rule, navy bottom',
}


def build(k, layout):
    ig = layout == 'instagram'
    im, boxes, face = BUILDERS[k](ig)
    for b in boxes:
        lo, hi = (IG_TOP, IG_BOT - 20) if ig else (30, 1890)
        assert b[1] >= lo and b[3] <= hi, (k, layout, b)
        assert b[2] < face[0] - 25 or b[0] > face[2] + 25 or b[3] < face[1] - 25 or b[1] > face[3] + 25, (k, layout, b, face)
    path = OUT / layout / f'{k}-ai-homework-cover.jpg'
    path.parent.mkdir(parents=True, exist_ok=True)
    im = im.convert('RGB')
    im.save(path, quality=93, subsampling=0)
    assert path.stat().st_size < 2_000_000, path
    records.append({'option': k, 'layout': layout, 'design': DESIGNS[k], 'plate': PLATES[k], 'file': str(path),
                    'dimensions': [W, H], 'bytes': path.stat().st_size,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'text_boxes': boxes, 'face_box': face})
    return im


def main():
    finals = {(k, l): build(k, l) for k in 'ABC' for l in ('youtube', 'instagram')}
    sheet = Image.new('RGB', (1140, 1270), (238, 237, 233))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), 'AI Homework | Cover Choices, Round 2', font=font('Arial Bold.ttf', 32), fill=(14, 26, 33))
    d.text((24, 64), 'Top: YouTube Shorts full cover     Bottom: Instagram grid crop', font=font('Arial.ttf', 22), fill=(65, 75, 79))
    for n, k in enumerate('ABC'):
        x = 24 + n * 370
        d.text((x, 108), f'{k}. {LABELS[k]}', font=font('Arial Bold.ttf', 21), fill=(14, 26, 33))
        sheet.paste(finals[k, 'youtube'].resize((340, 604), Image.Resampling.LANCZOS), (x, 144))
        sheet.paste(finals[k, 'instagram'].crop((0, IG_TOP, W, IG_BOT)).resize((340, 453), Image.Resampling.LANCZOS), (x, 762))
    d.text((24, 1230), 'All three are AI images made by Codex. A is a younger version of me; B and C are other people.',
           font=font('Arial.ttf', 21), fill=(50, 62, 66))
    sheet.save(OUT / 'REVIEW-ai-homework-round2-three-covers.jpg', quality=94, subsampling=0)
    (HERE / 'cover-manifest-round2.json').write_text(json.dumps({
        'job': 'DS-31', 'category': 'CONTENT', 'status': 'awaiting-dan-pick', 'round': 2,
        'dan': 'I don\'t like any of these. ... a college student looking ripped, exercising in the gym, while a robot is doing their homework on a laptop ... New top text: "Make time to work out." Bottom text: "Let AI do your homework." Give me three unique, exact designs ... Make one of these a younger version of me, and two of them somebody else.',
        'top_text': TOP, 'bottom_text': BOT, 'film_untouched': True,
        'generation': 'Codex subscription, gpt-6.1-sol high: 3 images + 1 age-down edit on A',
        'designs': DESIGNS, 'outputs': records}, indent=2) + '\n')


if __name__ == '__main__':
    main()
