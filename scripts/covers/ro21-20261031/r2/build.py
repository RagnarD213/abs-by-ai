"""RO-21 thumbnails, round 2: Dan's title and four figures on six backgrounds. Usage: build.py [R1 .. R6]"""
from pathlib import Path
import json, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import distance_transform_edt
import build as b1
from build import put, chip, sha, W, H, B, PM, IMPACT, DIN, MANROPE, FONT

R = B / 'r2'
OUT = R / 'designs'
OUT.mkdir(exist_ok=True)
FONT.update({'R1': IMPACT, 'R2': IMPACT, 'R3': DIN, 'R4': MANROPE, 'R5': IMPACT, 'R6': IMPACT})
L1, L2 = 'Body Fat Percentage:', 'Which One Are You?'
SHIFT = {'R3': 42, 'R5': 22, 'R6': 84}
LEVELS = [('35%', 183), ('25%', 497), ('15%', 805), ('8%', 1113)]


def picture(k):
    p = R / 'assets' / f'{k}.png'
    if not p.exists():
        p = R / 'google' / f'{k}.png'
    pic = ImageOps.fit(Image.open(p).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    d = SHIFT.get(k, 0)
    if d:  # figures stand high in this plate: slide down, mirror the wall into the gap, the crop only takes thigh
        im = Image.new('RGBA', (W, H))
        im.paste(pic, (0, d))
        im.paste(ImageOps.flip(pic.crop((0, 0, W, d))), (0, 0))
        return im
    return pic


def tags(im, tm, k, bg, fg, y=640):
    return [chip(im, tm, k, t, x, y, bg, fg) for t, x in LEVELS]


def band(im, tm, h, fill, rule=None):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, h), fill=fill)
    if rule:
        d.rectangle((0, h, W - 1, h + 7), fill=rule)
    ImageDraw.Draw(tm).rectangle((0, 0, W - 1, h + 7), fill=255)


def design(k, im, tm):
    if k == 'R1':  # X7's look: yellow band, dark and red Impact, black tags
        band(im, tm, 194, '#FFD400', '#101010')
        return [put(im, tm, k, L1, (30, 10), 92, 1220, '#101519', center=True),
                put(im, tm, k, L2, (30, 100), 96, 1220, '#C21A12', center=True)] + tags(im, tm, k, '#0A0A0A', '#FFD400')
    if k == 'R2':  # black band, white and yellow Impact, yellow tags
        band(im, tm, 194, '#050709', '#FFD400')
        return [put(im, tm, k, L1, (30, 10), 92, 1220, '#FFFFFF', center=True),
                put(im, tm, k, L2, (30, 100), 96, 1220, '#FFD400', center=True)] + tags(im, tm, k, '#FFD400', '#0A0A0A')
    if k == 'R3':  # red band, tall white condensed, white tags
        band(im, tm, 199, '#D3171D')
        return [put(im, tm, k, L1, (30, 8), 96, 1220, '#FFFFFF', center=True),
                put(im, tm, k, L2, (30, 102), 96, 1220, '#FFE26A', center=True)] + tags(im, tm, k, '#FFFFFF', '#B3131A')
    if k == 'R4':  # white band, black Manrope with red second line
        band(im, tm, 195, '#FFFFFF', '#E01B1B')
        return [put(im, tm, k, L1, (30, 12), 86, 1220, '#0A0A0A', center=True),
                put(im, tm, k, L2, (30, 102), 86, 1220, '#D3171D', center=True)] + tags(im, tm, k, '#D3171D', '#FFFFFF')
    if k == 'R5':  # no band: white Impact with a black edge on the sky
        return [put(im, tm, k, L1, (30, 14), 92, 1220, '#FFFFFF', stroke=5, center=True),
                put(im, tm, k, L2, (30, 110), 92, 1220, '#FFD400', stroke=5, center=True)] + tags(im, tm, k, '#0A0A0A', '#FFFFFF')
    if k == 'R6':  # no band: white and cyan Impact on the dark wall
        return [put(im, tm, k, L1, (30, 18), 92, 1220, '#FFFFFF', center=True),
                put(im, tm, k, L2, (30, 112), 92, 1220, '#6FE3F0', center=True)] + tags(im, tm, k, '#6FE3F0', '#06121A')
    raise SystemExit(k)


def build(k):
    im = picture(k)
    pp = R / f'picture-{k}.jpg'
    im.convert('RGB').save(pp, quality=98)
    mp = R / f'person-{k}.png'
    subprocess.run([str(PM), str(pp), str(mp)], check=True, capture_output=True)
    person = np.array(Image.open(mp).convert('L').resize((W, H))) > 100
    tm = Image.new('L', (W, H))
    boxes = design(k, im, tm)
    out = OUT / f'RO21-{k}.jpg'
    im.convert('RGB').save(out, quality=95, subsampling=0)
    head = np.array(tm) > 0
    head[560:] = False  # the level tags sit on the shorts on purpose; the headline is what must clear the heads
    overlap = int((head & person).sum())
    clear = float(distance_transform_edt(~person)[head].min())
    r = dict(design=k, file=out.name, sha256=sha(out), bytes=out.stat().st_size, size=[W, H],
             headline_person_overlap_pixels=overlap, headline_person_clearance_px=round(clear, 2), text_boxes=boxes)
    print(json.dumps({x: r[x] for x in ('design', 'bytes', 'headline_person_overlap_pixels', 'headline_person_clearance_px')}), flush=True)
    return r


if __name__ == '__main__':
    keys = sys.argv[1:] or ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    res = [build(k) for k in keys]
    q = R / 'qc.json'
    old = {r['design']: r for r in json.loads(q.read_text())} if q.exists() else {}
    old.update({r['design']: r for r in res})
    q.write_text(json.dumps(list(old.values()), indent=2) + '\n')
