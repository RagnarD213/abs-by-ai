#!/usr/bin/env python3
"""Hair-top track for the hair-anchored crops (ad-edit lesson 107) -- REV 4.

Samples BASE.mov (the graded 4K, unchanged between revisions) at 8/s, runs hairdet.detect on the 4K head region
(x 1430-2530, y 0-900, native scale -- never a downscaled frame), and maps every sample onto the tight timeline
through tight_cuts.json (a re-cut needs no re-extract). Writes hairtrack.json:
  {fps, keeps_sig, hdr_col:[4K x 1430..2530 -> door-panel luma], samples:[[t_tight|null, hair|null, t_base, skin, cx, climb, valid], ...]}
and the NATIVE-scale proof sheet pv/hairtrack_proof.jpg: the 8 tallest valid samples + 4 at the median, contrast-
stretched 4K crops with a 50-px grid and the detected hair line -- LOOK at it before anything renders.
  python3 hairtrack.py
"""
import hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import hairdet as HD
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=f"{HERE}/base.mov"; PV=f"{HERE}/pv"; os.makedirs(PV,exist_ok=True)
FPS=8; X0,Y0,CW,CH=1430,0,1100,900
tc=json.load(open(f"{HERE}/tight_cuts.json")); keeps=tc["keeps"]
sig=hashlib.md5(json.dumps(keeps).encode()).hexdigest()[:12]
def to_tight(t):
    acc=0.0
    for a,b in keeps:
        if a<=t<=b: return round(acc+t-a,3)
        acc+=b-a
    return None
def frames(video,fps,x0,y0,w,h):
    p=subprocess.Popen([FF,"-v","error","-i",video,"-vf",f"fps={fps},crop={w}:{h}:{x0}:{y0}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
    k=0
    while True:
        buf=p.stdout.read(w*h*3)
        if len(buf)<w*h*3: break
        yield k/fps, np.frombuffer(buf,np.uint8).reshape(h,w,3).astype(int); k+=1
    p.wait()
if __name__=="__main__":
    rows=[]; hdr=[]
    for tb,im in frames(BASE,FPS,X0,Y0,CW,CH):
        d=HD.detect(im,1980,X0)
        Y=0.299*im[...,0]+0.587*im[...,1]+0.114*im[...,2]
        hdr.append(np.median(Y[100:180],axis=0))
        rows.append([to_tight(tb), d["hair"] if d["valid"] else None, round(tb,3), d["skin"], d["cx"], d["climb"], d["valid"]])
        if len(rows)%400==0: print(f"  {len(rows)} samples ({tb:.0f}s)",flush=True)
    hdr_col=np.median(np.stack(hdr),axis=0)          # the static per-column door-panel luma, 4K x = X0 + index
    full=np.zeros(3840); full[X0:X0+CW]=hdr_col; full[:X0]=hdr_col[0]; full[X0+CW:]=hdr_col[-1]
    out={"src":"base.mov","fps":FPS,"keeps_sig":sig,"detector":"hairdet.py","hdr_col":[round(float(v),2) for v in full],"samples":rows}
    try:
        old=json.load(open(f"{HERE}/hairtrack.json"))
        if old.get("refine",{}).get("keeps_sig")==sig and old.get("refine",{}).get("src")=="punched.mov": out["refine"]=old["refine"]; print("kept the delivered-scale refine samples (same cut)")
    except Exception: pass
    json.dump(out,open(f"{HERE}/hairtrack.json","w"))
    on=[(t,h,tb,cl) for t,h,tb,_,_,cl,v in rows if t is not None and h is not None]
    miss=[(t,tb,why) for t,h,tb,_,_,cl,v in rows if t is not None and h is None for why in [("short" if (cl or 0)<HD.CLIMB[0] else "long")]]
    hs=np.array([h for _,h,_,_ in on]); cl=np.array([c for *_,c in on])
    print(f"{len(rows)} base samples at {FPS}/s, {sum(1 for r in rows if r[0] is None)} inside removed spans, "
          f"{len(on)} valid on the tight timeline, {len(miss)} discarded ({sum(1 for m in miss if m[2]=='short')} short climbs, {sum(1 for m in miss if m[2]=='long')} long)")
    print(f"hair top (4K px): min {hs.min()}  p10 {np.percentile(hs,10):.0f}  median {np.median(hs):.0f}  p90 {np.percentile(hs,90):.0f}  max {hs.max()}")
    print(f"climb (hair top -> skin start): min {cl.min()}  median {np.median(cl):.0f}  max {cl.max()}")
    print(f"door-panel header luma over the band: {np.median(hdr_col[1900-X0:2060-X0]):.1f}")
    # the longest run of consecutive misses on the tight timeline (a segment with no valid sample fails the build)
    run=best=0
    for t,h,*_ in rows:
        if t is None: continue
        run=run+1 if h is None else 0; best=max(best,run)
    print(f"longest run of discarded samples: {best} ({best/FPS:.2f} s)")
    # proof sheet: 8 tallest + 4 median, exact 4K grabs
    srt=sorted(on,key=lambda r:r[1]); picks=srt[:8]+srt[len(srt)//2-2:len(srt)//2+2]
    items=[]
    for t,h,tb,c in picks:
        raw=subprocess.run([FF,"-v","error","-ss",f"{tb:.3f}","-i",BASE,"-frames:v","1","-vf",f"crop={CW}:{CH}:{X0}:{Y0}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        im=np.frombuffer(raw[:CW*CH*3],np.uint8).reshape(CH,CW,3).astype(int); d=HD.detect(im,1980,X0)
        items.append((f"tight {t:.2f}s base {tb:.2f}s  hair {d['hair']} skin {d['skin']} climb {d['climb']} {'VALID' if d['valid'] else 'MISS'}",im,X0,d))
    HD.proof_sheet(items,f"{PV}/hairtrack_proof.jpg")
    print(f"proof sheet {PV}/hairtrack_proof.jpg (8 tallest + 4 median, native 4K scale) -- LOOK AT IT")
    print(f"hairtrack.json written, keyed to tight cut {sig}")
