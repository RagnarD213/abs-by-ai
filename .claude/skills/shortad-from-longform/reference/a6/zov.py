#!/usr/bin/env python3
"""Where are his OVERLAYS and FLASHES, to the frame? On talk frames, his picture = the raw at the EDL offset, warped
by his framing, plus his grade (a per-region gain/offset) plus his overlays. The residual after a per-region linear fit
is ~0 where nothing is overlaid; an overlay lifts it. Also: one-frame white flashes (frame mean >> neighbours)."""
import json, numpy as np, cv2
HF, RF = 24.0, 30000/1001
his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1,144,256)
raw = np.memmap('raw256.gray', np.uint8, 'r').reshape(-1,144,256)
E = json.load(open('edl_picture.json'))
REG = dict(check=(169,8,247,69), topleft=(0,26,64,56), mid_lt=(60,100,196,120), cta=(20,114,236,127),
           num=(4,127,150,138))
def warp(k, fr):
    s, x, y = fr; M = np.float32([[s, 0, -x*s/7.5], [0, s, -y*s/7.5]])
    return cv2.warpAffine(raw[int(k)], M, (256,144), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
rows = []
for s in E:
    for n in range(s['n0'], s['n1']):
        fr = s['framing'][n-s['n0']]; k = round((n/HF + s['off'])*RF)
        h = his[n].astype(np.float32); w = warp(k, fr)
        d = {}
        for name, (x0,y0,x1,y1) in REG.items():
            a = h[y0:y1, x0:x1].ravel(); b = w[y0:y1, x0:x1].ravel()
            A = np.vstack([b, np.ones_like(b)]).T; coef, *_ = np.linalg.lstsq(A, a, rcond=None)
            d[name] = float(np.abs(a - A@coef).mean())
        rows.append((n, d))
json.dump(rows, open('ov_resid.json','w'))
# report on/off intervals per region
import collections
for name in REG:
    v = np.array([d[name] for _, d in rows]); ns = np.array([n for n, _ in rows])
    base = np.median(v); thr = max(3*base, base+4)
    on = v > thr
    iv = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j+1 < len(on) and on[j+1] and ns[j+1] == ns[j]+1: j += 1
            if j - i >= 5: iv.append((ns[i]/HF, (ns[j]+1)/HF))
            i = j+1
        else: i += 1
    print(f'{name:8s} base {base:5.2f} thr {thr:5.2f}: ' + ', '.join(f'{a:.2f}-{b:.2f}' for a, b in iv))
# flashes: frame mean much brighter than both neighbours (1-2 frame white flash)
m = his.reshape(len(his), -1).mean(1)
fl = [n for n in range(1, len(m)-2) if m[n] - max(m[n-1], m[n+2] if m[n+1] > m[n-1]+20 else m[n+1]) > 18]
print('flash frames:', [(n, round(n/HF,3), round(float(m[n]-m[n-1]),1)) for n in fl])
