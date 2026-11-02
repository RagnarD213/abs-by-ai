#!/usr/bin/env python3
"""DS-52 cover layouts, 2026-11-02, adapted from the DS-49 builder.

Eight distinct images, paired Instagram and YouTube layouts, same title copy.
The real studio-blue-247 cutout preserves original person pixels. Sources and
private generation records live in the ignored review folder. Run build.py,
check.py, then review.py after registering and shuffling the blind set once.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Short-form video content/covers/review/ds52-zepbound-free-20261102'
SRC = OUT / 'sources'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
FONTS = {
    'A': (SUP/'DIN Condensed Bold.ttf', 0),
    'B': (SUP/'Impact.ttf', 0),
    'C': (SUP/'Futura.ttc', 4),
    'D': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8),
    'E': (SUP/'Baskerville.ttc', 2),
    'F': (SUP/'DIN Alternate Bold.ttf', 0),
    'G': (SUP/'Futura.ttc', 4),
    'H': (SUP/'Impact.ttf', 0),
}
PM = Path.home()/'.cache/absbyai/personmask/personmask'
CUT = ROOT/'photos/finalized social media photos/_cutouts'
SHORTS = {
    # C retains the real studio-blue-247 cutout over a generated backdrop.
    'ds52': dict(slug='ds-52_zepbound-free', copy=['Why Zepbound', 'Is Actually Free'],
                 cutout='studio-blue-247', waist=0.72),
}
LETTERS = 'ABCDEFGH'
# Every letter has its own design. Model provenance stays in the private records.
STYLE = {}
YT_ZOOM = {'A': 1.12, 'B': 1.10, 'E': 1.10, 'F': 1.10, 'G': 1.10, 'H': 1.10}
ZOOM = {}   # letter: (x0, y0, x1, y1) crop on the 941x1672 Codex plate when Codex frames him too small

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

D_LINES = ['Why Zepbound', 'Is Actually', 'Free']
D_BG = (4, 10, 18)

def d_layout(platform):
    limit = 1675 if platform == 'instagram' else 1800
    sizes = [122, 144, 136] if platform == 'instagram' else [170, 200, 190]
    fs = [fit('D', line, size, 990) for line, size in zip(D_LINES, sizes)]
    heights = [f.getbbox(line, anchor='mt', stroke_width=4)[3] for f, line in zip(fs, D_LINES)]
    return fs, heights, limit-sum(heights)-28

def title(im, mask, k, platform, copy):
    k = STYLE.get(k, k)
    y = 260 if platform == 'instagram' else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    if k == 'D':
        # Dan's approved bottom-title format: large picture, no eyebrow, three balanced lines.
        fs, heights, yy = d_layout(platform)
        bounds = []
        for i, (line, f, height) in enumerate(zip(D_LINES, fs, heights)):
            box = f.getbbox(line, anchor='mt', stroke_width=4)
            draw.text((W//2, yy), line, font=f, anchor='mt', fill='#49E4EF' if i == 2 else 'white', stroke_width=4, stroke_fill='#05101B')
            md.text((W//2, yy), line, font=f, anchor='mt', fill=255, stroke_width=4)
            bounds.append([W//2+box[0], yy+box[1], W//2+box[2], yy+box[3]])
            yy += height+14
        return bounds
    if k == 'A':
        draw.rectangle((0, y-24, W, y+330), fill='#FFD400')
        size, spacing, colors = 190, 152, ['#111318', '#BB1E1E']
    elif k == 'B':
        size, spacing, colors = 156, 155, ['#FFFFFF', '#49E4EF']
    elif k == 'C':
        draw.rounded_rectangle((36, y-25, W-36, y+315), radius=12, fill='#05372C')
        size, spacing, colors = 130, 145, ['#FFFFFF', '#E3F778']
    elif k == 'F':
        draw.rectangle((0,y-24,W,y+330),fill='#FF971F')
        size, spacing, colors=150,150,['#151617','#151617']
    elif k == 'G':
        draw.rectangle((0,y-24,W,y+330),fill='#143CBE')
        size, spacing, colors=134,145,['#FFFFFF','#D9EEFF']
    elif k == 'H':
        size, spacing, colors=150,150,['#FFFFFF','#BDEF63']
    else:
        size, spacing, colors = 142, 148, ['#531E16', '#A5271F']
        draw.line((100, y-20, W-100, y-20), fill='#C8A463', width=4)
        draw.line((100, y+312, W-100, y+312), fill='#C8A463', width=4)
    bounds = []
    for i, word in enumerate(copy):
        f = fit(k, word, size, 920 if k == 'C' else 950)
        box = f.getbbox(word, anchor='mt')
        xx = W//2; yy = y+i*spacing
        stroke = 4 if k == 'B' else 0
        draw.text((xx, yy), word, font=f, anchor='mt', fill=colors[i], stroke_width=stroke, stroke_fill='#071322')
        md.text((xx, yy), word, font=f, anchor='mt', fill=255, stroke_width=stroke)
        bounds.append([xx+box[0]-stroke, yy+box[1]-stroke, xx+box[2]+stroke, yy+box[3]+stroke])
    return bounds

def person_top(im):
    with tempfile.TemporaryDirectory(prefix='ds52-cover-') as temp:
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
        src = src.crop(ZOOM[k])
    im = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')
    info = {'plate': str(plate.relative_to(ROOT)), 'plate_sha256': sha(plate)}
    if k == 'D':
        # Keep the full torso above the bottom title; Instagram hair stays inside the profile crop.
        hair = 260 if platform == 'instagram' else 140
        B = d_layout(platform)[2]-10
        top = person_top(Image.fromarray(np.array(src)).convert('RGBA'))
        sc = W/src.width   # never narrower than the frame
        pic = src.resize((round(src.width*sc), round(src.height*sc)), Image.Resampling.LANCZOS)
        x0 = (pic.width-W)//2; yt = round(hair-top*sc)   # align actual hair to its measured target
        assert yt+top*sc >= (250 if platform == 'instagram' else 60), (platform, yt+top*sc)
        im = Image.new('RGBA', (W, H), D_BG+(255,))
        im.alpha_composite(pic.crop((x0, max(0, -yt), x0+W, max(0, -yt)+B-max(0, yt))).convert('RGBA'), (0, max(0, yt)))
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = D_BG
        for row in range(B-30, B): a[row, :, 3] = round(255*(row-(B-30))/30)
        im.alpha_composite(Image.fromarray(a))
        info.update(plate_person_top=top, scale=sc, picture_top=yt, picture_bottom=B)
    if platform == 'youtube' and k in YT_ZOOM:
        # YouTube shows the whole frame: zoom in so Dan fills the space the Instagram grid reserve left empty.
        f = YT_ZOOM[k]; top0 = person_top(im); target = 90+{'E': 340, 'B': 330}.get(k, 355)
        off = min(H*(1-1/f), max(0, top0-target/f)); cw = W/f
        im = im.crop((round(W/2-cw/2), round(off), round(W/2+cw/2), round(off+H/f))).resize((W, H), Image.Resampling.LANCZOS)
        info.update(youtube_zoom=f, youtube_zoom_offset=round(off))
    if k in 'BEH':
        a = np.zeros((H, W, 4), np.uint8); a[:, :, :3] = [244, 233, 211] if k == 'E' else [5,13,26]
        fade = 850 if k == 'B' else 700
        for y in range(fade):
            a[y, :, 3] = int(220*max(0, 1-y/fade))
        if k == 'E':
            # Hold a solid navy band behind the gold serif, then fade out above his hair.
            end = min(700 if platform == 'instagram' else 450, person_top(im)-35); solid = max(0,end-100)   # YouTube: zoomed face starts ~450
            a[:, :, 3] = 0
            for y in range(end):
                a[y, :, 3] = 238 if y < solid else int(238*(1-(y-solid)/(end-solid)))
        im.alpha_composite(Image.fromarray(a))
    if k == 'C':
        p = CUT/f"{spec['cutout']}_CUTOUT.png"
        raw = Image.open(p).convert('RGBA'); b = raw.getchannel('A').getbbox(); b = (b[0], b[1], b[2], min(b[3], round(raw.height*spec['waist'])))
        sub = raw.crop(b)
        top = 650 if platform == 'instagram' else 480
        scale = (H-top+60)/sub.height
        sub = sub.resize((round(sub.width*scale), round(sub.height*scale)), Image.Resampling.LANCZOS)
        pad = 20; layer = Image.new('RGBA', (sub.width+2*pad, sub.height+2*pad)); layer.alpha_composite(sub, (pad, pad))
        x = (W-sub.width)//2-pad; y = top-pad
        line = Image.new('RGBA', layer.size, 'white'); line.putalpha(layer.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line, (x, y)); im.alpha_composite(layer, (x, y))
        info.update(real_photo=True, source=str(p.relative_to(ROOT)), source_sha256=sha(p),
                    source_person_pixels_preserved=True, source_crop=list(b), scale=scale, subject_top=top)
    elif k != 'D':
        # Keep the whole headline panel clear of actual hair, not just the glyphs.
        top = person_top(im)
        target = (260 if platform == 'instagram' else 90)+{'E': 340, 'B': 330}.get(k, 355)
        shift = max(0, target-top)
        if shift:
            color = tuple(int(v) for v in np.array(im.convert('RGB'))[:40].reshape(-1, 3).mean(axis=0))
            shifted = Image.new('RGBA', (W, H), color+(255,)); shifted.alpha_composite(im.crop((0, 0, W, H-shift)), (0, shift)); im = shifted
            # Feather the join so the moved picture has no hard top edge.
            f = np.zeros((H, W, 4), np.uint8); f[:, :, :3] = color
            L = max(1, min(160, top-30))
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
                assert all((200 if platform == 'instagram' else 50) <= b[1] < b[3] <= (1680 if platform == 'instagram' else 1850) for b in bounds), bounds
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
