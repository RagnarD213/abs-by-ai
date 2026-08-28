#!/usr/bin/env python3
"""Anisotropic local magnifier — the Facetune 'enlarge eyes' tool.

Unlike local-warp.py (radial bulge, one strength), this takes SEPARATE horizontal and
vertical gains, because Dan's standing note on eyes is "larger and especially TALLER".
Content inside the ellipse is magnified about (CX,CY) by GX across and GY down, with a
smooth falloff to identity at the ellipse edge. Everything outside is pixel-identical.

Usage:
  python3 eye-warp.py SRC OUT CX CY RX RY GX GY
  e.g. python3 eye-warp.py in.jpg out.jpg 1806 951 155 115 1.05 1.18

Gains are multipliers: 1.00 = no change, 1.18 = 18% bigger. Radii should be roughly
1.5x the eye's half-width and ~3x its half-height so the falloff lands on plain skin,
not on the lash line. Get CX/CY/w/h from Vision landmarks, never by eye.
"""
import sys
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
src, out = sys.argv[1], sys.argv[2]
cx, cy, rx, ry, gx, gy = (float(v) for v in sys.argv[3:9])

img = np.asarray(Image.open(src)).astype(np.float32)
H, W = img.shape[:2]

x0, x1 = max(0, int(cx - rx - 4)), min(W, int(cx + rx + 4))
y0, y1 = max(0, int(cy - ry - 4)), min(H, int(cy + ry + 4))
ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
dx, dy = (xs - cx) / rx, (ys - cy) / ry
t = np.sqrt(dx * dx + dy * dy)
inside = t < 1.0
fall = (1.0 - np.clip(t, 0, 1) ** 2) ** 2          # 1 at centre, 0 at the rim
ex = 1.0 + (gx - 1.0) * fall
ey = 1.0 + (gy - 1.0) * fall
# inverse map: to magnify the output, sample from a contracted source
sx = np.where(inside, cx + (xs - cx) / ex, xs)
sy = np.where(inside, cy + (ys - cy) / ey, ys)

x_f = np.clip(sx, 0, W - 2); y_f = np.clip(sy, 0, H - 2)
xi = np.floor(x_f).astype(np.int32); yi = np.floor(y_f).astype(np.int32)
xa = (x_f - xi)[..., None]; ya = (y_f - yi)[..., None]
img[y0:y1, x0:x1] = (img[yi, xi] * (1 - xa) * (1 - ya) + img[yi, xi + 1] * xa * (1 - ya)
                     + img[yi + 1, xi] * (1 - xa) * ya + img[yi + 1, xi + 1] * xa * ya)

Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out, quality=97, subsampling=0)
print('saved', out)
