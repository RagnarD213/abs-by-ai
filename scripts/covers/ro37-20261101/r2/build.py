"""RO-37 round 2 thumbnails: code-set type over the eight pictures. Usage: build.py [A B C D E G1 G2 G3]"""
from pathlib import Path
import json, hashlib, subprocess, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import distance_transform_edt

P = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
O = P / 'social media graphics/youtube/thumbnails/First Time At The Gym'
B = O / '_build-2026-11-02-r2'
OUT = B / 'designs'
OUT.mkdir(exist_ok=True)
W, H = 1280, 720
SUP = Path('/System/Library/Fonts/Supplemental')
PM = Path.home() / '.cache/absbyai/personmask/personmask'
IMPACT, DIN, MANROPE = SUP / 'Impact.ttf', SUP / 'DIN Condensed Bold.ttf', Path.home() / 'Library/Fonts/Manrope.ttf'
FONT = {'T1': IMPACT, 'T2': IMPACT, 'R1': MANROPE, 'R2': IMPACT, 'R3': DIN, 'R4': DIN}


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


def scrim(im, cx, cy, rw, rh, strength):
    """Elliptical dark falloff anchored at (cx, cy); no visible box edge."""
    y, x = np.mgrid[0:H, 0:W]
    dd = np.hypot((x - cx) / rw, (y - cy) / rh)
    o = np.zeros((H, W, 4), dtype=np.uint8)
    o[:, :, :3] = [6, 8, 12]
    o[:, :, 3] = (strength * np.clip(1 - dd, 0, 1) ** 1.2).astype(np.uint8)
    return Image.alpha_composite(im, Image.fromarray(o))


def picture(k):
    src = Image.open(B / 'assets' / f'{k}.png').convert('RGB')
    if k == 'T1':  # slide down so the band clears both heads
        im = Image.new('RGBA', (W, H), '#FFD400')
        im.paste(ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS), (0, 30))
        return im
    if k == 'T2':  # shift left and extend the dark right edge for the type column
        pic = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS)
        im = Image.new('RGB', (W, H))
        edge = pic.crop((W - 40, 0, W, H)).resize((300, H), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(30))
        im.paste(edge, (W - 300, 0))
        im.paste(pic.crop((260, 0, W, H)), (0, 0))
        im = im.convert('RGBA')
        return fade(im, 'right', 200, a=.42, b=.22)
    im = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    if k == 'R1':
        o = np.zeros((H, W, 4), dtype=np.uint8); o[:, :, :3] = [5, 10, 24]
        o[:, :, 3] = (235 * np.clip((300 - np.arange(H)) / 300, 0, 1))[:, None].astype(np.uint8)
        return Image.alpha_composite(im, Image.fromarray(o))
    if k == 'R2':
        return scrim(scrim(im, 0, 0, 640, 420, 215), W, 0, 640, 420, 215)
    if k == 'R3':
        return scrim(im, 0, 0, 900, 520, 225)
    if k == 'R4':
        return scrim(im, 0, H, 760, 560, 225)
    raise SystemExit(k)


L1, L2, L3, TOP = 'First Time', 'At The Gym?', 'Do This Instead', 'First Time At The Gym?'


def strip(im, mask, k, text, x, y, size, maxw, bg, fg):
    d = ImageDraw.Draw(im)
    r = put(Image.new('RGBA', (W, H)), Image.new('L', (W, H)), k, text, (x + 18, y + 12), size, maxw - 36, fg)
    x1, y1 = r['rect'][2] + 18, r['rect'][3] + 12
    d.rectangle((x, y, x1, y1), fill=bg)
    ImageDraw.Draw(mask).rectangle((x, y, x1, y1), fill=255)
    return put(im, mask, k, text, (x + 18, y + 12), size, maxw - 36, fg)


def design(k, im, tm):
    d = ImageDraw.Draw(im)
    if k == 'T1':  # yellow two-line band over the coaching scene
        d.rectangle((0, 0, 1279, 188), fill='#FFD400')
        d.rectangle((0, 188, 1279, 195), fill='#101010')
        return [put(im, tm, k, TOP, (30, 10), 88, 1220, '#101519', center=True),
                put(im, tm, k, L3, (30, 100), 80, 1220, '#C21A12', center=True)]
    if k == 'T2':  # stacked yellow, red, black blocks in the dark column
        return [block(im, tm, k, L1, 150, 128, 832, 1258, '#FFD400', '#0A0A0A'),
                block(im, tm, k, L2, 300, 128, 832, 1258, '#E01B1B', '#FFFFFF'),
                block(im, tm, k, L3, 450, 128, 832, 1258, '#0A0A0A', '#FFD400')]
    if k == 'R1':  # navy top fade, Manrope white and cyan
        return [put(im, tm, k, TOP, (60, 26), 92, 1160, '#FFFFFF', center=True),
                put(im, tm, k, L3, (60, 136), 76, 1160, '#5FD0FF', center=True)]
    if k == 'R2':  # stroked Impact split either side of his head
        return [put(im, tm, k, L1, (24, 24), 100, 450, '#FFFFFF', stroke=5),
                put(im, tm, k, L2, (24, 136), 100, 450, '#FFFFFF', stroke=5),
                put(im, tm, k, 'Do This', (836, 24), 100, 420, '#FFD400', stroke=5),
                put(im, tm, k, 'Instead', (836, 136), 100, 420, '#FFD400', stroke=5)]
    if k == 'R3':  # tall condensed white and gold, top left
        return [put(im, tm, k, TOP, (34, 26), 120, 640, '#FFFFFF'),
                put(im, tm, k, L3, (34, 148), 120, 600, '#E8B84A')]
    if k == 'R4':  # red and white label strips, bottom left
        return [strip(im, tm, k, L1, 16, 420, 84, 352, '#D3171D', '#FFFFFF'),
                strip(im, tm, k, L2, 16, 516, 84, 352, '#D3171D', '#FFFFFF'),
                strip(im, tm, k, L3, 16, 612, 70, 352, '#FFFFFF', '#0A0A0A')]
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
    keys = sys.argv[1:] or ['T1', 'T2', 'R1', 'R2', 'R3', 'R4']
    res = [build(k) for k in keys]
    q = B / 'qc.json'
    old = {r['design']: r for r in json.loads(q.read_text())} if q.exists() else {}
    old.update({r['design']: r for r in res})
    q.write_text(json.dumps(list(old.values()), indent=2) + '\n')
