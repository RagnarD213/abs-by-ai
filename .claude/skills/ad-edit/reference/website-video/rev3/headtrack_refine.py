#!/usr/bin/env python3
"""Refine the head track from the DELIVERED-scale picture (ad-edit lesson 106).

The first rev-3 render put the head 7-11 px from the top edge in three TIGHT segments although the
base-sampled track (headtrack.py, 4/s on the 4K, 90-px band) had placed it 33 px down: the delivered
frames are sampled at a different phase and the QC detector's narrower band reads the crown a few
rows higher. So the base track under-reads his tallest instant by up to ~30 px of 4K in some holds.

This runs the QC's own detector on `punched.mov` (the 1080p punched picture of the CURRENT plan),
converts every head top back into 4K coordinates through that segment's crop, and stores the samples
under "refine" in headtrack.json. layout.py takes the per-segment minimum over BOTH tracks, so the
next plan anchors to the tallest instant either sampler saw. Idempotent: re-running replaces "refine".
Requires: punched.mov rendered from the plan layout.py currently computes (same CROPS).
  python3 headtrack_refine.py
"""
import json, os, subprocess, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import layout as L, beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
V=f"{HERE}/punched.mov"; FPS=4; w,h=960,540; HAIR4K=40
cards=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]
segs=list(zip(L.PUNCH,L.CROPS))
p=subprocess.Popen([FF,"-v","error","-i",V,"-vf",f"fps={FPS},scale={w}:{h}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
ref=[]; k=0
while True:
    buf=p.stdout.read(w*h*3)
    if len(buf)<w*h*3: break
    t=k/FPS; k+=1
    seg=next((s for s in segs if s[0][0]<=t<s[0][1]),None)
    if seg is None or any(a-0.6<=t<=b+0.6 for a,b in cards): continue
    (a,b,l),(x0,y0,cw,ch)=seg
    cx=int(round((L.DAN_CX-x0)/cw*w))
    fr=np.frombuffer(buf,np.uint8).reshape(h,w,3).astype(int); band=fr[:,cx-45:cx+45]
    r,g,bb=band[...,0],band[...,1],band[...,2]; skin=((r>g+15)&(g>bb)&(r>120)).mean(1)
    hit=np.where(skin[:220]>=0.30)[0]
    if len(hit)==0: continue
    row1080=int(hit[0])*(1080/h)                    # forehead row in the delivered 1080p frame
    head4k=int(round(y0+row1080*(ch/1080)-HAIR4K))  # back into 4K coordinates through this segment's crop
    ref.append([round(t,3),head4k,round(t,3)])
p.wait()
ht=json.load(open(f"{HERE}/headtrack.json"))
sig=L._sig; assert ht["keeps_sig"]==sig
vals=[v for _,v,_ in ref]; assert min(vals)>=250, f"implausible head top {min(vals)} -- a hand or a highlight above the head?"
ht["refine"]={"src":"punched.mov","fps":FPS,"keeps_sig":sig,"samples":ref}
json.dump(ht,open(f"{HERE}/headtrack.json","w"))
print(f"{len(ref)} delivered-scale samples added under 'refine'  (4K head top min {min(vals)}  median {int(np.median(vals))})")
print("per segment: base min -> merged min (4K px), shift of the crop")
for (a,b,l),(x0,y0,cw,ch) in segs:
    base=[v for t,v in L.HEAD if a<=t<b]; rf=[v for t,v,_ in ref if a<=t<b]
    if not base or not rf: continue
    print(f"  {a:7.2f}-{b:7.2f} {l:5s}  {min(base):4d} -> {min(min(base),min(rf)):4d}   ({min(min(base),min(rf))-min(base):+d} px)")
