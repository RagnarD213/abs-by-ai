"""Find the Apple Watch per frame in the R4 corner footage (full-height cache, 1920 rows) and write stage15 watch boxes.
The grey band (neutral, mid luma) is the anchor; the box is the band plus 34 px. Boxes are in stage15's 'output px',
which subtracts OY 175, so 175 is added here (this cache starts at source row 0)."""
import numpy as np, json, sys
from scipy import ndimage as ndi
import sys; S = np.load(sys.argv[1], mmap_mode="r"); OUT = sys.argv[2]
OY, PAD, Y0 = 175, 34, 1000
ranges, miss = [], []
for i in range(S.shape[0]):
    f = np.asarray(S[i, Y0:]).astype(np.float32) / 255
    mx, mn = f.max(-1), f.min(-1); Y = f @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    band = ndi.binary_opening(((mx - mn) < 0.07) & (Y > 0.25) & (Y < 0.62), iterations=1)
    lab, n = ndi.label(band)
    if not n: miss.append(i); continue
    sz = ndi.sum(np.ones_like(Y), lab, np.arange(1, n + 1)); k = int(np.argmax(sz)) + 1
    if sz[k - 1] < 250: miss.append(i); continue
    ys, xs = np.where(lab == k)
    x0, x1, y0, y1 = xs.min() - 60, xs.max() + 60, ys.min() - PAD + Y0, ys.max() + 140 + Y0   # the face hangs below the band
    ranges.append([i, i, int(max(0, x0)), int(y0 + OY), int(min(1080, x1)), int(min(1920, y1) + OY)])
json.dump({"ranges": ranges}, open(OUT, "w"))
w = np.array([[r[4] - r[2], r[5] - r[3]] for r in ranges])
print("frames", S.shape[0], "boxes", len(ranges), "missed", len(miss), miss[:20], "box w/h median", np.median(w, 0), "max", w.max(0))
