#!/usr/bin/env python3
"""Terry Crews Fasting (DS-43) covers, 2026-10-30. Adapted from the DS-49 builder.

Plates: generate.sh (Codex gpt-6.1-sol high) and the extra options in google/. C layers the real studio cutout over a plate;
D layers a real frame of the Business Insider clip over the AI Dan laptop plate. Same headline on every design.
    python3 scripts/covers/ds43-20261030/build.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'Short-form video content/covers/review/ds43-terry-crews-20261030'
SRC = OUT/'sources'; GOOGLE = OUT/'google'; BUILT = OUT/'built'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
FONTS = {'din': (SUP/'DIN Condensed Bold.ttf', 0), 'impact': (SUP/'Impact.ttf', 0), 'futura': (SUP/'Futura.ttc', 4),
         'avenir': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8), 'bask': (SUP/'Georgia Bold.ttf', 0)}
PM = Path.home()/'.cache/absbyai/personmask/personmask'
CUTOUT = ROOT/'photos/finalized social media photos/_cutouts/studio-blue-240_CUTOUT.png'
TERRY = SRC/'terry-5.0.png'
COPY = ['Terry Crews Doesn\'t', 'Eat Until 2 PM']
BOTTOM = ['Terry Crews', 'Doesn\'t Eat', 'Until 2 PM']
STYLE = {  # top-band designs: font, band colour, text colours, size, spacing
    'A': ('din', '#FFD400', ['#111318', '#BB1E1E'], 190, 152),
    'B': ('impact', None, ['#FFFFFF', '#49E4EF'], 150, 155),
    'C': ('futura', '#0B3171', ['#FFFFFF', '#E3F778'], 120, 145),
    'F': ('impact', '#B3161B', ['#FFFFFF', '#FFD400'], 138, 150),
    'G': ('avenir', None, ['#FFFFFF', '#FFFFFF'], 150, 150),
    'H': ('bask', '#F7F0E0', ['#17233A', '#A5281F'], 120, 145),
}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(k, s):
    p, i = FONTS[k]; return ImageFont.truetype(str(p), s, index=i)
def fit(k, word, size, width):
    for n in range(size, 39, -1):
        f = font(k, n); b = f.getbbox(word)
        if b[2]-b[0] <= width: return f
    raise ValueError(word)

def top_title(im, mask, k, platform):
    fk, band, colors, size, spacing = STYLE[k]
    y = 260 if platform == 'instagram' else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    if band: draw.rectangle((0, y-24, W, y+spacing+size+10), fill=band)
    bounds = []
    for i, word in enumerate(COPY):
        f = fit(fk, word, size, 950); box = f.getbbox(word, anchor='mt')
        stroke = 0 if band else 5; yy = y+i*spacing
        draw.text((W//2, yy), word, font=f, anchor='mt', fill=colors[i], stroke_width=stroke, stroke_fill='#071322')
        md.text((W//2, yy), word, font=f, anchor='mt', fill=255, stroke_width=stroke)
        bounds.append([W//2+box[0]-stroke, yy+box[1]-stroke, W//2+box[2]+stroke, yy+box[3]+stroke])
    return bounds, y+spacing+size+10

def person_top(im):
    with tempfile.TemporaryDirectory(prefix='ds43-cover-') as t:
        i = Path(t)/'p.png'; m = Path(t)/'m.png'; im.convert('RGB').save(i)
        subprocess.run([str(PM), str(i), str(m)], capture_output=True, text=True, check=True)
        a = np.array(Image.open(m)) > 127
    r = np.where(a.any(axis=1))[0]
    return int(r.min()) if len(r) else H

def fill(path): return ImageOps.fit(Image.open(path).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')

def design_top(k, platform, plate):
    im = fill(plate)
    if k == 'B':
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = [5, 13, 26]
        for y in range(700): a[y, :, 3] = int(200*(1-y/700))
        im.alpha_composite(Image.fromarray(a))
    if k == 'C':
        raw = Image.open(CUTOUT).convert('RGBA'); sub = raw.crop(raw.getchannel('A').getbbox())
        top = 640 if platform == 'instagram' else 470
        sc = (H-top+60)/sub.height; sub = sub.resize((round(sub.width*sc), round(sub.height*sc)), Image.Resampling.LANCZOS)
        pad = 20; lay = Image.new('RGBA', (sub.width+2*pad, sub.height+2*pad)); lay.alpha_composite(sub, (pad, pad))
        x = W-sub.width-pad+40; y = top-pad
        line = Image.new('RGBA', lay.size, 'white'); line.putalpha(lay.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line, (x, y)); im.alpha_composite(lay, (x, y))
        return im, dict(real_photo=True, source=str(CUTOUT.relative_to(ROOT)), source_sha256=sha(CUTOUT), source_person_pixels_preserved=True)
    t = person_top(im); target = (250 if platform == 'instagram' else 80)+(330 if STYLE[k][1] else 330)+25
    if t < target:
        col = tuple(int(v) for v in np.array(im.convert('RGB'))[:40].reshape(-1, 3).mean(axis=0)); s = target-t
        n = Image.new('RGBA', (W, H), col+(255,)); n.alpha_composite(im.crop((0, 0, W, H-s)), (0, s)); im = n
        f = np.zeros((H, W, 4), np.uint8); f[:, :, :3] = col
        for yy in range(s, min(H, s+120)): f[yy, :, 3] = int(255*(1-(yy-s)/120))
        im.alpha_composite(Image.fromarray(f))
    return im, dict(source_person_top=t)

def design_d(platform):
    src = Image.open(SRC/'D.png').convert('RGB'); a = np.array(src).astype(float)
    # Grey backdrop to the film's deep blue: low-chroma greys outside the person and the laptop.
    bg = ((a.max(2)-a.min(2)) < 48) & (a.mean(2) > 95) & ~(np.array(Image.open(PM_mask(src))) > 127)
    bg[1170:1380, 170:600] = False
    m = np.array(Image.fromarray((bg*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(float)/255
    g = np.linspace(0, 1, a.shape[0])[:, None]; grad = np.zeros_like(a); grad[..., 0] = 6; grad[..., 1] = 30+22*g; grad[..., 2] = 78+44*g
    out = a*(1-m[..., None])+grad*m[..., None]
    t0, t1, d0 = (200, 880, 1100) if platform == 'instagram' else (0, 760, 1000)
    panel = Image.fromarray(out.astype(np.uint8)).crop((0, 640, 941, 640+round((H-d0)*941/W))).resize((W, H-d0), Image.Resampling.LANCZOS)
    ch = round((t1-t0)*1040/W)
    t = Image.open(TERRY).convert('RGB').crop((380, 6, 1420, 6+ch)).resize((W, t1-t0), Image.Resampling.LANCZOS)
    im = Image.new('RGBA', (W, H), '#0a0f18')
    im.paste(t, (0, t0)); im.paste(panel, (0, d0))
    return im, dict(terry_frame=str(TERRY.relative_to(ROOT)), terry_frame_sha256=sha(TERRY), title_y=t1)

def PM_mask(src):
    p = OUT/'sources/D-person.png'
    if not p.exists():
        i = OUT/'sources/D-rgb.png'; src.save(i); subprocess.run([str(PM), str(i), str(p)], capture_output=True, check=True)
    return p

def title_d(im, mask, y0):
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    draw.rectangle((0, y0, W, y0+220), fill='#FFD400'); md.rectangle((0, y0, W, y0+220), fill=255)
    bounds = []
    for i, w in enumerate(COPY):
        f = fit('impact', w, 100, 980); y = y0+6+i*104; b = f.getbbox(w, anchor='mt')
        draw.text((W//2, y), w, font=f, anchor='mt', fill='#111B2C'); bounds.append([W//2+b[0], y+b[1], W//2+b[2], y+b[3]])
    return bounds

def title_e(im, mask, platform):
    limit = 1675 if platform == 'instagram' else 1810
    sizes = [118, 118, 126] if platform == 'instagram' else [150, 150, 160]; fs = [fit('avenir', l, s, 980) for l, s in zip(BOTTOM, sizes)]
    hs = [f.getbbox(l, anchor='mt', stroke_width=4)[3] for f, l in zip(fs, BOTTOM)]
    y = limit-sum(hs)-28; top = y-34
    a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = (4, 10, 18); a[top:, :, 3] = 255
    for r in range(top-40, top): a[r, :, 3] = round(255*(r-top+40)/40)
    im.alpha_composite(Image.fromarray(a))
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask); bounds = []
    for i, (l, f, h) in enumerate(zip(BOTTOM, fs, hs)):
        b = f.getbbox(l, anchor='mt', stroke_width=4)
        draw.text((W//2, y), l, font=f, anchor='mt', fill='#FFD400' if i == 2 else 'white', stroke_width=4, stroke_fill='#05101B')
        md.text((W//2, y), l, font=f, anchor='mt', fill=255, stroke_width=4)
        bounds.append([W//2+b[0], y+b[1], W//2+b[2], y+b[3]]); y += h+14
    return bounds

def plate_for(k):
    return (GOOGLE if k in 'FGH' else SRC)/f'{k}.png'

rows = []
for k in 'ABCDEFGH':
    plate = plate_for(k)
    if not plate.exists(): print('missing', k); continue
    for pf in ['instagram', 'youtube']:
        d = BUILT/k/pf; d.mkdir(parents=True, exist_ok=True); p = d/f'ds-43_terry-crews_cover-{k}.png'
        mask = Image.new('L', (W, H))
        if k == 'D': im, info = design_d(pf)
        elif k == 'E':
            im, info = fill(plate), {}
        else: im, info = design_top(k, pf, plate)
        im.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
        if k == 'D': bounds = title_d(im, mask, info['title_y'])
        elif k == 'E': bounds = title_e(im, mask, pf)
        else: bounds, _ = top_title(im, mask, k, pf)
        if k == 'G': ImageDraw.Draw(im)
        im.convert('RGB').save(p); mask.save(p.with_name(p.stem+'.text-mask.png'))
        if pf == 'youtube':
            j = p.with_suffix('.jpg'); im.convert('RGB').save(j, quality=92); assert j.stat().st_size < 2_000_000
            info.update(jpeg_path=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
        rows.append(dict(letter=k, platform=pf, path=str(p.relative_to(ROOT)), sha256=sha(p), text_bounds=bounds, plate=str(plate.relative_to(ROOT)), plate_sha256=sha(plate), **info))
(BUILT/'manifest.json').write_text(json.dumps(rows, indent=1))
print('built', len(rows))
