#!/usr/bin/env python3
"""Where Dan sits in the locked-off frame. Background = per-pixel median of the roll;
subject = the region that differs from it. Centroid of the upper body gives the crop x."""
import json, os, subprocess, numpy as np
from PIL import Image
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC="/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1591.MP4"
S=json.load(open('edl_final.json'))
os.makedirs('_probe',exist_ok=True)
def grab(t,tag):
    p=f'_probe/{tag}.png'
    if not os.path.exists(p):
        subprocess.run([FF,'-v','error','-ss',f'{t:.4f}','-i',SRC,'-frames:v','1','-vf','scale=480:270','-y',p],check=False)
    im=Image.open(p).convert('L') if os.path.exists(p) else None
    return np.asarray(im,dtype=np.float32) if im is not None else None

# background from frames spread across the roll
bg=[]
for k,t in enumerate(np.linspace(4,376,40)):
    a=grab(float(t),f'bg{k:02d}')
    if a is not None: bg.append(a)
BG=np.median(np.stack(bg),0)
Image.fromarray(BG.astype(np.uint8)).save('_probe/_bg.png')

res=[]
for s in S:
    cs=[]
    for j,f in enumerate((0.2,0.5,0.8)):
        a=grab(s['src_in']+f*s['dur'], f's{s["i"]:03d}_{j}')
        if a is None: continue
        d=np.abs(a-BG)
        d=d[40:200]                      # head/torso band
        m=d>18
        if m.sum()<400: continue
        cols=m.sum(0).astype(np.float32)
        cols[cols<cols.max()*0.25]=0
        if cols.sum()==0: continue
        cs.append(float((cols*np.arange(480)).sum()/cols.sum())*4.0)   # ->1920 space
    res.append(dict(i=s['i'], cx=round(float(np.median(cs)),1) if cs else None, n=len(cs)))
json.dump(res,open('subject.json','w'),indent=1)
ok=[r['cx'] for r in res if r['cx']]
a=np.array(ok)
print(f'segments {len(res)}  measured {len(ok)}')
print(f'subject centre x: median {np.median(a):.0f}  mean {a.mean():.0f}  sd {a.std():.1f}  min {a.min():.0f}  max {a.max():.0f}   (frame width 1920)')
print(f'9:16 crop is 607 wide -> centred on median, window x = {np.median(a)-303:.0f} .. {np.median(a)+303:.0f}')
