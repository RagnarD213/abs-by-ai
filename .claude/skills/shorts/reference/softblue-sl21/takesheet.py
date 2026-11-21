"""Contact sheet of a 9:16 take: N frames evenly spaced (numbered by frame and seconds), small.  usage: takesheet.py TAKE OUT [N]"""
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
take, out = sys.argv[1], sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv) > 3 else 12
w, h = 270, 480
raw = subprocess.run([FF, "-v", "error", "-i", take, "-vf", f"scale={w}:{h}:in_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3); n = len(fr)
idx = [round(i * (n - 1) / (N - 1)) for i in range(N)]
cols = 6; rows = (N + cols - 1) // cols
S = Image.new("RGB", (cols * (w + 4), rows * (h + 4)), "white"); d = ImageDraw.Draw(S)
for k, i in enumerate(idx):
    x, y = (k % cols) * (w + 4), (k // cols) * (h + 4); S.paste(Image.fromarray(fr[i]), (x, y)); d.rectangle((x, y, x + 86, y + 16), fill="black"); d.text((x + 3, y + 2), f"f{i} {i / 24:.2f}s", fill="white")
S.save(out, quality=85); print(out, n, "frames")
