#!/usr/bin/env python3
"""How To Do Pull-Ups (DS-76) covers, 2026-10-29. Adapted from the DS-84 Hamstring Curls builder.

AI plates come from generate.sh (codex-image.sh, GPT-6.1 Sol high). C composites a real studio cutout over a
Codex background plate; the person pixels are never redrawn. Same headline per Short on all five designs;
only layout, type and colour change. Instagram keeps the title clear of the 4:5 grid crop; YouTube sits higher.

    python3 scripts/covers/ds76-20261029/build.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Short-form video content/covers/review/ds76-pull-ups-20261029'
SRC = OUT / 'sources'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
FONTS = {
    'A': (SUP/'DIN Condensed Bold.ttf', 0),
    'B': (SUP/'Impact.ttf', 0),
    'C': (SUP/'Futura.ttc', 4),
    'D': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8),
    'E': (SUP/'Baskerville.ttc', 2),
}
PM = Path.home()/'.cache/absbyai/personmask/personmask'
WAIST = 0.78   # studio-blue-249: keeps the top of the olive shorts; frame bottom cuts mid-shorts
CUT = ROOT/'photos/finalized social media photos/_cutouts'
SHORTS = {
    # A/B/D/E: AI Dan (identity reference). C: real studio photo studio-blue-249 over a Codex gym plate.
    'ds76': dict(slug='ds-76_pull-ups', copy=['How To Do', 'Pull-Ups'],
                 cutout='studio-blue-249', waist=WAIST),
}

# Source crop boxes (x0, y0, x1, y1) on the 941x1672 Codex plate.
# F/G/H (Dan, 2026-10-29): touched-up real screenshots; each borrows a headline style from round 1.
STYLE = {'F': 'A', 'G': 'B', 'H': 'C'}
LETTERS = 'ABCDEFGH'

ZOOM = {'A': (94, 300, 847, 1639)}   # A: Codex framed him small; zoom so face and abs read on a phone

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def font(k, size):
    p, i = FONTS[k]
    return ImageFont.truetype(str(p), size, index=i)

def fit(k, word, size, width):
    for n in range(size, 39, -1):
        f = font(k, n)
        b = f.getbbox(word)
        if b[2]-b[0] <= width:
            return f
    raise ValueError(word)

def title(im, mask, k, platform, copy):
    k = STYLE.get(k, k)
    y = 260 if platform == 'instagram' else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    if k == 'D':
        # Dan's approved bottom-title format: large picture, no eyebrow, three balanced lines.
        lines=['How To Do','Pull-Ups']; limit=1640 if platform=='instagram' else 1800
        sizes=[200,250] if platform=='instagram' else [215,270]
        fs=[fit(k,line,size,990) for line,size in zip(lines,sizes)]
        heights=[f.getbbox(line,anchor='mt',stroke_width=4)[3] for f,line in zip(fs,lines)]
        yy=limit-sum(heights)-28
        start=yy
        a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,10,18]
        for row in range(H):a[row,:,3]=round(248*min(1,max(0,(row-(start-180))/240)))
        im.alpha_composite(Image.fromarray(a));bounds=[]
        for i,(line,f,height) in enumerate(zip(lines,fs,heights)):
            box=f.getbbox(line,anchor='mt',stroke_width=4)
            draw.text((W//2,yy),line,font=f,anchor='mt',fill='#49E4EF' if i==1 else 'white',stroke_width=4,stroke_fill='#05101B')
            md.text((W//2,yy),line,font=f,anchor='mt',fill=255,stroke_width=4)
            bounds.append([W//2+box[0],yy+box[1],W//2+box[2],yy+box[3]])
            yy+=height+14
        return bounds
    if k == 'A':
        draw.rectangle((0, y-24, W, y+330), fill='#FFD400')
        size, spacing, colors = 190, 152, ['#111318', '#BB1E1E']
    elif k == 'B':
        size, spacing, colors = 156, 155, ['#FFFFFF', '#49E4EF']
    elif k == 'C':
        draw.rounded_rectangle((36, y-25, W-36, y+315), radius=12, fill='#0B3171')
        size, spacing, colors = 130, 145, ['#FFFFFF', '#E3F778']
    elif k == 'D':
        draw.polygon([(0, y-30), (W, y-30), (W, y+295), (0, y+345)], fill='#F6F5EE')
        draw.rectangle((48, y+24, 61, y+269), fill='#D52626')
        size, spacing, colors = 156, 140, ['#171C24', '#C82025']
    else:
        size, spacing, colors = 148, 148, ['#FFFFFF', '#E9C171']
        draw.line((100, y-20, W-100, y-20), fill='#C8A463', width=4)
        draw.line((100, y+312, W-100, y+312), fill='#C8A463', width=4)
    bounds = []
    for i, word in enumerate(copy):
        f = fit(k, word, size, 920 if k in 'CD' else 950)
        box = f.getbbox(word, anchor='mt')
        xx = W//2 + (20 if k == 'D' else 0); yy = y+i*spacing
        stroke = 4 if k == 'B' else 0
        draw.text((xx, yy), word, font=f, anchor='mt', fill=colors[i], stroke_width=stroke, stroke_fill='#071322')
        md.text((xx, yy), word, font=f, anchor='mt', fill=255, stroke_width=stroke)
        bounds.append([xx+box[0]-stroke, yy+box[1]-stroke, xx+box[2]+stroke, yy+box[3]+stroke])
    return bounds

def person_top(im):
    with tempfile.TemporaryDirectory(prefix='ds76-cover-') as temp:
        inp = Path(temp)/'picture.png'; mp = Path(temp)/'mask.png'; im.convert('RGB').save(inp)
        subprocess.run([str(PM), str(inp), str(mp)], capture_output=True, text=True, check=True)
        person = np.array(Image.open(mp)) > 127
    rows = np.where(person.any(axis=1))[0]
    return int(rows.min()) if len(rows) else H

def picture(key, k, platform):
    spec = SHORTS[key]
    plate = SRC/f'{k}.png'
    src = Image.open(plate).convert('RGB')
    if k in ZOOM:
        src = src.crop(ZOOM[k])   # E: Codex framed him too small; zoom so the abs read on a phone
    im = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    info = {'plate': str(plate.relative_to(ROOT)), 'plate_sha256': sha(plate)}
    if k == 'D':
        big=im.resize((round(W*1.12),round(H*1.12)),Image.Resampling.LANCZOS)
        xx=(big.width-W)//2
        im=big.crop((xx,0,xx+W,H))
        if platform=='instagram':
            # Profile's 3:4 crop starts at row 240. Keep all hair inside it.
            sh=150
            shifted=Image.new('RGBA',(W,H),(34,42,49,255))
            shifted.alpha_composite(im.crop((0,0,W,H-sh)),(0,sh))
            im=shifted
    if platform == 'youtube' and k not in 'CDF':   # F: keep the bar and his hands below the band
        # Drop the Instagram reserve while keeping the complete lower picture.
        im = im.crop((0, 145, W, H)).resize((W, H), Image.Resampling.LANCZOS)
    s = STYLE.get(k, k)
    if s in 'BE':
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = [5, 13, 26]
        fade = 850 if s == 'B' else 560   # E's zoomed face sits higher; keep it out of the fade
        for y in range(fade):
            a[y, :, 3] = int(220*max(0, 1-y/fade))
        if k == 'E':
            # Bright sky: hold a solid navy band behind the gold serif, then fade out above the bar.
            for y in range(700):
                a[y, :, 3] = 238 if y < 470 else int(238*(1-(y-470)/230))
        im.alpha_composite(Image.fromarray(a))
    if k == 'C':
        p = CUT/f"{spec['cutout']}_CUTOUT.png"
        raw = Image.open(p).convert('RGBA'); b = raw.getchannel('A').getbbox(); b=(b[0],b[1],b[2],min(b[3],round(raw.height*spec['waist'])))
        sub = raw.crop(b)
        top = 650 if platform == 'instagram' else 480
        scale = (H-top+60)/sub.height
        sub = sub.resize((round(sub.width*scale), round(sub.height*scale)), Image.Resampling.LANCZOS)
        pad = 20; layer = Image.new('RGBA', (sub.width+2*pad, sub.height+2*pad)); layer.alpha_composite(sub, (pad, pad))
        x = W-sub.width-30-pad; y = top-pad
        line = Image.new('RGBA', layer.size, 'white'); line.putalpha(layer.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line, (x, y)); im.alpha_composite(layer, (x, y))
        info.update(real_photo=True, source=str(p.relative_to(ROOT)), source_sha256=sha(p),
                    source_person_pixels_preserved=True, source_crop=list(b), scale=scale, subject_top=top)
    else:
        # Keep the whole headline panel clear of actual hair, not just the glyphs.
        top = person_top(im)
        target = (260 if platform == 'instagram' else 90)+({'D': 0, 'E': 340, 'B': 330}.get(s, 355) + (60 if k == 'F' else 0))   # F: the bar sits just above his hair
        shift = 0 if k=='D' else max(0, target-top)
        if shift:
            color = tuple(int(v) for v in np.array(im.convert('RGB'))[:40].reshape(-1, 3).mean(axis=0))
            if k == 'F':
                color = (10, 12, 16)   # F's top rows are the grey bar: a flat grey strip read as a mistake
            shifted = Image.new('RGBA', (W, H), color+(255,)); shifted.alpha_composite(im.crop((0, 0, W, H-shift)), (0, shift)); im = shifted
            # Feather the join so the moved picture has no hard top edge.
            f = np.zeros((H, W, 4), np.uint8); f[:, :, :3] = color
            L = max(1, min(160, top-30))   # stop above his hair (it now starts at top+shift)
            for yy in range(shift, min(H, shift+L)):
                f[yy, :, 3] = int(255*(1-(yy-shift)/L))
            im.alpha_composite(Image.fromarray(f))
        info.update(source_person_top=top, picture_shift=shift, minimum_subject_top=target)
    return im, info

def build(keys):
    for key in keys:
        spec = SHORTS[key]; rows = []
        for k in LETTERS:
            if not (SRC/f'{k}.png').exists():
                print('missing plate', key, k); continue
            for platform in ['instagram', 'youtube']:
                d = OUT/key/platform; d.mkdir(parents=True, exist_ok=True)
                im, info = picture(key, k, platform)
                p = d/f"{spec['slug']}_cover-{k}.png"
                im.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
                mask = Image.new('L', (W, H)); bounds = title(im, mask, k, platform, spec['copy'])
                assert all(30 <= b[0] < b[2] <= W-30 for b in bounds), bounds
                assert all((200 if platform == 'instagram' else 50) <= b[1] < b[3] <= (1680 if platform=='instagram' else 1850) for b in bounds), bounds
                if k == 'E':
                    ImageDraw.Draw(im).rectangle((22, 22, W-23, H-23), outline='#B5975A', width=4)
                im.convert('RGB').save(p)
                if platform == 'youtube':
                    j = p.with_suffix('.jpg'); im.convert('RGB').save(j, quality=92)
                    assert j.stat().st_size < 2_000_000
                    info.update(jpeg_path=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
                mask.save(d/f"{spec['slug']}_cover-{k}.text-mask.png")
                rows.append(dict(letter=k, platform=platform, path=str(p.relative_to(ROOT)), sha256=sha(p), text_bounds=bounds, **info))
        (OUT/key/'manifest.json').write_text(json.dumps({'status': 'awaiting Dan pick', 'copy': spec['copy'], 'outputs': rows}, indent=2))
        sheet = Image.new('RGB', (len(LETTERS)*300, 2*565), '#101722'); dr = ImageDraw.Draw(sheet)
        label = ImageFont.truetype(str(SUP/'Arial Bold.ttf'), 24)
        for row in rows:
            x = LETTERS.index(row['letter'])*300; y = 0 if row['platform'] == 'instagram' else 565
            dr.text((x+12, y+14), row['letter']+' / '+('Instagram' if y == 0 else 'YouTube'), font=label, fill='white')
            im = Image.open(ROOT/row['path']); im.thumbnail((280, 500)); sheet.paste(im, (x+10, y+52))
        sheet.save(OUT/key/'five-cover-choices.jpg', quality=95)
        print(f'{key}: built {len(rows)} covers and review sheet')

if __name__ == '__main__':
    build(sys.argv[1:] or list(SHORTS))
