#!/usr/bin/env python3
"""Round 8 (Dan, 2026-11-18): the three top food-swap graphics go back to the film look, without his head.
Takes the film stills (assets/swap-*.jpg) and paints the wood back over the hair at the bottom centre.
The hair area is a hand-placed ellipse per still so no food, tag or label is touched. Each row is refilled with
the wood colour found just left and right of the hair on that same row, which keeps the cabinet lines straight."""
import pathlib, numpy as np, cv2
A = pathlib.Path(__file__).resolve().parent.parent / 'assets'
JOBS = {'swap-eggs.jpg': ((382, 316), (98, 60)), 'swap-oil.jpg': ((421, 316), (112, 76)), 'swap-steak-v2.jpg': ((373, 316), (88, 44))}
rng = np.random.default_rng(7)
for name, (c, r) in JOBS.items():
    im = cv2.imread(str(A / name)).astype(np.float32); H, W = im.shape[:2]
    m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, c, r, 0, 0, 360, 255, -1)
    xl0, xl1, xr0, xr1 = c[0] - r[0] - 26, c[0] - r[0] - 5, c[0] + r[0] + 5, c[0] + r[0] + 22
    fill = im.copy()
    for y in range(max(0, c[1] - r[1] - 2), H):
        L, R = im[y, xl0:xl1].mean(axis=0), im[y, xr0:xr1].mean(axis=0)
        t = np.linspace(0, 1, xr0 - xl1)[:, None]
        fill[y, xl1:xr0] = L * (1 - t) + R * t
    grain = cv2.GaussianBlur(rng.normal(0, 5, (H, W)).astype(np.float32), (0, 0), 1.6)[..., None]
    fill = fill + grain
    f = cv2.GaussianBlur(m, (0, 0), 5).astype(np.float32)[..., None] / 255
    out = np.clip(im * (1 - f) + fill * f, 0, 255).astype(np.uint8)
    dst = A / (name.replace('-v2', '').replace('.jpg', '') + '-nohead.jpg')
    cv2.imwrite(str(dst), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(name, '->', dst.name)
