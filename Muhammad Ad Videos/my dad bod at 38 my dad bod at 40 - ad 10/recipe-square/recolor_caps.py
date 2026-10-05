#!/usr/bin/env python3
"""AS-06: the vertical's caption layer with ONLY the lit word's colour changed, olive -> Soft Blue Light cyan
(captions.py's own LIT for a softblue build). Every state, every frame, every white word and the alpha are untouched."""
import subprocess, numpy as np, sys
sys.path.insert(0, '.')
import vlib
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OL = np.array(vlib.OLIVE[:3], np.int16); CY = np.array((104, 197, 255), np.uint8)
W, H = 1080, 1920
src, dst = sys.argv[1], sys.argv[2]
r = subprocess.Popen([FF, "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
w = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-",
                      "-c:v", "png", "-pix_fmt", "rgba", "-video_track_timescale", "30000", dst], stdin=subprocess.PIPE)
n = changed = 0
while True:
    b = r.stdout.read(W * H * 4)
    if len(b) < W * H * 4: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 4).copy()
    m = (f[..., 3] > 0) & (np.abs(f[..., :3].astype(np.int16) - OL).sum(axis=2) < 40)
    if m.any():
        f[..., :3][m] = CY; changed += 1
    w.stdin.write(f.tobytes()); n += 1
w.stdin.close(); w.wait(); r.wait()
print(n, "frames,", changed, "with a lit word recoloured")
