#!/usr/bin/env python3
"""Head-top track for the head-anchored crops (ad-edit lesson 97): where is the top of Dan's head?

Dan on rev 2 (2026-09-02): "too much space above my head in all the shots ... crop in closer and
lower throughout." Rev 2's crops were top-anchored at a FIXED y=40 from one grid frame where his
head top read y~100; across the actual cut it sits at 296-340 (this script), so every shot carried
168-232 px of headroom at 1080p. Rev 3 anchors every punch segment to its own measured head top.

REV 3: samples BASE.mov (the graded 4K, which never changes between revisions) every 0.25 s and
maps each sample onto the tight timeline through tight_cuts.json, so a re-cut needs no re-extract.
Detector, validated on pv/headtrack_check.jpg + pv/headtrack_tallest.jpg: the first row of the
centre band (4K x 1800-2160) that is >= 30 % skin (r > g+15, g > b, r > 120) is his forehead; the
buzz cut adds ~40 px of 4K above it. When he looks down the forehead fails the skin test and the
value jumps 300+ px LOW -- misses only ever go DOWN, so layout.py takes the per-segment MINIMUM.

  python3 headtrack.py    -> headtrack.json {fps, keeps_sig, samples:[[t_tight|null, head_top|null, t_base], ...]}
"""
import glob, hashlib, json, os, subprocess
import numpy as np, cv2
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=f"{HERE}/base.mov"; D=f"{HERE}/pv/_htb"; os.makedirs(D,exist_ok=True)
FPS=4; S=4; HAIR=40; BAND=(450,540)          # 960-wide frames: x 450-540 = 4K 1800-2160

tc=json.load(open(f"{HERE}/tight_cuts.json")); keeps=tc["keeps"]
sig=hashlib.md5(json.dumps(keeps).encode()).hexdigest()[:12]
dur=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",BASE],
                         capture_output=True,text=True).stdout)
if len(glob.glob(f"{D}/*.png"))<int(dur*FPS)-2:
    for f in glob.glob(f"{D}/*.png"): os.remove(f)
    subprocess.run([FF,"-v","error","-y","-i",BASE,"-vf",f"fps={FPS},scale=960:540",f"{D}/%05d.png"],check=True)
def to_tight(t):
    acc=0.0
    for a,b in keeps:
        if a<=t<=b: return round(acc+t-a,3)
        acc+=b-a
    return None                                   # inside a removed span
rows=[]
for i,p in enumerate(sorted(glob.glob(f"{D}/*.png"))):
    im=cv2.imread(p)[:, BAND[0]:BAND[1]].astype(int); b,g,r=im[...,0],im[...,1],im[...,2]
    skin=((r>g+15)&(g>b)&(r>120)).mean(1)
    hit=np.where(skin[5:300]>=0.30)[0]
    tb=i/FPS
    ht=None if len(hit)==0 else int(hit[0]+5)*S-HAIR
    rows.append([to_tight(tb),ht,round(tb,3)])
out={"src":"base.mov","fps":FPS,"keeps_sig":sig,"hair_4k":HAIR,"samples":rows}
try:
    old=json.load(open(f"{HERE}/headtrack.json"))
    if old.get("refine",{}).get("keeps_sig")==sig: out["refine"]=old["refine"]; print("kept the delivered-scale refine samples (same cut)")
except Exception: pass
json.dump(out,open(f"{HERE}/headtrack.json","w"))
on=[ht for t,ht,_ in rows if t is not None and ht is not None]
print(f"{len(rows)} base samples at {FPS}/s, {sum(1 for t,_,_ in rows if t is None)} inside removed spans, "
      f"{sum(1 for t,ht,_ in rows if t is not None and ht is None)} without a detection")
print(f"head_top on the tight timeline (4K px): min {min(on)}  p10 {np.percentile(on,10):.0f}  median {np.median(on):.0f}  "
      f"p90 {np.percentile(on,90):.0f}  max {max(on)}   (values > ~450 are look-down misses)")
print(f"headtrack.json written, keys to tight cut {sig}")
