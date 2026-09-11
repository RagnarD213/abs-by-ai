#!/usr/bin/env python3
"""His vignette, measured AFTER the LUT: median(his luma / base luma) in radial bins on framing-1.0 talk frames.
The LUT was fitted on a centre-weighted mask, so what is left radially is his vignette. Writes vignette.json."""
import json, subprocess, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
E=json.load(open('edl_picture.json'))
ns=[]
for s in E:
    for k in range(s['n0']+8, s['n1']-8, 24):
        if tuple(s['framing'][k-s['n0']])==(1.0,0.0,0.0): ns.append(k)
ns=ns[::3][:40]
W,H=480,270
def grab(src,n):
    b=subprocess.run([FF,'-nostdin','-v','error','-ss',f'{n/FPS+0.0002:.5f}','-i',src,'-frames:v','1','-vf',f'scale={W}:{H}:flags=area','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(H,W).astype(np.float32)+1
his=np.stack([grab('reference.mp4',n) for n in ns]); ours=np.stack([grab('base.mp4',n) for n in ns])
ys,xs=np.mgrid[0:H,0:W]; r=np.hypot((xs-W/2)/(W/2),(ys-H/2)/(H/2))
ratio=his/ours
bins=np.linspace(0,1.45,16); prof=[]
for a,b in zip(bins[:-1],bins[1:]):
    m=(r>=a)&(r<b)
    if m.sum()<50: continue
    prof.append((round(float((a+b)/2),3), round(float(np.median(ratio[:,m])),3)))
print('radial gain his/ours:',prof)
json.dump(prof,open('vignette.json','w'))
