#!/usr/bin/env python3
"""Head-top track of the 4K tight cut: where is the top of Dan's head, frame by frame?

Dan on rev 2 (2026-09-02): "too much space above my head in all the shots ... crop in closer and
lower throughout." The rev-2 crops were top-anchored at a FIXED y=40 from one frame where his
head top read y~100; on other takes he stands lower, so the headroom balloons. This measures the
head top every 0.5 s (OpenCV Haar face box; head top = face top - 0.30 x face height) and reports
it per punch segment, so the crop can be anchored to the head instead of to the frame.
  python3 headtrack.py            -> headtrack.json + a per-segment report
"""
import json, os, subprocess, glob, sys
import numpy as np, cv2
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import layout as L
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; HERE=os.path.dirname(os.path.abspath(__file__))
D=f"{HERE}/pv/_ht"; os.makedirs(D,exist_ok=True)
if len(glob.glob(f"{D}/*.png"))<400:
    subprocess.run([FF,"-v","error","-y","-i",f"{HERE}/tight.mov","-vf","fps=2,scale=960:540",f"{D}/%05d.png"],check=True)
# OpenCV 5 ships no CascadeClassifier, and the doorway HEADER above Dan's head is as dark as his
# hair, so "first dark row" reads the frame top. Instead: the first row of the centre band (4K
# x 1800-2160) that is >= 30 % SKIN (r > g+15, g > b, r > 120) is the top of his forehead; his
# buzz cut adds ~40 px of 4K above that (measured on the grid frame: forehead ~140, head top ~100).
# Validated on pv/headtrack_check.jpg.
rows=[]; S=4; HAIR=40
for i,p in enumerate(sorted(glob.glob(f"{D}/*.png"))):
    im=cv2.imread(p)[:, 450:540].astype(int); b,g,r=im[...,0],im[...,1],im[...,2]
    skin=((r>g+15)&(g>b)&(r>120)).mean(1)
    hit=np.where(skin[5:300]>=0.30)[0]
    t=i/2.0
    if len(hit)==0: rows.append((t,None)); continue
    fy=int(hit[0])+5
    rows.append((t,dict(forehead=int(fy*S),head_top=int(fy*S)-HAIR,cx=1980)))
json.dump(rows,open(f"{HERE}/headtrack.json","w"))
ht=[r[1]["head_top"] for r in rows if r[1]]; cx=[r[1]["cx"] for r in rows if r[1]]
print("samples without a detection:",[r[0] for r in rows if not r[1]][:20])
print(f"{len(rows)} samples, {len(ht)} with a face   head_top min {min(ht)}  p10 {np.percentile(ht,10):.0f}  median {np.median(ht):.0f}  p90 {np.percentile(ht,90):.0f}  max {max(ht)}   cx median {np.median(cx):.0f}")
print("\nper punch segment: level, head_top min/med/max (4K px), and the DELIVERED headroom above the head in 1080p px (crop y0=40)")
for a,b,lvl in L.PUNCH:
    seg=[r[1]["head_top"] for r in rows if r[1] and a<=r[0]<b]
    if not seg: print(f"  {a:7.2f}-{b:7.2f} {lvl:5s}  (no face samples)"); continue
    x0,y0,w,h=L.LEVELS[lvl]; k=1080/h
    print(f"  {a:7.2f}-{b:7.2f} {lvl:5s}  head_top {min(seg):4d}/{int(np.median(seg)):4d}/{max(seg):4d}   headroom {int((min(seg)-y0)*k):4d}-{int((max(seg)-y0)*k):4d} px")
