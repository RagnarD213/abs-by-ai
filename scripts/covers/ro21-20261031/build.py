"""RO-21 thumbnails: code-set type over the eight pictures. Usage: build.py [A B C D E G1 G2 G3]"""
from pathlib import Path
import json, hashlib, subprocess, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import distance_transform_edt

P = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
O = P / 'social media graphics/youtube/thumbnails/What Every Body Fat Percentage Looks Like'
B = O / '_build-2026-10-31'
OUT = B / 'designs'
OUT.mkdir(exist_ok=True)
W, H = 1280, 720
SUP = Path('/System/Library/Fonts/Supplemental')
PM = Path.home() / '.cache/absbyai/personmask/personmask'
REAL = P / 'photos/finalized social media photos/_cutouts/studio-white-59_CUTOUT.png'
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
    return put(im, mask, k, text, (x0 + 22, y + 14), h, x1 - x0 - 44, fg, center=True)


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
        if k == 'G3':  # slide the picture down under the band; the crop only takes thigh
            im = Image.new('RGBA', (W, H), '#D3171D')
            im.paste(pic, (0, 85))
            return im
        return pic
    if k != 'C':
        return ImageOps.fit(Image.open(B / 'assets' / f'ai-{k}.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    im = ImageOps.fit(Image.open(B / 'assets/ai-C.png').convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    raw = Image.open(REAL).convert('RGBA')
    bb = raw.getchannel('A').getbbox()
    crop = [bb[0], bb[1], bb[2], round(bb[1] + (bb[3] - bb[1]) * .655)]  # waist crop: the shorts stay out of the picture
    src = raw.crop(crop)
    scale = 700 / src.height
    src = src.resize((round(src.width * scale), 700), Image.Resampling.LANCZOS)
    x, y = -24, 20
    im.alpha_composite(src, (x, y))
    (B / 'real-photo-provenance.json').write_text(json.dumps(dict(
        source=str(REAL), sha256=sha(REAL), crop=crop, scale=scale, position=[x, y],
        person_pixels='Original cutout transformed by crop/resize/composite only; no AI redraw or colour/body alteration'), indent=2) + '\n')
    return im


HEAD = 'Body Fat:', 'Which One Are You?'


def design(k, im, tm):
    d = ImageDraw.Draw(im)
    if k == 'A':  # yellow two-line band over three levels
        d.rectangle((0, 0, 1279, 199), fill='#FFD400')
        d.rectangle((0, 199, 1279, 206), fill='#101010')
        return [put(im, tm, k, HEAD[0], (30, 10), 92, 1220, '#101519', center=True),
                put(im, tm, k, HEAD[1], (30, 100), 100, 1220, '#C21A12', center=True),
                chip(im, tm, k, '35%', 200, 636), chip(im, tm, k, '20%', 640, 636), chip(im, tm, k, '8%', 1085, 636)]
    if k == 'B':  # stacked yellow, red, black blocks
        return [block(im, tm, k, 'Body Fat:', 96, 150, 762, 1244, '#FFD400', '#0A0A0A'),
                block(im, tm, k, 'Which One', 286, 150, 762, 1244, '#E01B1B', '#FFFFFF'),
                block(im, tm, k, 'Are You?', 476, 150, 762, 1244, '#0A0A0A', '#FFD400')]
    if k == 'C':  # real photo, Manrope stack, level row
        return [put(im, tm, k, 'Body Fat:', (716, 120), 100, 530, '#FFFFFF'),
                put(im, tm, k, 'Which One', (716, 240), 100, 530, '#FFFFFF'),
                put(im, tm, k, 'Are You?', (716, 360), 106, 530, '#5FD0FF'),
                chip(im, tm, k, '35%', 786, 512, '#FFFFFF', '#0B1B2E', 52), chip(im, tm, k, '20%', 950, 512, '#FFFFFF', '#0B1B2E', 52),
                chip(im, tm, k, '8%', 1096, 512, '#5FD0FF', '#0B1B2E', 52)]
    if k == 'D':  # white and cyan Impact on the dark side
        return [put(im, tm, k, 'Body Fat:', (38, 150), 124, 500, '#FFFFFF'),
                put(im, tm, k, 'Which One', (38, 296), 118, 500, '#6FE3F0'),
                put(im, tm, k, 'Are You?', (38, 436), 118, 500, '#FFFFFF')]
    if k == 'E':  # gold and dark condensed on the white wall
        return [put(im, tm, k, 'Body Fat:', (760, 150), 170, 480, '#101519'),
                put(im, tm, k, 'Which One', (760, 310), 170, 480, '#B8860B'),
                put(im, tm, k, 'Are You?', (760, 468), 170, 480, '#101519')]
    if k == 'G1':  # white stroked Impact, top left
        return [put(im, tm, k, 'Body Fat:', (34, 24), 96, 440, '#FFFFFF', stroke=5),
                put(im, tm, k, 'Which One', (34, 126), 96, 440, '#FFD400', stroke=5),
                put(im, tm, k, 'Are You?', (34, 228), 96, 440, '#FFD400', stroke=5)]
    if k == 'G2':  # white bar, black Manrope with one red word
        d.rectangle((0, 0, 1279, 176), fill='#FFFFFF')
        d.rectangle((0, 176, 1279, 184), fill='#E01B1B')
        ImageDraw.Draw(tm).rectangle((0, 0, 1279, 184), fill=255)
        return [put(im, tm, k, 'Body Fat: Which One Are You?', (28, 46), 90, 1224, '#0A0A0A', center=True)]
    if k == 'G3':  # red band, white condensed
        d.rectangle((0, 0, 1279, 190), fill='#D3171D')
        ImageDraw.Draw(tm).rectangle((0, 0, 1279, 190), fill=255)
        return [put(im, tm, k, 'Body Fat: Which One Are You?', (30, 28), 150, 1220, '#FFFFFF', center=True)]
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
    out = OUT / f'RO21-{k}.jpg'
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
