#!/usr/bin/env python3
"""Build Play Store assets: 9:16 padded phone screenshots + 1024x500 feature graphic."""
import os
from PIL import Image, ImageDraw, ImageFont

SC = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(SC, 'shots')
OUT = os.path.join(SC, 'play')
PROJ = '/Users/danielrose/Documents/Claude/Projects/Abs By AI'
os.makedirs(OUT, exist_ok=True)

BG = (246, 245, 242)
INK = (26, 26, 24)

# Play requires 16:9 or 9:16. Source is 1080x2400 (20:9), so pad width to 1350.
ORDER = [
    ('03-transformations.png', '01-before-after.png'),
    ('01-upload.png',          '02-upload.png'),
    ('02-daily-brief.png',     '03-daily-brief.png'),
    ('04-features.png',        '04-everything-included.png'),
    ('05-trainer.png',         '05-ai-trainer.png'),
    ('06-nutritionist.png',    '06-ai-nutritionist.png'),
]

for src, dst in ORDER:
    im = Image.open(os.path.join(SHOTS, src)).convert('RGB')
    w, h = im.size
    target_w = round(h * 9 / 16)
    canvas = Image.new('RGB', (target_w, h), BG)
    canvas.paste(im, ((target_w - w) // 2, 0))
    canvas.save(os.path.join(OUT, dst), 'PNG', optimize=True)
    kb = os.path.getsize(os.path.join(OUT, dst)) / 1024
    print(f'{dst}: {canvas.size[0]}x{canvas.size[1]} ratio={canvas.size[0]/canvas.size[1]:.4f} {kb:.0f}KB')

# ---- Feature graphic: 1024x500 ----
FW, FH = 1024, 500
fg = Image.new('RGB', (FW, FH), BG)
d = ImageDraw.Draw(fg)

def font(sz, bold=True):
    p = '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'
    return ImageFont.truetype(p, sz)

# Right side: before/after pair from the real proof assets.
pair_h = 360
gap = 12
pad_r = 40
imgs = []
for name in ('male2-before.webp', 'male2-after.webp'):
    p = Image.open(os.path.join(PROJ, 'public/img/proof', name)).convert('RGB')
    ratio = pair_h / p.size[1]
    nw = int(p.size[0] * ratio)
    imgs.append(p.resize((nw, pair_h), Image.LANCZOS))

pair_w = imgs[0].size[0] + gap + imgs[1].size[0]
# Cap the pair so text keeps room.
max_pair_w = 420
if pair_w > max_pair_w:
    k = max_pair_w / pair_w
    pair_h = int(pair_h * k)
    imgs = [i.resize((int(i.size[0] * k), pair_h), Image.LANCZOS) for i in imgs]
    pair_w = imgs[0].size[0] + gap + imgs[1].size[0]

px = FW - pad_r - pair_w
py = (FH - pair_h) // 2

def rounded(img, r=16):
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=r, fill=255)
    out = Image.new('RGB', img.size, BG)
    out.paste(img, (0, 0), mask)
    return out

fg.paste(rounded(imgs[0]), (px, py))
fg.paste(rounded(imgs[1]), (px + imgs[0].size[0] + gap, py))

# Labels on each panel
lf = font(19)
for i, (label, fill, txtcol) in enumerate([('BEFORE', (0, 0, 0), (255, 255, 255)), ('AFTER', (43, 90, 235), (255, 255, 255))]):
    ox = px if i == 0 else px + imgs[0].size[0] + gap
    bb = d.textbbox((0, 0), label, font=lf)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    bx, by = ox + 12, py + pair_h - th - 26
    d.rounded_rectangle([bx, by, bx + tw + 22, by + th + 16], radius=11, fill=fill)
    d.text((bx + 11, by + 7), label, font=lf, fill=txtcol)

# Left side: logo mark + wordmark + tagline
pad_l = 56
mark = Image.open(os.path.join(PROJ, 'public/img/icon-512.png')).convert('RGBA')
mark_sz = 78
mark = mark.resize((mark_sz, mark_sz), Image.LANCZOS)
top = 96
fg.paste(mark, (pad_l - 8, top), mark)

d.text((pad_l + mark_sz + 4, top + 16), 'Abs by AI', font=font(50), fill=INK)

lines = ['See yourself with abs.', 'Then get the AI plan', 'to make it real.']
y = top + mark_sz + 34
tf = font(34)
for ln in lines:
    d.text((pad_l, y), ln, font=tf, fill=INK)
    y += 46

# AI disclosure under the pair — matches the labelling used on the site and in ads.
df = font(17, bold=False)
disc = 'AI-generated example — not a real transformation'
db = d.textbbox((0, 0), disc, font=df)
d.text((px + (pair_w - (db[2]-db[0])) // 2, py + pair_h + 14), disc, font=df, fill=(122, 120, 114))

fg.save(os.path.join(OUT, 'feature-graphic-1024x500.png'), 'PNG', optimize=True)
print('feature graphic:', fg.size, f"{os.path.getsize(os.path.join(OUT,'feature-graphic-1024x500.png'))/1024:.0f}KB")

# ---- App icon 512x512 with alpha ----
icon = Image.open(os.path.join(PROJ, 'public/img/icon-512.png')).convert('RGBA')
assert icon.size == (512, 512), icon.size
icon.save(os.path.join(OUT, 'app-icon-512.png'), 'PNG')
print('icon:', icon.size, icon.mode)
