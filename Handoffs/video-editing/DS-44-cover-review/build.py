#!/usr/bin/env python3
"""DS-44 Hormozi Fat Guy cover review: five unique designs, YouTube + Instagram layouts.

1 real pool photo (photo-247) as shot; 2 real studio cutout (studio-white-49) over a Codex
podcast-studio plate; 3 Codex AI Dan (stop gesture at a food tower, yellow band); 4 the real
opening frame of the Short (the reaction layout, handoff's suggestion for a Codex slot); 5 Codex's
own concept (red stop line taped high on a jar of food). All type is set here, never generated.
The approved film is untouched. Same headline on all five.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = Path(__file__).resolve().parent
PROJECT = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
OUT = PROJECT / 'Short-form video content/Hormozi Fat Guy - DS-44/covers'
ASSETS = OUT / 'assets'
PHOTOS = PROJECT / 'photos/finalized social media photos'
FRAME = ASSETS / 'r2-frame-0.4s.png'  # R2 master at 0.4 s, before the first caption
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE = (255, 253, 246)
YELLOW = (255, 214, 10)
INK = (12, 12, 14)
L1, L2 = "Why Aren't You", '200 Pounds Heavier?'
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


def text(im, copy, x, y, name, size, color, maxwidth, align='left', index=0, stroke=0, stroke_fill=(7, 14, 18)):
    d = ImageDraw.Draw(im)
    f = fit(d, copy, name, size, maxwidth, index, stroke)
    b = d.textbbox((0, 0), copy, font=f, stroke_width=stroke)
    width = b[2] - b[0]
    if align == 'center':
        x -= width // 2
    elif align == 'right':
        x -= width
    d.text((x - b[0], y - b[1]), copy, font=f, fill=color, stroke_width=stroke, stroke_fill=stroke_fill)
    box = [x, y, x + width, y + b[3] - b[1]]
    assert box[0] >= 24 and box[2] <= W - 24, (copy, box)
    return box


def fill(path):
    im = Image.open(path).convert('RGB')
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))
    return im.convert('RGBA')


def scrim(im, top, bottom, alpha, reverse=False, color=(5, 8, 12)):
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    for y in range(max(0, top), min(H, bottom)):
        t = (y - top) / max(1, bottom - top)
        d.line((0, y, W, y), fill=int(alpha * (t if reverse else 1 - t)))
    layer = Image.new('RGBA', (W, H), color + (0,))
    layer.putalpha(mask)
    return Image.alpha_composite(im, layer)


def pool(ig):
    """1: real pool photo as shot; white line over a huge yellow line, stroked, centred low over the water."""
    src = PHOTOS / 'photo-247_FINAL_PRIMARY.jpg'
    raw = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    scale = max(H / raw.height, W / raw.width)
    im = raw.resize((round(raw.width * scale), round(raw.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - W) // 2
    im = im.crop((left, 0, left + W, H)).convert('RGBA')
    im = scrim(im, 1150, 1920, 150, reverse=True)
    y = 1150 if ig else 1290
    b1 = text(im, L1.upper(), 540, y, 'Impact.ttf', 100, WHITE, 820, 'center', stroke=6)
    b2 = text(im, '200 POUNDS', 540, b1[3] + 24, 'Impact.ttf', 150, YELLOW, 1000, 'center', stroke=8)
    b3 = text(im, 'HEAVIER?', 540, b2[3] + 18, 'Impact.ttf', 150, YELLOW, 1000, 'center', stroke=8)
    return im, [b1, b2, b3], {'source': str(src), 'treatment': 'real photo as shot, resize/crop only',
                              'hair_face_box': FACE.get('pool')}


def cutout(im, filename, x, y, height, end_frac):
    source = PHOTOS / '_cutouts' / filename
    raw = Image.open(source).convert('RGBA')
    left, top, right, bottom = raw.getbbox()
    end = top + round((bottom - top) * end_frac)
    subject = raw.crop((left, top, right, end))
    subject = subject.resize((round(subject.width * height / subject.height), height), Image.Resampling.LANCZOS)
    glow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    rim = Image.new('RGBA', subject.size, (255, 40, 30, 0))
    rim.putalpha(subject.getchannel('A').filter(ImageFilter.MaxFilter(9)).point(lambda v: int(v * 0.55)))
    glow.alpha_composite(rim, (x, y))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(18)))
    im.alpha_composite(subject, (x, y))
    a = subject.getchannel('A')
    head = a.crop((0, 0, subject.width, round(height * 0.22))).getbbox()
    face = [x + head[0], y + head[1], x + head[2], y + round(height * 0.22)]
    return im, {'source': str(source), 'treatment': 'real cutout, resize and composite only; no AI redraw',
                'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'crop_to_fraction': end_frac, 'position': [x, y], 'height': height, 'hair_face_box': face}


def studio(ig):
    """2: real studio cutout in the podcast studio plate; Manrope left stack, second line in a red box."""
    h = 1000 if ig else 1330
    probe, subject = cutout(Image.new('RGBA', (W, H)), 'studio-white-49_CUTOUT.png', 0, 0, h, 0.74)
    hb = subject['hair_face_box']
    dx = 540 - (hb[0] + hb[2]) // 2  # centre his head
    im = fill(ASSETS / 'generated-2.png')
    im, subject = cutout(im, 'studio-white-49_CUTOUT.png', dx, H - h - (240 if ig else 0), h, 0.74)
    y = 320 if ig else 120
    b1 = text(im, L1, 70, y, 'Manrope', 108, WHITE, 940)
    d = ImageDraw.Draw(im)
    f = fit(d, L2, 'Manrope', 104, 900)
    bb = d.textbbox((0, 0), L2, font=f)
    bx, by = 70, b1[3] + 40
    box = [bx - 22, by - 18, bx + bb[2] - bb[0] + 22, by + bb[3] - bb[1] + 26]
    d.rectangle(box, fill=(196, 22, 28))
    d.text((bx - bb[0], by - bb[1]), L2, font=f, fill=WHITE)
    return im, [b1, box], subject


def ai_dan(ig):
    """3: Codex AI Dan stopping a food tower; full-width yellow band at the top, black condensed type."""
    im = fill(ASSETS / 'generated-3.png')
    off = 330 if ig else 80  # push the picture down so the band clears his hair
    moved = Image.new('RGBA', (W, H), im.getpixel((W // 2, 8)))
    moved.alpha_composite(im, (0, off))
    im = moved
    # Measured on the plate: hair top 15.5% of height, face 19-35% of width down to 23%.
    face = [int(0.18 * W), int(0.155 * H) + off, int(0.36 * W), int(0.23 * H) + off]
    top = 240 if ig else 0
    d = ImageDraw.Draw(im)
    band = [0, top, W, top + (280 if ig else 290)]
    d.rectangle(band, fill=YELLOW)
    b1 = text(im, L1.upper(), 540, top + 36, 'DIN Condensed Bold.ttf', 108, INK, 980, 'center')
    b2 = text(im, L2.upper(), 540, b1[3] + 20, 'DIN Condensed Bold.ttf', 108, INK, 1010, 'center')
    return im, [band, b1, b2], {'generated': True, 'reference': 'studio-white-49_FINAL_PRIMARY.jpg + R2 frame 30.6 s', 'hair_face_box': face}


def reaction(ig):
    """4: the Short's real opening frame (clip full screen, Dan small lower left); white speech bubble from the host."""
    im = Image.open(FRAME).convert('RGBA')
    d = ImageDraw.Draw(im)
    y0 = 1040 if ig else 1090
    bubble = [430, y0, 1050, y0 + 330]
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([bubble[0] + 10, bubble[1] + 14, bubble[2] + 10, bubble[3] + 14], 46, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(bubble, 46, fill=WHITE)
    d.polygon([(640, y0 + 4), (720, y0 + 4), (610, y0 - 120)], fill=WHITE)  # tail up to the host
    b1 = text(im, L1, 740, y0 + 48, 'Arial Black.ttf', 74, INK, 560, 'center')
    b2 = text(im, '200 Pounds', 740, b1[3] + 20, 'Arial Black.ttf', 92, (196, 22, 28), 570, 'center')
    b3 = text(im, 'Heavier?', 740, b2[3] + 16, 'Arial Black.ttf', 92, (196, 22, 28), 570, 'center')
    # small Dan (lower left corner of the real frame) measured on the frame: hair top y~1300, face x 70-230 to y~1450
    face = [40, 1290, 260, 1470]
    return im, [bubble], {'source': 'R2 master 0.4 s (real frame, no AI)', 'hair_face_box': face}


def jar(ig):
    """5: Codex's own concept: red stop line taped high on a jar of fast food; white Futura stack top-left, navy field."""
    im = fill(ASSETS / 'generated-5.png')
    if ig:  # push the jar down so the stack clears it inside the grid crop
        moved = Image.new('RGBA', (W, H), im.getpixel((W // 2, 10)))
        moved.alpha_composite(im, (0, 170))
        im = moved
    y = 310 if ig else 130
    b1 = text(im, L1, 70, y, 'Futura.ttc', 104, WHITE, 940, index=2)
    b2 = text(im, '200 Pounds', 70, b1[3] + 30, 'Futura.ttc', 150, WHITE, 940, index=2)
    b3 = text(im, 'Heavier?', 70, b2[3] + 26, 'Futura.ttc', 150, (255, 64, 52), 940, index=2)
    return im, [b1, b2, b3], None


FACE = {}
BUILDERS = {1: pool, 2: studio, 3: ai_dan, 4: reaction, 5: jar}
LABELS = {1: 'Real Pool Photo', 2: 'Real Studio Photo', 3: 'AI Dan Says Stop', 4: 'The Opening Frame', 5: 'Stop Line Set Too High'}
DESIGNS = {
    1: 'Real pool photo as shot; white Impact line over a huge yellow stroked two-line stack, centred low over the water',
    2: 'Real studio cutout with a red rim light in a dark Codex podcast studio; Manrope left stack, second line white on a red box',
    3: 'AI Dan on a bathroom scale holding up a stop hand to a tower of burgers; full-width yellow band on top, black DIN Condensed',
    4: 'Real opening frame of the Short (host full screen, Dan small lower left); white speech bubble from the host, red Arial Black',
    5: "Codex's concept: a red stop line taped near the top of an overfilled jar of fast food on navy; white and red Futura stacked top left",
}


def build(i, layout):
    ig = layout == 'instagram'
    im, boxes, subject = BUILDERS[i](ig)
    for b in boxes:
        assert b[1] >= (240 if ig else 0), (i, layout, b)
        assert b[3] <= (1640 if ig else 1860), (i, layout, b)
        if subject and subject.get('hair_face_box'):
            h = subject['hair_face_box']
            assert b[2] < h[0] - 25 or b[0] > h[2] + 25 or b[3] < h[1] - 25 or b[1] > h[3] + 25, (i, layout, b, h)
    path = OUT / layout / f'{i}-hormozi-fat-guy-cover.jpg'
    path.parent.mkdir(parents=True, exist_ok=True)
    im = im.convert('RGB')
    im.save(path, quality=93, subsampling=0)
    assert path.stat().st_size < 2_000_000, path
    records.append({'option': i, 'layout': layout, 'design': DESIGNS[i], 'file': str(path), 'dimensions': [W, H],
                    'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'text_boxes': boxes, 'subject': subject})
    return im


def main():
    finals = {(i, l): build(i, l) for i in range(1, 6) for l in ('youtube', 'instagram')}
    sw = 1560
    sheet = Image.new('RGB', (sw, 1150), (238, 237, 233))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), 'Hormozi Fat Guy | Cover Choices', font=font('Manrope', 33), fill=(14, 26, 33))
    d.text((24, 66), 'Top: YouTube Shorts full cover     Bottom: Instagram grid (3:4 crop)', font=font('Arial.ttf', 22), fill=(65, 75, 79))
    for i in range(1, 6):
        x = 24 + (i - 1) * 306
        d.text((x, 112), f'{i}. {LABELS[i]}', font=font('Arial Bold.ttf', 20), fill=(14, 26, 33))
        sheet.paste(finals[i, 'youtube'].resize((278, 494), Image.Resampling.LANCZOS), (x, 150))
        tile = finals[i, 'instagram'].crop((0, 240, W, 1680)).resize((278, 370), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x, 664))
    d.text((24, 1060), 'Same headline on all five. 1, 2 and 4 are real (4 is the Short\'s own opening frame); 3 and 5 are AI images made by Codex.',
           font=font('Arial.ttf', 22), fill=(50, 62, 66))
    d.text((24, 1096), 'Works for either version (scripted or off-the-cuff). Pick 1-5.', font=font('Arial Bold.ttf', 22), fill=(50, 62, 66))
    sheet.save(OUT / 'REVIEW-hormozi-fat-guy-five-covers.jpg', quality=94, subsampling=0)
    (HERE / 'cover-manifest.json').write_text(json.dumps({
        'job': 'DS-44', 'category': 'CONTENT', 'status': 'awaiting-dan-pick', 'headline': f'{L1} {L2}',
        'film_untouched': True, 'generation': 'Codex subscription, gpt-6.1-sol high, 3 images (2 plate, 3 AI Dan, 5 Codex concept)',
        'designs': DESIGNS, 'outputs': records}, indent=2) + '\n')


if __name__ == '__main__':
    main()
