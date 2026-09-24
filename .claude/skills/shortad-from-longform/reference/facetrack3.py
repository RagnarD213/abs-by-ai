#!/usr/bin/env python3
"""Face track, smoothed PER SOURCE-CONTINUOUS SEGMENT, zero-phase AND ENDPOINT-ANCHORED.

facetrack2.py averaged a forward slope-limited pass with a backward one. Each pass is exact at
the end it starts from and lagging at the other end, so the AVERAGE is off at BOTH ends -- by up
to 72 source px (128 on the phone) on this ad, measured as the crop's landing error at his cuts
(20.98 s) and its exit error just before them (83.25 s). On the phone that reads as "he lands
off-centre after the cut and the frame slides into place" -- the one thing a per-segment track
exists to prevent.

Fix: blend the two passes with a weight that trusts the FORWARD pass at the segment start and the
BACKWARD pass at the segment end (w = i/(n-1)), so out[0] == m[0] and out[-1] == m[-1] exactly,
and the middle is still the zero-phase average. Both passes obey the slope limit; the blend adds
at most |fwd-bwd|/n per sample, which is negligible.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "cut"))
import landing
FPS = 30000/1001
raw = np.load('raw_torso.npy')
idx = np.arange(len(raw)); ok = ~np.isnan(raw)
r = np.interp(idx, idx[ok], raw[ok])
FPS_T = 4
CROP_W = 608
SLOPE = 200.0/FPS_T                      # px per sample
S = json.load(open('edl_picture.json'))   # picture segments, not audio

out = r.copy()
for s in S:
    i0 = int(round(s['cut_in']*FPS_T)); i1 = int(round(s['cut_out']*FPS_T))
    i0 = max(0, i0); i1 = min(len(r), max(i1, i0+1))
    t = np.arange(i0, i1) * (FPS/FPS_T)                  # sample index -> frame index
    out[i0:i1] = landing.smooth_segment(t, r[i0:i1], SLOPE*FPS_T, fps=FPS)   # the shared smoother (_shared/cut/landing.py)
cx = np.clip(out - CROP_W/2, 0, 1920-CROP_W)
json.dump(dict(fps=FPS_T, crop_w=CROP_W, x=[round(float(v),1) for v in cx]),
          open('facetrack.json','w'))
print(f'{len(cx)} samples   centre {out.min():.0f}..{out.max():.0f} (sd {out.std():.1f})')
land, exit_ = [], []
for s in S[1:]:
    i0 = int(np.ceil(s['cut_in']*FPS_T - 1e-6)); j = i0-1
    if 0 <= i0 < len(r): land.append(abs(r[i0]-out[i0]))
    if 0 <= j < len(r): exit_.append(abs(r[j]-out[j]))
print(f'landing error at the first sample after a splice: median {np.median(land):.0f}  p90 {np.percentile(land,90):.0f}  max {np.max(land):.0f} src px')
print(f'exit error at the last sample before a splice:    median {np.median(exit_):.0f}  p90 {np.percentile(exit_,90):.0f}  max {np.max(exit_):.0f} src px')
v = np.abs(np.diff(cx))*FPS_T
print(f'crop pan rate: p90 {np.percentile(v,90):.0f} px/s  p99 {np.percentile(v,99):.0f}  max {v.max():.0f} (source px; splices excluded below)')
spl = set(int(np.ceil(s['cut_in']*FPS_T-1e-6)) for s in S[1:])
vv = [abs(cx[i+1]-cx[i])*FPS_T for i in range(len(cx)-1) if (i+1) not in spl]
print(f'   inside segments only: p90 {np.percentile(vv,90):.0f}  p99 {np.percentile(vv,99):.0f}  max {np.max(vv):.0f} px/s')
