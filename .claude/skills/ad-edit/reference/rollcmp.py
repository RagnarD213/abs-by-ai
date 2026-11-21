#!/usr/bin/env python3
"""Do two raw rolls measure the same? If yes, one grade chain serves both."""
import subprocess,sys
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
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
PS=(10,30,50,70,90)
res={}
import json
for lbl,path,times,vf in json.load(open(sys.argv[1])):
    fs=frames(path,times,vf); s=skin(fs)
    res[lbl]={c:np.percentile(s[:,i],PS) for i,c in enumerate("rgb")}
    res[lbl]['_dark']=np.percentile(np.concatenate([f.reshape(-1,3) for f in fs]),1,axis=0)
    print(f"{lbl}: {len(fs)} frames, {len(s)} skin px")
ks=list(res)
print("\n      "+"".join(f"{k:>26}" for k in ks))
for j,p in enumerate(PS):
    for c in "rgb":
        print(f"  p{p}{c} "+"".join(f"{res[k][c][j]:26.0f}" for k in ks))
print("  p1    "+"".join(f"{str(res[k]['_dark'].round(1)):>26}" for k in ks))
if len(ks)==2:
    d=np.mean([abs(res[ks[0]][c][j]-res[ks[1]][c][j]) for c in "rgb" for j in range(len(PS))])
    print(f"\nmean |diff| between the two: {d:.1f} levels")
