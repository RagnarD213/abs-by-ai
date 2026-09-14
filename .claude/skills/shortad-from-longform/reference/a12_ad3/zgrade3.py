#!/usr/bin/env python3
"""SECTION-BY-SECTION colour match to his grade, on top of the global per-channel curves (zgrade2.py --post).

Measured 2026-09-13 after the global fix: averaged over the ad our skin matched his (137/91/56 vs 137/90/57), but his grade
is NOT one grade -- the opening 0-43 s is warmer (skin R-G 57-60 vs ours 52-54, G ~8 high on ours) while most of the rest
matches within 1-4 levels. A global table cannot be warm in one section and neutral in another, and Dan watched exactly
that opening ("I look more tan").

Per EDL segment: matched scene pixels (ours = base x vignette -> global curves, his = his file read as BT.709), leak frames
and misregistered pairs dropped, then the Monge-Kantorovich linear transfer (mean + covariance -> 3x3 A and offset t). That
is a DISTRIBUTION match, so it is immune to the pixel misregistration that flattens a regression. Parameters are smoothed
over time (Gaussian, 5 s) and interpolated per frame, so an invisible join cannot pop colour. Validated on held-out frames.
Writes grade_seg.json: keypoints [n, A(9), t(3)]."""
import json, subprocess, numpy as np, sys
sys.path.insert(0,'.')
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
E=json.load(open('edl_picture.json')); C=json.load(open('crop.json'))['frames']
import beats as B
tl,ov=B.timeline(); kind={}
for b in tl:
    for n in range(b['n0'],b['n1']): kind[n]=b['kind']
FL=set()
for a,b in B.FLASH_WINDOWS:
    for n in range(a-8,b+8): FL.add(n)
CUR=np.array(json.load(open('grade_post.json'))['curves'],np.uint8)
V=json.load(open('vignette.json')); ys,xs=np.mgrid[0:1080,0:1920]; rad=np.hypot((xs-960)/960,(ys-540)/540)
VIG=np.clip(np.interp(rad,[v[0] for v in V],[v[1] for v in V]),0.3,1.05).astype(np.float32)
def dec(src,n):
    b=subprocess.run([FF,'-v','error','-ss',f'{n/FPS+0.001:.4f}','-i',src,'-frames:v','1','-vf','scale=in_color_matrix=bt709:in_range=tv','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(1080,1920,3)
def ours_of(base):
    o=np.clip(base.astype(np.float32)*VIG[...,None]+0.5,0,255).astype(np.uint8)
    return np.stack([CUR[c][o[...,c]] for c in range(3)],-1).astype(np.float32)
def pairs(n):
    x0,y0,w,h=C[str(n)]
    his=dec('ref/ad3_v6hd.mp4',n).astype(np.float32); ours=ours_of(dec('base.mp4',n))
    Y,X=np.mgrid[80:1350:6,40:1040:6]; bx=np.clip((x0+X*w/1080).astype(int),0,1919); by=np.clip((y0+Y*h/1920).astype(int),0,1079)
    k=by<740; hh=his[by,bx][k]; oo=ours[by,bx][k]
    ok=np.abs(hh.mean(1)-oo.mean(1))<40
    return oo[ok], hh[ok]
def sqrtm(M):
    w,v=np.linalg.eigh((M+M.T)/2); return (v*np.sqrt(np.maximum(w,1e-9)))@v.T
def mkl(src,dst):
    ms,md=src.mean(0),dst.mean(0); Cs=np.cov(src.T)+np.eye(3)*1e-3; Cd=np.cov(dst.T)+np.eye(3)*1e-3
    Cs2=sqrtm(Cs); Ci=np.linalg.inv(Cs2); A=Ci@sqrtm(Cs2@Cd@Cs2)@Ci
    return A, md-A@ms
keys=[]; hold={}
for i,s in enumerate(E):
    ks=[k for k in range(s['n0']+6,s['n1']-6,10) if tuple(s['framing'][k-s['n0']])==(1.0,0.0,0.0) and kind.get(k) in ('talk',) and str(k) in C and k not in FL]
    if len(ks)<2: continue
    fitk, holdk = ks[0::2][:5], ks[1::2][:3]
    S=[];T=[]
    for n in fitk:
        o,h=pairs(n); S.append(o); T.append(h)
    S=np.concatenate(S); T=np.concatenate(T)
    if len(S)<3000: continue
    A,t=mkl(S,T)
    keys.append(dict(n=float(np.mean(fitk)), A=A, t=t, seg=i)); hold[i]=holdk
    print(f'seg {i:2d} n~{np.mean(fitk):6.0f} pairs {len(S):7d}  diag A {np.diag(A).round(3)}  t {t.round(1)}', flush=True)
# smooth parameters over time (sigma 5 s) so neighbouring segments of one shot cannot wobble the colour
ns=np.array([k['n'] for k in keys]); P=np.array([np.r_[k['A'].ravel(),k['t']] for k in keys])
sig=5*FPS; Ps=np.zeros_like(P)
for j,n in enumerate(ns):
    w=np.exp(-0.5*((ns-n)/sig)**2); Ps[j]=(w[:,None]*P).sum(0)/w.sum()
def params_at(n):
    if n<=ns[0]: p=Ps[0]
    elif n>=ns[-1]: p=Ps[-1]
    else:
        j=np.searchsorted(ns,n); a=(n-ns[j-1])/(ns[j]-ns[j-1]); p=Ps[j-1]*(1-a)+Ps[j]*a
    return p[:9].reshape(3,3), p[9:]
# held-out validation
def sat(a):
    mx=a.max(-1); mn=a.min(-1); return np.where(mx>1,(mx-mn)/np.maximum(mx,1),0)
rows=[]
print('\nHELD-OUT per segment:  skin R-G  his / before / after      skin median his | before | after')
for k in keys:
    i=k['seg']; Hs=[];Bs=[];As=[]
    for n in hold[i]:
        o,h=pairs(n); A,t=params_at(n); a=np.clip(o@A.T+t,0,255)
        sk=(h[:,0]>h[:,1]+15)&(h[:,1]>h[:,2])&(h.mean(1)>70)&(h.mean(1)<200)
        Hs.append(h);Bs.append(o);As.append(a); rows.append((h,o,a))
    h=np.concatenate(Hs);o=np.concatenate(Bs);a=np.concatenate(As)
    sk=(h[:,0]>h[:,1]+15)&(h[:,1]>h[:,2])&(h.mean(1)>70)&(h.mean(1)<200)
    if sk.sum()<300: continue
    mh,mo,ma=np.median(h[sk],0),np.median(o[sk],0),np.median(a[sk],0)
    print(f'  seg {i:2d}  {mh[0]-mh[1]:4.0f} / {mo[0]-mo[1]:4.0f} / {ma[0]-ma[1]:4.0f}     {mh.round(0)} | {mo.round(0)} | {ma.round(0)}')
H=np.concatenate([r[0] for r in rows]);O=np.concatenate([r[1] for r in rows]);Aa=np.concatenate([r[2] for r in rows])
for nm,x in (('HIS',H),('before',O),('after',Aa)):
    print(f'  ALL {nm:6s} RGB {x.mean(0).round(1)} sat {sat(x).mean():.3f}  median|err| {np.median(np.abs(x-H),0).round(2) if nm!="HIS" else ""}')
if '--write' in sys.argv:
    json.dump(dict(keys=[[float(n)]+p.round(6).tolist() for n,p in zip(ns,Ps)],
                   why="section-by-section MKL colour match to his grade (BT.709 read), smoothed 5 s; Dan 2026-09-13"),
              open('grade_seg.json','w'))
    print('grade_seg.json written,', len(ns), 'keypoints')
