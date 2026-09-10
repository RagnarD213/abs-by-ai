#!/usr/bin/env python3
"""Framing fit of Zeeshan's cut against the raw roll, on the 256x144 gray caches.
For every 6th frame of his cut (0.25 s): guess the raw frame from the acoustic offset profile, then for each scale s
resize the raw frame by s and locate his template (x 64-165, y 8-112: head and torso, clear of his checklist and CTA
bar) inside it with normalised cross-correlation. Best (r, s, X0, Y0) per sample, over raw frames guess-3..guess+3.
Also per-frame scene-change score (mean |diff|) for the beat sheet. Writes fit.json, scenes.npy."""
import json, numpy as np, cv2, sys
HF, RF = 24.0, 30000/1001
his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1,144,256)
raw = np.memmap('raw256.gray', np.uint8, 'r').reshape(-1,144,256)
NH, NR = len(his), len(raw)
prof = json.load(open('offset_profile.json'))
PT = np.array([p[0] for p in prof if p[1] is not None and p[2] > 0.6]); PO = np.array([p[1] for p in prof if p[1] is not None and p[2] > 0.6])
def off(t):
    j = np.searchsorted(PT, t); c = [k for k in (j-1, j) if 0 <= k < len(PT)]
    return PO[min(c, key=lambda k: abs(PT[k]-t))]
X0T, X1T, Y0T, Y1T = 64, 166, 8, 112
SC = np.round(np.arange(1.00, 1.62, 0.02), 3)
out = []
for n in range(0, NH, 6):
    t = n/HF; g = int(round((t+off(t))*RF))
    T = his[n, Y0T:Y1T, X0T:X1T].astype(np.float32)
    if T.std() < 3: out.append(dict(n=n, r=0.0)); continue
    best = (-9,)
    for k in range(max(0,g-3), min(NR, g+4)):
        Rf = raw[k].astype(np.float32)
        for s in SC:
            W, H = int(round(256*s)), int(round(144*s))
            Rs = cv2.resize(Rf, (W, H), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
            res = cv2.matchTemplate(Rs, T, cv2.TM_CCOEFF_NORMED)
            _, mv, _, ml = cv2.minMaxLoc(res)
            if mv > best[0]:
                # template top-left in Rs = (X0 + X0T, Y0 + Y0T)  ->  crop origin of his frame in Rs = (ml - T offset)
                best = (mv, float(s), ml[0]-X0T, ml[1]-Y0T, k)
    r, s, X0, Y0, k = best
    # express the crop in 1920x1080 raw pixels: his frame = raw[y:y+1080/s, x:x+1920/s] scaled up
    out.append(dict(n=n, t=round(t,3), r=round(r,3), s=s, x=round(X0/s*7.5,1), y=round(Y0/s*7.5,1), k=int(k), g=g))
    if n % 600 == 0: print(n, out[-1], flush=True)
json.dump(out, open('fit.json','w'))
d = np.array([np.abs(his[i].astype(np.int16)-his[i-1].astype(np.int16)).mean() for i in range(1, NH)])
np.save('scenes.npy', d)
r = np.array([o['r'] for o in out]); print('samples', len(out), 'talk(r>=0.6)', (r>=0.6).mean().round(3))
