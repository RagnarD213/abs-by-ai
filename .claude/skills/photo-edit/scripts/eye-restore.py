#!/usr/bin/env python3
"""Put Dan's REAL eyes back into a retouched frame, then optionally enlarge them.

Why this exists: the hard-definition retouch narrows the eye APERTURE — it paints the lid
further down and takes the iris and sclera with it. A geometric enlarge cannot fix that
(you just get a bigger closed eye), and a re-roll re-rolls the whole face. So: alpha-blend
the ORIGINAL eye back inside a feathered ellipse, tone-match it to the retouched skin, then
magnify with eye-warp's anisotropic gains.

The original and the retouch are close to aligned but NOT identical - the face can shift
10-15px - so pass BOTH eye centres (from Vision landmarks) and the patch is offset to match.

Usage:
  python3 eye-restore.py EDIT ORIG OUT ECX ECY OCX OCY W H [GX GY]
    EDIT  retouched frame (full res)
    ORIG  original, already upscaled to EDIT's exact size
    ECX/ECY  eye centre in EDIT      OCX/OCY  same eye's centre in ORIG
    W/H   eye landmark width/height  GX/GY  magnification (default 1.0 = restore only)
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
edit_p, orig_p, out_p = sys.argv[1:4]
ecx, ecy, ocx, ocy, w, h = (float(v) for v in sys.argv[4:10])
gx, gy = (float(v) for v in sys.argv[10:12]) if len(sys.argv) > 11 else (1.0, 1.0)

E = np.asarray(Image.open(edit_p).convert('RGB')).astype(np.float32)
O = np.asarray(Image.open(orig_p).convert('RGB')).astype(np.float32)
H_, W_ = E.shape[:2]

# 1. shift the original so its eye sits exactly on the retouch's eye
dx, dy = int(round(ecx - ocx)), int(round(ecy - ocy))
Os = np.roll(np.roll(O, dy, axis=0), dx, axis=1)

# 2. feathered ellipse over the eye + lid, deliberately stopping short of the crow's feet
rx, ry = w * 0.85, h * 1.9
x0, x1 = max(0, int(ecx - rx * 1.6)), min(W_, int(ecx + rx * 1.6))
y0, y1 = max(0, int(ecy - ry * 1.6)), min(H_, int(ecy + ry * 1.6))
ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
d = np.sqrt(((xs - ecx) / rx) ** 2 + ((ys - ecy) / ry) ** 2)
m = np.clip((1.30 - d) / 0.55, 0, 1)                      # 1 inside, ramp to 0 by d=1.30
m = np.asarray(Image.fromarray((m * 255).astype(np.uint8))
               .filter(ImageFilter.GaussianBlur(6)), np.float32) / 255.0

# 3. tone-match the original patch to the retouched skin, measured on the mask's outer ring
ring = (m > 0.12) & (m < 0.55)
patch, base = Os[y0:y1, x0:x1], E[y0:y1, x0:x1]
if ring.sum() > 50:
    for c in range(3):
        g = base[..., c][ring].mean() / max(patch[..., c][ring].mean(), 1e-6)
        patch[..., c] *= float(np.clip(g, 0.85, 1.18))

# 4. composite
E[y0:y1, x0:x1] = base * (1 - m[..., None]) + patch * m[..., None]

# 5. anisotropic magnify about the eye centre
if gx != 1.0 or gy != 1.0:
    wrx, wry = w * 1.55, h * 3.2
    x0, x1 = max(0, int(ecx - wrx - 4)), min(W_, int(ecx + wrx + 4))
    y0, y1 = max(0, int(ecy - wry - 4)), min(H_, int(ecy + wry + 4))
    ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    ddx, ddy = (xs - ecx) / wrx, (ys - ecy) / wry
    t = np.sqrt(ddx * ddx + ddy * ddy)
    inside = t < 1.0
    fall = (1.0 - np.clip(t, 0, 1) ** 2) ** 2
    ex, ey = 1.0 + (gx - 1.0) * fall, 1.0 + (gy - 1.0) * fall
    sx = np.where(inside, ecx + (xs - ecx) / ex, xs)
    sy = np.where(inside, ecy + (ys - ecy) / ey, ys)
    xf, yf = np.clip(sx, 0, W_ - 2), np.clip(sy, 0, H_ - 2)
    xi, yi = np.floor(xf).astype(np.int32), np.floor(yf).astype(np.int32)
    xa, ya = (xf - xi)[..., None], (yf - yi)[..., None]
    E[y0:y1, x0:x1] = (E[yi, xi] * (1 - xa) * (1 - ya) + E[yi, xi + 1] * xa * (1 - ya)
                       + E[yi + 1, xi] * (1 - xa) * ya + E[yi + 1, xi + 1] * xa * ya)

Image.fromarray(np.clip(E, 0, 255).astype(np.uint8)).save(out_p, quality=97, subsampling=0)
print('saved', out_p)
