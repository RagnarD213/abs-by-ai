#!/usr/bin/env python3
"""RA-04 round 4: does the 16:9 CTA box (upper left, gfx16_04.py) stay clear of Dan over the CTA hold? Grabs frames of every hold the
CTA overlaps at its 16:9 crop, person mask (Apple Vision), counts person pixels inside the box + 20 px. Writes round4/cta16_check.json."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
import ra01lib as L
B = json.load(open("beats.json")); CUT = json.load(open("cut.json")); A = L.Aspect("16x9"); FPS = L.FPS
_G = json.load(open("grade.json")); GRADE = L.grade(_G["exposure"], _G["saturation"])
box = json.loads(sys.argv[1]) if len(sys.argv) > 1 else [60, 296, 60 + 560, 416]
a, b = B["cta"][0]; res = []
def src_t(t):
    for p in CUT["pieces"]:
        if p["t_in"] <= t < p["t_out"]: return p["src_in"] + t - p["t_in"]
for p in B["punch"]:
    pa, pb = p["beat"]
    if pb <= a or pa >= b: continue
    cw, ch = A.levels[p["level"]]; y = int(round(p["hair_min"] - 0.04*ch)); y -= y % 2
    x = int(round(p["cx16"] - cw/2)); x = max(0, min(2160-cw, x - x % 2))
    for t in np.linspace(max(a, pa) + 0.05, pb - 0.05, 8):
        st = src_t(t)
        if st is None: continue
        out = f"/tmp/cta16_{t:.2f}.png"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{st:.3f}", "-i", L.ROLL, "-frames:v", "1",
                        "-vf", f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{GRADE},scale=1920:1080:flags=lanczos", out], check=True)
        m = L.person_mask(Image.open(out))
        x0, y0, x1, y1 = box; sub = m[max(0, y0-20):y1+20, max(0, x0-20):x1+20]
        cols = np.where(m.any(0))[0]
        res.append(dict(t=round(float(t), 2), person_px_in_box=int(sub.sum()), person_x=[int(cols[0]), int(cols[-1])] if len(cols) else None,
                        rows_left_of_650=int(m[:, :650].any(1).sum())))
        print(res[-1], flush=True)
json.dump(dict(box=box, frames=res), open("round4/cta16_check.json", "w"), indent=1)
