#!/usr/bin/env python3
"""RA-07 round 2 look check: the RA-14 (Cheat Code) framing and colour carried to roll C1664, judged beside RA-14's
approved round 3 frames (Dan's picks: F2 wider framing, C2 brighter golden skin).

Framing candidates (both on the 9:16 lattice w = 18m, h = 32m, y0 = hold's hair_min - 4 % of crop height):
  A  head-size conversion (handoff): close 738x1312, wide 918x1632  (RA-14 x1.276, his head 370 vs 290 px)
  B  body-landmark conversion (RA-05 lesson 3): close 648x1152, wide 810x1440 (same distance under the waistband as RA-14)
Colour candidates:
  L14  RA-14's baked C2 LUT as is (made for C1667, where his face sat 1.5 stops under)
  L05  the same look re-baked for C1664 by RA-05 (exposure 1.6 instead of 2.4, every other param identical)
"""
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
W7 = "/Volumes/Extreme/_edit_work/ra07"
CUT = json.load(open(f"{W7}/cut.json")); TRK = json.load(open(f"{W7}/framing.json"))["samples"]
LUTS = {"L14": "/Volumes/Extreme/_edit_work/ra14/round2/colour/luts/ra14_C2_brighter_gold.cube",
        "L05": "/Volumes/Extreme/_edit_work/ra05/colour/luts/ra05_C2_brighter_gold.cube"}
FR = {"A": {"close": (738, 1312), "wide": (918, 1632)}, "B": {"close": (648, 1152), "wide": (810, 1440)}}
# two moments of this ad: close on "firing their personal trainer" (6.5 s), wide on "Because AI can do three things" (10.3 s)
MOM = {"close": 6.5, "wide": 10.3}
OUT = f"{W7}/round2/look"


def src_of(t):
    p = next(p for p in CUT["pieces"] if p["t_in"] <= t < p["t_out"])
    return p["src_in"] + (t - p["t_in"])


def hold(t):
    s = [x for x in TRK if t - 1.5 <= x["t"] <= t + 1.5]
    c = min(s, key=lambda x: abs(x["t"] - t))
    return min(x["hair"] for x in s), c["cx"]


res = {}
for shot, t in MOM.items():
    hm, cx = hold(t)
    for fk, fv in FR.items():
        cw, ch = fv[shot]
        y = int(round(hm - 0.04*ch)); y -= y % 2; x = int(round(cx - cw/2)); x -= x % 2
        for lk, lut in LUTS.items():
            o = f"{OUT}/{shot}_{fk}_{lk}.png"
            subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{src_of(t):.4f}", "-i", L.ROLL, "-frames:v", "1",
                            "-vf", f"crop={cw}:{ch}:{x}:{y},{L.DECODE},lut3d=file={lut}:interp=tetrahedral,scale=1080:1920:flags=lanczos",
                            o], check=True)
            res[f"{shot}_{fk}_{lk}"] = dict(crop=[cw, ch, x, y], bottom_src=y + ch, hair_min=hm)

# RA-14 approved round 3 frames: hold dan01 is close (NEAR), dan02 wide (FAR)
R14 = "/Volumes/Extreme/_edit_work/ra14/round3/seg"
for shot, seg in (("close", "dan02"), ("wide", "dan03")):
    pass
B14 = json.load(open("/Volumes/Extreme/_edit_work/ra14/beats_r3.json"))
refs = {}
for i, p in enumerate(B14["punch"]):
    k = "close" if p["level"] == "NEAR" else "wide"
    if k in refs or p["beat"][1] - p["beat"][0] < 2.0: continue
    refs[k] = f"dan{i:02d}"
for shot, seg in refs.items():
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", "1.0", "-i", f"{R14}/{seg}.mp4", "-frames:v", "1",
                    "-vf", "scale=in_color_matrix=bt709:in_range=tv", f"{OUT}/{shot}_RA14.png"], check=True)


def face(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    # skin pixels in the upper half, centre band: his face
    fb = a[150:700, 280:800]
    sk = (fb[..., 0] > fb[..., 1] + 12) & (fb[..., 1] > fb[..., 2]) & (fb[..., 0] > 70)
    f = fb[sk]; fy = 0.2126*f[:, 0] + 0.7152*f[:, 1] + 0.0722*f[:, 2]
    import colorsys
    return dict(face_luma=round(float(fy.mean()), 1), RG=round(float(f[:, 0].mean()/f[:, 1].mean()), 3),
                GB=round(float(f[:, 1].mean()/f[:, 2].mean()), 3), skin_px=int(sk.sum()))


meas = {}
for shot in MOM:
    names = [f"{shot}_RA14"] + [f"{shot}_{fk}_{lk}" for fk in FR for lk in LUTS]
    ims = [Image.open(f"{OUT}/{n}.png").convert("RGB").resize((432, 768), Image.LANCZOS) for n in names]
    sh = Image.new("RGB", (432*len(ims), 800), (0, 0, 0)); d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(zip(names, ims)):
        sh.paste(im, (432*i, 0)); m = face(f"{OUT}/{n}.png"); meas[n] = m
        d.text((432*i + 6, 772), f"{n}  face {m['face_luma']}  R/G {m['RG']}", fill=(255, 255, 0))
    sh.save(f"{OUT}/sheet_{shot}.jpg", quality=88)
json.dump(dict(crops=res, faces=meas, refs=refs), open(f"{OUT}/lookcheck.json", "w"), indent=1)
for k, v in meas.items(): print(k, v)
