#!/usr/bin/env python3
"""Local bulge/pinch warp — the Facetune 'reshape' tool. Use for geometry-only edits
(fuller fabric drape, slimming a spot) that AI edit models refuse or restyle.
Positive strength magnifies the region (bigger), negative pinches (smaller).

Usage:
  python3 local-warp.py SRC OUT CX CY RX RY STRENGTH
  e.g. python3 local-warp.py in.jpg out.jpg 1920 2415 165 195 0.30

Coordinates are pixels in SRC. Strength: 0.10 barely visible, 0.20-0.30 subtle-but-real,
>0.45 risks visible distortion of straight lines near the edge of the ellipse.
Everything outside the ellipse is untouched (pixel-identical).
"""
import sys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
cx, cy, rx, ry = (float(v) for v in sys.argv[3:7])
strength = float(sys.argv[7])

img = np.asarray(Image.open(src)).astype(np.float32)
H, W = img.shape[:2]

x0, x1 = max(0, int(cx - rx - 4)), min(W, int(cx + rx + 4))
y0, y1 = max(0, int(cy - ry - 4)), min(H, int(cy + ry + 4))
ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
dx = (xs - cx) / rx
dy = (ys - cy) / ry
t = np.sqrt(dx * dx + dy * dy)
inside = t < 1.0
f = 1.0 - strength * (1.0 - t ** 2) ** 2  # smooth falloff, zero at ellipse edge
sx = np.where(inside, cx + dx * f * rx, xs)
sy = np.where(inside, cy + dy * f * ry, ys)

x_f = np.clip(sx, 0, W - 2); y_f = np.clip(sy, 0, H - 2)
xi = np.floor(x_f).astype(np.int32); yi = np.floor(y_f).astype(np.int32)
xa = (x_f - xi)[..., None]; ya = (y_f - yi)[..., None]
img[y0:y1, x0:x1] = (img[yi, xi] * (1 - xa) * (1 - ya) + img[yi, xi + 1] * xa * (1 - ya)
                     + img[yi + 1, xi] * (1 - xa) * ya + img[yi + 1, xi + 1] * xa * ya)

Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out, quality=97, subsampling=0)
print('saved', out)
