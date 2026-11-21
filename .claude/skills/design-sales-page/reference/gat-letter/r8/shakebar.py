#!/usr/bin/env python3
"""Round 8 (Dan, 2026-11-18): one graphic for "eat less of this": a protein shake and a protein bar, in the film look
(wood kitchen backdrop, red Less tag, white Poppins labels), so it is obvious what both are.
Backdrop: the clean wood from the film still, mirrored across the width. Items: gen/shake.png and gen/bar.png, cut off white."""
import pathlib, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H0 = pathlib.Path(__file__).resolve().parent
A = H0.parent / 'assets'
S = 2                                   # draw at 2x the film still for sharp type
W, H = 780 * S, 400 * S

# ---- backdrop
wood = np.array(Image.open(A / 'swap-oil-nohead.jpg').convert('RGB'))[:, 232:452]      # clean wood columns
tile = np.concatenate([wood, wood[:, ::-1]], axis=1)
row = np.concatenate([tile] * 3, axis=1)[:, :780]
bg = Image.fromarray(row).resize((W, round(311 * S * 1.0)), Image.LANCZOS)
canvas = Image.new('RGB', (W, H))
canvas.paste(bg.resize((W, H), Image.LANCZOS), (0, 0))
canvas = canvas.filter(ImageFilter.GaussianBlur(3))
# the film darkens the edges a little
v = Image.new('L', (W, H), 0); d = ImageDraw.Draw(v)
d.ellipse((-W * .25, -H * .5, W * 1.25, H * 1.5), fill=255)
v = v.filter(ImageFilter.GaussianBlur(160))
canvas = Image.composite(canvas, Image.eval(canvas, lambda p: int(p * .72)), v)

def cutout(path, light=236):
    im = Image.open(path).convert('RGB'); a = np.array(im).astype(np.int16)
    white = (a.min(axis=2) > light) & (np.ptp(a, axis=2) < 16)      # white backdrop and, for a lower `light`, its soft shadow
    fg = (~white).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    fg = np.where(lab == big, 255, 0).astype(np.uint8)
    cnt, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)       # outline only: clear plastic and foil stay solid
    solid = np.zeros_like(fg); cv2.drawContours(solid, cnt, -1, 255, -1)
    solid = cv2.erode(solid, np.ones((5, 5), np.uint8))
    x, y, w, h = cv2.boundingRect(solid)
    rgba = Image.fromarray(np.array(im)[y:y + h, x:x + w]).convert('RGBA')
    rgba.putalpha(Image.fromarray(solid[y:y + h, x:x + w]).filter(ImageFilter.GaussianBlur(1.3)))
    return rgba

def place(item, cx, cy, box_w, box_h):
    k = min(box_w / item.width, box_h / item.height)
    it = item.resize((round(item.width * k), round(item.height * k)), Image.LANCZOS)
    x, y = round(cx - it.width / 2), round(cy - it.height / 2)
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (x + 6, y + 14), it.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(sh, (0, 0), sh)
    canvas.paste(it, (x, y), it)

place(cutout(H0 / 'gen/shake.png'), W * .27, H * .44, W * .30, H * .70)
place(cutout(H0 / 'gen/bar2.png', light=214), W * .71, H * .46, W * .46, H * .62)      # matte wrapper: cuts cleanly off white

d = ImageDraw.Draw(canvas)
def label(text, cx, y):
    f = ImageFont.truetype(str(H0 / 'fonts/Poppins-Bold.ttf'), 30 * S)
    w = d.textlength(text, font=f)
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((cx - w / 2, y + 3), text, font=f, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(5)); canvas.paste(sh, (0, 0), sh)
    ImageDraw.Draw(canvas).text((cx - w / 2, y), text, font=f, fill='white')
label('Protein Shake', W * .27, H - 62 * S)
label('Protein Bar', W * .71, H - 62 * S)

# the red "Less" tag, as in the film stills
f = ImageFont.truetype(str(H0 / 'fonts/Poppins-SemiBold.ttf'), 31 * S)
d = ImageDraw.Draw(canvas)
tw = d.textlength('Less', font=f); pw, ph = tw + 54 * S, 56 * S
x0, y0 = 40 * S, 18 * S
d.rounded_rectangle((x0 - 3 * S, y0 - 3 * S, x0 + pw + 3 * S, y0 + ph + 3 * S), radius=(ph + 6 * S) // 2, fill='white')
d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=ph // 2, fill=(215, 38, 61))
d.text((x0 + (pw - tw) / 2, y0 + 4 * S), 'Less', font=f, fill='white')

canvas.save(A / 'swap-shake-bar.jpg', quality=90, optimize=True)
print('swap-shake-bar.jpg', canvas.size)
