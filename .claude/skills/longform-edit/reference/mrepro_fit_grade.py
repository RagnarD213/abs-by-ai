#!/usr/bin/env python3
"""Fit per-roll tone curves raw->his render by percentile matching on centre box,
using conform frames with scale=1.0 and ncc>=0.85. Writes grade_fit.json."""
import json, subprocess, numpy as np

BASE='/Volumes/Extreme/_edit_work/abwheel'
SHOOT=("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, "
       "indoor talking content, outdoor workout content | jeff chagrin | dan rose")
tr=json.load(open(f'{BASE}/mrepro/framing_track.json'))

def grab(src,t):
    r=subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(t),"-i",src,
                      "-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-"],capture_output=True)
    return np.frombuffer(r.stdout,dtype=np.uint8).reshape(1080,1920,3).astype(np.float32)

fits={}
for roll in ['C1630','C1631','C1632','C1633']:
    cands=[x for x in tr if x['roll']==roll and x['ncc']>=0.85 and x['scale']<=1.02 and abs(x['dx'])<=4 and abs(x['dy'])<=4]
    if len(cands)<3:
        cands=[x for x in tr if x['roll']==roll and x['ncc']>=0.80 and x['scale']<=1.06]
    step=max(1,len(cands)//5)
    sel=cands[::step][:5]
    print(roll,len(cands),"candidates, using",[x['t'] for x in sel])
    P=np.arange(1,100)
    src_p={0:[],1:[],2:[]}; dst_p={0:[],1:[],2:[]}
    for x in sel:
        cf=grab(f'{BASE}/mrepro/ref_hd.mp4',x['t'])
        rf=grab(f'{SHOOT}/{roll}.MP4',x['src'])
        # centre box
        cb=cf[270:810,480:1440]; rb=rf[270:810,480:1440]
        for ch in range(3):
            src_p[ch].append(np.percentile(rb[:,:,ch],P))
            dst_p[ch].append(np.percentile(cb[:,:,ch],P))
    curve={}
    for ch in range(3):
        s=np.mean(src_p[ch],axis=0); d=np.mean(dst_p[ch],axis=0)
        # sample control points for ffmpeg curves: x at percentiles 2,25,50,80,98
        pts=[]
        for pi in [1,24,49,79,97]:
            pts.append((round(float(s[pi])/255,4), round(float(d[pi])/255,4)))
        curve[ch]=pts
        err=np.abs(s-d).mean()
        print(f"  ch{ch} mean |raw-his| over percentiles: {err:.1f} levels; pts={pts}")
    fits[roll]=curve
json.dump(fits,open(f'{BASE}/mrepro/grade_fit.json','w'),indent=1)
