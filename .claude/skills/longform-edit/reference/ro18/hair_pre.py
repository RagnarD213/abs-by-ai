"""Pre-build hair check on the SOURCE: every 0.5 s of every shot, Apple Vision person mask on a 1280x720 frame of the 4K
roll, hair top in source px. Then the top margin each locked crop would leave (in 1080-scale output px).
usage: hair_pre.py  -> framing/hair_pre.json"""
import json, os, subprocess, glob
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
W = "/Volumes/Extreme/_edit_work/RO-18/round1"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
import sys; sys.path.insert(0, f"{W}/recipe")
import frames as Fr
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W4S": (2690, 1513, 110, 183)}
S = json.load(open(f"{W}/shots.json")); wd = f"{W}/framing/pre"; os.makedirs(wd, exist_ok=True)
jobs = []
for s in S:
    a, b = s["src_f0"]/FPS, s["src_f1"]/FPS
    for t in np.arange(a + 0.1, b - 0.05, 0.5): jobs.append((s["id"], round(float(t), 3)))
def grab(j):
    sid, t = j; out = f"{wd}/{t:09.3f}.jpg"
    if not os.path.exists(out):
        src, lt = Fr.roll_t(t)
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{lt:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=1280:720:in_color_matrix=bt709:in_range=tv", "-q:v", "3", out], check=True)
    return out
with ThreadPoolExecutor(4) as ex: files = list(ex.map(grab, jobs))
md = f"{wd}/masks"; os.makedirs(md, exist_ok=True)
todo = [f for f in files if not os.path.exists(os.path.join(md, os.path.basename(f)[:-4] + ".mask.png"))]
for i in range(0, len(todo), 200): subprocess.run([PM, md] + todo[i:i+200], check=True, capture_output=True)
rows = []
for (sid, t), f in zip(jobs, files):
    m = np.asarray(Image.open(os.path.join(md, os.path.basename(f)[:-4] + ".mask.png")).convert("L"), np.float32) / 255
    ys = np.where((m > 0.5).sum(1) >= 3)[0]; xs = np.where((m > 0.5).sum(0) >= 3)[0]
    top = int(ys[0]) * 3 if len(ys) else None                     # source px (3840 / 1280)
    rows.append(dict(shot=sid, t=t, top=top, x0=int(xs[0]) * 3 if len(xs) else None, x1=int(xs[-1]) * 3 if len(xs) else None))
res = {}
for fm, (cw, ch, x, y) in CROP.items():
    mar = [((r["top"] - y) * 1080 / ch, r) for r in rows if r["top"] is not None]
    res[fm] = dict(min=round(min(m for m, _ in mar), 1), p5=round(float(np.percentile([m for m, _ in mar], 5)), 1),
                   median=round(float(np.median([m for m, _ in mar])), 1),
                   worst=[(round(m, 1), r["shot"], r["t"]) for m, r in sorted(mar, key=lambda z: z[0])[:8]])
json.dump(dict(rows=rows, margins=res), open(f"{W}/framing/hair_pre.json", "w"), indent=1)
print(len(rows), "samples"); print(json.dumps(res, indent=1))
