#!/usr/bin/env python3
"""Alcohol And Abs Shorts (SL-10) covers, 2026-11-01. Adapted from the DS-49 and DS-43 builders.

Plates: generate.sh (Codex gpt-6.1-sol high) in sources/, the Google options in google/. C layers a real studio cutout over a plate;
person pixels are never redrawn. Same headline on all eight per Short; only layout, type and colour change. Instagram keeps the title
clear of the 3:4 grid crop; YouTube sits higher.
    python3 scripts/covers/sl10-20261101/build.py [s1 s2 ...]
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'Short-form video content/covers/review/sl10-alcohol-20261101'
SRC = OUT/'sources'; GOOGLE = OUT/'google'; BUILT = OUT/'built'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
FONTS = {'din': (SUP/'DIN Condensed Bold.ttf', 0), 'impact': (SUP/'Impact.ttf', 0), 'futura': (SUP/'Futura.ttc', 4),
         'avenir': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8), 'bask': (SUP/'Baskerville.ttc', 2)}
PM = Path.home()/'.cache/absbyai/personmask/personmask'
CUT = ROOT/'photos/finalized social media photos/_cutouts'
SHORTS = {
    's1': dict(slug='alcohol-short1_your-drinks-should-taste-bad', title='Your Drinks Should Taste Bad',
               copy=['Your Drinks Should', 'Taste Bad'], bottom=['Your Drinks', 'Should', 'Taste Bad'], cutout='studio-blue-247',
               layouts=dict(F='yellow', G='white', H='bottom')),
    's2': dict(slug='alcohol-short2_your-nightly-wine-is-killing-your-abs', title='Your Nightly Wine Is Killing Your Abs',
               copy=['Your Nightly Wine', 'Is Killing Your Abs'], bottom=['Your Nightly', 'Wine Is Killing', 'Your Abs'], cutout='studio-blue-213',
               layouts=dict(F='yellow', G='gold', H='white')),
    's3': dict(slug='alcohol-short3_stop-drinking-3-hours-before-bed', title='Stop Drinking 3 Hours Before Bed',
               copy=['Stop Drinking', '3 Hours Before Bed'], bottom=['Stop Drinking', '3 Hours', 'Before Bed'], cutout='studio-blue-173',
               layouts=dict(F='white', G='yellow', H='gold')),
    's4': dict(slug='alcohol-short4_what-killed-my-urge-to-drink', title='What Killed My Urge To Drink',
               copy=['What Killed My', 'Urge To Drink'], bottom=['What Killed', 'My Urge', 'To Drink'], cutout='studio-blue-169',
               layouts=dict(F='yellow', G='white', H='gold')),
}
LETTERS = 'ABCDEFGH'
BASE = dict(A='yellow', B='white', C='navy', D='bottom', E='gold')
D_BG = (4, 10, 18)
# (short, letter): person_top override as a row on the 1080-wide picture, for party plates whose friends stand taller than Dan.
HAIR_ROW = {}
# (short, letter): picture zoom for the bottom layout.
BOTTOM_ZOOM = {('s2', 'D'): 0.92, ('s3', 'D'): 0.86}
# Short: where the real cutout's head starts (Instagram, YouTube), so it clears the props on the plate.
CUT_TOP = {'s2': (780, 620)}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def font(k, size):
    p, i = FONTS[k]
    return ImageFont.truetype(str(p), size, index=i)

def fit(k, word, size, width):
    for n in range(size, 39, -1):
        f = font(k, n); b = f.getbbox(word)
        if b[2]-b[0] <= width: return f
    raise ValueError(word)

def d_layout(spec, platform):
    limit = 1675 if platform == 'instagram' else 1800
    lines = spec['bottom']
    fs = [fit('avenir', line, 200 if platform == 'youtube' else 150, 990) for line in lines]
    n = min(f.size for f in fs); fs = [font('avenir', n) for _ in lines]
    heights = [f.getbbox(l, anchor='mt', stroke_width=4)[3] for f, l in zip(fs, lines)]
    return fs, heights, limit-sum(heights)-28

def title(im, mask, layout, platform, spec):
    y = 260 if platform == 'instagram' else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask); copy = spec['copy']
    if layout == 'bottom':
        fs, heights, yy = d_layout(spec, platform); bounds = []
        for i, (line, f, height) in enumerate(zip(spec['bottom'], fs, heights)):
            box = f.getbbox(line, anchor='mt', stroke_width=4)
            draw.text((W//2, yy), line, font=f, anchor='mt', fill='#49E4EF' if i == len(fs)-1 else 'white', stroke_width=4, stroke_fill='#05101B')
            md.text((W//2, yy), line, font=f, anchor='mt', fill=255, stroke_width=4)
            bounds.append([W//2+box[0], yy+box[1], W//2+box[2], yy+box[3]]); yy += height+14
        return bounds
    if layout == 'yellow':
        draw.rectangle((0, y-24, W, y+330), fill='#FFD400')
        k, size, spacing, colors = 'din', 190, 152, ['#111318', '#BB1E1E']
    elif layout == 'white':
        k, size, spacing, colors = 'impact', 156, 155, ['#FFFFFF', '#49E4EF']
    elif layout == 'navy':
        draw.rounded_rectangle((36, y-25, W-36, y+315), radius=12, fill='#0B3171')
        k, size, spacing, colors = 'futura', 130, 145, ['#FFFFFF', '#E3F778']
    else:
        k, size, spacing, colors = 'bask', 148, 148, ['#FFFFFF', '#E9C171']
        draw.line((100, y-20, W-100, y-20), fill='#C8A463', width=4); draw.line((100, y+312, W-100, y+312), fill='#C8A463', width=4)
    bounds = []
    for i, word in enumerate(copy):
        f = fit(k, word, size, 920 if k == 'futura' else 950); box = f.getbbox(word, anchor='mt')
        yy = y+i*spacing; stroke = 4 if k == 'impact' else 0
        draw.text((W//2, yy), word, font=f, anchor='mt', fill=colors[i], stroke_width=stroke, stroke_fill='#071322')
        md.text((W//2, yy), word, font=f, anchor='mt', fill=255, stroke_width=stroke)
        bounds.append([W//2+box[0]-stroke, yy+box[1]-stroke, W//2+box[2]+stroke, yy+box[3]+stroke])
    return bounds

def person_top(im):
    with tempfile.TemporaryDirectory(prefix='sl10-cover-') as temp:
        inp = Path(temp)/'p.png'; mp = Path(temp)/'m.png'; im.convert('RGB').save(inp)
        subprocess.run([str(PM), str(inp), str(mp)], capture_output=True, text=True, check=True)
        person = np.array(Image.open(mp)) > 127
    rows = np.where(person.any(axis=1))[0]
    return int(rows.min()) if len(rows) else H

def plate_path(s, k):
    return (GOOGLE if k in 'FGH' else SRC)/f'{s}-{k}.png'

def picture(s, k, layout, platform):
    spec = SHORTS[s]; plate = plate_path(s, k)
    src = Image.open(plate).convert('RGB')
    im = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    info = {'plate_sha256': sha(plate), 'source': 'real+plate' if k == 'C' else 'ai'}
    if layout == 'bottom':
        hair = 260 if platform == 'instagram' else 140
        fs, heights, yy = d_layout(spec, platform); B = yy-10
        z = BOTTOM_ZOOM.get((s, k), 1.0) if platform == 'instagram' else 1.0
        pic = im.resize((round(W*z), round(H*z)), Image.Resampling.LANCZOS)
        top = HAIR_ROW.get((s, k)) or person_top(pic)
        out = Image.new('RGBA', (W, H), D_BG+(255,))
        y0 = hair-top; x0 = (W-pic.width)//2
        if x0 > 0:   # zoomed out: the sides continue as a blur of the same picture
            out.alpha_composite(im.filter(ImageFilter.GaussianBlur(45)))
        part = pic.crop((max(0, -x0), max(0, -y0), max(0, -x0)+min(W, pic.width), max(0, -y0)+B-max(0, y0)))
        if x0 > 0:   # feather its side edges into that blur
            edge = np.ones(part.size[0], np.float32); ramp = np.linspace(0, 1, 60)
            edge[:60] = ramp; edge[-60:] = ramp[::-1]
            alpha = np.array(part.getchannel('A'), np.float32)*edge[None, :]
            part.putalpha(Image.fromarray(alpha.astype(np.uint8)))
        out.alpha_composite(part, (max(0, x0), max(0, y0)))
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = D_BG
        a[B:, :, 3] = 255
        for row in range(B-90, B): a[row, :, 3] = round(255*(row-(B-90))/90)
        if y0 > 0:
            for row in range(0, min(H, y0+120)): a[row, :, 3] = max(a[row, 0, 3], round(255*max(0, 1-(row-y0)/120)) if row >= y0 else 255)
        out.alpha_composite(Image.fromarray(a))
        return out, info
    if platform == 'youtube' and k != 'C':
        f = 1.12; top0 = HAIR_ROW.get((s, k)) or person_top(im); target = 90+(350 if layout in ('white', 'gold') else 355)
        off = min(H*(1-1/f), max(0, top0-target/f)); cw = W/f
        im = im.crop((round(W/2-cw/2), round(off), round(W/2+cw/2), round(off+H/f))).resize((W, H), Image.Resampling.LANCZOS)
    if k == 'C':
        p = CUT/f"{spec['cutout']}_CUTOUT.png"
        raw = Image.open(p).convert('RGBA'); b = raw.getchannel('A').getbbox(); sub = raw.crop(b)
        top = CUT_TOP.get(s, (650, 480))[platform != 'instagram']
        scale = (H-top+60)/sub.height
        sub = sub.resize((round(sub.width*scale), round(sub.height*scale)), Image.Resampling.LANCZOS)
        pad = 20; layer = Image.new('RGBA', (sub.width+2*pad, sub.height+2*pad)); layer.alpha_composite(sub, (pad, pad))
        x = W-sub.width-10-pad; y = top-pad
        line = Image.new('RGBA', layer.size, 'white'); line.putalpha(layer.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line, (x, y)); im.alpha_composite(layer, (x, y))
        info.update(real_photo=True, cutout=str(p.relative_to(ROOT)), cutout_sha256=sha(p), person_pixels_preserved=True)
    else:
        top = HAIR_ROW.get((s, k)) or person_top(im)
        target = (260 if platform == 'instagram' else 90)+(350 if layout in ('white', 'gold') else 355)
        shift = max(0, target-top)
        if shift:
            strip = ImageOps.flip(im.crop((0, 0, W, max(20, top-20)))).resize((W, shift)).filter(ImageFilter.GaussianBlur(30))
            shifted = Image.new('RGBA', (W, H)); shifted.alpha_composite(im.crop((0, 0, W, H-shift)), (0, shift)); shifted.alpha_composite(strip, (0, 0)); im = shifted
        info.update(person_top=top, shift=shift)
    if layout in ('white', 'gold'):
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = [5, 13, 26]
        if layout == 'white':
            for y in range(850): a[y, :, 3] = int(220*max(0, 1-y/850))
        else:
            solid, end = (470, 590) if platform == 'instagram' else (405, 440)
            for y in range(end): a[y, :, 3] = 238 if y < solid else int(238*(1-(y-solid)/(end-solid)))
        im.alpha_composite(Image.fromarray(a))
    return im, info

def build(keys):
    for s in keys:
        spec = SHORTS[s]; rows = []
        for k in LETTERS:
            if not plate_path(s, k).exists():
                print('missing plate', s, k); continue
            layout = BASE.get(k) or spec['layouts'][k]
            for platform in ['instagram', 'youtube']:
                d = BUILT/s/k; d.mkdir(parents=True, exist_ok=True)
                im, info = picture(s, k, layout, platform)
                p = d/f'{platform}.png'
                im.convert('RGB').save(d/f'{platform}.picture.png')
                mask = Image.new('L', (W, H)); bounds = title(im, mask, layout, platform, spec)
                assert all(30 <= b[0] < b[2] <= W-30 for b in bounds), (s, k, bounds)
                if layout == 'gold': ImageDraw.Draw(im).rectangle((22, 22, W-23, H-23), outline='#B5975A', width=4)
                im.convert('RGB').save(p); mask.save(d/f'{platform}.text-mask.png')
                if platform == 'youtube':
                    j = p.with_suffix('.jpg'); im.convert('RGB').save(j, quality=92); assert j.stat().st_size < 2_000_000
                    info.update(jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
                rows.append(dict(letter=k, platform=platform, layout=layout, sha256=sha(p), text_bounds=bounds, **info))
        (BUILT/s/'manifest.json').write_text(json.dumps({'status': 'awaiting Dan pick', 'copy': spec['copy'], 'outputs': rows}, indent=2))
        print(s, 'built', len(rows))

if __name__ == '__main__':
    build(sys.argv[1:] or list(SHORTS))
