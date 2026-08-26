#!/usr/bin/env python3
"""Fit (scale, dx, dy) mapping the conform to Muhammad's rendered frame, sampled at 4 fps.
FFT cross-correlation for the shift, a loop over scales, so 931 frames run in seconds."""
import json, os, sys
import numpy as np
from PIL import Image

W, H = 320, 180
SCALES = np.round(np.arange(1.00, 1.45, 0.02), 3)
MAXSH  = 18

def nz(a):
    a = a.astype(np.float32); a -= a.mean(); s = a.std()
    return a/s if s > 1e-6 else a

def best_shift(rn, zn):
    """peak of the circular cross-correlation, restricted to +-MAXSH."""
    C = np.fft.irfft2(np.fft.rfft2(rn) * np.conj(np.fft.rfft2(zn)), s=(H, W)) / (H*W)
    idx = [(dy, dx) for dy in range(-MAXSH, MAXSH+1) for dx in range(-MAXSH, MAXSH+1)]
    vals = [C[dy % H, dx % W] for dy, dx in idx]
    k = int(np.argmax(vals))
    return idx[k][1], idx[k][0], float(vals[k])

def fit(ref, base):
    rn = nz(ref)
    bimg = Image.fromarray(base)
    best = (1.0, 0, 0, -1.0)
    for s in SCALES:
        cw, ch = W/s, H/s
        box = ((W-cw)/2, (H-ch)/2, (W+cw)/2, (H+ch)/2)
        z = np.asarray(bimg.resize((W, H), Image.BILINEAR, box=box))
        dx, dy, v = best_shift(rn, nz(z))
        if v > best[3]: best = (float(s), dx, dy, v)
    return best

if __name__ == '__main__':
    S = json.load(open('edl_final.json'))
    R = lambda d, n: np.asarray(Image.open(f'ref_audit/{d}/{n:05d}.png').convert('L'))
    out = []
    for s in S:
        i, a, b = s['i'], s['cut_in'], s['cut_out']
        res = []
        for f in (0.25, 0.5, 0.75):
            n = int(round((a + (b-a)*f) * 4)) + 1
            n = max(1, min(931, n))
            res.append(fit(R('gr', n), R('gb', n)))
        pick = max(res, key=lambda r: r[3])            # the frame that fit best
        sc = float(np.median([r[0] for r in res]))
        out.append(dict(i=i, t0=a, t1=b, dur=round(b-a,3),
                        scale=sc, scales=[r[0] for r in res],
                        dx=pick[1], dy=pick[2], ncc=round(pick[3],3)))
        print(f'{i:3d} {a:7.2f}-{b:7.2f} ({b-a:5.2f}s) s={sc:.2f} '
              f'all={[f"{r[0]:.2f}" for r in res]} dx={pick[1]:+3d} dy={pick[2]:+3d} ncc={pick[3]:.3f}',
              flush=True)
    json.dump(out, open('ref_audit/framing.json','w'), indent=1)
