#!/usr/bin/env python3
"""Invest In Your Health Shorts (SL-20) covers, 2026-11-05.

Eight choices per Short: five Codex (A-E) and three Google (F-H, blind test; Dan only ever sees X labels).
A/B/D/E and F-H are AI images of Dan made from a real identity reference. C is a REAL studio photo:
Codex makes the background only, the original cutout pixels are composited in code with a white keyline.
Same approved title on every design per Short; only layout, type, colour and picture change.
Instagram keeps all type inside the 3:4 profile crop (y 240-1680); YouTube uses the whole 1080x1920.

    python3 scripts/covers/sl20-20261105/build.py [s1 s2 s3]
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Short-form video content/covers/review/sl20-invest-20261105'
SRC = OUT / 'sources'
CUT = ROOT / 'photos/finalized social media photos/_cutouts'
PM = Path.home() / '.cache/absbyai/personmask/personmask'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')

SHORTS = {
    's1': dict(slug='invest-short1_dont-bother-dating-unless-youre-ripped',
               title="Don't Bother Dating Unless You're Ripped",
               two=["Don't Bother Dating", "Unless You're Ripped"],
               three=["Don't Bother", "Dating Unless", "You're Ripped"],
               cutout='studio-blue-171', waist=0.68),
    's2': dict(slug='invest-short2_why-being-fat-destroys-your-relationship',
               title='Why Being Fat Destroys Your Relationship',
               two=['Why Being Fat Destroys', 'Your Relationship'],
               three=['Why Being Fat', 'Destroys Your', 'Relationship'],
               cutout='studio-white-32', waist=0.68),
    's3': dict(slug='invest-short3_you-cant-afford-to-not-work-out',
               title="You Can't Afford To NOT Work Out",
               two=["You Can't Afford", 'To NOT Work Out'],
               three=["You Can't", 'Afford To NOT', 'Work Out'],
               cutout='studio-blue-34', waist=0.665),
}

# Letter -> design. A-E Codex, F-H Google (internal only).
#  Y  yellow band, black/red DIN Condensed (Dan's most-picked look)
#  BT bottom title, three big balanced lines, no eyebrow (Dan 2026-10-27)
#  N  real photo: navy rounded panel, white/lime Futura, white keyline cutout
#  F  dark top fade, white/cyan Impact
#  S  editorial: gold rules, white/gold Baskerville, thin gold frame
#  R  red slab: white Avenir Next Condensed on a slanted red block, bottom-left
#  T  split-screen: centred white Impact on a black bar across the seam
#  P  top-left stack: three left-aligned Impact lines, the middle one black on a yellow highlight
STYLE = {
    's1': {'A': 'Y', 'B': 'T', 'C': 'N', 'D': 'F', 'E': 'S', 'F': 'Y', 'G': 'N', 'H': 'P'},
    's2': {'A': 'Y', 'B': 'P', 'C': 'N', 'D': 'F', 'E': 'S', 'F': 'T', 'G': 'R', 'H': 'Y'},
    's3': {'A': 'Y', 'B': 'P', 'C': 'N', 'D': 'F', 'E': 'S', 'F': 'N', 'G': 'Y', 'H': 'T'},
}
LETTERS = 'ABCDEFGH'

# Round 2 (Dan, 2026-11-06): "I don't like any of these. I want four new designs with four new, unique, AI-generated
# images ... me, ripped, holding hands with a hot girl ... a fat version of me sits on the side, looking miserable,
# jealous, and pathetic." Four Codex plates r2A-r2D, each its own design; built under the Short 1 and Short 2 titles.
SHORTS['s1r2'] = dict(SHORTS['s1'])
SHORTS['s2r2'] = dict(SHORTS['s2'])
R2_STYLE = {'A': 'Y', 'B': 'F', 'C': 'P', 'D': 'T'}
STYLE['s1r2'] = dict(R2_STYLE)
STYLE['s2r2'] = dict(R2_STYLE)
GOOGLE = {'F': 'G-g{n}F', 'G': 'G-g{n}G', 'H': 'G-g{n}H'}

# Per-plate source crop (x0, y0, x1, y1) on the generated plate, and a downward picture shift
# per platform, set after looking at every plate (keeps type off faces and hair).
TUNE = {
    ('s2', 'C'): {'flip': True},   # table and empty chair on the left, clear of the cutout
}
FONTS = {
    'Y': (SUP/'DIN Condensed Bold.ttf', 0), 'BT': (SUP/'Impact.ttf', 0), 'N': (SUP/'Futura.ttc', 4),
    'F': (SUP/'Impact.ttf', 0), 'S': (SUP/'Baskerville.ttc', 3),
    'R': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8), 'T': (SUP/'Impact.ttf', 0),
    'P': (SUP/'Impact.ttf', 0),
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def font(style, size):
    p, i = FONTS[style]
    return ImageFont.truetype(str(p), size, index=i)


def fit(style, text, size, width, stroke=0):
    for n in range(size, 39, -1):
        f = font(style, n)
        b = f.getbbox(text, stroke_width=stroke)
        if b[2] - b[0] <= width:
            return f
    raise ValueError(text)


def person_mask(im):
    with tempfile.TemporaryDirectory(prefix='sl20-cover-') as t:
        i, m = Path(t)/'p.png', Path(t)/'m.png'
        im.convert('RGB').save(i)
        r = subprocess.run([str(PM), str(i), str(m)], capture_output=True, text=True, check=True)
        mask = np.array(Image.open(m).convert('L')) > 127
        try:
            faces = json.loads(r.stdout).get('faces', [])
        except ValueError:
            faces = []
        person_mask.faces = faces
        return mask


# Google identity retries (one each): g3G retry kept; g2F failed twice (neither man was Dan), so dropped.
PLATE_OVERRIDE = {('s3', 'G'): 'G-g3G-r2'}
DROPPED = {('s2', 'F')}


def plate_path(key, letter):
    if key.endswith('r2'):
        return SRC / f'r2{letter}.png'
    if (key, letter) in PLATE_OVERRIDE:
        return SRC / f'{PLATE_OVERRIDE[(key, letter)]}.png'
    n = key[1]
    name = GOOGLE[letter].format(n=n) if letter in GOOGLE else f'{key}{letter}'
    return SRC / f'{name}.png'


def picture(key, letter, platform):
    spec, style = SHORTS[key], STYLE[key][letter]
    plate = plate_path(key, letter)
    src = Image.open(plate).convert('RGB')
    t = TUNE.get((key, letter), {})
    if 'crop' in t:
        src = src.crop(t['crop'])
    if t.get('flip'):
        src = ImageOps.mirror(src)
    im = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS, centering=t.get('centering', (0.5, 0.5))).convert('RGBA')
    info = {'plate': str(plate.relative_to(ROOT)), 'plate_sha256': sha(plate)}
    if letter == 'C' and not key.endswith('r2'):
        p = CUT / f"{spec['cutout']}_CUTOUT.png"
        raw = Image.open(p).convert('RGBA')
        b = raw.getchannel('A').getbbox()
        b = (b[0], b[1], b[2], b[1] + round((b[3]-b[1]) * spec['waist']))
        sub = raw.crop(b)
        top = t.get('top_' + platform, 760 if platform == 'instagram' else 620)
        scale = min((H - top + 40) / sub.height, 860 / sub.width)
        sub = sub.resize((round(sub.width*scale), round(sub.height*scale)), Image.Resampling.LANCZOS)
        pad = 20
        layer = Image.new('RGBA', (sub.width + 2*pad, sub.height + 2*pad))
        layer.alpha_composite(sub, (pad, pad))
        x = W - sub.width - pad - t.get('right', 10)
        y = H + 40 - sub.height - pad
        line = Image.new('RGBA', layer.size, 'white')
        line.putalpha(layer.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line, (x, y)); im.alpha_composite(layer, (x, y))
        info.update(subject_top_actual=y + pad, real_photo=True, source=str(p.relative_to(ROOT)), source_sha256=sha(p),
                    source_person_pixels_preserved=True, source_crop=list(b), scale=round(scale, 4), subject_top=top)
        return im, info
    shift = t.get('shift_' + platform, auto_shift(key, letter, platform, im))
    if shift:
        color = tuple(int(v) for v in np.array(im.convert('RGB'))[:30].reshape(-1, 3).mean(axis=0))
        moved = Image.new('RGBA', (W, H), color + (255,))
        moved.alpha_composite(im.crop((0, 0, W, H - shift)), (0, shift))
        f = np.zeros((H, W, 4), np.uint8); f[:, :, :3] = color
        L = t.get('feather', 140)
        for yy in range(shift, min(H, shift + L)):
            f[yy, :, 3] = int(255 * (1 - (yy - shift) / L))
        moved.alpha_composite(Image.fromarray(f))
        im = moved
    info['picture_shift'] = shift
    return im, info


def auto_shift(key, letter, platform, im):
    """Move the picture down until every person's top sits clear of the top type panel."""
    if STYLE[key][letter] in ('BT', 'R'):
        return 0
    dummy = Image.new('RGBA', (W, H)); m = Image.new('L', (W, H))
    title(dummy, m, key, letter, platform)
    rows = np.where(np.array(m).max(axis=1) > 0)[0]
    bottom = int(rows.max())
    pm = person_mask(im)
    prow = np.where(pm.sum(axis=1) > 6)[0]
    top = int(prow.min()) if len(prow) else H
    return min(520, max(0, bottom + 55 - top))


def gradient(im, rgb, rows):
    """rows: callable y -> alpha 0..255"""
    a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = rgb
    for y in range(H):
        a[y, :, 3] = max(0, min(255, int(rows(y))))
    im.alpha_composite(Image.fromarray(a))


def title(im, mask, key, letter, platform):
    spec, style = SHORTS[key], STYLE[key][letter]
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    ig = platform == 'instagram'
    y0 = 262 if ig else 96
    bounds = []

    def put(xy, text, f, fill, stroke=0, sfill=None, anchor='mt'):
        draw.text(xy, text, font=f, anchor=anchor, fill=fill, stroke_width=stroke, stroke_fill=sfill)
        md.text(xy, text, font=f, anchor=anchor, fill=255, stroke_width=stroke)
        bb = f.getbbox(text, anchor=anchor, stroke_width=stroke)
        bounds.append([xy[0]+bb[0], xy[1]+bb[1], xy[0]+bb[2], xy[1]+bb[3]])
        return bb[3] - bb[1]

    lines = spec['two']
    if style == 'Y':
        f = [fit('Y', l, 175, 960) for l in lines]
        hs = [ff.getbbox(l, anchor='mt')[3] for ff, l in zip(f, lines)]
        band = (0, y0 - 34, W, y0 + hs[0] + hs[1] + 26 + 34)
        draw.rectangle(band, fill='#FFD400'); md.rectangle(band, fill=128)
        y = y0
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((W//2, y), l, ff, '#111318' if i == 0 else '#BB1E1E')
            y += hs[i] + 26
    elif style == 'BT':
        three = spec['three']
        limit = 1650 if ig else 1830
        f = [fit('BT', l, 230, 990, 4) for l in three]
        hs = [ff.getbbox(l, anchor='mt', stroke_width=4)[3] for ff, l in zip(f, three)]
        y = limit - sum(hs) - 2*14
        start = y
        gradient(im, (4, 10, 18), lambda r: 245*min(1, max(0, (r - (start - 200))/240)))
        for i, (l, ff) in enumerate(zip(three, f)):
            put((W//2, y), l, ff, '#FFD400' if i == 1 else 'white', 4, '#05101B')
            y += hs[i] + 14
    elif style == 'N':
        f = [fit('N', l, 120, 940) for l in lines]
        hs = [ff.getbbox(l, anchor='mt')[3] for ff, l in zip(f, lines)]
        box = (36, y0 - 28, W - 36, y0 + sum(hs) + 22 + 30)
        draw.rounded_rectangle(box, radius=14, fill='#0B3171'); md.rounded_rectangle(box, radius=14, fill=128)
        y = y0
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((W//2, y), l, ff, 'white' if i == 0 else '#E3F778')
            y += hs[i] + 22
    elif style == 'F':
        f = [fit('F', l, 150, 960, 4) for l in lines]
        hs = [ff.getbbox(l, anchor='mt', stroke_width=4)[3] for ff, l in zip(f, lines)]
        end = y0 + sum(hs) + 20
        gradient(im, (5, 13, 26), lambda r: 235 if r < end else 235*max(0, 1 - (r - end)/160))
        y = y0
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((W//2, y), l, ff, 'white' if i == 0 else '#49E4EF', 4, '#071322')
            y += hs[i] + 20
    elif style == 'S':
        f = [fit('S', l, 128, 900) for l in lines]
        hs = [ff.getbbox(l, anchor='mt')[3] for ff, l in zip(f, lines)]
        end = y0 + sum(hs) + 24
        gradient(im, (6, 10, 18), lambda r: 236 if r < end + 30 else 236*max(0, 1 - (r - end - 30)/150))
        draw.line((110, y0 - 30, W - 110, y0 - 30), fill='#C8A463', width=4)
        draw.line((110, end + 18, W - 110, end + 18), fill='#C8A463', width=4)
        y = y0
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((W//2, y), l, ff, 'white' if i == 0 else '#E9C171')
            y += hs[i] + 24
    elif style == 'R':
        f = [fit('R', l, 150, 900) for l in lines]
        hs = [ff.getbbox(l, anchor='lt')[3] for ff, l in zip(f, lines)]
        limit = 1640 if ig else 1800
        y = limit - sum(hs) - 18
        poly = [(0, y - 50), (W - 40, y - 80), (W - 40, limit + 30), (0, limit + 30)]
        gradient(im, (8, 8, 10), lambda r: 200*min(1, max(0, (r - (y - 420))/300)))
        draw.polygon(poly, fill='#C8161D'); md.polygon(poly, fill=128)
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((60, y), l, ff, 'white' if i == 0 else '#FFE14D', anchor='lt')
            y += hs[i] + 18
    elif style == 'T':
        f = [fit('T', l, 150, 960, 4) for l in lines]
        hs = [ff.getbbox(l, anchor='mt', stroke_width=4)[3] for ff, l in zip(f, lines)]
        bar = (0, y0 - 36, W, y0 + sum(hs) + 20 + 36)
        draw.rectangle(bar, fill='#0A0A0C'); md.rectangle(bar, fill=128)
        draw.rectangle((0, bar[3], W, bar[3] + 10), fill='#FFD400')
        y = y0
        for i, (l, ff) in enumerate(zip(lines, f)):
            put((W//2, y), l, ff, 'white' if i == 0 else '#FFD400', 4, '#000000')
            y += hs[i] + 20
    elif style == 'P':
        three = spec['three']
        f = [fit('P', l, 150, 860, 4) for l in three]
        hs = [ff.getbbox(l, anchor='lt', stroke_width=4)[3] for ff, l in zip(f, three)]
        end = y0 + sum(hs) + 2*22
        gradient(im, (6, 8, 12), lambda r: 225 if r < end else 225*max(0, 1 - (r - end)/170))
        y = y0
        for i, (l, ff) in enumerate(zip(three, f)):
            if i == 1:
                bb = ff.getbbox(l, anchor='lt')
                hl = (40, y + bb[1] - 12, 60 + bb[2] + 20, y + bb[3] + 12)
                draw.rectangle(hl, fill='#FFD400'); md.rectangle(hl, fill=128)
                put((60, y), l, ff, '#0A0A0A', anchor='lt')
            else:
                put((60, y), l, ff, 'white', 4, '#05080D', anchor='lt')
            y += hs[i] + 22
    if style == 'S':
        draw.rectangle((22, 22, W - 23, H - 23), outline='#B5975A', width=4)
    return bounds


def build(keys):
    for key in keys:
        spec = SHORTS[key]
        rows = []
        for letter in ('ABCD' if key.endswith('r2') else LETTERS):
            if (key, letter) in DROPPED:
                continue
            if not plate_path(key, letter).exists():
                print('missing plate', key, letter)
                continue
            for platform in ('instagram', 'youtube'):
                d = OUT / key / platform; d.mkdir(parents=True, exist_ok=True)
                im, info = picture(key, letter, platform)
                pic = im.copy()
                mask = Image.new('L', (W, H))
                bounds = title(im, mask, key, letter, platform)
                lo, hi = (230, 1690) if platform == 'instagram' else (40, 1880)
                assert all(20 <= b[0] < b[2] <= W - 20 for b in bounds), (key, letter, bounds)
                assert all(lo <= b[1] < b[3] <= hi for b in bounds), (key, letter, platform, bounds)
                # Type vs people: fraction of glyph pixels that land on a person (face/hair checked by eye on the sheet).
                pm = person_mask(pic)
                faces = person_mask.faces
                glyph = np.array(mask) == 255
                anytype = np.array(mask) > 0
                overlap = int((glyph & pm).sum())
                face_hits = []
                for fx0, fy0, fx1, fy1 in [list(map(int, f)) for f in faces]:
                    fw, fh = fx1 - fx0, fy1 - fy0
                    a, b, c, e = max(0, fx0 - fw//4), max(0, fy0 - fh//2), min(W, fx1 + fw//4), min(H, fy1 + fh//5)
                    face_hits.append(int(anytype[b:e, a:c].sum()))
                p = d / f"{spec['slug']}_cover-{letter}.png"
                im.convert('RGB').save(p)
                pic.convert('RGB').save(d / f"{p.stem}.picture.png")
                mask.save(d / f"{p.stem}.text-mask.png")
                row = dict(letter=letter, style=STYLE[key][letter], platform=platform, path=str(p.relative_to(ROOT)),
                           sha256=sha(p), bytes=p.stat().st_size, text_bounds=bounds, glyph_person_overlap_px=overlap,
                           faces=faces, type_on_face_or_hair_px=face_hits, **info)
                if platform == 'youtube':
                    j = p.with_suffix('.jpg')
                    im.convert('RGB').save(j, quality=90)
                    assert j.stat().st_size < 2_000_000
                    row.update(jpeg_path=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
                rows.append(row)
        (OUT / key / 'manifest.json').write_text(json.dumps(
            {'status': 'awaiting Dan pick', 'title': spec['title'], 'outputs': rows}, indent=2))
        sheet = Image.new('RGB', (len(LETTERS)*300, 2*565), '#101722')
        dr = ImageDraw.Draw(sheet)
        lab = ImageFont.truetype(str(SUP/'Arial Bold.ttf'), 24)
        for r in rows:
            x = LETTERS.index(r['letter'])*300; y = 0 if r['platform'] == 'instagram' else 565
            dr.text((x+12, y+14), f"{r['letter']} {r['platform'][:2]} face{sum(r['type_on_face_or_hair_px'])}", font=lab, fill='white')
            t = Image.open(ROOT / r['path']); t.thumbnail((280, 500)); sheet.paste(t, (x+10, y+52))
        sheet.save(OUT / key / 'internal-sheet.jpg', quality=92)
        print(f'{key}: {len(rows)} covers')


if __name__ == '__main__':
    build(sys.argv[1:] or ['s1', 's2', 's3'])
