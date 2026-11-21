#!/usr/bin/env python3
"""Anchors per SHOT, sampled across the shot's OWN span - not per EDL beat.

A beat median is the wrong centre for a 15-45s slice of it: he drifts inside a beat. The skill
says "measure a centre per SHOT" and this is that.

⚠ BOTH anchors are recorded and compared, because which one is right is a property of the
FRAMING, not of the pipeline. On the Zepbound roll (framed cut at the waist, arms swinging
through the 60%-coverage band) the torso block was bimodal and 150px wrong; on THIS roll he is
framed chest-up and the two agree. Verify on drawn frames before trusting either.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'recentre'))
from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(['node','-e',"console.log(JSON.stringify(require('./config.js')))"]).decode())['SRC']
man = [m for m in json.load(open('shots/manifest.json')) if m.get('src') != 'ai']
N = 12
os.makedirs('work/ms', exist_ok=True)
out = {}
print(f"{'shot':12s} {'dur':>6s} {'head':>7s} {'torso':>7s} {'|d|px':>6s} {'sd(px)':>7s} {'silL':>6s} {'silR':>6s}")
for m in man:
    d = os.path.join('work/ms', m['name']); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d,'*')): os.remove(f)
    pngs=[]
    for k in range(N):
        t = m['absStart'] + m['dur']*(k+0.5)/N
        f = os.path.join(d, f'{k}.png')
        subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f'{t:.3f}','-i',SRC,
                        '-frames:v','1','-vf','scale=640:360',f], check=True)
        pngs.append(f)
    r = subprocess.run(['recentre/personmask', d]+pngs, capture_output=True, text=True)
    assert 'ERR' not in r.stdout, r.stdout
    H=[];T=[];L=[];R=[]
    for f in sorted(glob.glob(os.path.join(d,'*.mask.png'))):
        a = anchors(cv2.imread(f, cv2.IMREAD_GRAYSCALE) > 127)
        if a: H.append(a['head']); T.append(a['torso']); L.append(a['l']); R.append(a['r'])
    assert len(H) >= 8, f"{m['name']}: only {len(H)} masks"
    hd=float(np.median(H)); tr=float(np.median(T))
    out[m['name']] = {'head': round(hd,4), 'torso': round(tr,4),
                      'sd_px': round(float(np.std(H))*1920,1), 'n': len(H),
                      'silL': round(float(np.min(L)),4), 'silR': round(float(np.max(R)),4)}
    print(f"{m['name']:12s} {m['dur']:6.1f} {hd:7.4f} {tr:7.4f} {abs(hd-tr)*1920:6.0f} "
          f"{out[m['name']]['sd_px']:7.1f} {out[m['name']]['silL']:6.3f} {out[m['name']]['silR']:6.3f}")
json.dump(out, open('work/shotgeom.json','w'), indent=1)
hs=[v['head'] for v in out.values()]; ts=[v['torso'] for v in out.values()]
print(f"\nhead spread {(max(hs)-min(hs))*1920:.0f}px   torso spread {(max(ts)-min(ts))*1920:.0f}px   "
      f"max |head-torso| {max(abs(v['head']-v['torso']) for v in out.values())*1920:.0f}px")
