#!/usr/bin/env python3
"""DS-44 Hormozi Fat Guy, cover round 2 (Dan, 2026-10-23): "New design. Split screen of Hormozi and fat guy in
video. Title: Alex Hormozi's Weight Loss Mental Shift. 3 design variations."

Real frames from the interview source (YouTube 37mqHjJOS50, our cut hormozi_140-220.mkv): Hormozi at 49.5 s,
the caller at 30.0 s (the webcam banner above his head is cropped out). No AI. All type set here.
Each design is laid out inside the visible box: full 1080x1920 for YouTube, the 3:4 grid window (y 240-1680)
for Instagram, with the pictures running on past it.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = Path(__file__).resolve().parent
PROJECT = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
OUT = PROJECT / 'Short-form video content/Hormozi Fat Guy - DS-44/covers/round2'
ASSETS = PROJECT / 'Short-form video content/Hormozi Fat Guy - DS-44/covers/assets'
HORMOZI = ASSETS / 'interview-49.5s-hormozi.png'
CALLER = ASSETS / 'interview-30.0s-caller.png'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE = (255, 253, 246)
YELLOW = (255, 214, 10)
INK = (10, 10, 12)
RED = (206, 26, 30)
NAVY = (10, 24, 48)
# Faces measured on the 1920x1080 source frames: [x0, y0 (top of cap / hair), x1, y1 (chin)].
FACE_H = [920, 50, 1360, 640]
FACE_C = [740, 165, 1190, 600]
BANNER_BOTTOM = 155  # caller's webcam "No card in camera" banner ends here
records = []


def font(name, size, index=0):
    if name == 'Manrope':
        f = ImageFont.truetype(MANROPE, size)
        f.set_variation_by_name('ExtraBold')
        return f
    return ImageFont.truetype(str(SUP / name), size, index=index)


def fit(d, copy, name, size, maxwidth, index=0, stroke=0):
    f = font(name, size, index)
    while d.textbbox((0, 0), copy, font=f, stroke_width=stroke)[2] > maxwidth:
        size -= 2
        f = font(name, size, index)
    return f


def text(im, copy, x, y, name, size, color, maxwidth, align='left', index=0, stroke=0, stroke_fill=INK):
    d = ImageDraw.Draw(im)
    f = fit(d, copy, name, size, maxwidth, index, stroke)
    b = d.textbbox((0, 0), copy, font=f, stroke_width=stroke)
    width = b[2] - b[0]
    if align == 'center':
        x -= width // 2
    d.text((x - b[0], y - b[1]), copy, font=f, fill=color, stroke_width=stroke, stroke_fill=stroke_fill)
    box = [x, y, x + width, y + b[3] - b[1]]
    assert box[0] >= 24 and box[2] <= W - 24, (copy, box)
    return box


def crop_src(src, s, cx_to, top_to, face, size, min_src_y=0):
    """Scale src by s and cut `size`, so the face centre-x lands at cx_to and the face top at top_to.
    Asserts the cut stays inside the picture: no filler anywhere."""
    im = Image.open(src).convert('RGB')
    im = ImageEnhance.Contrast(im).enhance(1.06)
    if min_src_y:  # drop the webcam banner rows entirely
        im = im.crop((0, min_src_y, im.width, im.height))
        face = [face[0], face[1] - min_src_y, face[2], face[3] - min_src_y]
    big = im.resize((round(im.width * s), round(im.height * s)), Image.Resampling.LANCZOS)
    x0 = round((face[0] + face[2]) / 2 * s - cx_to)
    y0 = round(face[1] * s - top_to)
    x0 = min(max(0, x0), big.width - size[0])
    y0 = min(max(0, y0), big.height - size[1])
    assert x0 >= 0 and y0 >= 0 and x0 + size[0] <= big.width and y0 + size[1] <= big.height, (src, s, size, x0, y0)
    out = big.crop((x0, y0, x0 + size[0], y0 + size[1]))
    fx = [round(face[0] * s - x0), round(face[1] * s - y0), round(face[2] * s - x0), round(face[3] * s - y0)]
    return out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2)), fx


def shift(f, dx, dy):
    return [f[0] + dx, f[1] + dy, f[2] + dx, f[3] + dy]


def stacked(Hc):
    """A: Hormozi over the caller, stacked halves; black centre band with yellow rules and Impact type."""
    im = Image.new('RGB', (W, Hc), INK)
    band_h = 290
    band_y = round(Hc * 0.43)
    p1, f1 = crop_src(HORMOZI, band_y / 1080 * 1.02, 560, 40, FACE_H, (W, band_y))
    im.paste(p1, (0, 0))
    hc = Hc - band_y - band_h
    p2, f2 = crop_src(CALLER, max(hc / 925, 1.0) * 1.02, 540, 30, FACE_C, (W, hc), BANNER_BOTTOM)
    im.paste(p2, (0, band_y + band_h))
    d = ImageDraw.Draw(im)
    d.rectangle((0, band_y, W, band_y + band_h), fill=INK)
    d.rectangle((0, band_y, W, band_y + 10), fill=YELLOW)
    d.rectangle((0, band_y + band_h - 10, W, band_y + band_h), fill=YELLOW)
    b1 = text(im, "ALEX HORMOZI'S", 540, band_y + 40, 'Impact.ttf', 110, YELLOW, 1000, 'center')
    b2 = text(im, 'WEIGHT LOSS MENTAL SHIFT', 540, b1[3] + 22, 'Impact.ttf', 100, WHITE, 1010, 'center')
    return im, [b1, b2], [f1, shift(f2, 0, band_y + band_h)]


def diagonal(Hc):
    """B: diagonal split with a red slash, Hormozi upper left, caller lower right; headline low over a dark fade."""
    ya, yb = round(Hc * 0.56), round(Hc * 0.38)   # slash: left edge ya, right edge yb
    p1, f1 = crop_src(HORMOZI, ya / 1080 * 1.0, 400, 50, FACE_H, (W, ya))
    py = round(Hc * 0.36)
    p2, f2 = crop_src(CALLER, (Hc - py) / 925, 760, round(Hc * 0.10), FACE_C, (W, Hc - py), BANNER_BOTTOM)
    im = Image.new('RGB', (W, Hc), INK)
    im.paste(p2, (0, py))
    mask = Image.new('L', (W, Hc), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (W, 0), (W, yb), (0, ya)], fill=255)
    top = Image.new('RGB', (W, Hc), INK)
    top.paste(p1, (0, 0))
    im = Image.composite(top, im, mask)
    d = ImageDraw.Draw(im)
    d.line([(0, ya), (W, yb)], fill=RED, width=22)
    fade = Image.new('L', (W, Hc), 0)
    fd = ImageDraw.Draw(fade)
    f0 = round(Hc * 0.64)
    for y in range(f0, Hc):
        fd.line((0, y, W, y), fill=int(240 * min(1, (y - f0) / (Hc * 0.12))))
    im = Image.composite(Image.new('RGB', (W, Hc), INK), im, fade)
    y = round(Hc * 0.735)
    b1 = text(im, "Alex Hormozi's", 60, y, 'Manrope', 104, WHITE, 960)
    b2 = text(im, 'Weight Loss', 60, b1[3] + 20, 'Manrope', 104, WHITE, 960)
    b3 = text(im, 'Mental Shift', 60, b2[3] + 20, 'Manrope', 104, YELLOW, 960)
    return im, [b1, b2, b3], [f1, shift(f2, 0, py)]


def side_by_side(Hc):
    """C: two portrait panels side by side with a white gutter, framed on navy; name line above, two lines below, Futura."""
    im = Image.new('RGB', (W, Hc), NAVY)
    d = ImageDraw.Draw(im)
    top_h = round(Hc * (0.17 if Hc < 1900 else 0.20))
    ph = round(Hc * 0.50)
    pw = (W - 14) // 2
    b1 = text(im, "Alex Hormozi's", 540, round(top_h * 0.42), 'Futura.ttc', 104, WHITE, 960, 'center', index=2)
    p1, f1 = crop_src(HORMOZI, ph / 1080 * 1.0, pw // 2, 40, FACE_H, (pw, ph))
    p2, f2 = crop_src(CALLER, ph / 925 * 1.0, pw // 2 + 20, 40, FACE_C, (pw, ph), BANNER_BOTTOM)
    im.paste(p1, (0, top_h))
    im.paste(p2, (pw + 14, top_h))
    d.rectangle((pw, top_h, pw + 14, top_h + ph), fill=WHITE)
    d.rectangle((0, top_h + ph, W, top_h + ph + 12), fill=RED)
    y = top_h + ph + 12 + round(Hc * 0.05)
    b2 = text(im, 'Weight Loss', 540, y, 'Futura.ttc', 128, WHITE, 960, 'center', index=2)
    b3 = text(im, 'Mental Shift', 540, b2[3] + 26, 'Futura.ttc', 128, (255, 70, 56), 960, 'center', index=2)
    return im, [b1, b2, b3], [shift(f1, 0, top_h), shift(f2, pw + 14, top_h)]


def place(k, ig):
    """YouTube: the design at full height. Instagram: the design at the 3:4 grid height, extended above and below
    with its own edge colour so the grid crop shows the whole design."""
    if not ig:
        return BUILDERS[k](H)
    im, boxes, faces = BUILDERS[k](1440)
    full = Image.new('RGB', (W, H), im.getpixel((W // 2, 2)))
    full.paste(im.crop((0, 0, W, 1)).resize((W, 240)), (0, 0))
    full.paste(im.crop((0, 1439, W, 1440)).resize((W, 240)), (0, 1680))
    full.paste(im, (0, 240))
    return full, [shift(b, 0, 240) for b in boxes], [shift(f, 0, 240) for f in faces]


BUILDERS = {'A': stacked, 'B': diagonal, 'C': side_by_side}
LABELS = {'A': 'Stacked, Centre Band', 'B': 'Diagonal Split', 'C': 'Side By Side'}
DESIGNS = {
    'A': 'Hormozi on top, caller below, full-width halves; black centre band with yellow rules, yellow ALEX HORMOZI\'S over white WEIGHT LOSS MENTAL SHIFT in Impact',
    'B': 'Diagonal split with a red slash, Hormozi upper left, caller lower right; headline low on a dark fade in Manrope, second line yellow',
    'C': 'Two portrait panels side by side with a white gutter on navy; Futura name line above, Weight Loss / Mental Shift below with a red rule, Mental Shift in red',
}


def build(k, layout):
    ig = layout == 'instagram'
    im, boxes, faces = place(k, ig)
    lo, hi = (240, 1680) if ig else (0, 1920)
    for b in boxes:
        assert b[1] >= lo + 30 and b[3] <= hi - 30, (k, layout, b)
        for f in faces:
            assert b[2] < f[0] - 20 or b[0] > f[2] + 20 or b[3] < f[1] - 20 or b[1] > f[3] + 20, (k, layout, b, f)
    for f in faces:
        assert f[1] >= lo + 10, ('face cut at top', k, layout, f)
    path = OUT / layout / f'{k}-hormozi-mental-shift-cover.jpg'
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, quality=93, subsampling=0)
    assert path.stat().st_size < 2_000_000, path
    records.append({'option': k, 'layout': layout, 'design': DESIGNS[k], 'file': str(path), 'bytes': path.stat().st_size,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'text_boxes': boxes, 'faces': faces})
    return im


def main():
    finals = {(k, l): build(k, l) for k in BUILDERS for l in ('youtube', 'instagram')}
    sheet = Image.new('RGB', (1000, 1150), (238, 237, 233))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), 'Hormozi Fat Guy | Split-Screen Covers', font=font('Manrope', 33), fill=(14, 26, 33))
    d.text((24, 66), 'Top: YouTube Shorts full cover     Bottom: Instagram grid (3:4 crop)', font=font('Arial.ttf', 22), fill=(65, 75, 79))
    for i, k in enumerate(BUILDERS):
        x = 24 + i * 320
        d.text((x, 112), f'{k}. {LABELS[k]}', font=font('Arial Bold.ttf', 20), fill=(14, 26, 33))
        sheet.paste(finals[k, 'youtube'].resize((278, 494), Image.Resampling.LANCZOS), (x, 150))
        sheet.paste(finals[k, 'instagram'].crop((0, 240, W, 1680)).resize((278, 370), Image.Resampling.LANCZOS), (x, 664))
    d.text((24, 1060), 'Real frames from the interview, no AI. Same title on all three.', font=font('Arial.ttf', 22), fill=(50, 62, 66))
    d.text((24, 1096), 'Pick A, B or C.', font=font('Arial Bold.ttf', 22), fill=(50, 62, 66))
    sheet.save(OUT / 'REVIEW-hormozi-split-screen-covers.jpg', quality=94, subsampling=0)
    (HERE / 'cover-manifest-round2.json').write_text(json.dumps({
        'job': 'DS-44', 'round': 2, 'status': 'awaiting-dan-pick', 'headline': "Alex Hormozi's Weight Loss Mental Shift",
        'dan_words': "New design. Split screen of Hormozi and fat guy in video. Title: Alex Hormozi's Weight Loss Mental Shift. 3 design variations",
        'sources': {'hormozi': str(HORMOZI), 'caller': str(CALLER)}, 'generation': 'none (real frames)',
        'designs': DESIGNS, 'outputs': records}, indent=2) + '\n')


if __name__ == '__main__':
    main()
