"""Where does his arm run off the side of the upright camera frame? Every 3rd frame of each presenter run: rows of solid body touching the first or last columns of the matte, below the chin."""
import json, sys, numpy as np
sys.path.insert(0, "recipe"); import r2
from PIL import Image
runs = []
for i in range(6):
    for p in (f"r3/full/c{i}.build.json", f"r3/full_v5/c{i}.build.json"):
        try: runs += json.load(open(p))["runs"]; break
        except FileNotFoundError: pass
out = []
for r in runs:
    if r["kind"] != "presenter": continue
    L = R = 0; n = 0; first = last = None; mL = mR = 0
    for f in range(r["f0"], r["f1"], 3):
        k = r["src_k0"] + f - r["f0"]; p = r2.mpath3(r["roll"], k)
        try: a = np.asarray(Image.open(p))
        except FileNotFoundError: continue
        n += 1; l = int((a[:, 4] > 128).sum()); rr = int((a[:, -5] > 128).sum()); mL = max(mL, l); mR = max(mR, rr)
        if l > 14: L += 1
        if rr > 14: R += 1
        if l > 14 or rr > 14:
            first = first or f; last = f
    if L or R: out.append(dict(shot=r["shot"], roll=r["roll"], src_k0=r["src_k0"], framing=r["framing"], placement=r["placement"], rect=r["rect"], bg=r["bg_type"], t0=round(r["f0"] * 1001 / 30000, 1), t1=round(r["f1"] * 1001 / 30000, 1), L=L, R=R, n=n, maxL=mL, maxR=mR))
json.dump(out, open("r3/slice/hits.json", "w"), indent=0)
for o in out: print(o["t0"], o["t1"], o["shot"], o["framing"], o["placement"], o["rect"][:1], o["bg"], "L", o["L"], o["maxL"], "R", o["R"], o["maxR"], "of", o["n"])
print(len(out))
