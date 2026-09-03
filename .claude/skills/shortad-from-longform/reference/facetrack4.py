#!/usr/bin/env python3
"""Face track on EXACT frame indices (raw_torso.npy + raw_torso_n.npy), smoothed per picture segment,
zero-phase, endpoint-anchored (median window shrinks to zero at the segment ends), slope-limited.
Writes facetrack.json = {n: [frame indices], x: [crop x per sample]} -- render.py interpolates in frame time."""
import json, numpy as np
raw = np.load('raw_torso.npy'); n = np.load('raw_torso_n.npy').astype(int)
FPS = 30000/1001; CROP_W = 608
SLOPE_PXS = 170.0                         # source px/s (~300 px/s on the phone), the re-audit's cap
ok = ~np.isnan(raw); r = np.interp(n, n[ok], raw[ok])
S = json.load(open('edl_picture.json'))
out = np.empty_like(r)
def limit_fwd(x, t, lim):
    o = [x[0]]
    for i in range(1, len(x)):
        dt = (t[i]-t[i-1])/FPS
        o.append(o[-1] + float(np.clip(x[i]-o[-1], -lim*dt, lim*dt)))
    return np.array(o)
for s in S:
    m = (n >= s['n0']) & (n < s['n1'])
    idx = np.where(m)[0]
    if len(idx) == 0: continue
    seg = r[idx]; t = n[idx]; L = len(seg)
    if L < 4: out[idx] = seg; continue
    k = 3
    med = np.array([np.median(seg[j-min(k, j, L-1-j):j+min(k, j, L-1-j)+1]) for j in range(L)])
    f = limit_fwd(med, t, SLOPE_PXS); b = limit_fwd(med[::-1], (-t)[::-1], SLOPE_PXS)[::-1]
    w = (t - t[0])/max(1, t[-1]-t[0])
    out[idx] = (1-w)*f + w*b
cx = np.clip(out - CROP_W/2, 0, 1920-CROP_W)
json.dump(dict(n=[int(v) for v in n], x=[round(float(v),1) for v in cx], crop_w=CROP_W), open('facetrack.json','w'))
land, exit_ = [], []
for s in S[1:]:
    i0 = np.where(n == s['n0'])[0]; i1 = np.where(n == s['n0']-1)[0]
    if len(i0): land.append(abs(r[i0[0]]-out[i0[0]]))
    if len(i1): exit_.append(abs(r[i1[0]]-out[i1[0]]))
v = np.abs(np.diff(cx))/(np.diff(n)/FPS)
spl = set(int(s['n0']) for s in S[1:])
vv = np.array([v[i] for i in range(len(v)) if int(n[i+1]) not in spl])
print(f'{len(n)} samples; landing |raw-track| at n0: median {np.median(land):.0f} max {np.max(land):.0f}; at n0-1: median {np.median(exit_):.0f} max {np.max(exit_):.0f} (source px)')
print(f'crop pan inside segments: p90 {np.percentile(vv,90):.0f}  p99 {np.percentile(vv,99):.0f}  max {vv.max():.0f} px/s source  (x1.78 on the phone -> max {vv.max()*1080/608:.0f})')
