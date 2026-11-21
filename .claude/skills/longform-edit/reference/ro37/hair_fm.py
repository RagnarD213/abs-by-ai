"""Hair clearance on the first-minute draft (VIDEO-RULES 2026-10-20): every 0.25 s of presenter picture, Vision person mask on
the delivered 1080p frames; clearance = top of the hair minus the picture's top edge (frame top for the close-up, the panel's
top edge y=40 for the portrait panel). Needs >= 20 px on every valid sample. Writes review/first-minute/hair.json."""
import sys, os, json, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import build as B
W = B.W; FF = B.FF; FM = f"{W}/review/first-minute"
PM = f"{B.P}/.claude/skills/shorts/reference/recentre/personmask"
src = f"{FM}/DRAFT - First Time At The Gym R1 - first minute.mp4"; wd = "/tmp/absbyai-scratch/RO-37/hair_fm"; os.makedirs(wd, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json")); S = json.load(open(f"{W}/shots.json"))
segs = B.segments(S, R, 0, B.fr(61.09))
if not os.environ.get("REUSE_MASKS"):
  for f in glob.glob(f"{wd}/f_*.jpg"): os.remove(f)
  subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", src, "-vf", "fps=4", "-q:v", "3", f"{wd}/f_%05d.jpg"], check=True)
fs = sorted(glob.glob(f"{wd}/f_*.jpg")); keep = []
for k, f in enumerate(fs):
    t = (k + 0.5) / 4; g = B.fr(t)
    sg = next((s for s in segs if s[1] <= g < s[2]), None)
    if sg and sg[0] == "pres": keep.append((t, f, sg[3]["framing"]))
if not os.environ.get("REUSE_MASKS"): subprocess.run([PM, f"{wd}/m"] + [f for _, f, _ in keep], check=True, capture_output=True)
rows = []
for t, f, fm in keep:
    mp = f"{wd}/m/" + os.path.basename(f)[:-4] + ".mask.png"
    if not os.path.exists(mp): rows.append((t, fm, None)); continue
    m = np.asarray(Image.open(mp).convert("L")) > 127
    if fm == "W": m = m[:, 528:528 + 864]
    rs = m.sum(1); ok = (rs >= 12)
    ys = [y for y in range(len(rs) - 4) if ok[y:y + 4].all()]          # the head: 4 consecutive rows of >= 12 px (stray specks ignored)
    rows.append((round(t, 2), fm, (int(ys[0]) - (40 if fm == "W" else 0)) if ys else None))
v = [x for _, _, x in rows if x is not None]
worst = min((r for r in rows if r[2] is not None), key=lambda r: r[2])
out = dict(samples=len(rows), measured=len(v), missed=len(rows) - len(v), min_px=min(v), median_px=int(np.median(v)), worst=worst,
           by_framing={k: min(x for _, f, x in rows if f == k and x is not None) for k in ("W", "T")}, verdict="PASS" if min(v) >= 20 else "FAIL")
json.dump(out, open(f"{FM}/hair.json", "w")); print(out)
