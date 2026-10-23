#!/usr/bin/env python3
"""RA-09: the approved pool look (RA-14 C2 'brighter gold', Dan 2026-10-14, carried unchanged to RA-12 R2, finalized 2026-10-21)
re-baked for roll C1666, which reads about 4 % darker on skin than C1667 through the same LUT (126-129 vs 132-141).
Three options that vary one property each: A the approved look unchanged (recommended; face luma measures the same on both rolls, 115.5 vs 115.9), B a third of a stop brighter, C richer colour."""
import json, sys
import numpy as np
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09/colour"); import lab
N = 65
C2 = dict(expo=2.4, knee=0.45, sat=0.85, vib=0.50, contrast=0.20, pivot=0.46, skin_rot=8, skin_sat=0.96)
LOOKS = {
 "A_approved": dict(C2),
 "B_brighter": dict(C2, expo=2.4*1.26),
 "C_richer":   dict(C2, sat=0.95, vib=0.60),
}
g = np.linspace(0, 1, N); Bc, Gc, Rc = np.meshgrid(g, g, g, indexing="ij"); rgb = np.stack([Rc.ravel(), Gc.ravel(), Bc.ravel()], 1)
out = {}
for name, p in LOOKS.items():
    v = lab.grade(rgb, **p); path = f"/Volumes/Expansion/_edit_work/RA-09/colour/luts/ra09_{name}.cube"
    with open(path, "w") as f:
        f.write(f'TITLE "RA-09 {name}"\nLUT_3D_SIZE {N}\n'); np.savetxt(f, v, fmt="%.6f")
    out[name] = dict(params=p, lut=path, filter=f"lut3d=file={path}:interp=tetrahedral"); print("wrote", path)
out["RA12_C2"] = dict(params=C2, lut="/Volumes/Extreme/_edit_work/ra14/round2/colour/luts/ra14_C2_brighter_gold.cube",
    filter="lut3d=file=/Volumes/Extreme/_edit_work/ra14/round2/colour/luts/ra14_C2_brighter_gold.cube:interp=tetrahedral")
json.dump(out, open("/Volumes/Expansion/_edit_work/RA-09/colour/looks.json", "w"), indent=1)
