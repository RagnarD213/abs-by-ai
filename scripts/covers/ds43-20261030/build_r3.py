#!/usr/bin/env python3
"""Terry Crews (DS-43) cover round 3. Dan, 2026-10-30: the round 2 X4 design and expression, new headline, and Terry monstrously ripped and
flexing, not standing around. Real footage frames; a frame narrower than the layout is anchored to the bottom and its top row colour fills up."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import hashlib, json
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'Short-form video content/covers/review/ds43-terry-crews-20261030'
R = BASE/'r3'; DAN = BASE/'r2/dan/codex/1.png'
W, H = 1080, 1920
FONT = '/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf'
COPY = ["Why Terry Crews Doesn't", 'Eat Until 2 PM']
# id, frame, crop (x0, x1, y0), Dan's width cap, side
SHOTS = [('a', 'Z-46.8', (1129, 1920, 0), 620, 'left'), ('b', 'Z-55.2', (760, 1360, 205), 620, 'left'), ('c', 'Z-75', (660, 1340, 50), 620, 'right')]
GAMMA = {'Z-46.8': 1.1}
BOTTOM = {'Z-75': 1030}   # below this is the photo's file name on the monitor
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fit(t, s, w):
    for n in range(s, 39, -1):
        f = ImageFont.truetype(FONT, n); b = f.getbbox(t)
        if b[2]-b[0] <= w: return f
    raise ValueError(t)
def cutout(p):
    a = np.array(Image.open(p).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    alpha = 1-np.clip((g-np.maximum(r, b)-18)/34, 0, 1); a[..., 1] = np.minimum(g, np.maximum(r, b)*1.02)
    im = Image.fromarray(np.dstack([a, alpha*255]).astype(np.uint8)).convert('RGBA')
    al = im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8)); im.putalpha(al)
    im = im.crop(al.point(lambda v: 255 if v > 40 else 0).getbbox())
    w = (np.array(im.getchannel('A')) > 128).sum(1); low = len(w)-1
    while low > len(w)*.6 and w[low] > .96*w[len(w)-5]: low -= 1
    return im.crop((0, 0, im.width, low+1))
cut = cutout(DAN); rows = []
for d, fr, (x0, x1, y0), dw, side in SHOTS:
    src = Image.open(R/f'terry/{fr}.png').convert('RGB')
    if GAMMA.get(fr, 1) != 1: src = src.point(lambda v: round(255*(v/255)**(1/GAMMA[fr])))
    crop = src.crop((x0, y0, x1, BOTTOM.get(fr, 1080))); sc = W/crop.width; h = round(crop.height*sc)
    pic = crop.resize((W, h), Image.Resampling.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    top_col = tuple(int(v) for v in np.array(pic)[:6].reshape(-1, 3).mean(0))
    for pf in ['instagram', 'youtube']:
        band_end = 520 if pf == 'instagram' else 340; y = 262 if pf == 'instagram' else 80; step = 124
        im = Image.new('RGBA', (W, H), top_col+(255,))
        if h > H-band_end: pic2 = pic.crop((0, h-(H-band_end), W, h)); im.paste(pic2, (0, band_end))
        else: im.paste(pic, (0, H-h))
        s = dw/cut.width; c = cut.resize((dw, round(cut.height*s)), Image.Resampling.LANCZOS)
        im.alpha_composite(c, (0 if side == 'left' else W-dw, H-c.height))
        dr = ImageDraw.Draw(im); dr.rectangle((0, 0, W, band_end), fill='#FFD400'); bounds = []
        for i, (t, col) in enumerate(zip(COPY, ['#111318', '#BB1E1E'])):
            f = fit(t, 136, 1000); b = f.getbbox(t, anchor='mt'); dr.text((W//2, y+i*step), t, font=f, anchor='mt', fill=col)
            bounds.append([W//2+b[0], y+i*step+b[1], W//2+b[2], y+i*step+b[3]])
        o = R/f'built/{d}'; o.mkdir(parents=True, exist_ok=True); p = o/f'{pf}.png'; im.convert('RGB').save(p)
        if pf == 'youtube': im.convert('RGB').save(o/'youtube.jpg', quality=92)
        assert all(25 <= b[0] and b[2] <= 1055 and (240 if pf == 'instagram' else 50) <= b[1] for b in bounds), bounds
        rows.append(dict(design=d, platform=pf, path=str(p.relative_to(ROOT)), sha256=sha(p), terry_frame=fr, crop=[x0, x1, y0], text=bounds))
(R/'built/manifest.json').write_text(json.dumps(rows, indent=1))
n = len(SHOTS); s = Image.new('RGB', (n*400, 2*715), '#222')
for i, row in enumerate(rows):
    t = Image.open(ROOT/row['path']); t.thumbnail((396, 708)); s.paste(t, ((i//2)*400, (i%2)*715))
s.save(R/'built/sheet.jpg', quality=90); print('built', len(rows))
