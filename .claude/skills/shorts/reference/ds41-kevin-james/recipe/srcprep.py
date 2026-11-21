"""Decode a piece's source frames at cache scale (0.75: area resize, rows above the laptop crop) into a uint8 memmap, for the
stage 1.5 optical flow.   python3 srcprep.py T0 NFRAMES OUT.npy   (DS-44 copy of the R2 srcprep at 0.75 instead of 0.5)"""
import numpy as np, sys
from common import frames
T0, N, OUT = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
import os
ROWS = int(os.environ.get("ROWS", "2618"))     # 2880 when the laptop is kept
mm = np.lib.format.open_memmap(OUT, "w+", np.uint8, (N, ROWS, 1620, 3))
n = 0
for i, f in enumerate(frames(T0, nframes=N, scale=(1620, 2880))):
    mm[i] = (np.clip(f[:ROWS], 0, 1) * 255 + 0.5).astype(np.uint8); n += 1
mm.flush(); assert n == N, f"decoded {n} of {N}"
print("ok", n)
