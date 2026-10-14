#!/usr/bin/env python3
"""RA-06 round 1, outdoor rule (Dan, 2026-10-14): colour, crop and voice options on THIS ad's frames.
  colour  RA-01 grade (R1) and RA-14's three looks re-baked for C1664 (C1, C2 = Dan's RA-14 pick, C3), close + wide, beside
          approved references (RA-01, Ad 1, website video)
  crop    RA-14's three shot-size pairs converted to C1664 by body landmark (pair 2 = Dan's RA-14 pick), same two moments
  voice   mix.wav (bass lift, Dan's RA-14 pick) vs mix_nobass.wav, the cut's first 14 s (speech from 0.08 s)"""
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06"); import ra01lib as L
LK = json.load(open("colour/looks.json")); LOOKS = {k[:2]: LK[k]["filter"] for k in LK}
LOOKS = {k: LOOKS[k] for k in ("R1", "C1", "C2", "C3")}
CLOSE_T, WIDE_T = 322.0, 328.0             # source times inside hold 2 (NEAR) and hold 3 (FAR)
HAIR, WAIST = 1106, 2170                   # hair top and waistband on this roll (framing.json; RA-05 landmark)
PAIRS = {"pair 1": ((630, 1120), (738, 1312)), "pair 2": ((648, 1152), (810, 1440)), "pair 3": ((684, 1216), (846, 1504))}
CX = {"close": 1120.0, "wide": 1147.0}
FNT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
def grab(t, w, h, cx, look, out):
    x = int(round(cx - w/2)); x -= x % 2; y = int(round(HAIR - 0.04*h)); y -= y % 2
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", L.ROLL, "-frames:v", "1", "-vf",
                    f"crop={w}:{h}:{x}:{y},{L.DECODE},{look},scale=1080:1920:flags=lanczos", out], check=True)
    return out, (w, h, x, y)
def row(items, out, h=900):
    ims = []
    for path, lab in items:
        i = Image.open(path).convert("RGB"); i = i.resize((int(i.width*h/i.height), h), Image.LANCZOS)
        d = ImageDraw.Draw(i); d.rectangle((0, 0, i.width, 48), fill=(0, 0, 0)); d.text((10, 6), lab, font=FNT, fill=(255, 220, 0))
        ims.append(i)
    s = Image.new("RGB", (sum(i.width for i in ims) + 8*len(ims), h)); x = 0
    for i in ims: s.paste(i, (x, 0)); x += i.width + 8
    s.save(out, quality=88); print(out, s.size)
REF = "/Volumes/Extreme/_edit_work/ra14/round2/stills/"
NAMES = {"R1": "RA-01 grade", "C1": "C1 approved level", "C2": "C2 brighter gold (your RA-14 pick)", "C3": "C3 brighter cool"}
for shot, t, wh in (("close", CLOSE_T, PAIRS["pair 2"][0]), ("wide", WIDE_T, PAIRS["pair 2"][1])):
    items = [(grab(t, *wh, CX[shot], f, f"look/{shot}_{k}.png")[0], NAMES[k]) for k, f in LOOKS.items()]
    refs = [(REF + "ref-ra01-a.jpg", "approved RA-01"), (REF + "ref-ad1-a.jpg", "approved Ad 1")] if shot == "close" else \
           [(REF + "ref-ra01-b.jpg", "approved RA-01"), (REF + "ref-web.jpg", "approved website video")]
    row(items + refs, f"look/sheet_{shot}.jpg")
crops = {}
for p, (c, w_) in PAIRS.items():
    a, cc = grab(CLOSE_T, *c, CX["close"], LOOKS["C2"], f"look/crop_{p[-1]}_close.png")
    b, cw = grab(WIDE_T, *w_, CX["wide"], LOOKS["C2"], f"look/crop_{p[-1]}_wide.png")
    crops[p] = {"close": cc, "wide": cw}
row([(f"look/crop_{n}_{s}.png", f"pair {n} {s} {PAIRS['pair '+n][0 if s == 'close' else 1][0]}x{PAIRS['pair '+n][0 if s == 'close' else 1][1]}")
     for n in "123" for s in ("close", "wide")], "look/sheet_crops.jpg", h=800)
json.dump({"pairs": crops, "close_t": CLOSE_T, "wide_t": WIDE_T}, open("look/crops.json", "w"), indent=1)
for shot in ("close", "wide"):
    for k in LOOKS:
        a = np.asarray(Image.open(f"look/{shot}_{k}.png").convert("RGB")).astype(float)
        fb = a[160:560, 330:760]; sk = (fb[..., 0] > fb[..., 1]+12) & (fb[..., 1] > fb[..., 2]) & (fb[..., 0] > 70); f = fb[sk]
        print(shot, k, f"face luma {(0.2126*f[:,0]+0.7152*f[:,1]+0.0722*f[:,2]).mean():5.1f}")
# voice A/B: the cut's first 14 s, both mixes level matched by the chain (-14.2 LUFS each); speech from 0.08 s
for n, src in (("A_bass", "mix.wav"), ("B_no_bass", "mix_nobass.wav")):
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-t", "14", "-i", src, "-af", "afade=t=out:st=13.7:d=0.3",
                    "-c:a", "aac", "-b:a", "192k", f"look/voice_{n}.m4a"], check=True)
env = json.load(open("env.json")); print("voice clips written (window = film 0-14 s, first word at 0.08 s)")
