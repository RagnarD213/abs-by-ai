"""Processing box for one key range: Dan's horizontal extent over every 4th frame at 1/8 scale (green excess < 0.06, largest
blob), plus a 240 px margin for fast hands between samples; full height. x0/x1 are multiples of 4 so the 0.75 output scale lands on
whole pixels.   python3 box16.py F0 N  ->  prints 'x0 x1' (4K px)"""
import sys, numpy as np, cv2
from common16 import frames, W
F0, N = int(sys.argv[1]), int(sys.argv[2])
xs0, xs1 = [], []
for i, f in enumerate(frames(F0, N, scale=(480, 270))):
    if i % 4: continue
    fg = (f[..., 1] - np.maximum(f[..., 0], f[..., 2])) < 0.06
    n, lab = cv2.connectedComponents(fg.astype('uint8'))
    if n < 2: continue
    sizes = np.bincount(lab.ravel()); sizes[0] = 0; m = lab == sizes.argmax()
    cols = np.where(m.any(0))[0]; xs0.append(cols[0] * 8); xs1.append(cols[-1] * 8 + 8)
x0 = max(0, (min(xs0) - 240) // 4 * 4); x1 = min(W, -(-(max(xs1) + 240) // 4) * 4)
print(x0, x1)
