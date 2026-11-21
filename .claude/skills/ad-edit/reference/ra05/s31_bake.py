#!/usr/bin/env python3
"""RA-05: RA-14 round 2's three looks re-baked for roll C1664, which is about half a stop brighter in the source than
C1667 (RA-14's LUTs put the face at 104 / 122 here against 81 / 96 there). Same tone curve, saturation and skin secondary;
only the exposure is lowered so each look lands on the SAME face brightness RA-14 showed Dan. One 65-point .cube per look."""
import json, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/colour"); import lab
N = 65
E1 = float(sys.argv[1]) if len(sys.argv) > 1 else 1.05
E2 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.40
BASE = dict(expo=E2, knee=0.45, sat=0.85, vib=0.50, contrast=0.20, pivot=0.46)
LOOKS = {
 "C1_approved_level": dict(expo=E1, knee=0.55, sat=0.85, vib=0.50, contrast=0.15, pivot=0.44, skin_rot=5, skin_sat=0.98),
 "C2_brighter_gold":  dict(BASE, skin_rot=8, skin_sat=0.96),
 "C3_brighter_cool":  dict(BASE, wb=(0.955, 1.0, 1.055), skin_rot=9, skin_sat=0.97),
}
g = np.linspace(0, 1, N); Bc, Gc, Rc = np.meshgrid(g, g, g, indexing="ij"); rgb = np.stack([Rc.ravel(), Gc.ravel(), Bc.ravel()], 1)
out = {}
for name, p in LOOKS.items():
    v = lab.grade(rgb, **p); path = f"/Volumes/Extreme/_edit_work/ra05/colour/luts/ra05_{name}.cube"
    with open(path, "w") as f:
        f.write(f'TITLE "RA-05 {name}"\nLUT_3D_SIZE {N}\n'); np.savetxt(f, v, fmt="%.6f")
    out[name] = dict(params=p, lut=path, filter=f"lut3d=file={path}:interp=tetrahedral"); print("wrote", path)
out["R1_ra01"] = dict(params=dict(expo=1.15, post_sat=1.25), lut="/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.15.cube",
                      filter="lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.15.cube:interp=tetrahedral,eq=saturation=1.25")
json.dump(out, open("/Volumes/Extreme/_edit_work/ra05/colour/looks.json", "w"), indent=1)
