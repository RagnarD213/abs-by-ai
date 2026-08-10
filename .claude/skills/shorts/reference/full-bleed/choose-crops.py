#!/usr/bin/env python3
"""Pick a 9:16 crop window per shot and render a review sheet of the ACTUAL vertical
frames, so the framing is checked by eye instead of assumed."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
man = json.load(open(os.path.join(SHOTS, 'manifest.json')))
plan = json.loads(subprocess.check_output(
    ['node', '-e', "const p=require('./plan.js');console.log(JSON.stringify({SHOTS:p.SHOTS,TALK_X:p.TALK_X}))"],
    cwd=HERE).decode())
SPEC, TALK_X = plan['SHOTS'], plan['TALK_X']

CROP_FRAC = 9 / 16 * (9 / 16)  # 9:16 window on a 16:9 frame = 0.3164 of the width


def auto_x(im):
    """Centre of the most detailed 9:16-wide column band — where the subject is."""
    g = im.convert('L').filter(ImageFilter.GaussianBlur(1.2))
    edges = ImageChops.difference(g, g.filter(ImageFilter.GaussianBlur(4)))
    px = edges.load()
    w, h = edges.size
    col = [0] * w
    for x in range(w):
        s = 0
        for y in range(0, h, 3):        # every 3rd row is plenty and 3x faster
            s += px[x, y]
        col[x] = s
    # smooth
    k = 9
    sm = [sum(col[max(0, i - k):min(w, i + k + 1)]) for i in range(w)]
    win = max(8, int(w * CROP_FRAC))
    best, bi = -1, 0
    run = sum(sm[:win])
    for i in range(w - win):
        if run > best:
            best, bi = run, i
        run += sm[i + win] - sm[i]
    return (bi + win / 2) / w


chosen = {}
for m in man:
    spec = SPEC[m['name']]
    im = Image.open(os.path.join(SHOTS, m['name'] + '.jpg')).convert('RGB')
    if spec['t'] == 'talk':
        x = TALK_X
    elif spec['t'] == 'pip':
        x = TALK_X
    elif spec['t'] == 'card':
        x = 0.5
    elif spec.get('x') is not None:
        x = spec['x']
    else:
        x = auto_x(im)
    # keep the window fully inside the frame
    x = min(max(x, CROP_FRAC / 2), 1 - CROP_FRAC / 2)
    chosen[m['name']] = round(x, 4)

json.dump(chosen, open(os.path.join(SHOTS, 'crops.json'), 'w'), indent=1)

# ---- review sheet: render each shot as it will actually appear, 9:16 ----------------
TH_W = 150
TH_H = round(TH_W * 16 / 9)
COLS = 14
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 13)
except OSError:
    font = ImageFont.load_default()

tiles = []
for m in man:
    spec = SPEC[m['name']]
    im = Image.open(os.path.join(SHOTS, m['name'] + '.jpg')).convert('RGB')
    W, H = im.size
    if spec['t'] == 'card':
        # whole 16:9 frame, letterboxed into the vertical frame (J2 card, mocked flat here)
        tile = Image.new('RGB', (TH_W, TH_H), (13, 14, 11))
        cw = round(TH_W * 0.90)
        card = im.resize((cw, round(cw * H / W)), Image.LANCZOS)
        tile.paste(card, ((TH_W - cw) // 2, (TH_H - card.height) // 2))
        ImageDraw.Draw(tile).rectangle(
            [(TH_W - cw) // 2 - 3, (TH_H - card.height) // 2 - 3,
             (TH_W + cw) // 2 + 2, (TH_H + card.height) // 2 + 2],
            outline=(140, 152, 88), width=2)
    else:
        cw = W * CROP_FRAC
        x0 = min(max(chosen[m['name']] * W - cw / 2, 0), W - cw)
        tile = im.crop((round(x0), 0, round(x0 + cw), H)).resize((TH_W, TH_H), Image.LANCZOS)
    bar = 34
    out = Image.new('RGB', (TH_W, TH_H + bar), (18, 18, 18))
    out.paste(tile, (0, 0))
    d = ImageDraw.Draw(out)
    colour = {'talk': (150, 220, 150), 'broll': (230, 230, 230),
              'card': (255, 200, 90), 'pip': (255, 120, 120)}[spec['t']]
    d.text((4, TH_H + 2), m['name'][:14], font=font, fill=colour)
    d.text((4, TH_H + 17), f"{spec['t']} x={chosen[m['name']]:.2f}", font=font, fill=colour)
    tiles.append(out)

rows = (len(tiles) + COLS - 1) // COLS
w, h = tiles[0].width, tiles[0].height
sheet = Image.new('RGB', (COLS * (w + 6) + 6, rows * (h + 6) + 6), (6, 6, 6))
for i, t in enumerate(tiles):
    r, c = divmod(i, COLS)
    sheet.paste(t, (6 + c * (w + 6), 6 + r * (h + 6)))
p = os.path.join(SHOTS, 'review-crops.jpg')
sheet.save(p, quality=90)
print(f'{len(tiles)} tiles -> {p} ({sheet.width}x{sheet.height})')
