#!/usr/bin/env python3
"""Torso centre per BEAT, measured with Apple Vision.

One locked camera for 23 minutes, but the cut splices 62 takes together and Dan shifts
behind the counter between them - so a single TALK_X is exactly the mistake that shipped 10
off-centre Shorts on 2026-08-27. Every beat any chosen candidate touches gets its own
measurement.

Anchor is the TORSO BLOCK (recentre/anchor.py), not the mask centroid: his hands leave frame
while he talks and drag a centroid 100-500px between adjacent frames.

Also reports the silhouette EXTREMES (l, r) per beat, because the second question this
batch has to answer is what a 724px window centred on him actually contains - and whether
it slices the AG1 bag's logo, which would read as sloppy.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'recentre'))
from anchor import anchors

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4"
SP = json.load(open('work/splices.json'))
CUTS = [s['cut'] for s in SP] + [1409.523]

# beats each of the eight picks touches, by EDL index
WANT = {'A': [2, 3], 'J': [10, 11, 12], 'C': [18, 19], 'M': [30, 31],
        'H': [42, 43], 'E': [45], 'B': [46], 'D': [56, 57, 58]}

N = 6
os.makedirs('work/mk', exist_ok=True)
jobs = []
for seg, beats in WANT.items():
    for b in beats:
        a, z = CUTS[b], CUTS[b + 1]
        name = f'{seg}-b{b:02d}'
        d = os.path.join('work/mk', name)
        os.makedirs(d, exist_ok=True)
        for k in range(N):
            t = a + (z - a) * (k + 0.5) / N
            f = os.path.join(d, f'{k}.png')
            if not os.path.exists(f):
                subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.3f}',
                                '-i', SRC, '-frames:v', '1', '-vf', 'scale=640:360', f],
                               check=True)
        jobs.append((seg, b, name, d, a, z))

for _, _, name, d, _, _ in jobs:
    pngs = sorted(glob.glob(os.path.join(d, '[0-9].png')))
    r = subprocess.run(['recentre/personmask', d] + pngs, capture_output=True, text=True)
    assert 'ERR' not in r.stdout, r.stdout

out = {}
print(f"{'beat':10s} {'dur':>6s} {'torso':>7s} {'sd(px)':>7s} {'sil l':>7s} {'sil r':>7s}")
for seg, b, name, d, a, z in jobs:
    A = []
    for f in sorted(glob.glob(os.path.join(d, '*.mask.png'))):
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        an = anchors(m > 127)
        if an: A.append(an)
    assert len(A) >= 4, f'{name}: only {len(A)} usable masks'
    tor = float(np.median([x['torso'] for x in A]))
    sd = float(np.std([x['torso'] for x in A])) * 1920
    l = float(np.min([x['l'] for x in A])); r = float(np.max([x['r'] for x in A]))
    out[name] = {'seg': seg, 'beat': b, 'start': round(a, 3), 'end': round(z, 3),
                 'torso': round(tor, 4), 'sd_px': round(sd, 1),
                 'sil_l': round(l, 3), 'sil_r': round(r, 3)}
    print(f"{name:10s} {z-a:6.1f} {tor:7.4f} {sd:7.1f} {l:7.3f} {r:7.3f}")
json.dump(out, open('work/beatgeom.json', 'w'), indent=1)
t = [v['torso'] for v in out.values()]
print(f"\ntorso across beats: {min(t):.4f} .. {max(t):.4f}  "
      f"(spread {(max(t)-min(t))*1920:.0f}px of source, "
      f"{(max(t)-min(t))*1920*1080/724:.0f}px in the delivered frame)")
