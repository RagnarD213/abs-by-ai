#!/usr/bin/env python3
"""RA-06 round 3: brighter split-screen panels (Dan: "This footage looks very dark").
Bakes the approved C2 look (grade.json params) at several exposures per B-roll roll, renders each panel's crop at one
frame, measures Dan's skin luma on the panel, and writes a sheet beside talking-head stills of the round 1 draft.
  python3 s06b_split_bake.py            -> round3/split/luts/*.cube, round3/split/bake_sheet.jpg, bake.json
"""
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06/colour")
import ra01lib as L, lab
O = "/Volumes/Extreme/_edit_work/ra06/round3/split"
R = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
P = dict(json.load(open("/Volumes/Extreme/_edit_work/ra06/grade.json"))["params"])
EXPOS = [float(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else "1.6,2.2,2.8,3.4".split(","))]
PANELS = [("C1683", 136.5, (1920, 1080, 1066, 1000), "Spiderman"), ("C1682", 17.0, (2560, 1440, 1000, 560), "Toe"),
          ("C1677", 138.8, (2560, 1440, 1146, 270), "Vacuum")]
N = 33
g = np.linspace(0, 1, N); Bc, Gc, Rc = np.meshgrid(g, g, g, indexing="ij"); rgb = np.stack([Rc.ravel(), Gc.ravel(), Bc.ravel()], 1)
import os; os.makedirs(f"{O}/luts", exist_ok=True)
luts = {}
for e in EXPOS:
    p = dict(P, expo=e); v = lab.grade(rgb, **p); path = f"{O}/luts/c2_e{e:.2f}.cube"
    with open(path, "w") as f:
        f.write(f'TITLE "RA-06 split C2 expo {e}"\nLUT_3D_SIZE {N}\n'); np.savetxt(f, v, fmt="%.6f")
    luts[e] = path

def grab(src, t, vf, wh):
    b = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-vf", vf + ",format=rgb24", "-frames:v", "1",
                        "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3)

def skin(a):
    r, gg, b = [a[..., i].astype(int) for i in range(3)]
    m = (r > gg) & (gg > b) & (r - b > 25) & (r > 60) & (r < 250)
    y = 0.2126*r + 0.7152*gg + 0.0722*b
    return float(np.median(y[m])) if m.sum() > 200 else -1, int(m.sum())

PW, PH = 1032, 580
rows, meas = [], {}
for roll, t, (w, h, x, y), name in PANELS:
    row = []
    for e in EXPOS:
        vf = f"crop={w}:{h}:{x}:{y},{L.DECODE},lut3d=file={luts[e]}:interp=tetrahedral,scale={PW}:{PH}:flags=lanczos"
        a = grab(f"{R}/{roll}.MP4", t, vf, (PW, PH)); s = skin(a); meas[f"{name} e{e}"] = s
        im = Image.fromarray(a.copy()); ImageDraw.Draw(im).text((12, 10), f"{name} expo {e}  skin {s[0]:.0f}", fill=(255, 255, 0))
        row.append(im)
    rows.append(row)
# talking-head references from the delivered round 1 draft (C2 look as Dan approved it)
ref = []
for t in (3.0, 9.0, 44.5):
    a = grab("/Volumes/Extreme/_edit_work/ra06/draft_9x16.mp4", t, L.DECODE, (1080, 1920))
    s = skin(a[300:1500]); meas[f"talk {t}"] = s
    im = Image.fromarray(a.copy()); ImageDraw.Draw(im).text((20, 20), f"talking head t={t} skin {s[0]:.0f}", fill=(255, 255, 0)); ref.append(im)
cols = len(EXPOS)
S = Image.new("RGB", (PW*cols + 1080*3//2 + 20, max(PH*3, 1920*3//4)), "white")
for r, row in enumerate(rows):
    for c, im in enumerate(row): S.paste(im, (c*PW, r*PH))
for k, im in enumerate(ref[:2]):
    S.paste(im.resize((540, 960)), (PW*cols + 20 + (k % 2)*540, 0))
S.save(f"{O}/bake_sheet.jpg", quality=88)
json.dump({"luts": {str(k): v for k, v in luts.items()}, "skin_median_luma": meas}, open(f"{O}/bake.json", "w"), indent=1)
for k, v in meas.items(): print(f"{k:<16} skin {v[0]:6.1f}  px {v[1]}")

# body-only boxes (panel px, measured off bake_sheet.jpg): the skin median inside the box
BOX = {"Spiderman": (200, 200, 470, 350), "Toe": (550, 380, 820, 500), "Vacuum": (275, 110, 460, 290)}
