#!/usr/bin/env python3
"""DS-19 X8 (design H) text revision, 2026-11-02.

Dan picked X8 for How To Use Battle Ropes but the title straddled the dark ceiling and the grey wall.
Same picture, three title treatments, every line held inside the dark ceiling band with a clear margin
above the wall edge. The picture moves down so the band is tall enough for a bigger title.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, subprocess
import numpy as np
from build import OUT, ROOT, PM, W, H, SUP, sha

KEY = 'ds19'
PLATE = OUT/KEY/'sources'/'H.png'
DEST = OUT/KEY/'x8-text-r2'
AVENIR = Path('/System/Library/Fonts/Avenir Next Condensed.ttc')
EDGE_MARGIN = 45            # clear dark between the lowest glyph and the wall edge
TOP = {'instagram': 270, 'youtube': 95}
EDGE = {'instagram': 660, 'youtube': 500}   # target wall-edge row per platform

def f(path, size, index=0):
    from PIL import ImageFont
    return ImageFont.truetype(str(path), size, index=index)

def fit(path, index, word, size, width):
    for n in range(size, 39, -1):
        fo = f(path, n, index); b = fo.getbbox(word)
        if b[2]-b[0] <= width:
            return fo
    raise ValueError(word)

def scaled_plate():
    src = Image.open(PLATE).convert('RGB')
    s = W/src.width
    return src.resize((W, round(src.height*s)), Image.Resampling.LANCZOS)

def wall_edge(im):
    a = np.array(im.convert('L')).astype(float).mean(axis=1)
    return int(np.argmax(a[:900] > 25))   # first row of the grey wall below the near-black ceiling

def picture(platform):
    pl = scaled_plate(); edge = wall_edge(pl)
    shift = max(0, EDGE[platform]-edge)
    ceiling = tuple(int(v) for v in np.array(pl)[:40].reshape(-1, 3).mean(axis=0))
    im = Image.new('RGB', (W, H), ceiling); im.paste(pl.crop((0, 0, W, H-shift)), (0, shift))
    return im.convert('RGBA'), dict(plate=str(PLATE.relative_to(ROOT)), plate_sha256=sha(PLATE),
                                    plate_wall_edge=edge, picture_shift=shift, wall_edge=edge+shift)

def draw_lines(im, mask, lines, top, gap):
    """lines: (text, font, fill, stroke). Centred, stacked from top."""
    d, md = ImageDraw.Draw(im), ImageDraw.Draw(mask); y = top; bounds = []
    for text, fo, fill, stroke in lines:
        b = fo.getbbox(text, anchor='mt', stroke_width=stroke)
        d.text((W//2, y-b[1]), text, font=fo, anchor='mt', fill=fill, stroke_width=stroke, stroke_fill='#05080D')
        md.text((W//2, y-b[1]), text, font=fo, anchor='mt', fill=255, stroke_width=stroke)
        bounds.append([W//2+b[0], y, W//2+b[2], y+b[3]-b[1]]); y += b[3]-b[1]+gap
    return bounds

def variant(v, im, mask, platform, room):
    """room: pixels between TOP and the wall edge minus margin."""
    top = TOP[platform]; k = 1.0 if platform == 'instagram' else 0.92
    if v == 'V1':
        # X8's own look, bigger and fully in the dark: Impact, white over lime.
        a = fit(SUP/'Impact.ttf', 0, 'How To Use', round(150*k), 900)
        b = fit(SUP/'Impact.ttf', 0, 'Battle Ropes', round(190*k), 990)
        lines = [('How To Use', a, 'white', 0), ('Battle Ropes', b, '#BDEF63', 0)]; gap = 22
    elif v == 'V2':
        # Small lime kicker over one huge white line.
        a = fit(AVENIR, 8, 'How To Use', round(104*k), 700)
        b = fit(SUP/'DIN Condensed Bold.ttf', 0, 'Battle Ropes', round(250*k), 1000)
        lines = [('How To Use', a, '#BDEF63', 0), ('Battle Ropes', b, 'white', 0)]; gap = 18
    else:
        # Lime block with near-black type, the block itself inside the dark band.
        a = fit(SUP/'Impact.ttf', 0, 'How To Use', round(120*k), 820)
        b = fit(SUP/'Impact.ttf', 0, 'Battle Ropes', round(165*k), 880)
        hb = sum(fo.getbbox(t)[3]-fo.getbbox(t)[1] for t, fo in [('How To Use', a), ('Battle Ropes', b)])+20
        pad = 34; y0 = top; y1 = top+hb+2*pad
        ImageDraw.Draw(im).rounded_rectangle((70, y0, W-70, y1), radius=18, fill='#BDEF63')
        ImageDraw.Draw(mask).rounded_rectangle((70, y0, W-70, y1), radius=18, fill=255)
        bounds = draw_lines(im, Image.new('L', (W, H)), [('How To Use', a, '#0B0F14', 0), ('Battle Ropes', b, '#0B0F14', 0)], y0+pad, 20)
        return [[70, y0, W-70, y1]] + bounds
    bounds = draw_lines(im, mask, lines, top, gap)
    return bounds

def main():
    rows = []
    for platform in ['instagram', 'youtube']:
        base, info = picture(platform)
        for v in ['V1', 'V2', 'V3']:
            d = DEST/platform; d.mkdir(parents=True, exist_ok=True)
            p = d/f'ds-19_battle-ropes_cover-X8-{v}.png'
            im = base.copy(); im.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
            mask = Image.new('L', (W, H)); bounds = variant(v, im, mask, platform, None)
            low = max(b[3] for b in bounds)
            assert low <= info['wall_edge']-EDGE_MARGIN, (v, platform, low, info['wall_edge'])
            assert all(30 <= b[0] and b[2] <= W-30 for b in bounds), bounds
            im.convert('RGB').save(p); mask.save(p.with_name(p.stem+'.text-mask.png'))
            row = dict(variant=v, platform=platform, path=str(p.relative_to(ROOT)), sha256=sha(p), text_bounds=bounds,
                       lowest_text=low, clear_dark_below_text=info['wall_edge']-low, **info)
            if platform == 'youtube':
                j = p.with_suffix('.jpg'); im.convert('RGB').save(j, quality=92); assert j.stat().st_size < 2_000_000
                row.update(jpeg_path=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
            # Face and person checks on the exact render.
            pic, pm = p.with_name(p.stem+'.picture.png'), p.with_name(p.stem+'.person-mask.png')
            faces = json.loads(subprocess.run([str(PM), str(pic), str(pm)], capture_output=True, text=True, check=True).stdout)['faces']
            person = np.array(Image.open(pm)) > 127; tm = np.array(mask) > 0
            row.update(faces=len(faces), text_person_pixels=int((person & tm).sum()),
                       person_top=int(np.where(person.any(axis=1))[0].min()))
            grid_ok = platform != 'instagram' or min(b[1] for b in bounds) >= 240
            row['passed'] = len(faces) == 1 and row['text_person_pixels'] == 0 and grid_ok
            if platform == 'instagram':
                im.convert('RGB').crop((0, 240, W, 1680)).resize((270, 360), Image.Resampling.LANCZOS).save(d/f'grid-{v}.jpg', quality=95)
            rows.append(row)
    (DEST/'manifest.json').write_text(json.dumps({'status': 'awaiting Dan pick of V1/V2/V3', 'picked_from': 'X8 (design H)', 'outputs': rows}, indent=2))
    sheet = Image.new('RGB', (3*360, 2*660), '#101722'); dr = ImageDraw.Draw(sheet)
    for r in rows:
        x = ['V1', 'V2', 'V3'].index(r['variant'])*360; y = 0 if r['platform'] == 'instagram' else 660
        dr.text((x+12, y+12), f"{r['variant']} / {r['platform']}", fill='white')
        t = Image.open(ROOT/r['path']); t.thumbnail((340, 605)); sheet.paste(t, (x+10, y+44))
    sheet.save(DEST/'sheet.jpg', quality=92)
    print(json.dumps([{k: r[k] for k in ['variant', 'platform', 'passed', 'faces', 'text_person_pixels', 'lowest_text', 'wall_edge', 'person_top']} for r in rows], indent=1))

if __name__ == '__main__':
    main()
