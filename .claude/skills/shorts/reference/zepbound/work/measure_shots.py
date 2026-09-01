#!/usr/bin/env python3
"""Torso centre per SHOT, sampled across the shot's OWN span - not per EDL beat.

The first cut of this batch set every crop from a 6-frame median over the whole beat, and the
delivered-file centering gate then read A +71px, E +53px, G -98px: he drifts inside a beat (b27
measured sd 152px), so a beat median is the wrong centre for a 15-45s slice of it. The skill says
"measure a centre per SHOT" and this is that.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'recentre'))
from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js')))"]).decode())['SRC']
man = json.load(open('shots/manifest.json'))
N = 10
os.makedirs('work/ms', exist_ok=True)
out = {}
print(f"{'shot':10s} {'dur':>6s} {'torso':>7s} {'sd(px)':>7s}  {'beat median':>11s}")
beat = json.load(open('work/beatgeom.json'))
byb = {v['beat']: v['torso'] for v in beat.values()}
for m in man:
    d = os.path.join('work/ms', m['name']); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*')): os.remove(f)
    pngs = []
    for k in range(N):
        t = m['absStart'] + m['dur'] * (k + 0.5) / N
        f = os.path.join(d, f'{k}.png')
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', SRC,
                        '-frames:v', '1', '-vf', 'scale=640:360', f], check=True)
        pngs.append(f)
    r = subprocess.run(['recentre/personmask', d] + pngs, capture_output=True, text=True)
    assert 'ERR' not in r.stdout, r.stdout
    A = []
    for f in sorted(glob.glob(os.path.join(d, '*.mask.png'))):
        a = anchors(cv2.imread(f, cv2.IMREAD_GRAYSCALE) > 127)
        if a: A.append(a['torso'])
    assert len(A) >= 6, m['name']
    tor = float(np.median(A)); sd = float(np.std(A)) * 1920
    out[m['name']] = {'torso': round(tor, 4), 'sd_px': round(sd, 1), 'n': len(A)}
    print(f"{m['name']:10s} {m['dur']:6.1f} {tor:7.4f} {sd:7.1f}  {byb.get(m['beat'], float('nan')):11.4f}  "
          f"({(tor-byb.get(m['beat'],tor))*1920*1080/738:+.0f}px delivered vs beat)")
json.dump(out, open('work/shotgeom.json', 'w'), indent=1)
