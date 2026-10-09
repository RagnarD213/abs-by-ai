"""Look round stills: three moments x (camera original, A, B, C) at the camera frame, plus the punch-in size in each option's
recommended grade; measured numbers per option (frame median luma / saturation, skin median luma / saturation / hue)."""
import json, os, sys, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro07/recipe")
import frames as F
from skin import skin
from measure import stats
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round1/look"; os.makedirs(O, exist_ok=True)
PICK = ["hook.0r1", "r2a.0r1", "t3.0r1", "e2b.0r1"]; S = {s["id"]: s for s in F.S}; num = {}
for p in PICK:
    s = S[p]; f = (s["src_f0"]+s["src_f1"])//2
    for k in ("raw", "A", "B", "C"):
        im = F.frame_src(f, p, "W", look=None if k == "raw" else k, raw=(k == "raw")); im.save(f"{O}/{p}_{k}.jpg", quality=90)
        a = np.asarray(im.resize((960, 540)), np.float32)/255; st = stats(a); sk = skin(a) or {}
        num.setdefault(k, []).append(dict(luma=st["luma"], sat=st["sat"], skinY=sk.get("y"), skinS=sk.get("s"), hue=sk.get("h")))
    for k in ("A", "B", "C"): F.frame_src(f, p, "T", look=k).save(f"{O}/{p}_T-{k}.jpg", quality=90)
num = {k: {m: round(float(np.median([x[m] for x in v if x[m] is not None])), 3) for m in v[0]} for k, v in num.items()}
json.dump(num, open(f"{O}/numbers.json", "w"), indent=1); print(num)
