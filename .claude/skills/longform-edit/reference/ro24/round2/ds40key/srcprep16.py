"""Source frames at output scale (area) into a uint8 memmap, for stage 1.5's optical flow.   python3 srcprep16.py F0 N OUT.npy [X0 X1]  (4K box)"""
import numpy as np, sys
from common16 import frames, OW, OH
F0, N, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
X0, X1 = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 3840)
x0, x1 = X0 * 3 // 4, X1 * 3 // 4
mm = np.lib.format.open_memmap(OUT, "w+", np.uint8, (N, OH, x1 - x0, 3)); n = 0
for i, f in enumerate(frames(F0, N, scale=(OW, OH))):
    mm[i] = (np.clip(f[:, x0:x1], 0, 1) * 255 + 0.5).astype(np.uint8); n += 1
mm.flush(); assert n == N, f"decoded {n} of {N}"; print("srcprep ok", n)
