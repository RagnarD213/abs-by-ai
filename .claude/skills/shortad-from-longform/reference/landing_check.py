#!/usr/bin/env python3
"""Measured on the DELIVERED file: torso x at n0-1, n0, n0+2 for every picture cut in a talk/window beat, and the
per-cut crop jump; plus duplicated-first-frame check (diff n0 -> n0+1) at every cut."""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image
sys.path.insert(0,'rc'); from anchor import anchors
sys.path.insert(0,'.'); import beats as BT
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V=sys.argv[1]; P=json.load(open('edl_picture.json')); tl,_=BT.timeline()
def kind_at(t):
    for b in tl:
        if b['t0']<=t<b['t1']: return b['kind']
    return '?'
cuts=[s for s in P[1:] if kind_at(s['cut_in']) in ('talk',) and kind_at(s['cut_in']-0.05)=='talk']
want=sorted(set(v for s in cuts for v in (s['n0']-1, s['n0'], s['n0']+1, s['n0']+2)))
subprocess.run(['rm','-rf','lc'],check=False); os.makedirs('lc/fr'); os.makedirs('lc/m')
open('lc/sel.txt','w').write("select='"+'+'.join(f'eq(n,{n})' for n in want)+"',scale=270:480")
subprocess.run([FF,'-nostdin','-v','error','-y','-i',V,'-filter_script:v','lc/sel.txt','-fps_mode','passthrough','lc/fr/%05d.png'],check=True)
fs=sorted(glob.glob('lc/fr/*.png')); assert len(fs)==len(want),(len(fs),len(want))
for i in range(0,len(fs),60): subprocess.run(['./rc/personmask','lc/m']+fs[i:i+60],check=True,capture_output=True)
X={}
for f,nn in zip(sorted(glob.glob('lc/m/*.mask.png')),want):
    m=np.asarray(Image.open(f).convert('L'),dtype=np.float32)/255>0.5
    a=anchors(m); X[nn]=(a['torso']-0.5)*1080 if a and m.mean()>0.2 else np.nan
G={}
for f,nn in zip(fs,want): G[nn]=np.asarray(Image.open(f).convert('L'),dtype=np.float32)
rows=[]
for s in cuts:
    n0=s['n0']; a,b,c=X.get(n0-1,np.nan),X.get(n0,np.nan),X.get(n0+2,np.nan)
    dup=float(np.abs(G[n0+1]-G[n0]).mean())
    rows.append((s['cut_in'],a,b,c,dup))
A=np.array([[r[1],r[2],r[3]] for r in rows]); D=np.array([r[4] for r in rows])
print(f'{len(rows)} talk cuts on {V}')
print(f'  |x| at n0-1: median {np.nanmedian(np.abs(A[:,0])):.0f}  >70: {(np.abs(A[:,0])>70).sum()} | at n0: median {np.nanmedian(np.abs(A[:,1])):.0f}  >70: {(np.abs(A[:,1])>70).sum()} | at n0+2: median {np.nanmedian(np.abs(A[:,2])):.0f}  >70: {(np.abs(A[:,2])>70).sum()}')
print(f'  duplicated frame after the cut (mean |diff| n0->n0+1 < 0.5): {(D<0.5).sum()} of {len(D)}   min diff {D.min():.2f}')
for r in rows:
    if max(abs(r[1]),abs(r[2]),abs(r[3]))>70 or r[4]<0.5: print(f'    cut {r[0]:8.3f}: x(n0-1) {r[1]:+5.0f}  x(n0) {r[2]:+5.0f}  x(n0+2) {r[3]:+5.0f}   diff(n0->n0+1) {r[4]:.2f}')
