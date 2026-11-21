#!/usr/bin/env python3
"""RA-06: grade check for the split-screen exercise clips (8/28 landscape B-roll rolls) against the presenter in the
approved C2 look. All B-roll is colour corrected to sit with the film's look before Dan sees it (VIDEO-RULES 2026-10-11).
Writes look/split_check.jpg: presenter wide shot beside each clip, plus skin luma per image."""
import json, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
import ra01lib as L
R = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
G = json.load(open("grade.json"))["filter"]
EXTRA = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
def grab(roll, t, vf):
    p = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", str(t), "-i", f"{R}/{roll}.MP4", "-frames:v", "1",
                        "-vf", f"{L.DECODE},{G}{(',' + vf) if vf else ''},format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True)
    return p.stdout
def img(roll, t, w, h, vf=""):
    return Image.frombytes("RGB", (w, h), grab(roll, t, vf))
def skin(a):
    a = np.asarray(a).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (r > g + 8) & (g > b) & (r > 60) & (r - b < 110)
    return round(float((0.2126*r + 0.7152*g + 0.0722*b)[m].mean()), 1), round(float(m.mean()*100), 2)
pres = img("C1664", 330, 2160, 3840).crop((735, 1060, 735+810, 1060+1440)).resize((405, 720))
tiles = [("presenter FAR", pres)]
for roll, t in (("C1682", 14.0), ("C1677", 125.0), ("C1683", 140.0)):
    vf = EXTRA.get(roll, "")
    im = img(roll, t, 3840, 2160, vf)
    tiles.append((f"{roll} {vf or 'C2 as is'}", im.resize((1280, 720))))
W = sum(t[1].width for t in tiles) + 10*len(tiles); sheet = Image.new("RGB", (W, 720), (0, 0, 0)); x = 0
for name, im in tiles:
    sheet.paste(im, (x, 0)); print(f"{name:<40} skin luma {skin(im)}"); x += im.width + 10
sheet.save("look/split_check.jpg", quality=90)
