"""RO-37 round 2 checks on the rendered pictures (build.json of each render):
  hair: clearance above the hair on every cut-out frame (VIDEO-RULES 2026-10-20: >= 20 px at 1080p)
  lower thirds: how much of Dan's silhouette is inside each strip, every 3rd frame (he stands right of it by design;
                a hand reaching in is reported with its time, a torso overlap fails)
  cuts: no take join without a framing change, no background swap under a still Dan (r2.checks)
  python3 checks.py BUILD.json [BUILD.json ...]  -> prints and writes round2/review/checks.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
import numpy as np, cv2
lay = json.load(open(f"{r2.W2}/hf/lt/layout.json")) if os.path.exists(f"{r2.W2}/hf/lt/layout.json") else {}
res = dict(hair=dict(frames=0, min=None, worst=[]), lt={}, cuts=r2.checks())
for bp in sys.argv[1:]:
    b = json.load(open(bp))
    rows = [h for h in b["hair"] if h[1] is not None]
    res["hair"]["frames"] += len(b["hair"]); res["hair"]["missing"] = res["hair"].get("missing", 0) + sum(1 for h in b["hair"] if h[1] is None)
    for h in rows:
        if h[3] == "corner": continue                     # the corner sits 470+ px down; nothing near the top
        if res["hair"]["min"] is None or h[1] < res["hair"]["min"]: res["hair"]["min"] = h[1]
    res["hair"]["worst"] = sorted(res["hair"]["worst"] + [(h[1], round(h[0] / r2.FPS, 2), h[2], h[3]) for h in rows if h[3] != "corner"])[:5]
    for run in b["runs"]:
        if run["kind"] != "presenter": continue
        for gid, L in lay.items():
            it = next(r for r in r2.LTS if r["id"] == gid)
            a, z = max(run["f0"], r2.fr(it["t0"]) + 18), min(run["f1"], r2.fr(it["t1"]) - 6)   # strip fully in
            if a >= z: continue
            x, y, w, h = run["rect"]; k = run["k"]; sx = w / r2.MW
            y0 = L["band"][0] + 8; x1 = L["strip_right"]
            worst = res["lt"].get(gid, dict(px=0, t=None))
            for q in range(a, z, 3):
                kk = run["src_k0"] + (q - run["f0"]); p = r2.mpath(run["roll"], kk)
                if not os.path.exists(p): continue
                al = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
                big = cv2.resize(al, (w, h), interpolation=cv2.INTER_NEAREST)
                X0, Y0, X1, Y1 = max(86, x), max(y0, y), min(x1, x + w), min(1016, y + h)
                n = int((big[Y0 - y:Y1 - y, X0 - x:X1 - x] > 128).sum()) if X1 > X0 and Y1 > Y0 else 0
                if n > worst["px"]: worst = dict(px=n, t=round(q / r2.FPS, 2))
            res["lt"][gid] = worst
json.dump(res, open(f"{r2.W2}/review/checks.json", "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
