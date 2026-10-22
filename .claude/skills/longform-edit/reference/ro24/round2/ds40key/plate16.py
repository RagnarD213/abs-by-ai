"""Clean plate for C1726 (the DS-40 plate.py method): per-pixel temporal median of the screen at quarter res, 1.5 fps over a
stretch of the take, pixels where Dan never moved filled by normalised convolution.   python3 plate16.py [F0 NFRAMES NAME]
(default: 13380 5400 plate = 446.4-626.6 s, the stretch around the first minute)"""
import numpy as np, os, sys
from PIL import Image
from scipy import ndimage as ndi
from common16 import frames, WORK, OW, OH
os.makedirs(WORK, exist_ok=True)
sw, sh = 960, 540
stack, masks = [], []
PF0, PN, NAME = (int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]) if len(sys.argv) > 3 else (13380, 5400, "plate")
for f in frames(PF0, PN, scale=(sw, sh), fps=1.5):
    ex = f[..., 1] - np.maximum(f[..., 0], f[..., 2])
    scr = ndi.binary_erosion((ex > 0.10) & (f[..., 1] > 0.25), iterations=4)
    stack.append(f); masks.append(scr)
S = np.stack(stack); M = np.stack(masks); print("frames", len(S), "never screen", round(float((M.mean(0) == 0).mean()), 4))
plate = np.full((sh, sw, 3), np.nan, np.float32)
for c in range(3):
    plate[..., c] = np.nanmedian(np.where(M, S[..., c], np.nan), 0)
known = ~np.isnan(plate[..., 0]); out = np.where(known[..., None], plate, 0).astype(np.float32); done = known.copy()
acc = out * known[..., None]; wsum = known.astype(np.float32)
for sig in [4, 8, 16, 32, 64, 128]:
    a = np.stack([ndi.gaussian_filter(acc[..., c], sig) for c in range(3)], -1); w = ndi.gaussian_filter(wsum, sig)
    sel = (~done) & (w > 0.02); out[sel] = (a / np.maximum(w, 1e-6)[..., None])[sel]; done |= sel
print("unfilled", round(float((~done).mean()), 5))
np.save(f"{WORK}/{NAME}_q.npy", out); np.save(f"{WORK}/{NAME}_known_q.npy", known)
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(f"{WORK}/{NAME}_q.png")
po = np.stack([ndi.zoom(out[..., c], (OH / sh, OW / sw), order=1) for c in range(3)], -1).astype(np.float32)
np.save(f"{WORK}/{NAME}_out.npy", po)       # stage15 reads it beside src_u8 (used only for watch-glass boxes)
g = out[..., 1]; ex = g - np.maximum(out[..., 0], out[..., 2])
print("plate G %.3f..%.3f excess %.3f..%.3f" % (np.percentile(g, 1), np.percentile(g, 99), np.percentile(ex, 1), np.percentile(ex, 99)))
