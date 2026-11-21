"""RO-20 look bake-off stills: two roll moments x (raw, A, D, E, F) at the camera frame (W) and the 1.3x punch-in (T),
plus per-option numbers (frame median luma / saturation, skin median luma, Y90, saturation, hue)."""
import json, os, subprocess, sys, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/look/opt"; os.makedirs(O, exist_ok=True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1511.MP4"
G = json.load(open(f"{W}/grades.json"))["C1511"]; OPTS = [k for k in G if k not in ("stats", "tank")]
MOM = {"m1": (600.0, 237), "m2": (3300.0, 150)}      # roll time, punch-in x0
def grab(t, vf, out):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", SRC, "-frames:v", "1", "-vf", vf, out], check=True)
BASE = "scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrp16le"
def stats(p):
    a = np.asarray(Image.open(p).convert("RGB").resize((960, 540)), np.float32)/255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = a.max(2); mn = a.min(2); d = mx-mn+1e-6
    h = np.where(mx == r, ((g-b)/d) % 6, np.where(mx == g, (b-r)/d+2, (r-g)/d+4))*60; s = d/(mx+1e-6); y = 0.2126*r+0.7152*g+0.0722*b
    sk = (h > 4) & (h < 40) & (s > 0.22) & (s < 0.8) & (mx > 0.15) & (np.arange(960)[None, :] > 250) & (np.arange(960)[None, :] < 800)
    return dict(luma=round(float(np.median(y)), 3), sat=round(float(np.median(s)), 3), skinY=round(float(np.median(y[sk])), 3), skinY90=round(float(np.percentile(y[sk], 90)), 3),
                skinS=round(float(np.median(s[sk])), 3), hue=round(float(np.median(h[sk])), 1))
num = {}
for m, (t, x0) in MOM.items():
    for k in ["raw"] + OPTS:
        g = "" if k == "raw" else "," + G[k]
        grab(t, BASE + g + ",format=rgb24", f"{O}/{m}_W_{k}.png")
        grab(t, f"crop=1477:831:{x0}:0," + BASE + g + ",format=rgb24", f"{O}/{m}_T_{k}.png")
        num.setdefault(k, {})[m] = stats(f"{O}/{m}_W_{k}.png")
json.dump(num, open(f"{O}/numbers.json", "w"), indent=1)
for k, v in num.items(): print(k, v)
for r in sys.argv[1:]: print(os.path.basename(r), stats(r))
