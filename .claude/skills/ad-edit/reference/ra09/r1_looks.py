#!/usr/bin/env python3
"""RA-09 round 1 colour options: A the approved pool look (RA-14 C2, carried to RA-12 R2, finalized 10-21), B a third of a stop brighter,
C richer colour, on the same two moments at the plan's own crops (close = hold 0 NEAR, wide = hold 1 FAR), beside RA-14's approved stills."""
import json, subprocess, sys
from PIL import Image
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09"); import ra01lib as L
LOOKS = json.load(open("colour/looks.json")); PL = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
A = L.Aspect("9x16"); SP = CUT["speed"]
def src_t(t):
    p = next(p for p in CUT["pieces"] if p["t_in"] <= t < p["t_out"]); return p["src_in"] + (t - p["t_in"]) * SP
MOM = {"close": (0, 3.30), "wide": (1, 6.60)}
meta = {}
for which, (hi, t) in MOM.items():
    pu = PL["punch"][hi]; cw, ch = A.levels[pu["level"]]
    k = int(round((t - pu["beat"][0]) * L.FPS)); cx = pu["track"][min(k, len(pu["track"]) - 1)]
    x0 = int(round(cx - cw / 2)); y0 = int(round(pu["hair_min"] - 0.04 * ch)); s = src_t(t)
    for name in ("A_approved", "B_brighter", "C_richer"):
        f = LOOKS[name]["filter"]; out = f"r1/options/look-{name}-{which}.jpg"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{s:.4f}", "-i", L.ROLL, "-frames:v", "1",
                        "-vf", f"crop={cw}:{ch}:{x0}:{y0},{L.DECODE},{f},scale=1080:1920:flags=lanczos", "-q:v", "2", out], check=True)
    Image.open(f"/Volumes/Extreme/_edit_work/ra14/round2/stills/K-C2_brighter_gold-{which}.jpg").convert("RGB").save(f"r1/options/look-ref-ra14-approved-{which}.jpg", quality=92)
    meta[which] = dict(film_t=t, src_t=round(s, 3), level=pu["level"], crop=[cw, ch, x0, y0])
json.dump(meta, open("r1/options/looks_meta.json", "w"), indent=1); print(meta)
