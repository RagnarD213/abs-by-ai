#!/usr/bin/env python3
"""The round-3 look-at sheets: exactly the frames this round touched, from the DELIVERED masters.

  1  9:16  the lean hold 20.25-23.19 -- every frame of 22.10-22.30 plus the join at 20.254
  2  16:9  the five consecutive frames at each of the eight VISIBLE NEAR<->FAR joins
  3  16:9  the CTA 2 beat, composited, eight frames across it
  4  both  the end-card tail, eight frames
  5  both  the first and the last frame
Writes r3/look/*.jpg at readable size.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L

FD = 1001/30000
OUT = "r3/look"; os.makedirs(OUT, exist_ok=True)


def grabs(src, idxs, w):
    """Exact frame indices -> PIL images scaled to width w."""
    ims = []
    for n in idxs:
        p = f"{OUT}/_t.png"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", src,
                        "-vf", f"select='eq(n\\,{n})'", "-vsync", "0", "-frames:v", "1",
                        "-y", p], check=True)
        im = Image.open(p).convert("RGB")
        h = int(im.height*w/im.width)
        im = im.resize((w, h), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 150, 22], fill=(0, 0, 0))
        d.text((4, 5), f"f{n}  {n*FD:.3f}s", fill=(255, 255, 0))
        ims.append(im)
    return ims


def sheet(ims, cols, path):
    w, h = ims[0].size
    rows = (len(ims)+cols-1)//cols
    s = Image.new("RGB", (w*cols, h*rows), (20, 20, 20))
    for i, im in enumerate(ims):
        s.paste(im, (w*(i % cols), h*(i//cols)))
    s.save(path, quality=92)
    print("  ", path, s.size)


M9, M16 = "master_9x16.mp4", "master_16x9.mp4"
TL9 = json.load(open("timeline_9x16.json"))
TL16 = json.load(open("timeline_16x9.json"))
TOT = TL9["total_frames"]

# 1 -- the 9:16 lean, every frame 22.05..22.35, and the join into the hold
f0, f1 = int(round(22.05/FD)), int(round(22.35/FD))
sheet(grabs(M9, list(range(f0, f1+1)), 260), 5, f"{OUT}/9x16_lean_22s.jpg")
j = int(round(20.254/FD))
sheet(grabs(M9, [j-2, j-1, j, j+1, j+2], 300), 5, f"{OUT}/9x16_join_20.25.jpg")

# 2 -- the eight visible 16:9 NEAR<->FAR joins, five frames each
dan16 = [it for it in TL16["items"] if it["kind"] == "dan"]
vis = [b["f0"] for a, b in zip(dan16, dan16[1:]) if b["f0"] == a["f1"]]
print("  visible 16:9 joins at frames", vis)
for k, n in enumerate(vis):
    sheet(grabs(M16, [n-2, n-1, n, n+1, n+2], 420), 5, f"{OUT}/16x9_join{k}_{n}.jpg")

# 3 -- the 16:9 CTA 2 beat, composited
B = json.load(open("beats.json"))
a, b = B["cta"][1]
idx = [int(round((a + (b-a)*i/7)/FD)) for i in range(8)]
sheet(grabs(M16, idx, 480), 4, f"{OUT}/16x9_cta2.jpg")
a, b = B["cta"][0]
sheet(grabs(M16, [int(round((a + (b-a)*i/3)/FD)) for i in range(4)], 480), 4, f"{OUT}/16x9_cta1.jpg")

# 4 -- the end-card tail, both aspects
ec = next(it for it in TL9["items"] if it["name"] == "end_card")
idx = [ec["f0"] + int((ec["n"]-1)*i/7) for i in range(8)]
sheet(grabs(M9, idx, 250), 4, f"{OUT}/9x16_endcard.jpg")
sheet(grabs(M16, idx, 430), 4, f"{OUT}/16x9_endcard.jpg")

# 5 -- first and last frame
sheet(grabs(M9, [0, TOT-1], 330) + grabs(M16, [0, TOT-1], 330), 2, f"{OUT}/first_last.jpg")
os.remove(f"{OUT}/_t.png")
print("done")
