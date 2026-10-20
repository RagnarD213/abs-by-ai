#!/usr/bin/env python3
"""DS-31 AI Homework cover review: five unique designs, YouTube + Instagram layouts.

Option 1 is the real pool photo (photo-273) as shot; option 2 is Dan's real studio
cutout (studio-blue-100) over a Codex chalkboard plate; options 3-5 are Codex images
(gpt-6.1-sol, high). All type is set here, never generated. The approved film is untouched.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = Path(__file__).resolve().parent
PROJECT = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
OUT = PROJECT / 'Short-form video content/AI Homework - DS-31/covers'
ASSETS = OUT / 'assets'
PHOTOS = PROJECT / 'photos/finalized social media photos'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE = (255, 253, 246)
L1, L2 = 'Let AI Do', 'Your Homework'
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


def plate(i):
    im = Image.open(ASSETS / f'generated-{i}.png').convert('RGB')
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS)
    # 941x1672 -> 1080x1920 is a 1.15x enlargement; a light unsharp restores edge crispness.
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))
    return im.convert('RGBA')


def scrim(im, top, bottom, alpha, reverse=False, color=(5, 13, 20)):
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    for y in range(max(0, top), min(H, bottom)):
        t = (y - top) / max(1, bottom - top)
        d.line((0, y, W, y), fill=int(alpha * (t if reverse else 1 - t)))
    layer = Image.new('RGBA', (W, H), color + (0,))
    layer.putalpha(mask)
    return Image.alpha_composite(im, layer)


def highlighter(im, box, color, pad=(26, 14), angle=-2.5):
    """A tilted marker stroke behind a line of type."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + pad[0] * 2, y1 - y0 + pad[1] * 2
    strip = Image.new('RGBA', (w, h), color + (255,))
    strip = strip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(strip, (x0 - pad[0] - (strip.width - w) // 2, y0 - pad[1] - (strip.height - h) // 2))


def pool(ig):
    """Option 1: the real pool photo as shot; marker-strip headline over the water."""
    src = PHOTOS / 'photo-273_FINAL_PRIMARY.jpg'
    raw = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    scale = H / raw.height
    im = raw.resize((round(raw.width * scale), H), Image.Resampling.LANCZOS)
    left = (im.width - W) // 2
    im = im.crop((left, 0, left + W, H)).convert('RGBA')
    # Measured on the source: hair top 11.4% of height, face 37-61% of width down to 30%.
    face = [round(0.37 * raw.width * scale) - left, round(0.105 * H), round(0.61 * raw.width * scale) - left, round(0.30 * H)]
    y = 1262 if ig else 1430
    d = ImageDraw.Draw(im)
    f1 = fit(d, L1, 'Impact.ttf', 150, 760)
    f2 = fit(d, L2, 'Impact.ttf', 150, 940)
    tmp = Image.new('RGBA', (W, H))
    b1 = text(tmp, L1, 540, y, 'Impact.ttf', f1.size, (0, 0, 0), 760, 'center')
    b2 = text(tmp, L2, 540, y + (b1[3] - b1[1]) + 46, 'Impact.ttf', f2.size, (0, 0, 0), 940, 'center')
    highlighter(im, b1, (255, 222, 40), angle=-2.0)
    highlighter(im, b2, (255, 222, 40), angle=1.5)
    text(im, L1, 540, y, 'Impact.ttf', f1.size, (14, 14, 14), 760, 'center')
    text(im, L2, 540, b2[1], 'Impact.ttf', f2.size, (14, 14, 14), 940, 'center')
    return im, [b1, b2], {'source': str(src), 'treatment': 'real photo as shot, resize/crop only', 'hair_face_box': face}


def cutout(im, filename, x, y, height, end_frac, outline=0):
    source = PHOTOS / '_cutouts' / filename
    raw = Image.open(source).convert('RGBA')
    left, top, right, bottom = raw.getbbox()
    end = top + round((bottom - top) * end_frac)
    subject = raw.crop((left, top, right, end))
    subject = subject.resize((round(subject.width * height / subject.height), height), Image.Resampling.LANCZOS)
    if outline:
        rim = subject.getchannel('A').filter(ImageFilter.MaxFilter(outline * 2 + 1))
        edge = Image.new('RGBA', subject.size, WHITE + (0,))
        edge.putalpha(rim)
        im.alpha_composite(edge, (x, y))
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    shade = Image.new('RGBA', subject.size, (0, 0, 0, 0))
    shade.putalpha(subject.getchannel('A').point(lambda v: int(v * 0.4)))
    shadow.alpha_composite(shade, (x + 14, y + 16))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(subject, (x, y))
    a = subject.getchannel('A')
    head = a.crop((0, 0, subject.width, round(height * 0.2))).getbbox()
    face = [x + head[0], y, x + head[2], y + round(height * 0.2)]
    return im, {'source': str(source), 'treatment': 'real cutout, resize and composite only; no AI redraw',
                'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'crop_to_fraction': end_frac, 'position': [x, y], 'height': height, 'hair_face_box': face}


def chalkboard(ig):
    """Option 2: real studio photo (glasses) on a Codex chalkboard; chalk lettering upper left."""
    im = plate(2)
    im, subject = cutout(im, 'studio-blue-100_CUTOUT.png', 150, 770 if ig else 690, 1260 if ig else 1330, 0.80, outline=7)
    y = 330 if ig else 150
    b1 = text(im, 'Let AI Do', 64, y, 'Chalkduster.ttf', 132, WHITE, 900)
    b2 = text(im, 'Your', 64, b1[3] + 34, 'Chalkduster.ttf', 132, WHITE, 900)
    b3 = text(im, 'Homework', 64, b2[3] + 34, 'Chalkduster.ttf', 132, (255, 214, 92), 900)
    d = ImageDraw.Draw(im)
    # Chalk underline under the yellow word.
    for k in range(3):
        d.line((70, b3[3] + 26 + k * 5, 70 + int((b3[2] - b3[0]) * 0.9), b3[3] + 20 + k * 5), fill=(245, 243, 230, 210), width=5)
    return im, [b1, b2, b3], subject


def ai_dan(ig):
    """Option 3: Codex image of Dan training while the laptop writes; condensed headline on the wall."""
    im = plate(3)
    if ig:
        moved = Image.new('RGBA', (W, H), (14, 16, 20, 255))
        moved.alpha_composite(im, (0, 200))
        im = moved
    off = 200 if ig else 0
    # Measured on the plate: hair top at 27.6% of height, face spans 30-56% of width to 42%.
    face = [round(0.30 * W), round(0.272 * H) + off, round(0.56 * W), round(0.42 * H) + off]
    y = 262 if ig else 84
    b1 = text(im, L1, 540, y, 'DIN Condensed Bold.ttf', 210, WHITE, 980, 'center')
    b2 = text(im, L2, 540, b1[3] + 16, 'DIN Condensed Bold.ttf', 210, (94, 205, 255), 980, 'center')
    return im, [b1, b2], {'generated': True, 'reference': 'photo-273_FINAL_PRIMARY.jpg', 'hair_face_box': face}


def sticker_band(ig):
    """Option 4: Codex robot-hand notebook over dumbbell on orange; type in two white label boxes."""
    im = plate(4)
    d = ImageDraw.Draw(im)
    boxes = []
    y = 712
    for copy, size in ((L1, 138), (L2, 138)):
        f = fit(d, copy, 'Futura.ttc', size, 860, index=4)
        b = d.textbbox((0, 0), copy, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        x = 540 - w // 2
        d.rounded_rectangle((x - 34, y - 26, x + w + 34, y + h + 26), radius=22, fill=(255, 251, 242))
        d.text((x - b[0], y - b[1]), copy, font=f, fill=(20, 20, 22))
        boxes.append([x - 34, y - 26, x + w + 34, y + h + 26])
        y += h + 74
    return im, boxes, None


def hourglass(ig):
    """Option 5: Codex hourglass, laptop and kettlebell; heavy stacked type left with an amber bar."""
    im = plate(5)
    im = scrim(im, 0, 1100, 90, color=(4, 4, 6))
    y = 290 if ig else 190
    b1 = text(im, 'Let AI Do', 60, y, 'Arial Black.ttf', 124, WHITE, 540 if ig else 610)
    b2 = text(im, 'Your', 60, b1[3] + 30, 'Arial Black.ttf', 124, WHITE, 540 if ig else 610)
    b3 = text(im, 'Homework', 60, b2[3] + 30, 'Arial Black.ttf', 124, (255, 166, 52), 540 if ig else 610)
    ImageDraw.Draw(im).rectangle((64, b3[3] + 34, 300, b3[3] + 48), fill=(255, 166, 52))
    return im, [b1, b2, b3], None


BUILDERS = {1: pool, 2: chalkboard, 3: ai_dan, 4: sticker_band, 5: hourglass}
LABELS = {1: 'Real Pool Photo', 2: 'Real Studio Photo', 3: 'AI Dan In The Gym', 4: 'Robot Writes, You Lift', 5: 'Hourglass + Kettlebell'}
DESIGNS = {
    1: 'Real pool photo as shot; black Impact on two tilted yellow highlighter strips over the water, bottom centre',
    2: 'Real studio cutout with glasses and white keyline on a green chalkboard; white and yellow chalk lettering stacked upper left with a chalk underline',
    3: 'AI Dan curling a dumbbell beside a laptop writing his essay; tall white and sky-blue DIN Condensed headline centred across the top wall',
    4: 'Codex choice: robot hand writing in a notebook above a dumbbell on solid orange; Futura ExtraBold in two cream label boxes through the middle',
    5: 'Codex choice: hourglass, glowing laptop and kettlebell in a gym bag, dark amber light; heavy Arial Black stacked left with an amber bar',
}


def build(i, layout):
    ig = layout == 'instagram'
    im, boxes, subject = BUILDERS[i](ig)
    for b in boxes:
        assert b[1] >= (240 if ig else 60), (i, layout, b)
        assert b[3] <= (1650 if ig else 1830), (i, layout, b)
        if subject:
            h = subject['hair_face_box']
            assert b[2] < h[0] - 25 or b[0] > h[2] + 25 or b[3] < h[1] - 25 or b[1] > h[3] + 25, (i, layout, b, h)
    path = OUT / layout / f'{i}-ai-homework-cover.jpg'
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
    sheet = Image.new('RGB', (sw, 1130), (238, 237, 233))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), 'AI Homework | Cover Choices', font=font('Manrope', 33), fill=(14, 26, 33))
    d.text((24, 66), 'Top: YouTube Shorts full cover     Bottom: Instagram grid (4:5 crop)', font=font('Arial.ttf', 22), fill=(65, 75, 79))
    for i in range(1, 6):
        x = 24 + (i - 1) * 306
        d.text((x, 112), f'{i}. {LABELS[i]}', font=font('Arial Bold.ttf', 20), fill=(14, 26, 33))
        sheet.paste(finals[i, 'youtube'].resize((278, 494), Image.Resampling.LANCZOS), (x, 150))
        tile = finals[i, 'instagram'].crop((0, 240, W, 1590)).resize((278, 347), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x, 664))
    d.text((24, 1040), 'Same headline on all five. Options 1 and 2 are real photos; 3, 4 and 5 are AI images made by Codex.',
           font=font('Arial.ttf', 22), fill=(50, 62, 66))
    d.text((24, 1076), 'Pick 1, 2, 3, 4 or 5 (or two for YouTube and Instagram).', font=font('Arial Bold.ttf', 22), fill=(50, 62, 66))
    sheet.save(OUT / 'REVIEW-ai-homework-five-covers.jpg', quality=94, subsampling=0)
    (HERE / 'cover-manifest.json').write_text(json.dumps({
        'job': 'DS-31', 'category': 'CONTENT', 'status': 'awaiting-dan-pick', 'headline': f'{L1} {L2}',
        'film_untouched': True, 'generation': 'Codex subscription, gpt-6.1-sol high, 5 images (option 5 regenerated once: take 1 too close to option 4)',
        'designs': DESIGNS, 'outputs': records}, indent=2) + '\n')


if __name__ == '__main__':
    main()
