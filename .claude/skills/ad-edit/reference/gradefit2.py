#!/usr/bin/env python3
"""Fit STAGE 2 of the grade for a roll: raw -> (shared stage-1) -> fitted stage-2 -> ref.

Rule 27/39: per-channel percentile fit on SKIN pixels only; black point from each
video's own global p1; nothing else (no eq=contrast, no eq=saturation on top).
  gradefit2.py <raw> <ref> <out.txt> <raw_times> <ref_times> <stage1_filter>
"""
import subprocess, sys
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
OUR,REF,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
OUR_T=[float(x) for x in sys.argv[4].split(",")]
REF_T=[float(x) for x in sys.argv[5].split(",")]
G1=sys.argv[6]
def frames(path,times,vf=""):
    out=[]
    for t in times:
        ch=(vf+"," if vf else "")+"scale=320:180"
        raw=subprocess.run([FF,"-v","error","-ss",str(t),"-i",path,"-vframes","1","-vf",ch,
                            "-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        if len(raw)<180*320*3: continue
        f=np.frombuffer(raw[:180*320*3],dtype=np.uint8).reshape(180,320,3).astype(np.float32)
        if f.reshape(-1,3).std(0).mean()>22 and f.mean()<190: out.append(f)
    return out
def skin(fs):
    a=np.concatenate([f.reshape(-1,3) for f in fs]); r,g,b=a[:,0],a[:,1],a[:,2]
    return a[(r>g+8)&(g>b+4)&(r>55)&(r<250)&(r-b>18)&(r-b<130)]
def darkp(fs,p=1): return np.percentile(np.concatenate([f.reshape(-1,3) for f in fs]),p,axis=0)
PS=(10,30,50,70,90)
rf,of=frames(REF,REF_T),frames(OUR,OUR_T,G1)
rs,os_=skin(rf),skin(of)
rp={c:np.percentile(rs[:,i],PS) for i,c in enumerate("rgb")}
op={c:np.percentile(os_[:,i],PS) for i,c in enumerate("rgb")}
rd,od=darkp(rf),darkp(of)
print(f"frames ref {len(rf)} ours {len(of)};  skin px ref {len(rs)} ours {len(os_)}")
for j,p in enumerate(PS):
    print(f"  p{p:<3}"+" ".join(f"  {c}:{rp[c][j]:5.0f}/{op[c][j]:<5.0f}" for c in "rgb"))
print("black point ref",rd.round(1),"ours",od.round(1))
parts=[]
for i,c in enumerate("rgb"):
    xs,ys=[0.0],[round(float(rd[i])/255,4)]
    for j in range(len(PS)):
        x,y=float(op[c][j])/255,float(rp[c][j])/255
        if x-xs[-1]<0.05 or y<=ys[-1]: continue
        xs.append(round(x,3)); ys.append(round(min(0.995,y),3))
    xs.append(1.0); ys.append(1.0)
    parts.append(f"{c}='"+" ".join(f"{x}/{y}" for x,y in zip(xs,ys))+"'")
G2="curves="+":".join(parts)
FULL=G1+","+G2
print("\nSTAGE2:",G2)
open(OUT,"w").write(FULL)
ck=skin(frames(OUR,OUR_T,FULL))
cp={c:np.percentile(ck[:,i],PS) for i,c in enumerate("rgb")}
before=np.mean([abs(rp[c][j]-op[c][j]) for c in "rgb" for j in range(len(PS))])
after =np.mean([abs(rp[c][j]-cp[c][j]) for c in "rgb" for j in range(len(PS))])
print(f"skin mean |err| after stage1: {before:.1f} -> after stage2: {after:.1f} levels")
