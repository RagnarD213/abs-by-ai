#!/usr/bin/env python3
"""Frame-exact PICTURE EDL of Zeeshan's cut. For every frame of his cut, take the framing of the nearest fit samples
(fit.json) and find which raw frame (within +-12 of the acoustic guess) his picture shows, by warping the raw 256x144
gray frame with that framing and scoring NCC over the head/torso template. His picture cuts are where the matched raw
index stops advancing at 30000/1001 per 24 -- independent of his audio cuts (J/L cuts show as the difference).
Writes pic.json (per frame) and edl_picture.json (segments)."""
import json, numpy as np, cv2
HF, RF = 24.0, 30000/1001
his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1,144,256)
raw = np.memmap('raw256.gray', np.uint8, 'r').reshape(-1,144,256)
F = json.load(open('fit.json')); FS = {o['n']: o for o in F}
prof = json.load(open('offset_profile.json'))
PT = np.array([p[0] for p in prof if p[1] is not None and p[2] > 0.6]); PO = np.array([p[1] for p in prof if p[1] is not None and p[2] > 0.6])
def off(t):
    j = np.searchsorted(PT, t); c = [k for k in (j-1, j) if 0 <= k < len(PT)]
    return PO[min(c, key=lambda k: abs(PT[k]-t))]
Y0, Y1, X0, X1 = 8, 112, 64, 166
def warp(k, s, x, y):
    M = np.float32([[s, 0, -x*s/7.5], [0, s, -y*s/7.5]])
    return cv2.warpAffine(raw[k], M, (256,144), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def ncc(a, b):
    a = a.astype(np.float32); b = b.astype(np.float32); a -= a.mean(); b -= b.mean()
    return float((a*b).sum()/max(np.sqrt((a*a).sum()*(b*b).sum()), 1e-6))
out = []
for n in range(len(his)):
    t = n/HF; g = int(round((t+off(t))*RF))
    cands = [FS.get(6*(n//6)), FS.get(6*(n//6)+6)]
    cands = [c for c in cands if c and c.get('r', 0) >= 0.55]
    H = his[n, Y0:Y1, X0:X1]
    best = (-9, None, None)
    for c in cands:
        for k in range(max(0, g-12), min(len(raw), g+13)):
            v = ncc(H, warp(k, c['s'], c['x'], c['y'])[Y0:Y1, X0:X1])
            if v > best[0]: best = (v, k, c)
    if best[1] is None: out.append(dict(n=n, r=0.0)); continue
    v, k, c = best
    out.append(dict(n=n, r=round(v,3), k=int(k), s=c['s'], x=c['x'], y=c['y'], d=round(k - n*RF/HF, 2)))
json.dump(out, open('pic.json','w'))
r = np.array([o['r'] for o in out]); print('frames', len(out), 'r>=0.80:', (r>=0.80).sum(), ' r>=0.9:', (r>=0.9).sum())
