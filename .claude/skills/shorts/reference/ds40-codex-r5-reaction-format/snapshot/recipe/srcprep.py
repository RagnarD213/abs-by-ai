"""Decode the sample's source frames at output scale (area 2x2, rows above the laptop crop) into a uint8 memmap.
Used for optical flow (grey) and for the hand-masked watch glass (RGB).    python3 srcprep.py T0 NFRAMES OUT.npy"""
import numpy as np, sys
from common import frames
T0, N, OUT = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
mm = np.lib.format.open_memmap(OUT, "w+", np.uint8, (N, 1920, 1080, 3))
n = 0
for i, f in enumerate(frames(T0, nframes=N, scale=(1080, 1920))):
    mm[i] = (np.clip(f[:1920], 0, 1) * 255 + 0.5).astype(np.uint8); n += 1
mm.flush(); assert n == N, f"decoded {n} of {N}"
print("ok", n)
