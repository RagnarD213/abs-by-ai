#!/usr/bin/env python3
"""HIS bullet blur-in, measured at FULL RESOLUTION as two separate instants.

The brightness-threshold curve in ref/ov3.npz ((lum>170).mean()) does NOT mark his onset: blurred text is spread and
dim, so it only crosses the threshold about halfway through the blur. Measured on his 3106 bullet, the ov3 step is at
3106 while the text first APPEARS at 3100 and finishes sharpening at 3110. Our renderer starts its blur at the cue
frame, so the cue must be his ONSET, not the ov3 step.
  onset = first frame where new pixels appear in his left text panel (soft mass, |diff| > 28 over > 1 % of the panel)
  sharp = first frame where the difference's edge energy reaches 90 % of its plateau
"""
import subprocess, re, sys
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS=30000/1001; W,H=1920,1080
def panel(n0, n):
    p=subprocess.run([FF,'-v','error','-ss',f'{n0/FPS:.6f}','-i','ref/ad3_v6hd.mp4','-frames:v',str(n),
                      '-f','rawvideo','-pix_fmt','gray','-'],capture_output=True)
    a=np.frombuffer(p.stdout,np.uint8); k=len(a)//(W*H)
    return a[:k*W*H].reshape(k,H,W).astype(np.float32)[:, 100:1020, 40:900]

def measure(n, back=22, fwd=26):
    n0=n-back; P=panel(n0, back+fwd)
    if len(P) < back+4: return None
    ref=P[0]; cov=[]; edge=[]
    for i in range(len(P)):
        D=np.abs(P[i]-ref)
        cov.append((D>28).mean())
        edge.append((np.abs(np.diff(D,axis=1)).mean()+np.abs(np.diff(D,axis=0)).mean())/2)
    cov=np.array(cov); edge=np.array(edge)
    on=next((i for i in range(1,len(cov)) if cov[i]>0.01), None)
    if on is None: return None
    plat=np.median(edge[max(on+12,len(edge)-8):])
    if plat<=1e-6: return None
    sh=next((i for i in range(on,len(edge)) if edge[i]>=0.9*plat), None)
    return n0+on, (n0+sh if sh is not None else None)

src=open('beats.py').read()
onsets=[(m.group(1),m.group(2),int(m.group(3))) for m in re.finditer(r'\b(bul|ohd)\(\s*f?"((?:[^"\\]|\\.)*)"\s*,\s*(\d+)\s*\)', src)]
print(f"{'kind':5}{'ours':>7}{'his on':>8}{'delta':>7}{'sharp':>7}{'blur':>6}  text")
res=[]
for kind,text,n in onsets:
    r=measure(n)
    if r is None: print(f"{kind:5}{n:7d}{'?':>8}{'':>7}{'':>7}{'':>6}  {text[:36]} (no clean step)"); continue
    on,sh=r; blur=(sh-on) if sh else None
    res.append((kind,text,n,on,blur))
    print(f"{kind:5}{n:7d}{on:8d}{n-on:+7d}{(sh if sh else 0):7d}{(blur if blur else 0):6d}  {text[:36]}")
bl=[b for _,_,_,_,b in res if b]
print(f"\nHIS blur-in: median {np.median(bl):.1f} frames = {np.median(bl)/FPS:.3f} s   (ours REVEAL=0.27 = {0.27*FPS:.1f} fr)")
print("SUGGESTED beats.py cues (his onset):")
for kind,text,n,on,_ in res:
    if n!=on: print(f"  {kind}({text[:44]!r}, {n}) -> {on}")
