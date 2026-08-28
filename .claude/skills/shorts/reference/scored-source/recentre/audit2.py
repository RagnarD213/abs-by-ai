#!/usr/bin/env python3
"""One centring verdict per shot, for EVERY treatment, in the units Dan actually sees:
pixels off centre in the delivered 1080x1920 frame.

The reference audit only handled full-bleed 9:16 crops. This batch is mostly cards, and a
card can be off centre too - the subject sits inside the cardCrop rectangle rather than
inside a 9:16 window. Both are reduced to the same number here: project the measured torso
centre through whatever geometry that shot uses, and measure its distance from x=540.
"""
import glob, json, os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anchor import anchors
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.dirname(HERE)
L = json.load(open(os.path.join(BD, 'layout.json')))
CW, CH = L['canvas']; SRC_W, SRC_H = 1920, 1080
meta = json.load(open(os.path.join(HERE, 'fr.json')))
crops = json.load(open(os.path.join(BD, 'shots', 'crops.json')))

def project(sh, t):
    """Where a source-fraction t lands on the delivered canvas, and the crop's own centre."""
    if sh['t'] in ('talk', 'broll'):
        cw = L['talk']['zoomW'] if sh['zoom'] else L['talk']['cropW']
        x = crops[sh['shot']]
        x0 = round(min(max(x * SRC_W - cw / 2, 0), SRC_W - cw))
        if sh['minX0'] is not None: x0 = max(x0, sh['minX0'])
        k = CW / cw
        return (t * SRC_W - x0) * k, (x0 + cw / 2), k
    cc = sh['cardCrop'] or [0, 1, 0, 1]
    X0, X1 = cc[0] * SRC_W, cc[1] * SRC_W
    Y0, Y1 = cc[2] * SRC_H, cc[3] * SRC_H
    k = min(L['card']['w'] / (X1 - X0), L['card']['h'] / (Y1 - Y0))
    w = (X1 - X0) * k
    left = L['card']['x'] + (L['card']['w'] - w) / 2
    return left + (t * SRC_W - X0) * k, (X0 + X1) / 2, k

rows = []
for sh in meta['shots']:
    A = []
    for f in sorted(glob.glob(os.path.join(HERE, 'mk', sh['shot'], '*.mask.png'))):
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        a = anchors(m > 127)
        if a: A.append(a)
    if len(A) < 0.6 * max(1, sh['n']):
        rows.append(dict(shot=sh['shot'], seg=sh['seg'], t=sh['t'], dur=sh['dur'],
                         n=len(A), note='no subject in most frames')); continue
    T = np.median([a['torso'] for a in A])
    Lf = np.array([a['l'] for a in A]); Rf = np.array([a['r'] for a in A])
    px, _, k = project(sh, T)
    lpx = np.median([project(sh, v)[0] for v in Lf])
    rpx = np.median([project(sh, v)[0] for v in Rf])
    # how much of the subject falls outside the delivered frame, per side
    clipL = max(0.0, -lpx); clipR = max(0.0, rpx - CW)
    marL = max(0.0, lpx);   marR = max(0.0, CW - rpx)
    asym = max(min(clipL, marR), min(clipR, marL))
    rows.append(dict(shot=sh['shot'], seg=sh['seg'], t=sh['t'], dur=sh['dur'], n=len(A),
                     torso=round(float(T), 4), px=round(float(px), 1),
                     off=round(float(px - CW / 2), 1), cutoff=round(float(asym), 1),
                     subj_w=round(float(rpx - lpx), 1)))
json.dump(rows, open(os.path.join(HERE, 'audit.json'), 'w'), indent=1)
rows2 = [r for r in rows if 'off' in r]
rows2.sort(key=lambda r: -abs(r['off']))
print(f"{'shot':13}{'seg':4}{'treat':7}{'dur':>6}{'subj px':>9}{'centre px':>11}{'off':>8}{'cut-off':>9}  verdict")
for r in rows2:
    v = ('RE-CENTRE' if abs(r['off']) >= 110 or r['cutoff'] >= 90 else
         'borderline' if abs(r['off']) >= 60 else 'ok')
    print(f"{r['shot']:13}{r['seg']:4}{r['t']:7}{r['dur']:6.1f}{r['subj_w']:9.0f}"
          f"{r['px']:11.0f}{r['off']:8.0f}{r['cutoff']:9.0f}  {v}")
for r in rows:
    if 'off' not in r: print(f"{r['shot']:13}{r['seg']:4}{r['t']:7}{r['dur']:6.1f}    -- {r['note']}")
