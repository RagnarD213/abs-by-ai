"""Hair clearance on the first minute: every 0.25 s of on-camera picture (no full-screen item up), Vision person mask,
the top of the mask in 1080-scale px from the top edge. Writes round1/first-minute/hair.json."""
import json, os, glob, subprocess
import numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro10"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
src = f"{W}/round1/first-minute/DRAFT - RO-10 round 1 - first minute.mp4"; wd = f"{W}/round1/first-minute/_hair"; os.makedirs(wd, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json"))
full = [(it["t0"], it["t1"]) for it in R if it["t1"] and it["kind"] in ("scene", "title", "clip", "ai")]
subprocess.run([FF, "-v", "error", "-y", "-i", src, "-vf", "fps=4,scale=960:540", "-q:v", "3", f"{wd}/f_%05d.jpg"], check=True)
fs = sorted(glob.glob(f"{wd}/f_*.jpg")); keep = []
for k, f in enumerate(fs):
    t = (k + 0.5) / 4
    if not any(a - 0.05 <= t <= b + 0.05 for a, b in full): keep.append((t, f))
subprocess.run([PM, f"{wd}/m"] + [f for _, f in keep], check=True, capture_output=True)
tops = []
for t, f in keep:
    m = np.asarray(Image.open(f"{wd}/m/" + os.path.basename(f)[:-4] + ".mask.png").convert("L")) > 127
    ys = np.where(m[:, 200:760].sum(1) >= 3)[0]
    if len(ys): tops.append((round(t, 2), int(ys[0]) * 2))
v = [x for _, x in tops]
out = dict(samples=len(v), min_px=min(v), median_px=int(np.median(v)), worst_t=min(tops, key=lambda x: x[1])[0])
json.dump(out, open(f"{W}/round1/first-minute/hair.json", "w")); print(out)
