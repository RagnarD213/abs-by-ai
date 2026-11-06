#!/usr/bin/env python3
"""DS-77 T-Bar Rows, round 3 (Dan, 2026-11-06): four REAL touched-up screenshots, no AI anywhere.

Dan: "I want four touch-up screenshots, real images, not AI-generated."
Each cover is one real 4K frame from the finished Color C library clips, cropped to 9:16 and downscaled
(no upscaling), with photo-editing adjustments only: light denoise, exposure/contrast curve, local contrast
(CLAHE on lightness), a small saturation lift and an unsharp mask, applied to the whole frame. No generative
model, no inpainting, no extension: areas above or below the picture are flat colour blocks or a gradient.

    python3 scripts/covers/ds77-20261105/real_build.py
"""
from pathlib import Path
import hashlib, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'Short-form video content/covers/review/ds77-t-bar-rows-20261105'
LIB = Path('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed')
OUT = BASE/'ds77-real'; W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
COPY = ['How To Do', 'T-Bar Rows']

# label: frame file, source clip + time, crop x0 on the 3840x2160 frame (width 1215 = 9:16), design
DESIGNS = {
    'R1': dict(frame='real16-P.png', clip='B0723', t=5.0, x0=1350, style='yellow'),
    'R2': dict(frame='real16-Q.png', clip='B0724', t=1.75, x0=1300, style='cyan'),
    'R3': dict(frame='real16-S.png', clip='B0725', t=12.25, x0=1250, style='bottom'),
    'R4': dict(frame='real16-T.png', clip='B0725', t=5.0, x0=1560, style='plaque'),
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def touchup(rgb):
    """Photo-editing adjustments only, applied to every pixel the same way (float, from a 16-bit frame).
    Round 3b: no denoise and no tile-based contrast (they made the skin blotchy on the first pass)."""
    x = rgb.astype(np.float32)/65535.0
    x = np.power(x, 0.86)                                       # lift exposure (the gym footage is dark)
    x = np.clip(x + 0.10*(x-0.5)*(1-np.abs(2*x-1)), 0, 1)       # gentle S-curve
    lum = x.mean(axis=2, keepdims=True)
    x = np.clip(lum + (x-lum)*1.08, 0, 1)                       # saturation
    big = cv2.GaussianBlur(x, (0, 0), 30)
    x = np.clip(x + 0.30*(x-big), 0, 1)                         # clarity (wide, soft local contrast)
    fine = cv2.GaussianBlur(x, (0, 0), 1.2)
    x = np.clip(x + 0.40*(x-fine), 0, 1)                        # light sharpening
    return x

def to8(x):
    rng = np.random.default_rng(77)
    return np.clip(x*255 + rng.uniform(-0.5, 0.5, x.shape), 0, 255).astype(np.uint8)   # dither, no banding

def font(name, size, index=0):
    paths = {'din': SUP/'DIN Condensed Bold.ttf', 'impact': SUP/'Impact.ttf', 'futura': SUP/'Futura.ttc',
             'avenir': Path('/System/Library/Fonts/Avenir Next Condensed.ttc')}
    return ImageFont.truetype(str(paths[name]), size, index=index)

def fit(name, word, size, width, index=0):
    for n in range(size, 39, -1):
        f = font(name, n, index); b = f.getbbox(word)
        if b[2]-b[0] <= width: return f
    raise ValueError(word)

def lines(draw, y, spacing, fname, size, colors, width, index=0, stroke=0):
    bounds = []
    for i, word in enumerate(COPY):
        f = fit(fname, word, size, width, index); yy = y+i*spacing
        bx = f.getbbox(word, anchor='mt', stroke_width=stroke)
        draw.text((W//2, yy), word, font=f, anchor='mt', fill=colors[i], stroke_width=stroke, stroke_fill='#071322')
        bounds.append([W//2+bx[0], yy+bx[1], W//2+bx[2], yy+bx[3]])
    return bounds

def compose(photo, d, platform):
    top = 260 if platform == 'instagram' else 90          # Instagram keeps the title inside the 3:4 grid crop
    canvas = Image.new('RGB', (W, H), '#000000'); draw = ImageDraw.Draw(canvas)
    s = d['style']
    if s == 'bottom':
        # Picture fills the frame; a dark gradient at the bottom carries a large title.
        canvas.paste(photo, (0, 0))
        limit = 1640 if platform == 'instagram' else 1800
        g = np.zeros((H, W, 4), np.uint8); g[..., :3] = [4, 10, 18]
        start = limit-560
        for row in range(H): g[row, :, 3] = round(240*min(1, max(0, (row-start)/260)))
        canvas = Image.alpha_composite(canvas.convert('RGBA'), Image.fromarray(g)).convert('RGB'); draw = ImageDraw.Draw(canvas)
        fs = [fit('avenir', COPY[0], 210, 990, 8), fit('avenir', COPY[1], 260, 990, 8)]
        hs = [f.getbbox(w, anchor='mt', stroke_width=4)[3] for f, w in zip(fs, COPY)]
        yy = limit-sum(hs)-14; bounds = []
        for i, (w, f, h) in enumerate(zip(COPY, fs, hs)):
            bx = f.getbbox(w, anchor='mt', stroke_width=4)
            draw.text((W//2, yy), w, font=f, anchor='mt', fill='#49E4EF' if i else 'white', stroke_width=4, stroke_fill='#05101B')
            bounds.append([W//2+bx[0], yy+bx[1], W//2+bx[2], yy+bx[3]]); yy += h+14
        return canvas, bounds, 0
    # Top-block designs: a flat colour block holds the title; the real picture starts below it.
    if s == 'yellow':
        block = top+330; draw.rectangle((0, 0, W, block), fill='#0B0D10'); draw.rectangle((0, top-24, W, block), fill='#FFD400')
        bounds = lines(draw, top, 152, 'din', 190, ['#111318', '#BB1E1E'], 950)
    elif s == 'cyan':
        block = top+330; draw.rectangle((0, 0, W, block), fill='#07111F')
        bounds = lines(draw, top, 155, 'impact', 156, ['#FFFFFF', '#49E4EF'], 950, stroke=4)
    else:  # plaque
        block = top+345; draw.rectangle((0, 0, W, block), fill='#0A1A33')
        draw.rounded_rectangle((36, top-25, W-36, top+315), radius=12, fill='#0B3171', outline='#E3F778', width=3)
        bounds = lines(draw, top, 145, 'futura', 130, ['#FFFFFF', '#E3F778'], 920, index=4)
    canvas.paste(photo.crop((0, 0, W, H-block)), (0, block))
    draw.line((0, block, W, block), fill='#FFD400' if s == 'yellow' else '#49E4EF' if s == 'cyan' else '#E3F778', width=6)
    return canvas, bounds, block

def main():
    OUT.mkdir(parents=True, exist_ok=True); rows = []
    for label, d in DESIGNS.items():
        src = BASE/'frames'/d['frame']
        full = cv2.cvtColor(cv2.imread(str(src), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB); assert full.shape[:2] == (2160, 3840) and full.dtype == np.uint16, (full.shape, full.dtype)
        x0 = max(0, min(3840-1215, d['x0']))
        crop = full[:, x0:x0+1215]
        photo = Image.fromarray(to8(cv2.resize(touchup(crop), (W, H), interpolation=cv2.INTER_AREA)))   # 1215x2160 -> 1080x1920, downscale only
        for platform in ['instagram', 'youtube']:
            canvas, bounds, block = compose(photo, d, platform)
            p = OUT/platform/f'ds-77_t-bar-rows_real-{label}.png'; p.parent.mkdir(exist_ok=True)
            canvas.save(p); row = dict(label=label, platform=platform, path=str(p.relative_to(ROOT)), sha256=sha(p),
                                       source=f"{d['clip']} at {d['t']} s", source_frame=str(src.relative_to(ROOT)), source_frame_sha256=sha(src),
                                       crop_x0=x0, picture_top=block, text_bounds=bounds, ai_generated=False)
            if platform == 'youtube':
                j = p.with_suffix('.jpg'); canvas.save(j, quality=92); assert j.stat().st_size < 2_000_000
                row.update(jpeg=str(j.relative_to(ROOT)), jpeg_sha256=sha(j), jpeg_bytes=j.stat().st_size)
            rows.append(row)
    (OUT/'manifest.json').write_text(json.dumps(dict(status='awaiting Dan pick', round=3, copy=COPY, outputs=rows), indent=2))
    sheet = Image.new('RGB', (4*300, 2*560), '#101722'); dr = ImageDraw.Draw(sheet)
    for r in rows:
        x = list(DESIGNS).index(r['label'])*300; y = 0 if r['platform'] == 'instagram' else 560
        dr.text((x+10, y+10), f"{r['label']} {r['platform']}", fill='white')
        im = Image.open(ROOT/r['path']); im.thumbnail((280, 500)); sheet.paste(im, (x+10, y+45))
    sheet.save(OUT/'four-real.jpg', quality=95); print('built', len(rows))

if __name__ == '__main__':
    main()
