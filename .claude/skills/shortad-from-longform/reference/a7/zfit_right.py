#!/usr/bin/env python3
"""Second framing pass for his WINDOW beats (bullets left / Dan right): the centre template of zfit.py sits over his
text panel there. Re-fit every sample zfit scored < 0.80 with a RIGHT-HALF template (x 150-250 of 256) and keep the
better of the two; each sample records the template box it was fitted with (tb) so zpic2/zedl score with the same box."""
import json, numpy as np, cv2
HF, RF = 30000/1001, 30000/1001
his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1,144,256)
raw = np.memmap('raw256.gray', np.uint8, 'r').reshape(-1,144,256)
NR = len(raw)
prof = json.load(open('offset_profile.json'))
PT = np.array([p[0] for p in prof if p[1] is not None and p[2] > 0.6]); PO = np.array([p[1] for p in prof if p[1] is not None and p[2] > 0.6])
def off(t):
    j = np.searchsorted(PT, t); c = [k for k in (j-1, j) if 0 <= k < len(PT)]
    return PO[min(c, key=lambda k: abs(PT[k]-t))]
F = json.load(open('fit.json'))
TB_C = (64, 166, 8, 112); TB_R = (150, 252, 8, 112)
SC = np.round(np.arange(1.00, 1.62, 0.02), 3)
n_re = 0
for o in F:
    o.setdefault('tb', TB_C)
    if o.get('r', 0) >= 0.80: continue
    n = o['n']; t = n/HF; g = int(round((t+off(t))*RF))
    X0T, X1T, Y0T, Y1T = TB_R
    T = his[n, Y0T:Y1T, X0T:X1T].astype(np.float32)
    if T.std() < 3: continue
    best = (-9,)
    for k in range(max(0,g-3), min(NR, g+4)):
        Rf = raw[k].astype(np.float32)
        for s in SC:
            W, H = int(round(256*s)), int(round(144*s))
            Rs = cv2.resize(Rf, (W, H), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
            if Rs.shape[0] < T.shape[0] or Rs.shape[1] < T.shape[1]: continue
            res = cv2.matchTemplate(Rs, T, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(res)
            if mv > best[0]: best = (mv, float(s), ml[0]-X0T, ml[1]-Y0T, k)
    if best[0] > o.get('r', 0):
        r, s, X0, Y0, k = best
        o.update(r=round(r,3), s=s, x=round(X0/s*7.5,1), y=round(Y0/s*7.5,1), k=int(k), g=g, tb=TB_R); n_re += 1
json.dump(F, open('fit.json','w'))
r = np.array([o['r'] for o in F]); print('re-fitted', n_re, 'samples; talk(r>=0.6)', (r>=0.6).mean().round(3), ' r>=0.8', (r>=0.8).mean().round(3))
