#!/usr/bin/env python3
"""Fit (scale,dx,dy) of his render vs raw conform at 2fps across the whole cut.
High-NCC frames give the framing track (punch-ins + pushes); low-NCC frames are
inserts/graphics windows. Writes framing_track.json."""
import json, subprocess, numpy as np, os

BASE='/Volumes/Extreme/_edit_work/abwheel'
SHOOT=("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, "
       "indoor talking content, outdoor workout content | jeff chagrin | dan rose")
W,H=160,90
segs=json.load(open(f'{BASE}/mrepro/edl_final.json'))

def decode(src,fps,extra=None):
    cmd=["ffmpeg","-nostdin","-v","error","-i",src,"-vf",f"fps={fps},scale={W}:{H}","-f","rawvideo","-pix_fmt","gray","-"]
    r=subprocess.run(cmd,capture_output=True)
    d=np.frombuffer(r.stdout,dtype=np.uint8)
    n=len(d)//(W*H)
    return d[:n*W*H].reshape(n,H,W)

cachef=f'{BASE}/mrepro/fr_cache.npz'
if os.path.exists(cachef):
    z=np.load(cachef); cutv=z['cut']; rollv={r:z[r] for r in ['C1630','C1631','C1632','C1633']}
else:
    print("decoding...")
    cutv=decode(f'{BASE}/mrepro/ref_hd.mp4',2)
    rollv={r:decode(f'{SHOOT}/{r}.MP4',4) for r in ['C1630','C1631','C1632','C1633']}
    np.savez_compressed(cachef,cut=cutv,**rollv)
print("cut frames",len(cutv))

def src_at(t):
    for s in segs:
        if s['cut_in']-1e-6<=t<s['cut_out']:
            return s['roll'], s['src_in']+(t-s['cut_in'])*s['speed']
    return None,None

def warp(f,s,dx,dy):
    h,w=f.shape
    s=max(s,1.0)
    ch,cw=min(h,int(round(h/s))),min(w,int(round(w/s)))
    y0=int((h-ch)/2+dy); x0=int((w-cw)/2+dx)
    y0=max(0,min(h-ch,y0)); x0=max(0,min(w-cw,x0))
    c=f[y0:y0+ch,x0:x0+cw]
    yi=(np.arange(H)*ch/H).astype(int); xi=(np.arange(W)*cw/W).astype(int)
    return c[yi][:,xi]

def norm(f):
    f=f.astype(np.float32); zz=f-f.mean(); n=np.sqrt((zz**2).sum())+1e-9
    return zz/n

track=[]
for k in range(len(cutv)):
    t=k/2
    roll,src=src_at(t)
    if roll is None: continue
    j=int(round(src*4))
    rv=rollv[roll]
    if j>=len(rv): continue
    raw=rv[j]; v=norm(cutv[k]).reshape(-1)
    best=(-1,1.0,0,0)
    for s in [1.0,1.05,1.1,1.15,1.2,1.3,1.4,1.55,1.7]:
        for dx in [-24,-16,-8,0,8,16,24]:
            for dy in [-10,-5,0,5,10]:
                c=norm(warp(raw,s,dx,dy)).reshape(-1)
                cc=float((c*v).sum())
                if cc>best[0]: best=(cc,s,dx,dy)
    # refine scale around best
    b=best
    for s in [b[1]-0.03,b[1]-0.015,b[1]+0.015,b[1]+0.03]:
        if s<0.98: continue
        for dx in [b[2]-4,b[2],b[2]+4]:
            for dy in [b[3]-3,b[3],b[3]+3]:
                c=norm(warp(raw,s,dx,dy)).reshape(-1)
                cc=float((c*v).sum())
                if cc>best[0]: best=(cc,s,dx,dy)
    track.append({'t':round(t,2),'roll':roll,'src':round(src,3),
                  'ncc':round(best[0],3),'scale':round(best[1],3),
                  'dx':best[2],'dy':best[3]})
    if k%100==0: print(k,track[-1])
json.dump(track,open(f'{BASE}/mrepro/framing_track.json','w'))
good=[x for x in track if x['ncc']>=0.75]
print(f"\n{len(good)}/{len(track)} frames fit as conform (ncc>=0.75)")
