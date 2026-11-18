#!/usr/bin/env python3
"""Put a more appetizing steak into the food-swap still (assets/swap-steak.jpg -> assets/swap-steak-v2.jpg).
Removes the old steak cut-out by inpainting the wood behind it, cuts the new steak off its white background,
places it in the same spot and size, and keeps the original "More" tag and "Steak" label on top."""
import sys, pathlib
import numpy as np, cv2
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
A = HERE.parent / 'assets'
src = np.array(Image.open(A / 'swap-steak.jpg').convert('RGB'))
H, W = src.shape[:2]

# 1. old steak area (left item), minus the "More" tag and the label row
old = np.zeros((H, W), np.uint8)
cv2.rectangle(old, (88, 28), (286, 266), 255, -1)
cv2.rectangle(old, (34, 14), (176, 78), 255, -1)   # under the More pill too (pasted back on top)
keep = np.zeros((H, W), np.uint8)
cv2.rectangle(keep, (100, 268), (240, 311), 255, -1)    # "Steak" label
mask = cv2.bitwise_and(old, cv2.bitwise_not(keep))
clean = cv2.inpaint(cv2.cvtColor(src, cv2.COLOR_RGB2BGR), mask, 9, cv2.INPAINT_TELEA)
clean = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)

# 2. new steak cut out of its white background
st = Image.open(sys.argv[1] if len(sys.argv) > 1 else HERE / 'out/steak.jpg').convert('RGB')
a = np.array(st).astype(np.int16)
white = (a.min(axis=2) > 232) & (np.ptp(a, axis=2) < 18)
fg = (~white).astype(np.uint8) * 255
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
fg = np.where(lab == big, 255, 0).astype(np.uint8)
fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
x, y, w, h = cv2.boundingRect(fg)
cut = Image.fromarray(np.array(st)[y:y + h, x:x + w])
fg = cv2.erode(fg, np.ones((5, 5), np.uint8))          # drop the white fringe
alpha = Image.fromarray(fg[y:y + h, x:x + w]).filter(ImageFilter.GaussianBlur(1.2))

# 3. place it where the old steak sat (box about 70..300 x 30..262), keep aspect
bw, bh = 250, 236
s = min(bw / w, bh / h)
cut = cut.resize((round(w * s), round(h * s)), Image.LANCZOS)
alpha = alpha.resize(cut.size, Image.LANCZOS)
out = Image.fromarray(clean)
cx, cy = 186, 150
out.paste(cut, (cx - cut.width // 2, cy - cut.height // 2), alpha)

# 4. original tag and label back on top
orig = Image.fromarray(src)
from PIL import ImageDraw
pill = Image.new('L', (W, H), 0)
ImageDraw.Draw(pill).rounded_rectangle((39, 19, 170, 72), radius=26, fill=255)
out.paste(orig, (0, 0), pill)                                  # the More pill only, not the steak beside it
out.paste(orig.crop((100, 268, 240, 311)), (100, 268))
out.save(A / 'swap-steak-v2.jpg', quality=90)
print('saved', A / 'swap-steak-v2.jpg', out.size)
