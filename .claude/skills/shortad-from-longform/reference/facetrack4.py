#!/usr/bin/env python3
"""Face track on EXACT frame indices (raw_torso.npy + raw_torso_n.npy), smoothed per picture segment,
zero-phase, endpoint-anchored (median window shrinks to zero at the segment ends), slope-limited.
Writes facetrack.json = {n: [frame indices], x: [crop x per sample]} -- render.py interpolates in frame time."""
import json, os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "cut"))
import landing
raw = np.load('raw_torso.npy'); n = np.load('raw_torso_n.npy').astype(int)
FPS = 30000/1001; CROP_W = 608
SLOPE_PXS = 170.0                         # source px/s (~300 px/s on the phone), the re-audit's cap
ok = ~np.isnan(raw); r = np.interp(n, n[ok], raw[ok])
S = json.load(open('edl_picture.json'))
out = r.copy()
for s in S:
    m = (n >= s['n0']) & (n < s['n1'])
    if m.any():
        out[m] = landing.smooth_segment(n[m], r[m], SLOPE_PXS)     # the shared smoother (_shared/cut/landing.py)
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
