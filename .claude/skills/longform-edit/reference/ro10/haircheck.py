"""RO-10 dense hair check on the delivered file: every 0.25 s of presenter picture (not under a full-frame clip/scene/title),
Apple Vision person mask, top of the mask (hair) in 1080-scale px from the top edge.
usage: haircheck.py MASTER.mp4 PLAN.json OUT.json"""
import sys, os, json, subprocess, glob
import numpy as np
from PIL import Image
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
master, planp, outp = sys.argv[1:4]
plan = json.load(open(planp)); wd = os.path.join(os.path.dirname(outp), "hair_frames"); os.makedirs(wd, exist_ok=True)
subprocess.run([FF, "-v", "error", "-y", "-i", master, "-vf", "fps=4,scale=960:540:in_color_matrix=bt709:in_range=tv", "-q:v", "3", f"{wd}/f_%05d.jpg"], check=True)
frames = sorted(glob.glob(f"{wd}/f_*.jpg"))
pres = [(a, b, lab) for (a, b, lab), c in zip(plan["punch"], plan["punch_covered"]) if not c]
keep = []
for k, f in enumerate(frames):
    t = (k + 0.5) / 4.0                                     # fps filter samples mid-interval
    seg = next((p for p in pres if p[0] + 0.02 <= t < p[1] - 0.02), None)
    if seg: keep.append((t, f, seg[2]))
md = f"{wd}/masks"; os.makedirs(md, exist_ok=True)
B = 200
for i in range(0, len(keep), B):
    subprocess.run([PM, md] + [f for _, f, _ in keep[i:i+B]], check=True, capture_output=True)
rows = []
for t, f, lab in keep:
    mp = os.path.join(md, os.path.splitext(os.path.basename(f))[0] + ".mask.png")
    if not os.path.exists(mp): rows.append(dict(t=round(t, 2), lab=lab, top=None)); continue
    m = np.asarray(Image.open(mp).convert("L"), np.float32) / 255.0
    rowsum = (m > 0.5).sum(1)
    ys = np.where(rowsum >= 3)[0]
    top = int(ys[0]) * 2 if len(ys) else None               # back to 1080 scale
    rows.append(dict(t=round(t, 2), lab=lab, top=top, edge_rows=float((m[:6] > 0.5).mean())))
valid = [r for r in rows if r["top"] is not None]
tops = [r["top"] for r in valid]
worst = sorted(valid, key=lambda r: r["top"])[:15]
res = dict(master=master, samples=len(rows), valid=len(valid), min_top_px=min(tops) if tops else None,
           median_top_px=float(np.median(tops)) if tops else None, under_20=[r for r in valid if r["top"] < 20], worst=worst)
json.dump(dict(summary=res, rows=rows), open(outp, "w"), indent=1)
print(json.dumps(res, indent=1)[:3000])
