#!/usr/bin/env python3
"""Measured ON THE DELIVERED FILE, at every picture cut inside a talk beat:

  * the torso x at n0-1, n0 and n0+2 -- the crop must LAND on the incoming pose, not pan
    into it over the next second (A5.14: the audit measured him 78-190 px off after our
    cuts while every upstream statistic was green);
  * diff(n0 -> n0+1) >= 0.5 -- a duplicated first frame is a 33 ms hold on the incoming
    frame, invisible to the eye and a defect class (A5.17).

This build's picture is conformed at the AUDIO splices, so the cuts are the segment
boundaries of edl_frames.json (cumulative frames), not a separate picture EDL.

  python3 sqlanding.py <delivered.mp4>
"""
import json, os, subprocess, sys, glob
import numpy as np
from PIL import Image
sys.path.insert(0, 'rc'); from anchor import anchors
sys.path.insert(0, '.'); import beats as BT

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
V = sys.argv[1]
S = 270

tl, _ = BT.timeline()
def kind_at(t):
    for b in tl:
        if b['t0'] <= t < b['t1']: return b['kind']
    return '?'

E = json.load(open('edl_frames.json'))
cuts, n = [], 0
for s in E:
    if n > 0:
        t = n/FPS
        if kind_at(t) == 'talk' and kind_at(t-0.05) == 'talk':
            cuts.append(dict(n0=n, t=round(t, 3), i=s['i']))
    n += s['frames']
assert cuts, 'NOT MEASURED: no talk-to-talk picture cut found in edl_frames.json'

want = sorted({v for c in cuts for v in (c['n0']-1, c['n0'], c['n0']+1, c['n0']+2)})
subprocess.run(['rm', '-rf', 'lc'], check=False); os.makedirs('lc/fr'); os.makedirs('lc/m')
open('lc/sel.txt', 'w').write("select='" + '+'.join(f'eq(n,{k})' for k in want) + f"',scale={S}:{S}")
subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', V, '-filter_script:v', 'lc/sel.txt',
                '-fps_mode', 'passthrough', 'lc/fr/%05d.png'], check=True)
fs = sorted(glob.glob('lc/fr/*.png')); assert len(fs) == len(want), (len(fs), len(want))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', 'lc/m'] + fs[i:i+60], check=True, capture_output=True)
X, G = {}, {}
for f, nn in zip(fs, want):
    G[nn] = np.asarray(Image.open(f).convert('L'), dtype=np.float32)
for f, nn in zip(sorted(glob.glob('lc/m/*.mask.png')), want):
    m = np.asarray(Image.open(f).convert('L'), dtype=np.float32)/255 > 0.5
    a = anchors(m)
    X[nn] = (a['torso']-0.5)*1080 if a and m.mean() > 0.2 else np.nan

rows = []
for c in cuts:
    n0 = c['n0']
    rows.append((c['t'], X.get(n0-1, np.nan), X.get(n0, np.nan), X.get(n0+2, np.nan),
                 float(np.abs(G[n0+1]-G[n0]).mean())))
A = np.array([[r[1], r[2], r[3]] for r in rows]); D = np.array([r[4] for r in rows])
print(f'{len(rows)} talk-to-talk picture cuts on {V}')
print(f'  |x| at n0-1: median {np.nanmedian(np.abs(A[:,0])):.0f}  >70: {(np.abs(A[:,0])>70).sum()}'
      f' | at n0: median {np.nanmedian(np.abs(A[:,1])):.0f}  >70: {(np.abs(A[:,1])>70).sum()}'
      f' | at n0+2: median {np.nanmedian(np.abs(A[:,2])):.0f}  >70: {(np.abs(A[:,2])>70).sum()}')
dup = int((D < 0.5).sum())
print(f'  duplicated frame after the cut (mean |diff| n0->n0+1 < 0.5): {dup} of {len(D)}   min diff {D.min():.2f}')
bad = []
for r in rows:
    if np.nanmax(np.abs([r[1], r[2], r[3]])) > 70 or r[4] < 0.5:
        bad.append(r)
        print(f'    cut {r[0]:8.3f}: x(n0-1) {r[1]:+5.0f}  x(n0) {r[2]:+5.0f}  x(n0+2) {r[3]:+5.0f}   diff {r[4]:.2f}')
os.makedirs('logs', exist_ok=True)
json.dump(dict(video=os.path.basename(V), cuts=len(rows), duplicated=dup,
               over70_at_cut=int((np.abs(A[:,1])>70).sum()),
               flagged=[[round(x, 3) if x == x else None for x in r] for r in bad]),
          open('logs/landing.json', 'w'), indent=1)
sys.exit(1 if (dup or (np.abs(A[:,1])>70).sum()) else 0)
