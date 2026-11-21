#!/usr/bin/env python3
"""RA-06 round 3: one LUT per split-screen roll (C2 look, Dan's pick, at a per-roll exposure and midtone gamma), chosen from
s06b's bake so Dan's body reads at least as bright as on the talking shots (torso skin ~110) without blowing the pool deck.
Writes round3/split/luts/<roll>.cube + split_luts.json, and a measurement line per panel."""
import json, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06/colour")
import ra01lib as L, lab
O = "/Volumes/Extreme/_edit_work/ra06/round3/split"
R = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
P = dict(json.load(open("/Volumes/Extreme/_edit_work/ra06/grade.json"))["params"])
PICK = {"C1683": dict(expo=float(sys.argv[1]) if len(sys.argv) > 1 else 3.2, gamma=float(sys.argv[2]) if len(sys.argv) > 2 else 1.12),
        "C1682": dict(expo=float(sys.argv[3]) if len(sys.argv) > 3 else 2.9, gamma=float(sys.argv[4]) if len(sys.argv) > 4 else 1.05),
        "C1677": dict(expo=float(sys.argv[5]) if len(sys.argv) > 5 else 1.5, gamma=1.0)}
TEST = {"C1683": (136.5, (1920, 1080, 1066, 1000), (200, 200, 470, 350)), "C1682": (17.0, (2560, 1440, 1000, 560), (550, 380, 820, 500)),
        "C1677": (138.8, (2560, 1440, 1146, 270), (275, 110, 460, 290))}
N = 33
g = np.linspace(0, 1, N); Bc, Gc, Rc = np.meshgrid(g, g, g, indexing="ij"); rgb = np.stack([Rc.ravel(), Gc.ravel(), Bc.ravel()], 1)
out = {}
for roll, pk in PICK.items():
    v = lab.grade(rgb, **dict(P, **pk)); path = f"{O}/luts/{roll}.cube"
    with open(path, "w") as f:
        f.write(f'TITLE "RA-06 R3 split {roll}"\nLUT_3D_SIZE {N}\n'); np.savetxt(f, v, fmt="%.6f")
    t, (w, h, x, y), (x0, y0, x1, y1) = TEST[roll]
    b = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t}", "-i", f"{R}/{roll}.MP4", "-vf",
                        f"crop={w}:{h}:{x}:{y},{L.DECODE},lut3d=file={path}:interp=tetrahedral,scale=1032:580,format=rgb24",
                        "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(b, np.uint8).reshape(580, 1032, 3); c = a[y0:y1, x0:x1].astype(int)
    m = (c[..., 0] > c[..., 1]) & (c[..., 1] > c[..., 2]) & (c[..., 0] - c[..., 2] > 25)
    yy = 0.2126*c[..., 0] + 0.7152*c[..., 1] + 0.0722*c[..., 2]
    out[roll] = dict(params=pk, lut=path, filter=f"lut3d=file={path}:interp=tetrahedral", body_skin_median=round(float(np.median(yy[m])), 1),
                     clipped_pct=round(float((a.max(2) >= 250).mean()*100), 1))
    print(roll, out[roll]["params"], "body skin", out[roll]["body_skin_median"], "clipped %", out[roll]["clipped_pct"])
json.dump(dict(out, _rule="talking-head torso skin measures 107-113 on the round 1 draft; panels aim at or above it"),
          open(f"{O}/split_luts.json", "w"), indent=1)
