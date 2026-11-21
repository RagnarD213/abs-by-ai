"""Hair clearance on a built file: every 0.25 s, Vision person mask (largest blob), top of the mask in 1080-scale px from
the top edge, plus the body's left/right edge. usage: hair_first.py FILE OUT.json"""
import json, os, glob, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
src, outp = sys.argv[1:3]; wd = os.path.splitext(outp)[0]+"_frames"; os.makedirs(wd+"/m", exist_ok=True)
subprocess.run([FF, "-v", "error", "-y", "-i", src, "-vf", "fps=4,scale=960:540", "-q:v", "3", f"{wd}/f_%05d.jpg"], check=True)
fs = sorted(glob.glob(f"{wd}/f_*.jpg"))
for i in range(0, len(fs), 200): subprocess.run([PM, f"{wd}/m"]+fs[i:i+200], check=True, capture_output=True)
rows = []
for k, f in enumerate(fs):
    mp = f"{wd}/m/"+os.path.basename(f)[:-4]+".mask.png"
    if not os.path.exists(mp): continue
    m = np.asarray(Image.open(mp).convert("L").resize((960, 540))) > 127; lab, n = ndimage.label(m)
    if not n: continue
    m = lab == (1+int(np.argmax(ndimage.sum(m, lab, range(1, n+1))))); ys = np.where(m.sum(1) >= 3)[0]; xs = np.where(m.sum(0) >= 3)[0]
    rows.append([round((k+0.5)/4, 2), int(ys[0])*2, int(xs[0])*2, int(xs[-1])*2])
v = np.array(rows)
out = dict(samples=len(rows), hair_min_px=int(v[:, 1].min()), hair_median_px=int(np.median(v[:, 1])), hair_max_px=int(v[:, 1].max()), worst_t=float(v[np.argmin(v[:, 1]), 0]),
           left_min_px=int(v[:, 2].min()), right_max_px=int(v[:, 3].max()), rows=rows)
json.dump(out, open(outp, "w")); print({k: v for k, v in out.items() if k != "rows"})
