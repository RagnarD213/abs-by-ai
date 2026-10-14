#!/usr/bin/env python3
"""RA-05 look check: the four colour candidates (RA-01's approved grade + RA-14 round 2's three baked looks) on this
roll's own frames, at the close and wide sizes, beside approved references. Input-seek single frames."""
import subprocess, sys
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05"); import ra01lib as L
import json
LOOKS = {k[:2]: v["filter"] for k, v in json.load(open("colour/looks.json")).items()}
LOOKS = {k: LOOKS[k] for k in ("R1", "C1", "C2", "C3")}
SHOTS = {"close": (212.0, "crop=648:1152:794:1077"), "wide": (250.0, "crop=810:1440:713:1065")}
for k, f in LOOKS.items():
    for s, (t, crop) in SHOTS.items():
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", L.ROLL, "-frames:v", "1",
                        "-vf", f"{crop},{L.DECODE},{f},scale=1080:1920:flags=lanczos", f"look/{s}_{k}.png"], check=True)
R = "/Volumes/Extreme/_edit_work/ra14/round2/stills/"
def row(names, out):
    ims = [Image.open(n).convert("RGB") for n in names]; h = 900
    ims = [i.resize((int(i.width*h/i.height), h), Image.LANCZOS) for i in ims]
    s = Image.new("RGB", (sum(i.width for i in ims), h)); x = 0
    for i in ims: s.paste(i, (x, 0)); x += i.width
    s.save(out, quality=88); print(out, s.size)
row([f"look/close_{k}.png" for k in LOOKS] + [R+"ref-ra01-a.jpg", R+"ref-ad1-a.jpg"], "look/sheet_close.jpg")
row([f"look/wide_{k}.png" for k in LOOKS] + [R+"ref-ra01-b.jpg", R+"ref-web.jpg"], "look/sheet_wide.jpg")

import numpy as np
for s_ in ("close", "wide"):
    for k in LOOKS:
        a = np.asarray(Image.open(f"look/{s_}_{k}.png").convert("RGB")).astype(float)
        y = 0.2126*a[..., 0]+0.7152*a[..., 1]+0.0722*a[..., 2]
        fb = a[180:520, 330:760] if s_ == "close" else a[130:400, 400:690]
        sk = (fb[..., 0] > fb[..., 1]+12) & (fb[..., 1] > fb[..., 2]) & (fb[..., 0] > 70); f = fb[sk]
        fy = 0.2126*f[:, 0]+0.7152*f[:, 1]+0.0722*f[:, 2]
        print(s_, k, f"face luma {fy.mean():5.1f}  R/G {f[:,0].mean()/f[:,1].mean():.2f}  G/B {f[:,1].mean()/f[:,2].mean():.2f}  frame p50 {np.percentile(y,50):.0f} p99 {np.percentile(y,99):.0f}  over 250: {(y>250).mean()*100:.2f}%")
