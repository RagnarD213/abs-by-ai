#!/usr/bin/env python3
"""Per-frame: is Dan's conform visible in his render, and at which of the two framings?
NCC of the reference frame against the conform at scale 1.00 and 1.20. High -> talk is
on screen; low -> he covered it with an insert or a graphic."""
import numpy as np, json
from PIL import Image
W,H=320,180; MAXSH=20
def nz(a):
    a=a.astype(np.float32); a-=a.mean(); s=a.std(); return a/s if s>1e-6 else a
def peak(rn,zn):
    C=np.fft.irfft2(np.fft.rfft2(rn)*np.conj(np.fft.rfft2(zn)),s=(H,W))/(H*W)
    best=-9; arg=(0,0)
    for dy in range(-MAXSH,MAXSH+1):
        for dx in range(-MAXSH,MAXSH+1):
            v=C[dy%H,dx%W]
            if v>best: best,arg=v,(dx,dy)
    return float(best),arg
R=lambda d,n: np.asarray(Image.open(f'ref_audit/{d}/{n:05d}.png').convert('L'))
rows=[]
for n in range(1,932):
    r=nz(R('gr',n)); b=Image.fromarray(R('gb',n))
    best=(-9,1.0,0,0)
    for s in (1.00,1.10,1.20,1.30):
        cw,ch=W/s,H/s
        z=np.asarray(b.resize((W,H),Image.BILINEAR,box=((W-cw)/2,(H-ch)/2,(W+cw)/2,(H+ch)/2)))
        v,(dx,dy)=peak(r,nz(z))
        if v>best[0]: best=(v,s,dx,dy)
    rows.append(dict(t=round((n-1)/4,2), ncc=round(best[0],3), scale=best[1], dx=best[2], dy=best[3]))
json.dump(rows,open('ref_audit/cover.json','w'))
arr=np.array([x['ncc'] for x in rows])
print('frames',len(rows),'ncc>0.75:',int((arr>0.75).sum()),'=%.0f%% talk-visible'%(100*(arr>0.75).mean()))
