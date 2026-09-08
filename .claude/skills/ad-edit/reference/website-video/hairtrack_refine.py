#!/usr/bin/env python3
"""Refine the HAIR track from the DELIVERED-scale picture (ad-edit lesson 106, re-pointed at the hair detector).

Runs hairdet.detect on `punched.mov` (the 1080p punched picture of the CURRENT plan): the head region of each frame is
resized to 4K scale through that segment's crop and fed to the SAME detector as hairtrack.py, with the door panel's
static per-column luma from hairtrack.json. Every hair top is mapped back into 4K coordinates and stored under
"refine"; layout.py takes the per-segment minimum over BOTH tracks, so the next plan anchors to the tallest instant
either sampler saw. The plan -> render -> measure -> refine -> render loop can only move a crop UP, so it converges in
one pass. Idempotent. Requires punched.mov rendered from the plan layout.py currently computes (same CROPS).
  python3 hairtrack_refine.py
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import layout as L, beats as B, hairdet as HD
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
V=f"{HERE}/punched.mov"; FPS=8; W,H=1920,1080
cards=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]     # Dan replaced (cards + AI inserts)
segs=list(zip(L.PUNCH,L.CROPS)); hdr=np.array(L.HDR_COL,dtype=float)
p=subprocess.Popen([FF,"-v","error","-i",V,"-vf",f"fps={FPS}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
ref=[]; k=0; nmiss=0
while True:
    buf=p.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=k/FPS; k+=1
    seg=next((s for s in segs if s[0][0]<=t<s[0][1]),None)
    if seg is None or any(a-0.6<=t<=b+0.6 for a,b in cards): continue
    (a,b,l),(x0,y0,cw,ch)=seg; kk=ch/1080.0; cx=(L.DAN_CX-x0)/kk
    rx0=int(max(0,cx-420/kk)); rx1=int(min(W,cx+420/kk)); ry1=int(min(H,720/kk))
    fr=np.frombuffer(buf,np.uint8).reshape(H,W,3)[0:ry1,rx0:rx1]
    im=np.asarray(Image.fromarray(fr).resize((int(round((rx1-rx0)*kk)),int(round(ry1*kk))),Image.BILINEAR)).astype(int)
    d=HD.detect(im,cx_guess=L.DAN_CX,X0=x0+rx0*kk,hdr_col=hdr)
    if not d["valid"]: nmiss+=1; continue
    ref.append([round(t,3),int(round(y0+d["hair"])),round(t,3)])
p.wait()
ht=json.load(open(f"{HERE}/hairtrack.json")); sig=L._sig; assert ht["keeps_sig"]==sig
vals=[v for _,v,_ in ref]; assert vals and min(vals)>=150, f"implausible hair top {min(vals) if vals else None}"
ht["refine"]={"src":"punched.mov","fps":FPS,"keeps_sig":sig,"samples":ref}
json.dump(ht,open(f"{HERE}/hairtrack.json","w"))
print(f"{len(ref)} delivered-scale samples added under 'refine' ({nmiss} discarded)  (4K hair top min {min(vals)}  median {int(np.median(vals))})")
print("per segment: base min -> merged min (4K px), shift of the crop")
moved=0
for (a,b,l),(x0,y0,cw,ch) in segs:
    base=[v for t,v in L.HAIR if a<=t<b]; rf=[v for t,v,_ in ref if a<=t<b]
    if not base or not rf: continue
    m=min(min(base),min(rf)); moved+=(m<min(base))
    print(f"  {a:7.2f}-{b:7.2f} {l:5s}  {min(base):4d} -> {m:4d}   ({m-min(base):+d} px)")
print(f"{moved} segment(s) anchor higher after the refine")
