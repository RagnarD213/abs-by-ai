"""RO-37 round 3: Dan's pick C (touched-up shoulder press screenshot) with new copy, three text treatments.
Usage: build.py [V1 V2 V3]"""
from pathlib import Path
import json, hashlib, subprocess, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import distance_transform_edt

P = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
O = P / 'social media graphics/youtube/thumbnails/First Time At The Gym'
SRC = O / '_build-2026-11-02-r2/assets/R1.png'
B = O / '_build-2026-11-02-r3'
OUT = B / 'designs'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
PM = Path.home() / '.cache/absbyai/personmask/personmask'
ANTON = Path.home() / 'Library/Fonts/_dl/Anton-Regular.ttf'
MANROPE = Path.home() / 'Library/Fonts/Manrope.ttf'
L1, L2 = 'First Time At The Gym?', "Here's What To Do"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def font(path, n):
    f = ImageFont.truetype(str(path), n)
    if path == MANROPE:
        f.set_variation_by_name('ExtraBold')
    return f


def fit(path, text, size, maxw):
    while True:
        f = font(path, size)
        b = f.getbbox(text)
        if b[2] - b[0] <= maxw:
            return f, b
        size -= 1


def layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def top_dark(im, depth, strength, rgb=(4, 8, 18)):
    o = np.zeros((H, W, 4), dtype=np.uint8)
    o[:, :, :3] = rgb
    o[:, :, 3] = (strength * np.clip((depth - np.arange(H)) / depth, 0, 1) ** 0.8)[:, None].astype(np.uint8)
    return Image.alpha_composite(im, Image.fromarray(o))


def text_layer(path, text, size, maxw, cy, fill, stroke=0, stroke_fill='#000000', cx=W // 2):
    f, b = fit(path, text, size, maxw)
    w, h = b[2] - b[0], b[3] - b[1]
    x, y = cx - w // 2 - b[0], cy - h // 2 - b[1]
    L = layer()
    ImageDraw.Draw(L).text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return L, (cx - w // 2 - stroke, cy - h // 2 - stroke, cx + w // 2 + stroke, cy + h // 2 + stroke)


def shadow(L, blur, offset=(0, 0), alpha=200, color=(0, 0, 0)):
    a = L.getchannel('A').filter(ImageFilter.GaussianBlur(blur))
    a = a.point(lambda v: min(255, int(v * alpha / 255 * 1.6)))
    S = Image.new('RGBA', (W, H), color + (0,))
    S.putalpha(a)
    out = layer()
    out.alpha_composite(S, offset if offset[0] >= 0 and offset[1] >= 0 else (0, 0))
    return out


def glow(L, color, radii=(4, 12, 28), gain=(1.6, 1.2, 0.9)):
    out = layer()
    for r, g in zip(radii, gain):
        a = L.getchannel('A').filter(ImageFilter.GaussianBlur(r)).point(lambda v, g=g: min(255, int(v * g)))
        G = Image.new('RGBA', (W, H), color + (0,))
        G.putalpha(a)
        out = Image.alpha_composite(out, G)
    return out


def base():
    return ImageOps.fit(Image.open(SRC).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')


def v1():
    """White Anton headline with deep shadow, then a tilted yellow tag carrying the payoff."""
    im = top_dark(base(), 330, 225)
    boxes = []
    t1, r1 = text_layer(ANTON, L1, 112, 1180, 70, '#FFFFFF', stroke=3, stroke_fill='#0B0B0B')
    im = Image.alpha_composite(im, shadow(t1, 10, alpha=230))
    im = Image.alpha_composite(im, t1)
    boxes.append(r1)
    f, b = fit(ANTON, L2, 76, 760)
    w, h = b[2] - b[0], b[3] - b[1]
    tag = Image.new('RGBA', (w + 80, h + 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(tag)
    d.polygon([(18, 0), (w + 80, 0), (w + 62, h + 34), (0, h + 34)], fill='#FFD400')
    d.text((40 - b[0], 17 - b[1]), L2, font=f, fill='#0A0A0A')
    tag = tag.rotate(-2, resample=Image.Resampling.BICUBIC, expand=True)
    T = layer()
    tx, ty = W // 2 - tag.width // 2, 136
    T.alpha_composite(tag, (tx, ty))
    im = Image.alpha_composite(im, shadow(T, 8, alpha=200))
    im = Image.alpha_composite(im, T)
    boxes.append((tx, ty, tx + tag.width, ty + tag.height))
    return im, boxes


def v2():
    """Small red label for the question, huge yellow 3D payoff line underneath."""
    im = top_dark(base(), 340, 230)
    boxes = []
    f, b = fit(MANROPE, L1, 50, 900)
    w, h = b[2] - b[0], b[3] - b[1]
    x0, y0 = W // 2 - w // 2 - 26, 18
    P_ = layer()
    ImageDraw.Draw(P_).rounded_rectangle((x0, y0, x0 + w + 52, y0 + h + 28), radius=14, fill='#E01B1B')
    ImageDraw.Draw(P_).text((x0 + 26 - b[0], y0 + 14 - b[1]), L1, font=f, fill='#FFFFFF')
    im = Image.alpha_composite(im, shadow(P_, 8, alpha=180))
    im = Image.alpha_composite(im, P_)
    boxes.append((x0, y0, x0 + w + 52, y0 + h + 28))
    t2, r2 = text_layer(ANTON, L2, 146, 1200, 172, '#FFD400', stroke=6, stroke_fill='#0A0A0A')
    ext = layer()  # extrusion: stacked darker copies down-right
    dark, _ = text_layer(ANTON, L2, 146, 1200, 172, '#7A4A00', stroke=6, stroke_fill='#0A0A0A')
    for i in range(1, 9):
        ext.alpha_composite(dark, (i, i))
    im = Image.alpha_composite(im, shadow(ext, 12, alpha=220))
    im = Image.alpha_composite(im, ext)
    im = Image.alpha_composite(im, t2)
    boxes.append((r2[0], r2[1], r2[2] + 8, r2[3] + 8))
    return im, boxes


def v3():
    """A neon sign hanging from the gym ceiling: white question, yellow payoff, cyan glow."""
    im = top_dark(base(), 330, 200)
    boxes = []
    px0, py0, px1, py1 = 92, 22, 1188, 248
    S = layer()
    d = ImageDraw.Draw(S)
    for x in (px0 + 120, px1 - 120):  # hanging wires up to the ceiling
        d.line((x, 0, x, py0), fill=(150, 160, 175, 200), width=2)
    d.rounded_rectangle((px0, py0, px1, py1), radius=18, fill=(8, 12, 22, 215), outline=(90, 110, 140, 200), width=2)
    im = Image.alpha_composite(im, shadow(S, 14, alpha=160))
    im = Image.alpha_composite(im, S)
    boxes.append((px0, py0, px1, py1))
    t1, _ = text_layer(MANROPE, L1, 86, 1020, 84, '#F4FBFF')
    t2, _ = text_layer(ANTON, L2, 108, 960, 186, '#FFE36A')
    im = Image.alpha_composite(im, glow(t1, (40, 200, 255)))
    im = Image.alpha_composite(im, t1)
    im = Image.alpha_composite(im, glow(t2, (255, 170, 20)))
    im = Image.alpha_composite(im, t2)
    return im, boxes


def build(k):
    im, boxes = {'V1': v1, 'V2': v2, 'V3': v3}[k]()
    out = OUT / f'RO37-C-{k}.jpg'
    im.convert('RGB').save(out, quality=95, subsampling=0)
    pp = B / f'picture-{k}.jpg'
    base().convert('RGB').save(pp, quality=98)
    mp = B / f'person-{k}.png'
    subprocess.run([str(PM), str(pp), str(mp)], check=True, capture_output=True)
    person = np.array(Image.open(mp).convert('L').resize((W, H))) > 100
    tm = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in boxes:
        tm[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)] = True
    overlap = int((tm & person).sum())
    clear = float(distance_transform_edt(~person)[tm].min())
    r = dict(design=k, file=out.name, sha256=sha(out), bytes=out.stat().st_size, person_text_overlap_pixels=overlap,
             minimum_person_text_clearance_px=round(clear, 2), text_boxes=[list(map(int, b)) for b in boxes])
    print(json.dumps({x: r[x] for x in ('design', 'bytes', 'person_text_overlap_pixels', 'minimum_person_text_clearance_px')}), flush=True)
    return r


if __name__ == '__main__':
    res = [build(k) for k in (sys.argv[1:] or ['V1', 'V2', 'V3'])]
    (B / 'qc.json').write_text(json.dumps(res, indent=2) + '\n')
