#!/usr/bin/env python3
"""Terry Crews (DS-43) cover round 2. Dan, 2026-10-30: six unique designs, Terry full screen and ripped behind, Dan cut out in the corner
reacting to his laptop. Terry frames are real footage from the film's sources; corner Dan comes from r2/dan/<maker>/<n>.png on a green backdrop."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import hashlib, json, sys
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
R = ROOT/'Short-form video content/covers/review/ds43-terry-crews-20261030/r2'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
FONTS = {'din': SUP/'DIN Condensed Bold.ttf', 'impact': SUP/'Impact.ttf', 'georgia': SUP/'Georgia Bold.ttf', 'arial': SUP/'Arial Black.ttf'}
COPY = ["Terry Crews Doesn't", 'Eat Until 2 PM']
# id, frame, Terry's x in the source, Terry's place in the crop, Dan's side, maker, Dan image, font, band, line colours, size
DESIGNS = [('a', 'Z-119.3', 1410, .62, 'left',  'codex',  1, 'din',     '#FFD400', ['#111318', '#BB1E1E'], 150),
           ('b', 'Z-27.5',  1050, .36, 'right', 'google', 1, 'impact',  '#070B12', ['#FFFFFF', '#FFD400'], 128),
           ('c', 'R-44.9',   444, .50, 'right', 'codex',  2, 'din',     '#B3161B', ['#FFFFFF', '#FFE34D'], 150),
           ('d', 'Z-64.8',   990, .62, 'left',  'google', 2, 'arial',   '#FFFFFF', ['#0B3171', '#D0201F'], 96),
           ('e', 'Z-151.4',  786, .60, 'left',  'codex',  3, 'impact',  '#0B3171', ['#FFFFFF', '#49E4EF'], 128),
           ('f', 'Z-59',      806, .60, 'left',  'google', 3, 'georgia', '#F7F0E0', ['#17233A', '#A5281F'], 100)]
GAMMA = {'Z-27.5': 1.35, 'Z-119.3': 1.12, 'Z-59': 1.3, 'Z-151.4': 1.15}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fit(k, t, s, w):
    for n in range(s, 39, -1):
        f = ImageFont.truetype(str(FONTS[k]), n); b = f.getbbox(t)
        if b[2]-b[0] <= w: return f
    raise ValueError(t)
# Lid boxes on the 768x1376 plates (x0, top, x1, bottom): below the lid's top row only the lid survives, so no desk shows.
# Plate 1 showed keys above the lid, which no laptop does, so its lid is stretched up over them and his fingers go behind it.
LID = {'google/1': (58, 1128, 720, 1268, 1020), 'google/2': (106, 1053, 686, 1354, None), 'google/3': (0, 1076, 764, 1349, None)}
def cutout(p):
    key = f'{Path(p).parent.name}/{Path(p).stem}'
    if key in LID: return lid_cutout(p, LID[key])
    a = np.array(Image.open(p).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    key = np.clip((g-np.maximum(r, b)-18)/34, 0, 1); alpha = 1-key
    a[..., 1] = np.minimum(g, np.maximum(r, b)*1.02)   # despill
    im = Image.fromarray(np.dstack([a, alpha*255]).astype(np.uint8)).convert('RGBA')
    al = im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8)); im.putalpha(al)
    box = al.point(lambda v: 255 if v > 40 else 0).getbbox(); im = im.crop(box)
    # Drop the desk: the laptop then sits flush on the frame bottom. Desk rows are the wide run at the very bottom.
    w = (np.array(im.getchannel('A')) > 128).sum(1); low = len(w)-1
    while low > len(w)*.6 and w[low] > .96*w[len(w)-5]: low -= 1
    return im.crop((0, 0, im.width, low+1))
def lid_cutout(p, lid):
    x0, t, x1, b, up = lid; src = Image.open(p).convert('RGB'); a = np.array(src).astype(float); r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    alpha = 1-np.clip((g-np.maximum(r, bl)-18)/34, 0, 1)
    a[..., 1] = np.minimum(g, np.maximum(r, bl)*1.02)
    alpha[(up or t):] = 0
    im = Image.fromarray(np.dstack([a, alpha*255]).astype(np.uint8)).convert('RGBA')
    al = im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8)); im.putalpha(al)
    x0 += 8; x1 -= 8; b -= 8
    lidim = Image.fromarray(a.astype(np.uint8)).crop((x0, t, x1, b)).convert('RGBA')
    m = np.array(lidim).astype(float); grey = m[..., :3].mean(2, keepdims=True); m[..., :3] = grey*.9+m[..., :3]*.1; lidim = Image.fromarray(m.astype(np.uint8)).convert('RGBA')
    if up: lidim = lidim.resize((x1-x0, b-up), Image.Resampling.LANCZOS)
    im.alpha_composite(lidim, (x0, up or t))
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
    return im.crop((0, 0, im.width, im.height-round((b-(up or t))*.5)))

def picture(fr, tx, place, T):
    h = H-T; cw = round(1080*W/h); src = Image.open(R/f'terry/{fr}.png').convert('RGB')
    limit = (0, 955) if fr.startswith('R') else (0, 1920)
    x0 = max(limit[0], min(round(tx-place*cw), limit[1]-cw))
    if fr in GAMMA: src = src.point(lambda v: round(255*(v/255)**(1/GAMMA[fr])))
    pic = src.crop((x0, 0, x0+cw, 1080)).resize((W, h), Image.Resampling.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    return pic, x0
rows = []
for d, fr, tx, place, side, maker, n, fk, band, cols, size in DESIGNS:
    dan = R/f'dan/{maker}/{n}.png'
    if not dan.exists():
        print('missing', d, maker); dan = R/f'dan/codex/{n}.png'
    cut = cutout(dan)
    for pf in ['instagram', 'youtube']:
        T = 540 if pf == 'instagram' else 340; y = 270 if pf == 'instagram' else 70
        im = Image.new('RGBA', (W, H), band); pic, x0 = picture(fr, tx, place, T); im.paste(pic, (0, T))
        top = 1130 if pf == 'instagram' else 1070
        s = (H-top)/cut.height; c = cut.resize((round(cut.width*s), H-top), Image.Resampling.LANCZOS)
        if c.width > 760: s = 760/cut.width; c = cut.resize((760, round(cut.height*s)), Image.Resampling.LANCZOS)
        im.alpha_composite(c, (0 if side == 'left' else W-c.width, H-c.height))
        dr = ImageDraw.Draw(im); bounds = []; step = 132 if size >= 150 else 126
        for i, t in enumerate(COPY):
            f = fit(fk, t, size, 980); b = f.getbbox(t, anchor='mt'); dr.text((W//2, y+i*step), t, font=f, anchor='mt', fill=cols[i])
            bounds.append([W//2+b[0], y+i*step+b[1], W//2+b[2], y+i*step+b[3]])
        o = R/f'built/{d}'; o.mkdir(parents=True, exist_ok=True); p = o/f'{pf}.png'; im.convert('RGB').save(p)
        if pf == 'youtube': im.convert('RGB').save(o/'youtube.jpg', quality=92); assert (o/'youtube.jpg').stat().st_size < 2_000_000
        rows.append(dict(design=d, platform=pf, path=str(p.relative_to(ROOT)), sha256=sha(p), terry_frame=fr, x0=x0, text=bounds, dan=str(dan.relative_to(ROOT)), maker=maker))
(R/'built/manifest.json').write_text(json.dumps(rows, indent=1))
s = Image.new('RGB', (6*330, 2*585), '#222')
for i, row in enumerate(rows):
    t = Image.open(ROOT/row['path']); t.thumbnail((326, 580)); s.paste(t, ((i//2)*330, (i%2)*585))
s.save(R/'built/sheet.jpg', quality=90); print('built', len(rows))
