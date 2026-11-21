#!/usr/bin/env python3
"""END-TO-END grade correction, fitted where Dan's eye actually looks: the pixels inside our vertical crop, compared with his
file READ AS A PLAYER SHOWS IT (BT.709). (2026-09-13, Dan rejected render 9's colour: "Muhammad's look brighter, like the
colors are more vivid. I look more tan.")

Why a second stage: the 3D LUT (zlut.py) is a per-bin median with smoothing, fitted over the whole 16:9 frame. After the
decode fix it still left the vertical ~4 levels dark, ~7 short in blue and its whites at p95 237 against his 249 -- sparse
highlight bins get smoothed toward their neighbours, and his vignette is spatial where a colour table is not.
So: source = our graded base pixel, target = his pixel DIVIDED BY the vignette at that position (render3 re-applies the
vignette after the base, so the base must hold his un-vignetted colour). A 3rd-order RGB polynomial per channel, fitted by
least squares with two rounds of outlier trimming (misregistration at edges and motion), validated on HELD-OUT frames, then
composed into his.cube (new = poly(old)) so there is still exactly one grade stage."""
import json, subprocess, numpy as np, sys, os
sys.path.insert(0,'.')
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
E=json.load(open('edl_picture.json')); C=json.load(open('crop.json'))['frames']
import beats as B
tl,ov=B.timeline(); kind={}
for b in tl:
    for n in range(b['n0'],b['n1']): kind[n]=b['kind']
busy=set()
for o in ov:
    if o['kind'] in ('lt','pill'):
        for n in range(int(o['t0']*FPS)-3, int(o['t1']*FPS)+3): busy.add(n)
ns=[]
for s in E:
    for k in range(s['n0']+8, s['n1']-8, 16):
        if tuple(s['framing'][k-s['n0']])==(1.0,0.0,0.0) and kind.get(k)=='talk' and str(k) in C and k not in busy: ns.append(k)
fit_ns, hold_ns = ns[0::2], ns[1::2]
if '--all' in sys.argv: fit_ns = ns          # final curves: every usable talk frame (held-out report is then in-sample)
V=json.load(open('vignette.json'))
ys,xs=np.mgrid[0:1080,0:1920]; rad=np.hypot((xs-960)/960,(ys-540)/540)
VIG=np.clip(np.interp(rad,[v[0] for v in V],[v[1] for v in V]),0.3,1.05).astype(np.float32)
def grab(src,n):
    b=subprocess.run([FF,'-nostdin','-v','error','-ss',f'{n/FPS+0.001:.4f}','-i',src,'-frames:v','1','-vf','scale=in_color_matrix=bt709:in_range=tv','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(1080,1920,3).astype(np.float32)
def pairs(lst, stride=6):
    S=[];T=[];G=[];Hh=[]
    for n in lst:
        x0,y0,w,h=C[str(n)]
        Y,X=np.mgrid[60:1350:stride, 30:1050:stride]
        bx=np.clip((x0+X*w/1080).astype(int),0,1919); by=np.clip((y0+Y*h/1920).astype(int),0,1079)
        keep=by<900                                        # his lower thirds / pills live below this in his frame
        his=grab('ref/ad3_v6hd.mp4',n); base=grab('base.mp4',n)
        g=VIG[by,bx][keep]; S.append(base[by,bx][keep]); Hh.append(his[by,bx][keep]); G.append(g); T.append(his[by,bx][keep]/g[:,None])
    return np.concatenate(S), np.concatenate(T), np.concatenate(G), np.concatenate(Hh)
def feats(x):
    r,g,b=(x[:,0]/255.0),(x[:,1]/255.0),(x[:,2]/255.0)
    return np.stack([np.ones_like(r),r,g,b,r*r,g*g,b*b,r*g,r*b,g*b,r*r*r,g*g*g,b*b*b,r*r*g,r*r*b,g*g*r,g*g*b,b*b*r,b*b*g,r*g*b],1)
def sat(a):
    mx=a.max(-1); mn=a.min(-1); return np.where(mx>1,(mx-mn)/np.maximum(mx,1),0)
print(f'fit frames {len(fit_ns)}, held-out frames {len(hold_ns)}', flush=True)
MODE = 'post' if '--post' in sys.argv else ('qm' if '--qm' in sys.argv else 'poly')
# ⚠ WHY QUANTILE MAPPING BEATS PIXEL-PAIR REGRESSION HERE: his frame and ours are the same scene but never registered to
# the pixel (his punch micro-offsets, motion blur, codec softness). Regressing target on source with noise in the pairing
# ATTENUATES the fitted slope -- the classic errors-in-variables bias -- so the fit flattens contrast, lowers highlights
# and leaves the mean colour cast. Measured: the polynomial halved the per-pixel error and still left blue 69 vs 75 and
# whites p95 244 vs 249. Matching each channel's DISTRIBUTION over the same scene coordinates is immune to that.
S,T,G,Hh=pairs(fit_ns)
keep=np.ones(len(S),bool)
QS=np.linspace(0,1,513)
if MODE=='qm':
    MAPS=[(np.quantile(S[:,c],QS), np.maximum.accumulate(np.quantile(T[:,c],QS))) for c in range(3)]
if MODE=='post':
    # AFTER the vignette: source = what render3 actually has in hand (base x vignette), target = his pixel as shown.
    # Correcting before the vignette cannot lift a highlight past 255 at a position the vignette then darkens.
    SV=np.clip(S*G[:,None],0,255)
    MAPS=[(np.quantile(SV[:,c],QS), np.maximum.accumulate(np.quantile(Hh[:,c],QS))) for c in range(3)]
for it in (range(3) if MODE=='poly' else []):
    F=feats(S[keep]); coef=np.linalg.lstsq(F, T[keep]/255.0, rcond=None)[0]
    res=np.abs(feats(S)@coef*255-T).max(1); mad=np.median(res[keep]); keep=res<max(3*mad*1.4826, 6)
    print(f'  round {it}: kept {keep.mean()*100:.1f}% of {len(S)} pairs, median |res| {np.median(res[keep]):.2f}', flush=True)
def apply(x):
    if MODE in ('qm','post'):
        out=np.empty_like(x)
        for c,(sq,tq) in enumerate(MAPS):
            su,idx=np.unique(sq,return_index=True); out[:,c]=np.interp(x[:,c],su,tq[idx])
        return np.clip(out,0,255)
    return np.clip(feats(x)@coef*255, 0, 255)
S2,T2,G2,H2=pairs(hold_ns)
def rep(a): l=a.mean(1); return f"RGB {a.mean(0).round(1)} luma p5/50/95 {np.percentile(l,[5,50,95]).round(0)} sat {sat(a).mean():.3f}"
before=np.clip(S2*G2[:,None],0,255)
after=apply(before) if MODE=='post' else np.clip(apply(S2)*G2[:,None],0,255)
sk=(H2[:,0]>H2[:,1]+12)&(H2[:,1]>H2[:,2])&(H2.mean(1)>60)&(H2.mean(1)<200)
print('HELD-OUT, as the vertical shows it:')
print('  all  HIS   ', rep(H2)); print('       before', rep(before)); print('       after ', rep(after))
print('  skin HIS   ', rep(H2[sk])); print('       before', rep(before[sk])); print('       after ', rep(after[sk]))
print('  median |error| per channel before', np.median(np.abs(before-H2),0).round(2), 'after', np.median(np.abs(after-H2),0).round(2))
for nm,a in (('HIS',H2),('before',before),('after',after)):
    print(f'  per-channel p5/50/95  {nm:6s} R {np.percentile(a[:,0],[5,50,95]).round(0)} G {np.percentile(a[:,1],[5,50,95]).round(0)} B {np.percentile(a[:,2],[5,50,95]).round(0)}')
if '--write' in sys.argv and MODE=='post':
    # 256-entry curve per channel, applied by render3 to the base frame right after the vignette
    lut=np.stack([apply(np.repeat(np.arange(256,dtype=np.float32)[:,None],3,1))[:,c] for c in range(3)])
    json.dump(dict(mode='post', curves=np.round(lut).astype(int).tolist(), fit_frames=fit_ns, hold_frames=hold_ns,
                   why="Dan 2026-09-13 rejected render 9's colour; his file read as BT.709, matched per channel after the vignette"),
              open('grade_post.json','w'))
    print('grade_post.json written (3 x 256 curves)'); sys.exit(0)
if '--write' in sys.argv:
    lines=open('his.cube').read().strip().split('\n'); head=[l for l in lines if not l[:1].isdigit() and not l[:1]=='-']; vals=np.array([[float(v) for v in l.split()] for l in lines if l[:1].isdigit() or l[:1]=='-'])
    new=np.clip(apply(vals*255)/255.0, 0, 1)
    os.replace('his.cube','his_fit1.cube')
    with open('his.cube','w') as f:
        f.write('\n'.join(head).replace('(fitted)','(fitted, BT.709 read + end-to-end vertical correction 2026-09-13)')+'\n')
        for v in new: f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
    json.dump(dict(mode=MODE, maps=[[a.tolist(),b.tolist()] for a,b in MAPS] if MODE=='qm' else None,
                   coef=None if MODE=='qm' else coef.tolist(), fit_frames=fit_ns, hold_frames=hold_ns), open('grade2.json','w'))
    print('his.cube rewritten (previous kept as his_fit1.cube)')
