#!/usr/bin/env python3
"""RA-04 round 5: the before photo given headroom and the app's 4:5 shape, BEFORE the real generation.
The app returns a 4:5 result and trims a 2:3 upload top and bottom to get it, so the first take's result had his hair on the top
edge, and the lock screen's notch sat on his head. Here the plain overcast sky band above him (rows 0-STRETCH_SRC, no trees, no
hair) is stretched to STRETCH_DST rows with matched grain, then the photo is cropped to 1024x1280 from the top. Same man, same photo.
usage: python3 r5_before45.py IN.png OUT.png"""
import sys, numpy as np
from PIL import Image
STRETCH_SRC, STRETCH_DST = 90, 200
a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32); h, w, _ = a.shape
band = a[:STRETCH_SRC]
ys = np.linspace(0, STRETCH_SRC - 1, STRETCH_DST)
y0 = np.floor(ys).astype(int); y1 = np.minimum(y0 + 1, STRETCH_SRC - 1); t = (ys - y0)[:, None, None]
st = band[y0] * (1 - t) + band[y1] * t
rng = np.random.default_rng(5)
hp = band - np.stack([np.convolve(c, np.ones(9) / 9, mode="same") for c in band.reshape(-1, 3).T], 1).reshape(band.shape)
sd = float(hp[:, 20:-20].std())
st = st + rng.normal(0, sd * 0.9, st.shape[:2])[..., None]
out = np.concatenate([st, a[STRETCH_SRC:]], 0)[:1280]
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(sys.argv[2])
print("BEFORE45", sys.argv[2], out.shape, "grain sd", round(sd, 2))
