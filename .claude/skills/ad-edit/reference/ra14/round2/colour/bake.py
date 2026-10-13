#!/usr/bin/env python3
"""RA-14 round 2: bake each colour candidate into ONE 65^3 .cube (S-Log3 / S-Gamut3.Cine in, Rec.709 out), so the render
applies a candidate with a single lut3d and nothing else. The maths is lab.grade(); looks.json records every number."""
import json, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14/round2/colour")
import lab
N = 65
BASE = dict(expo=2.4, knee=0.45, sat=0.85, vib=0.50, contrast=0.20, pivot=0.46)
LOOKS = {
 # the approved RA-01 brightness (face luma about 80 against 78 on RA-01's master), cleaner and with the approved skin hue
 "C1_approved_level": dict(expo=1.8, knee=0.55, sat=0.85, vib=0.50, contrast=0.15, pivot=0.44, skin_rot=5, skin_sat=0.98),
 # about one stop over round 1: an outdoor pool day. Skin held on the approved hue (rot 10 read yellow in the face shadows
 # at native size; 8 is the natural tan). RECOMMENDED.
 "C2_brighter_gold":  dict(BASE, skin_rot=8, skin_sat=0.96),
 # the daylight white-balance candidate: a cooler background (whiter wall, bluer pool), skin held gold by the secondary
 "C3_brighter_cool":  dict(BASE, wb=(0.955, 1.0, 1.055), skin_rot=9, skin_sat=0.97),
}
g = np.linspace(0, 1, N)
Bc, Gc, Rc = np.meshgrid(g, g, g, indexing="ij")          # .cube order: R fastest
rgb = np.stack([Rc.ravel(), Gc.ravel(), Bc.ravel()], 1)
out = {}
for name, p in LOOKS.items():
    v = lab.grade(rgb, **p)
    path = f"/Volumes/Extreme/_edit_work/ra14/round2/colour/luts/ra14_{name}.cube"
    with open(path, "w") as f:
        f.write(f'TITLE "RA-14 {name}"\nLUT_3D_SIZE {N}\n')
        np.savetxt(f, v, fmt="%.6f")
    out[name] = dict(params=p, lut=path, filter=f"lut3d=file={path}:interp=tetrahedral")
    print("wrote", path)
out["R1_round1"] = dict(params=dict(expo=1.15, post_sat=1.25), lut="/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.15.cube",
                        filter="lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.15.cube:interp=tetrahedral,eq=saturation=1.25")
json.dump(out, open("/Volumes/Extreme/_edit_work/ra14/round2/colour/looks.json", "w"), indent=1)
