"""Round 5, before the full render: scan every tight (X) and medium (T) picture segment for a lean the per-shot `active`
flag misses (he bends and points at the equipment inside an otherwise still shot). Uses the 2-per-second person masks
framing.py already made. Per sample: hair top and head centre in the segment's own crop, scaled to the 1080 frame.
Flags a sample whose head drops > 90 px below the segment's median, or whose head centre sits > 17 % of the frame from
the segment's median, or whose hair is within 10 px of the top. usage: leanscan.py [X|XT]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import build as Bd
W = Bd.W; FPS = Bd.FPS; R = json.load(open(f"{W}/rolls.json")); sizes = sys.argv[1] if len(sys.argv) > 1 else "X"
full = [(Bd.fr(it["t0"]), Bd.fr(it["t1"])) for it in Bd.R if it["kind"] in Bd.FULL]
out = []
for sg in Bd.all_segments():
    if sg["framing"] not in sizes or sg["vis"] <= 0: continue
    roll = sg["roll"]; d = f"{W}/mask/{roll}"; t0 = json.load(open(d + "/done"))["t0"]; cw, ch, cx0, cy0 = sg["crop"]; z = 1080/ch
    rows = []
    for o in range(sg["o0"], sg["o1"]):
        if any(a <= o < b for a, b in full): continue
        lt = (sg["src0"] + o - sg["o0"] - R[roll]["f0"])/FPS; k = int((lt - t0)*2)
        if rows and rows[-1][0] == k: continue
        mp = f"{d}/m/f_{k+1:05d}.mask.png"
        if not os.path.exists(mp): continue
        m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
        ys = np.where(m.sum(1) >= 3)[0]
        if not len(ys): continue
        top = ys[0]; h = max(8, int((ys[-1]-top)*0.12)); hx = np.where(m[top:top+h].any(0))[0]
        rows.append((k, o/FPS, (top*2 - cy0)*z, ((hx[0]+hx[-1])*1.0 - cx0)*z if len(hx) else None))
    if len(rows) < 2: continue
    tops = np.array([r[2] for r in rows]); cxs = np.array([r[3] for r in rows if r[3] is not None]); mt, mc = np.median(tops), np.median(cxs)
    bad = [(round(r[1], 1), int(r[2] - mt), None if r[3] is None else int(r[3] - mc), int(r[2])) for r in rows if r[2] - mt > 90 or (r[3] is not None and abs(r[3] - mc) > 0.17*1920) or r[2] < 10]
    if bad: out.append(dict(key=sg["key"], shot=sg["shot"], size=sg["framing"], t0=round(sg["o0"]/FPS, 2), t1=round(sg["o1"]/FPS, 2), median_top=int(mt), flags=bad))
json.dump(out, open(f"{W}/round5/logs/leanscan_{sizes}.json", "w"), indent=1)
for r in out:
    print(f"{r['key']:14s} {r['size']} {r['t0']:7.2f}-{r['t1']:7.2f} hair {r['median_top']:3d}px  " + " ".join(f"{t}s(drop {a}, side {b}, top {c})" for t, a, b, c in r["flags"][:8]) + (" ..." if len(r["flags"]) > 8 else ""))
print(len(out), "segments flagged of", sum(1 for s in Bd.all_segments() if s["framing"] in sizes))
