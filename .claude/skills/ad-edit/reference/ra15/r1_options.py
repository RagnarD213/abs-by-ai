#!/usr/bin/env python3
"""RA-15 round 1 look options (outdoor rule, Dan 2026-10-14): three colour looks and three framing pairs on the SAME two
moments of C1668, 1080x1920. Close moment src 86.0 s ("a single photo of you"), wide moment src 101.0 s ("where you want to
be"). Crops follow the hair rule: y0 = lowest hair top within +-1.5 s minus 4 % of the crop height, x centred on the head."""
import json, subprocess, sys
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15"); import ra01lib as L
LOOKS = json.load(open("colour/looks.json")); FC = json.load(open("framing_choice.json"))
SAM = json.load(open("framing.json"))["samples"]
MOM = {"close": 86.0, "wide": 101.0}
ST = "round1/stills"; meta = {"moments": MOM, "pairs": {}, "looks": {}}
def full(look, t):
    p = f"look/full/{look}_{t}.png"
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t}", "-i", L.ROLL, "-frames:v", "1",
                    "-vf", f"{L.DECODE},{LOOKS[look]['filter']}", p], check=True)
    return Image.open(p).convert("RGB")
def cut(im, t, cw, ch):
    near = [s for s in SAM if abs(s["src"] - t) <= 1.5]; s0 = min(SAM, key=lambda s: abs(s["src"] - t))
    y0 = int(round(min(s["hair"] for s in near) - 0.04*ch)); x0 = int(round(s0["cx"] - cw/2)); x0 = max(0, min(2160-cw, x0))
    return im.crop((x0, y0, x0+cw, y0+ch)).resize((1080, 1920), Image.LANCZOS), (x0, y0)
F = {k: full(k, t) for k in ("C1_approved_level", "C2_brighter_gold", "C3_brighter_cool") for t in [0]} if False else None
for which, t in MOM.items():
    ims = {k: full(k, t) for k in ("C1_approved_level", "C2_brighter_gold", "C3_brighter_cool")}
    key = "NEAR" if which == "close" else "FAR"
    for fid, p in FC["options"].items():
        im, (x0, y0) = cut(ims["C2_brighter_gold"], t, *p[key]); im.save(f"{ST}/{fid}-{which}.jpg", quality=92)
        meta["pairs"].setdefault(fid, {"name": p["name"]})[which] = dict(crop=p[key], x0=x0, y0=y0, enlarge=round(1080/p[key][0], 2))
    for look, im0 in ims.items():
        im, _ = cut(im0, t, *FC["options"]["F2"][key]); im.save(f"{ST}/K-{look}-{which}.jpg", quality=92)
for w in ("close", "wide"):
    Image.open(f"/Volumes/Extreme/_edit_work/ra14/round2/stills/K-C2_brighter_gold-{w}.jpg").convert("RGB").save(f"{ST}/ref-ra14-approved-{w}.jpg", quality=92)
json.dump(meta, open(f"{ST}/options_meta.json", "w"), indent=1); print(json.dumps(meta["pairs"], indent=0))
