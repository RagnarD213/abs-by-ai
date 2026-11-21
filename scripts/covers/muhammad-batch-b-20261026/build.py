#!/usr/bin/env python3
"""Muhammad Shorts Batch B covers (DS-06, DS-10, DS-13), 2026-10-27. Adapted from the DS-55 builder.

AI plates come from generate.sh (codex-image.sh, GPT-6.1 Sol high). C composites a real studio cutout over a
Codex background plate; the person pixels are never redrawn. Same two-line copy per Short on all five designs;
only layout, type and colour change. Instagram keeps the title clear of the 4:5 grid crop; YouTube sits higher.

    python3 scripts/covers/muhammad-batch-b-20261026/build.py [ds06 ds10 ds13]
    python3 scripts/covers/muhammad-batch-b-20261026/build.py --r2      # Dan's 10-27 revisions of the picked A covers
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Short-form video content/covers/review/muhammad-batch-b-20261026'
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
CUT = ROOT/'photos/finalized social media photos/_cutouts'
SHORTS = {
    'ds06': dict(slug='ds-06_what-every-body-fat-percentage-looks-like', copy=['Every Body Fat %', 'Looks Like This'],
                 cutout='studio-blue-240', scale=True),
    'ds10': dict(slug='ds-10_3-unexpected-ways-zepbound-helped-me', copy=['3 Unexpected Ways', 'Zepbound Helped Me'],
                 cutout='studio-blue-249'),
    # Dan, 2026-10-27: A for all three. DS-06 A: poster higher, wider body-type range (Codex edit of the A plate).
    # DS-10 A: new title "Top 3 Non-Weight Loss Benefits Of Zepbound".
    'ds13': dict(slug='ds-13_the-1-change-i-made-to-get-abs-at-40', copy=['#1 Change I Made', 'For Abs At 40'],
                 cutout='studio-blue-213'),
}

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
    y = 260 if platform == 'instagram' else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
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
    with tempfile.TemporaryDirectory(prefix='mbb-cover-') as temp:
        inp = Path(temp)/'picture.png'; mp = Path(temp)/'mask.png'; im.convert('RGB').save(inp)
        subprocess.run([str(PM), str(inp), str(mp)], capture_output=True, text=True, check=True)
        person = np.array(Image.open(mp)) > 127
    rows = np.where(person.any(axis=1))[0]
    return int(rows.min()) if len(rows) else H

def body_fat_scale(im, platform):
    """DS-06 D: a vertical 30 to 10 percent ruler on the left, the marker on 10."""
    d = ImageDraw.Draw(im); f = font('D', 74)
    top = 760 if platform == 'instagram' else 640
    vals = ['30%', '25%', '20%', '15%', '10%']
    for i, v in enumerate(vals):
        yy = top + i*175
        lean = i == len(vals)-1
        if lean:
            d.rounded_rectangle((26, yy-52, 262, yy+52), radius=14, fill='#D52626')
        d.text((144, yy), v, font=f, anchor='mm', fill='#FFFFFF' if lean else '#171C24')
        if i < len(vals)-1:
            d.line((144, yy+50, 144, yy+125), fill='#171C24', width=5)

# ig_extra: the raised poster needs clearance under the Instagram title band.
R2 = {'ds06': dict(plate='ds06-A-r2-moved', ig_extra=60), 'ds10': dict(copy=['Top 3 Non-Weight Loss', 'Benefits Of Zepbound'])}

def picture(key, k, platform, plate_name=None, extra=0):
    spec = SHORTS[key]
    plate = SRC/f"{plate_name or f'{key}-{k}'}.png"
    im = ImageOps.fit(Image.open(plate).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    info = {'plate': str(plate.relative_to(ROOT)), 'plate_sha256': sha(plate)}
    if platform == 'youtube' and k != 'C':
        # Drop the Instagram reserve while keeping the complete lower picture.
        im = im.crop((0, 145, W, H)).resize((W, H), Image.Resampling.LANCZOS)
    if k in 'BE':
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = [5, 13, 26]
        for y in range(850):
            a[y, :, 3] = int(220*max(0, 1-y/850))
        im.alpha_composite(Image.fromarray(a))
    if k == 'C':
        p = CUT/f"{spec['cutout']}_CUTOUT.png"
        raw = Image.open(p).convert('RGBA'); b = raw.getchannel('A').getbbox(); sub = raw.crop(b)
        top = 650 if platform == 'instagram' else 480
        scale = min((780 if platform == 'instagram' else 860)/sub.width, (H-top-10)/sub.height)
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
        target = (260 if platform == 'instagram' else 90)+{'D': 365, 'E': 340, 'B': 330}.get(k, 355)
        shift = max(0, target-top, extra)   # extra: a minimum shift (raised DS-06 poster vs the title band)
        if shift:
            color = tuple(int(v) for v in np.array(im.convert('RGB'))[:40].reshape(-1, 3).mean(axis=0))
            shifted = Image.new('RGBA', (W, H), color+(255,)); shifted.alpha_composite(im.crop((0, 0, W, H-shift)), (0, shift)); im = shifted
        info.update(source_person_top=top, picture_shift=shift, minimum_subject_top=target)
    if k == 'D' and spec.get('scale'):
        body_fat_scale(im, platform)
    return im, info

def build(keys):
    for key in keys:
        spec = SHORTS[key]; rows = []
        for k in 'ABCDE':
            if not (SRC/f'{key}-{k}.png').exists():
                print('missing plate', key, k); continue
            for platform in ['instagram', 'youtube']:
                d = OUT/key/platform; d.mkdir(parents=True, exist_ok=True)
                im, info = picture(key, k, platform)
                p = d/f"{spec['slug']}_cover-{k}.png"
                mask = Image.new('L', (W, H)); bounds = title(im, mask, k, platform, spec['copy'])
                assert all(30 <= b[0] < b[2] <= W-30 for b in bounds), bounds
                assert all((200 if platform == 'instagram' else 50) <= b[1] < b[3] < 1620 for b in bounds), bounds
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
        sheet = Image.new('RGB', (5*300, 2*565), '#101722'); dr = ImageDraw.Draw(sheet)
        label = ImageFont.truetype(str(SUP/'Arial Bold.ttf'), 24)
        for row in rows:
            x = 'ABCDE'.index(row['letter'])*300; y = 0 if row['platform'] == 'instagram' else 565
            dr.text((x+12, y+14), row['letter']+' / '+('Instagram' if y == 0 else 'YouTube'), font=label, fill='white')
            im = Image.open(ROOT/row['path']); im.thumbnail((280, 500)); sheet.paste(im, (x+10, y+52))
        sheet.save(OUT/key/'five-cover-choices.jpg', quality=95)
        print(f'{key}: built {len(rows)} covers and review sheet')

def build_r2():
    """Revised A covers, saved beside the originals as _cover-A-r2 (originals untouched)."""
    for key, rev in R2.items():
        spec = SHORTS[key]; copy = rev.get('copy', spec['copy']); rows = []
        for platform in ['instagram', 'youtube']:
            d = OUT/key/platform
            im, info = picture(key, 'A', platform, rev.get('plate'), rev.get('ig_extra', 0) if platform == 'instagram' else 0)
            p = d/f"{spec['slug']}_cover-A-r2.png"
            mask = Image.new('L', (W, H)); bounds = title(im, mask, 'A', platform, copy)
            assert all(30 <= b[0] < b[2] <= W-30 for b in bounds), bounds
            im.convert('RGB').save(p)
            if platform == 'youtube':
                j = p.with_suffix('.jpg'); im.convert('RGB').save(j, quality=92)
                assert j.stat().st_size < 2_000_000
                info.update(jpeg_path=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
            rows.append(dict(letter='A-r2', platform=platform, path=str(p.relative_to(ROOT)), sha256=sha(p), copy=copy, text_bounds=bounds, **info))
        (OUT/key/'manifest-r2.json').write_text(json.dumps({'status': 'revised, awaiting Dan approval', 'outputs': rows}, indent=2))
        print(f'{key}: built A-r2 (Instagram + YouTube)')

if __name__ == '__main__':
    if '--r2' in sys.argv:
        build_r2()
    else:
        build(sys.argv[1:] or list(SHORTS))
