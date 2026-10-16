"""Diff a rebuilt card against the approved one: per-frame bounding box of pixels that differ by more than 6 levels."""
import subprocess, sys, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
a, b, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
def rd(p):
    return subprocess.Popen([FF, "-v", "error", "-i", p, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE).stdout
A, B = rd(a), rd(b); n = 0; box = [W, H, 0, 0]; sz = W*H*3
while True:
    x, y = A.read(sz), B.read(sz)
    if len(x) < sz or len(y) < sz: break
    d = np.abs(np.frombuffer(x, np.uint8).reshape(H, W, 3).astype(int) - np.frombuffer(y, np.uint8).reshape(H, W, 3)).max(2) > 6
    if d.any():
        ys, xs = np.where(d); box = [min(box[0], xs.min()), min(box[1], ys.min()), max(box[2], xs.max()), max(box[3], ys.max())]
    n += 1
print(b, n, "frames; differing pixels inside box", box)
