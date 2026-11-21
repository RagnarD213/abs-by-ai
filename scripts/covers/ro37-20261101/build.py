"""RO-37 thumbnails: code-set type over the eight pictures. Usage: build.py [A B C D E G1 G2 G3]"""
from pathlib import Path
import json, hashlib, subprocess, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import distance_transform_edt

P = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
O = P / 'social media graphics/youtube/thumbnails/First Time At The Gym'
B = O / '_build-2026-11-01'
OUT = B / 'designs'
OUT.mkdir(exist_ok=True)
W, H = 1280, 720
SUP = Path('/System/Library/Fonts/Supplemental')
PM = Path.home() / '.cache/absbyai/personmask/personmask'
REAL = P / 'photos/finalized social media photos/_cutouts/studio-blue-14_CUTOUT.png'
IMPACT, DIN, MANROPE = SUP / 'Impact.ttf', SUP / 'DIN Condensed Bold.ttf', Path.home() / 'Library/Fonts/Manrope.ttf'
FONT = {'A': IMPACT, 'B': IMPACT, 'C': MANROPE, 'D': IMPACT, 'E': DIN, 'G1': IMPACT, 'G2': MANROPE, 'G3': DIN}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def font(k, n):
    f = ImageFont.truetype(str(FONT[k]), n)
    if FONT[k] == MANROPE:
        f.set_variation_by_name('ExtraBold')
    return f


def put(im, mask, k, text, xy, size, maxw, color, stroke=0, center=False):
    x, y = xy
    while True:
        f = font(k, size)
        b = f.getbbox(text)
        ww = b[2] - b[0]
        if ww + 2 * stroke <= maxw:
            break
        size -= 1
    if center:
        x += round((maxw - ww) / 2)
    pos = (x - b[0], y - b[1])
    ImageDraw.Draw(im).text(pos, text, font=f, fill=color, stroke_width=stroke, stroke_fill='#050505')
    ImageDraw.Draw(mask).text(pos, text, font=f, fill=255, stroke_width=stroke + 3)
    return dict(text=text, font_size=size, rect=[x - stroke, y - stroke, x + ww + stroke, y + b[3] - b[1] + stroke])


def block(im, mask, k, text, y, h, x0, x1, bg, fg):
    d = ImageDraw.Draw(im)
    d.rectangle((x0 + 9, y + 9, x1 + 9, y + h + 9), fill='#000000')
    d.rectangle((x0, y, x1, y + h), fill=bg)
    ImageDraw.Draw(mask).rectangle((x0, y, x1, y + h), fill=255)
    r = put(Image.new('RGBA', (W, H)), Image.new('L', (W, H)), k, text, (x0 + 22, y), h, x1 - x0 - 44, fg, center=True)
    return put(im, mask, k, text, (x0 + 22, y + (h - (r['rect'][3] - r['rect'][1])) // 2), h, x1 - x0 - 44, fg, center=True)


def chip(im, mask, k, text, cx, y, bg='#0A0A0A', fg='#FFD400', size=58):
    f = font(k, size)
    b = f.getbbox(text)
    ww, hh = b[2] - b[0], b[3] - b[1]
    x0, x1 = cx - ww // 2 - 18, cx + ww // 2 + 18
    d = ImageDraw.Draw(im)
    d.rectangle((x0, y, x1, y + hh + 24), fill=bg)
    d.text((cx - ww // 2 - b[0], y + 12 - b[1]), text, font=f, fill=fg)
    ImageDraw.Draw(mask).rectangle((x0, y, x1, y + hh + 24), fill=255)
    return dict(text=text, rect=[x0, y, x1, y + hh + 24])


def fade(im, side, strength, a=.52, b=.3):
    o = np.zeros((H, W, 4), dtype=np.uint8)
    o[:, :, :3] = [6, 6, 8]
    x = np.arange(W) / W
    v = np.clip((a - x) / b, 0, 1) if side == 'left' else np.clip((x - (1 - a)) / b, 0, 1)
    o[:, :, 3] = (strength * v)[None, :].astype(np.uint8)
    return Image.alpha_composite(im, Image.fromarray(o))


def picture(k):
    if k[0] == 'G':
        pic = ImageOps.fit(Image.open(B / 'google' / f'{k}.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
        if k == 'G1':  # slide the picture down under the two-line bar; the crop only takes thigh
            im = Image.new('RGBA', (W, H), '#FFFFFF')
            im.paste(pic, (0, 84))
            return im
        return pic
    if k == 'A':  # slide the picture down so the band clears both heads of hair; the crop only takes thigh
        im = Image.new('RGBA', (W, H), '#FFD400')
        im.paste(ImageOps.fit(Image.open(B / 'assets/ai-A.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS), (0, 34))
        return im
    if k != 'C':
        return ImageOps.fit(Image.open(B / 'assets' / f'ai-{k}.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    im = ImageOps.fit(Image.open(B / 'assets/background-C.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    im = fade(im, 'right', 215, a=.62, b=.34)
    raw = Image.open(REAL).convert('RGBA')
    bb = raw.getchannel('A').getbbox()
    crop = [bb[0], bb[1], bb[2], round(bb[1] + (bb[3] - bb[1]) * .875)]  # waist crop: the shorts stay out of the picture
    src = raw.crop(crop)
    scale = 700 / src.height
    src = src.resize((round(src.width * scale), 700), Image.Resampling.LANCZOS)
    x, y = 8, 20
    im.alpha_composite(src, (x, y))
    (B / 'real-photo-provenance.json').write_text(json.dumps(dict(
        source=str(REAL), sha256=sha(REAL), crop=crop, scale=scale, position=[x, y],
        person_pixels='Original cutout transformed by crop/resize/composite only; no AI redraw or colour/body alteration'), indent=2) + '\n')
    return im


L1, L2, L3, TOP = 'First Time', 'At The Gym?', 'Do This Instead', 'First Time At The Gym?'


def design(k, im, tm):
    d = ImageDraw.Draw(im)
    if k == 'A':  # yellow two-line band over the two of him
        d.rectangle((0, 0, 1279, 199), fill='#FFD400')
        d.rectangle((0, 199, 1279, 206), fill='#101010')
        return [put(im, tm, k, TOP, (30, 10), 92, 1220, '#101519', center=True),
                put(im, tm, k, L3, (30, 100), 100, 1220, '#C21A12', center=True)]
    if k == 'B':  # stacked yellow, red, black blocks
        return [block(im, tm, k, L1, 110, 140, 700, 1244, '#FFD400', '#0A0A0A'),
                block(im, tm, k, L2, 280, 140, 700, 1244, '#E01B1B', '#FFFFFF'),
                block(im, tm, k, L3, 450, 140, 700, 1244, '#0A0A0A', '#FFD400')]
    if k == 'C':  # real photo, Manrope stack
        return [put(im, tm, k, L1, (700, 150), 96, 540, '#FFFFFF'),
                put(im, tm, k, L2, (700, 266), 96, 540, '#FFFFFF'),
                put(im, tm, k, L3, (700, 382), 74, 540, '#5FD0FF')]
    if k == 'D':  # white and cyan Impact on the dark side
        return [put(im, tm, k, L1, (38, 130), 124, 500, '#FFFFFF'),
                put(im, tm, k, L2, (38, 276), 118, 500, '#FFFFFF'),
                put(im, tm, k, L3, (38, 416), 100, 500, '#6FE3F0')]
    if k == 'E':  # gold and dark condensed on the white wall
        return [put(im, tm, k, L1, (640, 150), 170, 600, '#101519'),
                put(im, tm, k, L2, (640, 310), 170, 600, '#101519'),
                put(im, tm, k, L3, (640, 468), 120, 600, '#B8860B')]
    if k == 'G1':  # white bar, black Manrope with the red rule
        d.rectangle((0, 0, 1279, 176), fill='#FFFFFF')
        d.rectangle((0, 176, 1279, 184), fill='#E01B1B')
        ImageDraw.Draw(tm).rectangle((0, 0, 1279, 184), fill=255)
        return [put(im, tm, k, TOP, (28, 14), 84, 1224, '#0A0A0A', center=True),
                put(im, tm, k, L3, (28, 98), 72, 1224, '#E01B1B', center=True)]
    if k == 'G2':  # white stroked Impact, top left
        return [put(im, tm, k, L1, (34, 24), 96, 470, '#FFFFFF', stroke=5),
                put(im, tm, k, L2, (34, 126), 96, 470, '#FFFFFF', stroke=5),
                put(im, tm, k, L3, (34, 228), 84, 470, '#FFD400', stroke=5)]
    if k == 'G3':  # red band, white condensed
        d.rectangle((0, 0, 1279, 136), fill='#D3171D')
        ImageDraw.Draw(tm).rectangle((0, 0, 1279, 136), fill=255)
        return [put(im, tm, k, TOP + ' ' + L3, (30, 24), 120, 1220, '#FFFFFF', center=True)]
    raise SystemExit(k)


def build(k):
    im = picture(k)
    pp = B / f'picture-{k}.jpg'
    im.convert('RGB').save(pp, quality=98)
    mp = B / f'person-{k}.png'
    subprocess.run([str(PM), str(pp), str(mp)], check=True, capture_output=True)
    person = np.array(Image.open(mp).convert('L').resize((W, H))) > 100
    tm = Image.new('L', (W, H))
    boxes = design(k, im, tm)
    out = OUT / f'RO37-{k}.jpg'
    im.convert('RGB').save(out, quality=95, subsampling=0)
    tm.save(B / f'text-{k}.png')
    text = np.array(tm) > 0
    overlap = int((text & person).sum())
    clear = float(distance_transform_edt(~person)[text].min()) if person.any() else 999
    r = dict(design=k, file=out.name, sha256=sha(out), bytes=out.stat().st_size, size=[W, H],
             person_text_overlap_pixels=overlap, minimum_person_text_clearance_px=round(clear, 2), text_boxes=boxes)
    print(json.dumps({x: r[x] for x in ('design', 'bytes', 'person_text_overlap_pixels', 'minimum_person_text_clearance_px')}), flush=True)
    return r


if __name__ == '__main__':
    keys = sys.argv[1:] or ['A', 'B', 'C', 'D', 'E', 'G1', 'G2', 'G3']
    res = [build(k) for k in keys]
    q = B / 'qc.json'
    old = {r['design']: r for r in json.loads(q.read_text())} if q.exists() else {}
    old.update({r['design']: r for r in res})
    q.write_text(json.dumps(list(old.values()), indent=2) + '\n')
