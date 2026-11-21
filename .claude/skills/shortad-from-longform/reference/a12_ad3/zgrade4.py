#!/usr/bin/env python3
"""FINAL TRIM, fitted on the DELIVERED render 10 against his file (both read as BT.709), applied after render3's unsharp.
Render 10 measured: saturation 0.436/0.446 vs his 0.412/0.428, shadows p5 7-9 vs his 11-12, whites 244 vs 248 -- the unsharp
(amount 0.7 talk / 0.5 window) raises local contrast AFTER every colour stage, which the emulated fits never saw.
Per-channel distribution match (3 x 256 curves) + one saturation scale about Rec.709 luma. Validated on held-out frames.
Writes grade_final.json."""
import json, subprocess, numpy as np, sys
sys.path.insert(0,'.')
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
E=json.load(open('edl_picture.json')); C=json.load(open('crop.json'))['frames']
import beats as B
tl,_=B.timeline(); kind={}
for b in tl:
    for n in range(b['n0'],b['n1']): kind[n]=b['kind']
FL=set(n for a,b in B.FLASH_WINDOWS for n in range(a-8,b+8))
ns=[k for s in E for k in range(s['n0']+9,s['n1']-9,18) if tuple(s['framing'][k-s['n0']])==(1.0,0.0,0.0) and kind.get(k)=='talk' and str(k) in C and k not in FL]
fit_ns, hold_ns = ns[0::2], ns[1::2]
SRC = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'ad3_vertical_9x16.mp4'
def dec(src,n,w,h):
    b=subprocess.run([FF,'-v','error','-ss',f'{n/FPS+0.001:.4f}','-i',src,'-frames:v','1','-vf','scale=in_color_matrix=bt709:in_range=tv','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(h,w,3).astype(np.float32)
def pairs(lst):
    O=[];H=[];T=[]
    for n in lst:
        x0,y0,w,h=C[str(n)]
        Y,X=np.mgrid[80:1350:7,40:1040:7]; bx=np.clip((x0+X*w/1080).astype(int),0,1919); by=np.clip((y0+Y*h/1920).astype(int),0,1079)
        k=by<740
        O.append(dec(SRC,n,1080,1920)[Y,X][k]); H.append(dec('ref/ad3_v6hd.mp4',n,1920,1080)[by,bx][k]); T.append(np.full(k.sum(), n))
    return np.concatenate(O), np.concatenate(H), np.concatenate(T)
LW=np.array([0.2126,0.7152,0.0722],np.float32)
def sat(a):
    mx=a.max(-1); mn=a.min(-1); return float(np.where(mx>1,(mx-mn)/np.maximum(mx,1),0).mean())
def curve_apply(x, lut): return np.stack([lut[c][np.clip(x[:,c],0,255).astype(np.uint8)] for c in range(3)],1).astype(np.float32)
def sat_apply(x, s):
    L=(x@LW)[:,None]; return np.clip(L+s*(x-L),0,255)
O,H,_=pairs(fit_ns); print(f'fit {len(fit_ns)} frames, held-out {len(hold_ns)}', flush=True)
QS=np.linspace(0,1,1025)
lut=np.zeros((3,256),np.float32)
for c in range(3):
    sq=np.quantile(O[:,c],QS); tq=np.maximum.accumulate(np.quantile(H[:,c],QS)); su,ix=np.unique(sq,return_index=True)
    lut[c]=np.interp(np.arange(256),su,tq[ix])
lut=np.clip(np.round(lut),0,255).astype(np.uint8)
Oc=curve_apply(O,lut); target=sat(H)
lo,hi=0.7,1.2
for _ in range(25):
    mid=(lo+hi)/2
    if sat(sat_apply(Oc,mid))>target: hi=mid
    else: lo=mid
S=(lo+hi)/2; print(f'saturation scale {S:.3f}', flush=True)
O2,H2,T2=pairs(hold_ns); A2=sat_apply(curve_apply(O2,lut),S)
sk=(H2[:,0]>H2[:,1]+15)&(H2[:,1]>H2[:,2])&(H2.mean(1)>70)&(H2.mean(1)<200)
for part,m in (('open (0-43 s)',T2/FPS<43),('rest',T2/FPS>=43)):
    print(' HELD-OUT', part)
    for nm,a in (('his',H2),('render10',O2),('trimmed',A2)):
        s=np.median(a[m&sk],0)
        print(f'   {nm:9s} RGB {a[m].mean(0).round(1)} bright p5/50/95 {np.percentile(a[m].mean(1),[5,50,95]).round(0)} sat {sat(a[m]):.3f} skin {s.round(0)} R-G {s[0]-s[1]:.0f}')
if '--write' in sys.argv:
    json.dump(dict(curves=lut.tolist(), sat=S, why='final trim after unsharp, fitted on delivered render 10 vs his (BT.709), 2026-09-13'), open('grade_final.json','w'))
    print('grade_final.json written')
