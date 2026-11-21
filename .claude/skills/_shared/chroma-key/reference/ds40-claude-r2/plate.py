"""Estimate the clean plate (screen colour field) from frames where Dan has moved."""
import numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi
from common import frames
sw, sh = 540, 960
stack = []; masks = []
for f in frames(1386.0, dur=66.0, scale=(sw, sh), fps=1.5):
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    ex = g - np.maximum(r, b)
    scr = (ex > 0.10) & (g > 0.25)
    scr = ndi.binary_erosion(scr, iterations=4)   # stay clear of edges / spill
    stack.append(f); masks.append(scr)
S = np.stack(stack); M = np.stack(masks)
print("frames", len(S))
cov = M.mean(0)
print("pixels never screen:", (cov == 0).mean())
plate = np.zeros((sh, sw, 3), np.float32)
for c in range(3):
    v = np.where(M, S[..., c], np.nan)
    plate[..., c] = np.nanmedian(v, 0)
known = ~np.isnan(plate[..., 0])
# fill unknown (always covered) by normalized convolution at growing scales
filled = plate.copy(); filled[~known] = 0
wsum = known.astype(np.float32)
acc = filled * wsum[..., None]
out = filled.copy(); done = known.copy()
for sig in [4, 8, 16, 32, 64, 128]:
    a = np.stack([ndi.gaussian_filter(acc[..., c], sig) for c in range(3)], -1)
    w = ndi.gaussian_filter(wsum, sig)
    est = a / np.maximum(w, 1e-6)[..., None]
    sel = (~done) & (w > 0.02)
    out[sel] = est[sel]; done |= sel
print("unfilled after pyramid:", (~done).mean())
np.save("plate_q.npy", out); np.save("plate_known_q.npy", known)
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save("plate_q.png")
# report screen stats
g = out[..., 1]; ex = g - np.maximum(out[..., 0], out[..., 2])
print("plate G range %.3f..%.3f, excess %.3f..%.3f" % (np.percentile(g, 1), np.percentile(g, 99), np.percentile(ex, 1), np.percentile(ex, 99)))
for name, sl in [("top", slice(0, 100)), ("mid", slice(400, 500)), ("low", slice(800, 900))]:
    print(name, out[sl].reshape(-1, 3).mean(0).round(3))
