#!/usr/bin/env python3
"""Composite one still per treatment using the SAME geometry render.js will use,
so the look is approved before 7 minutes of video is encoded."""
import json, os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(HERE, '../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg')
SRC = os.path.join(HERE, '../V2 - How To Get Real Six Pack Abs With AI(2) - READY FOR UPLOAD.mp4')
L = json.load(open(os.path.join(HERE, 'layout.json')))
CROPS = json.load(open(os.path.join(HERE, 'shots', 'crops.json')))
OUT = os.path.join(HERE, 'shots', 'preview')
os.makedirs(OUT, exist_ok=True)
W, H = L['canvas']

BG = Image.open(os.path.join(HERE, 'assets', 'j2-bg.png')).convert('RGBA')
WM = Image.open(os.path.join(HERE, 'assets', 'wordmark.png')).convert('RGBA')


def frame(t):
    p = os.path.join(OUT, f'_src{t:.2f}.png')
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}',
                    '-i', SRC, '-frames:v', '1', p], check=True)
    return Image.open(p).convert('RGBA')


def compose(kind, t, shot=None, title=None):
    src = frame(t)
    sw, sh = src.size
    if kind in ('talk', 'broll'):
        cw = L['talk']['cropW']
        x0 = min(max(CROPS[shot] * sw - cw / 2, 0), sw - cw)
        out = src.crop((round(x0), 0, round(x0) + cw, sh)).resize((W, H), Image.LANCZOS)
    elif kind == 'card':
        c = L['card']
        out = BG.copy()
        out.alpha_composite(src.resize((c['w'], c['h']), Image.LANCZOS), (c['x'], c['y']))
        chip_p = os.path.join(HERE, 'assets', f'chip-{shot}.png')
        if os.path.exists(chip_p):
            ch = Image.open(chip_p).convert('RGBA')
            out.alpha_composite(ch, ((W - ch.width) // 2, c['chipY']))
    elif kind == 'pip':
        p = L['pip']
        box = L['pipBoxes'][shot]['box']
        out = BG.copy()
        g = src.crop(tuple(box))
        gw = round(g.width * p['gfxH'] / g.height)
        g = g.resize((gw, p['gfxH']), Image.LANCZOS)
        out.alpha_composite(g, ((W - gw) // 2, p['gfxTop']))
        # Dan's crop starts to the RIGHT of the PiP box, or the poster renders twice.
        dan_ar = p['danW'] / p['danH']
        cw = round(sh * dan_ar)
        x0 = min(L['pipBoxes'][shot]['srcX0'], sw - cw)
        assert x0 >= box[2], f'{shot}: Dan crop x0={x0} overlaps PiP box right edge {box[2]}'
        dan = src.crop((round(x0), 0, round(x0) + cw, sh)).resize((p['danW'], p['danH']), Image.LANCZOS)
        out.alpha_composite(dan, (p['danX'], p['danY']))
    out = out.convert('RGBA')
    out.alpha_composite(WM, (L['wordmark']['x'], L['wordmark']['y']))
    if title:
        out.alpha_composite(Image.open(os.path.join(HERE, 'assets', f'title-{title}.png')).convert('RGBA'))
    return out.convert('RGB')


jobs = [
    ('talk+title', 'talk', 101.5, 'A-p0-s00', 'A'),
    ('talk', 'talk', 1445.0, 'B-p1-s02', None),
    ('card-clock', 'card', 1441.8, 'B-p1-s01', None),
    ('card-phone', 'card', 293.5, 'I-p0-s05', None),
    ('card-lower3rd', 'card', 277.5, 'I-p0-s00', None),
    ('pip-seanray', 'pip', 146.9, 'A-p0-s06', None),
    ('pip-mikechang', 'pip', 162.3, 'A-p0-s09', None),
    ('broll-maid', 'broll', 650.5, 'G-p0-s02', None),
]
tiles = []
for name, kind, t, shot, title in jobs:
    im = compose(kind, t, shot, title)
    im.save(os.path.join(OUT, name + '.jpg'), quality=92)
    tiles.append((name, im))
    print(f'  {name:16s} {kind:6s} @{t}')

TW = 232
sheet = Image.new('RGB', (len(tiles) * (TW + 8) + 8, round(TW * 16 / 9) + 16), (0, 0, 0))
for i, (name, im) in enumerate(tiles):
    sheet.paste(im.resize((TW, round(TW * 16 / 9)), Image.LANCZOS), (8 + i * (TW + 8), 8))
sheet.save(os.path.join(OUT, 'preview-sheet.jpg'), quality=92)
print('->', os.path.join(OUT, 'preview-sheet.jpg'))
