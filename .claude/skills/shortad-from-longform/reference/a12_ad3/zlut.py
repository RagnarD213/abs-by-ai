#!/usr/bin/env python3
"""HIS GRADE AS A 3D LUT, fitted from pixel-for-pixel correspondences. On every talk segment at framing (1,0,0) his
frame IS the raw frame on the same pixel grid (the EDL puts them on the same instant), so each pixel is a (raw rgb ->
his rgb) sample. A per-channel curve could not fit him (centre box right = fridge 21 levels too red; wide fit = skin 9
off): his grade has cross-channel work. Binned 33^3 (median of his rgb per raw-rgb bin, overlays rejected by the
median), empty bins filled from a Gaussian-smoothed estimate. Validated on held-out frames by region. Writes his.cube."""
import json, subprocess, numpy as np
from scipy.ndimage import gaussian_filter
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
E = json.load(open('edl_picture.json'))
ns = []
for s in E:
    for k in range(s['n0']+6, s['n1']-6, 18):
        if tuple(s['framing'][k-s['n0']]) == (1.0, 0.0, 0.0): ns.append((k, k/(30000/1001) + s['off']))
fit, hold = ns[::2][:60], ns[1::2][:20]
W, H = 960, 540
def grab(src, t):
    # ⚠ DECODE AS A PLAYER DOES (2026-09-13, Dan rejected render 9's colour). His ad3_v6hd.mp4 carries NO colour tags, and
    # ffmpeg's scaler reads an untagged file with the BT.601 matrix -- but VLC and every browser show untagged HD as BT.709.
    # Fitted to the 601 reading, the grade matched his file in every ffmpeg measurement and looked darker, muddier and less
    # vivid than his in VLC. Force BT.709 / TV range on BOTH inputs (the raw is tagged 709 already; forcing it is a no-op).
    b = subprocess.run([FF,'-nostdin','-v','error','-ss',f'{t:.4f}','-i',src,'-frames:v','1','-vf',f'scale={W}:{H}:flags=area:in_color_matrix=bt709:in_range=tv',
                        '-pix_fmt','rgb24','-f','rawvideo','-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)/255
def pair(lst): return np.stack([grab('reference.mp4', n/(30000/1001)-0.01) for n, _ in lst]), np.stack([grab('raw.mp4', t+0.001) for _, t in lst])
Hf, Of = pair(fit)
# drop regions his overlays can occupy (checklist top-right, lower-third/CTA bands) -- the median rejects the rest
mask = np.ones((H, W), bool); mask[420:, :] = False; mask[0:210, 0:330] = False; mask[0:160, 830:] = False   # his lower thirds/chips, the note+title, the photo panels
src = Of[:, mask].reshape(-1, 3); dst = Hf[:, mask].reshape(-1, 3)
N = 33; idx = np.clip(np.round(src*(N-1)).astype(int), 0, N-1)
flat = idx[:, 0]*N*N + idx[:, 1]*N + idx[:, 2]
order = np.argsort(flat); flat_s = flat[order]; dst_s = dst[order]
uniq, start, cnt = np.unique(flat_s, return_index=True, return_counts=True)
lut = np.zeros((N*N*N, 3), np.float32); wts = np.zeros(N*N*N, np.float32)
for u, s0, c in zip(uniq, start, cnt):
    if c >= 6: lut[u] = np.median(dst_s[s0:s0+c], 0); wts[u] = min(c, 400)
lut = lut.reshape(N, N, N, 3); wts = wts.reshape(N, N, N)
# fill: smoothed weighted average, then blend toward identity far from any data
sm = np.stack([gaussian_filter(lut[..., c]*wts, 1.2) for c in range(3)], -1)
sw = gaussian_filter(wts, 1.2)[..., None]
g = np.stack(np.meshgrid(*[np.linspace(0, 1, N)]*3, indexing='ij'), -1)
est = np.where(sw > 1e-3, sm/np.maximum(sw, 1e-6), g)
filled = np.where(wts[..., None] > 0, 0.5*lut + 0.5*est, est)
# regions with no data at all: pull gently toward the nearest data via repeated smoothing
for _ in range(6):
    far = gaussian_filter(wts, 3.0)[..., None] < 0.5
    filled = np.where(far, np.stack([gaussian_filter(filled[..., c], 1.5) for c in range(3)], -1), filled)
filled = np.clip(filled, 0, 1)
print('bins with data:', int((wts > 0).sum()), 'of', N**3)
with open('his.cube', 'w') as f:
    f.write('TITLE "muhammad ad3 grade (fitted)"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
    for b in range(N):                     # .cube order: R fastest, then G, then B
        for gg in range(N):
            for r in range(N):
                v = filled[r, gg, b]; f.write(f'{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
# validate on held-out frames with trilinear lookup
from scipy.ndimage import map_coordinates
def apply(img):
    c = img.reshape(-1, 3)*(N-1)
    out = np.stack([map_coordinates(filled[..., k], c.T, order=1, mode='nearest') for k in range(3)], -1)
    return out.reshape(img.shape)
Hh, Oh = pair(hold)
P = np.stack([apply(o) for o in Oh])
REG = dict(centre=(slice(150,390), slice(325,635)), face=(slice(75,210), slice(415,545)), fridge=(slice(75,250), slice(625,750)),
           door=(slice(300,450), slice(75,225)), wall=(slice(10,60), slice(560,700)))
for k, r in REG.items():
    e = np.median(P[:, r[0], r[1]].reshape(-1, 3), 0)*255 - np.median(Hh[:, r[0], r[1]].reshape(-1, 3), 0)*255
    print(f'  held-out {k:7s} error R/G/B {np.round(e,1)}')
m2 = mask.copy()
print('  held-out mean |error| over the masked frame (levels):', np.round(np.abs(P[:, m2]-Hh[:, m2]).mean((0,1))*255, 2))
