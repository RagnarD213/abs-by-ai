"""Dense hair check on a rendered range: every 0.25 s of presenter picture (not under a full-screen clip or card), Apple
Vision person mask, top of the hair in 1080-scale px from the top edge, by segment and size. usage: hair_fm.py MASTER.mp4 OUT_DIR"""
import sys, os, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import build as Bd
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
master, out = sys.argv[1], sys.argv[2]; wd = f"{out}/hair_frames"; os.makedirs(wd + "/m", exist_ok=True)
for f in glob.glob(f"{wd}/*.jpg") + glob.glob(f"{wd}/m/*"): os.remove(f)
subprocess.run([Bd.FF, "-v", "error", "-y", "-i", master, "-vf", "fps=4,scale=960:540:in_color_matrix=bt709:in_range=tv", "-q:v", "3", f"{wd}/f_%05d.jpg"], check=True)
fs = sorted(glob.glob(f"{wd}/f_*.jpg")); full = [(it["t0"], it["t1"]) for it in Bd.R if it["kind"] in Bd.FULL]; sg = Bd.all_segments(); keep = []
for k, f in enumerate(fs):
    t = (k + 0.5)/4.0
    if any(a - 0.05 <= t < b + 0.05 for a, b in full): continue
    s = next((s for s in sg if s["o0"]/Bd.FPS + 0.04 <= t < s["o1"]/Bd.FPS - 0.04), None)
    if s: keep.append((t, f, s))
for i in range(0, len(keep), 200): subprocess.run([PM, wd + "/m"] + [f for _, f, _ in keep[i:i+200]], check=True, capture_output=True)
rows = []
for t, f, s in keep:
    mp = f"{wd}/m/" + os.path.splitext(os.path.basename(f))[0] + ".mask.png"
    if not os.path.exists(mp): rows.append(dict(t=t, key=s["key"], size=s["framing"], top=None)); continue
    m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
    ys = np.where(m.sum(1) >= 3)[0]; xs = np.where(m.any(0))[0]
    rows.append(dict(t=round(t, 2), key=s["key"], size=s["framing"], top=int(ys[0])*2 if len(ys) else None, left=int(xs[0])*2 if len(xs) else None, right=int(xs[-1])*2 if len(xs) else None))
by = {}
for r in rows: by.setdefault((r["key"], r["size"]), []).append(r)
print(f"{len(rows)} samples")
for (k, z), v in by.items():
    tops = [r["top"] for r in v if r["top"] is not None]
    print(f"  {k:14s} {z}  n {len(v):3d}  hair top min {min(tops):3d} median {int(np.median(tops)):3d} px   body x {min(r['left'] for r in v if r['left'] is not None)}-{max(r['right'] for r in v if r['right'] is not None)}")
bad = [r for r in rows if r["top"] is not None and r["top"] < 20]
print("under 20 px:", bad); json.dump(dict(rows=rows, under_20=bad), open(f"{out}/hair.json", "w"), indent=1)
