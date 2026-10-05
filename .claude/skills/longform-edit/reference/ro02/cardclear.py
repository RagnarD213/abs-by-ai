"""Before proposing a side card: his body against the card edge (x 752 + 24) on every piece the card spans, every 0.5 s,
person mask (largest blob) on the real graded, slid frame. Also the hair top. usage: cardclear.py -> round3/cardclear/cardclear.json"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro02/recipe")
from PIL import Image
from scipy import ndimage
import frames as F, build as Bd
W = "/Volumes/Extreme/_edit_work/ro02"; PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
wd = f"{W}/tmp/cardclear"; os.makedirs(wd+"/m", exist_ok=True); res = {}
for it in Bd.R:
    if it["kind"] not in Bd.CARDS: continue
    rows = []; fs = []
    for k, t in enumerate(np.arange(it["t0"]+0.1, it["t1"]-0.05, 0.5)):
        g = Bd.fr(t); sg = Bd.framing_at(g); sh = Bd.shot_of(sg)
        p = f"{wd}/{it['id']}_{k:03d}.jpg"; F.frame_src(sh, (sg["src0"]+g-sg["o0"])/Bd.FPS, sg["framing"], True, True).resize((960, 540)).save(p, quality=88); fs.append((p, t, sg["framing"], sg["shot"]))
    subprocess.run([PM, wd+"/m"]+[f[0] for f in fs], check=True, capture_output=True)
    for p, t, fm, shot in fs:
        m = np.asarray(Image.open(f"{wd}/m/"+os.path.basename(p)[:-4]+".mask.png").convert("L").resize((960, 540))) > 127; lab, n = ndimage.label(m)
        if not n: continue
        m = lab == (1+int(np.argmax(ndimage.sum(m, lab, range(1, n+1))))); xs = np.where(m.sum(0) >= 3)[0]; ys = np.where(m.sum(1) >= 3)[0]
        rows.append([round(float(t), 2), fm, shot, int(xs[0])*2, int(ys[0])*2])
    left = min(r[3] for r in rows); w = min(rows, key=lambda r: r[3])
    res[it["id"]] = dict(samples=len(rows), min_left_px=left, clear_px=left-752, worst=w, hair_min_px=min(r[4] for r in rows),
                         by_shot={s: min(r[3] for r in rows if r[2] == s)-752 for s in sorted({r[2] for r in rows})})
    print(it["id"], {k: v for k, v in res[it["id"]].items()}, flush=True)
os.makedirs(f"{W}/round3/cardclear", exist_ok=True); json.dump(res, open(f"{W}/round3/cardclear/cardclear.json", "w"), indent=1)
