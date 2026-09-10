#!/usr/bin/env python3
"""Zeeshan's PICTURE EDL, recovered two ways and reconciled:
  * every segment's OFFSET comes from the dense acoustic profile (his mix vs the raw lav, r~0.99, +-1 ms) -- the
    picture matcher alone jitters +-0.2 s in low-motion stretches because the mouth is a few pixels at 256x144;
  * every CUT FRAME comes from the picture: at each audio join inside a talk range, his frames are scored against the
    raw at the outgoing and the incoming offset (with his framing); the crossover is his picture cut (J/L cuts land
    1-15 frames off the audio join -- skill lesson A5.13).
Framing per frame = the best of the distinct (s,x,y) framings his fit found in that talk range.
Writes edl_audio.json, edl_picture.json."""
import json, numpy as np, cv2
HF, RF = 24.0, 30000/1001
his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1,144,256)
raw = np.memmap('raw256.gray', np.uint8, 'r').reshape(-1,144,256)
prof = json.load(open('offset_profile.json')); F = json.load(open('fit.json')); P = json.load(open('pic.json'))
# ---- audio runs -----------------------------------------------------------------------------------------
L = [(t+0.35, o) for t, o, r in prof if o is not None and r > 0.85]
runs = []
for tc, o in L:
    if runs and abs(o - np.median(runs[-1]['o'][-6:])) < 0.025: runs[-1]['t'].append(tc); runs[-1]['o'].append(o)
    else: runs.append(dict(t=[tc], o=[o]))
runs = [r for r in runs if len(r['t']) >= 3]
A = []
for r in runs:
    o = float(np.median(r['o']))
    if A and abs(A[-1]['off'] - o) < 0.02: A[-1]['t1'] = r['t'][-1]; continue
    A.append(dict(t0=r['t'][0], t1=r['t'][-1], off=o))
for i in range(len(A)-1):                     # audio join = midway through the unlocked gap between runs
    A[i]['join_after'] = (A[i]['t1'] + A[i+1]['t0'])/2
json.dump(A, open('edl_audio.json','w'), indent=1)
print(len(A), 'audio runs')
def run_at(t):
    for i, a in enumerate(A):
        if t < a.get('join_after', 1e9): return i
    return len(A)-1
# ---- talk ranges from the per-frame matcher ------------------------------------------------------------
r = np.array([p['r'] for p in P]); talk = r >= 0.80
m = his.reshape(len(his), -1).mean(1)
for n in range(1, len(P)-1):
    if m[n] - m[n-1] > 18 and talk[n-1]: talk[n] = True          # one-frame white flash on a talk cut
gi = 0
while gi < len(talk):
    if not talk[gi]:
        gj = gi
        while gj < len(talk) and not talk[gj]: gj += 1
        if gi > 0 and gj < len(talk) and gj - gi <= 12: talk[gi:gj] = True   # bridge short gaps inside talk
        gi = gj
    else: gi += 1
TR = []; i = 0
while i < len(P):
    if talk[i]:
        j = i
        while j+1 < len(P) and talk[j+1]: j += 1
        if j - i >= 3: TR.append((i, j+1))
        i = j+1
    else: i += 1
def framings(a, b):
    fs = [f for f in F if a <= f['n'] < b and f['r'] >= 0.9]
    out = []
    for f in fs:
        if not any(abs(f['s']-g[0]) < 0.03 and abs(f['x']-g[1]) < 40 and abs(f['y']-g[2]) < 40 for g in out):
            out.append((f['s'], f['x'], f['y']))
    return out or [(1.0, 0.0, 0.0)]
Y0, Y1, X0, X1 = 8, 112, 64, 166
def warp(k, fr):
    s, x, y = fr; M = np.float32([[s, 0, -x*s/7.5], [0, s, -y*s/7.5]])
    return cv2.warpAffine(raw[int(k)], M, (256,144), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def ncc(a, b):
    a = a.astype(np.float32); b = b.astype(np.float32); a -= a.mean(); b -= b.mean()
    return float((a*b).sum()/max(np.sqrt((a*a).sum()*(b*b).sum()), 1e-6))
def score(n, off, fr):
    k = round((n/HF + off)*RF)
    return ncc(his[n, Y0:Y1, X0:X1], warp(k, fr)[Y0:Y1, X0:X1])
SEG = []
for a, b in TR:
    FR = framings(a, b)
    def best(n, off):
        return max((score(n, off, fr), fr) for fr in FR)
    # runs active in this range
    ids = sorted(set(run_at(n/HF) for n in range(a, b)))
    cuts = []                                  # (frame, from_run, to_run)
    for i0, i1 in zip(ids[:-1], ids[1:]):
        j = A[i0]['join_after']; nj = int(round(j*HF))
        lo, hi = max(a, nj-24), min(b, nj+25)
        d = [best(n, A[i1]['off'])[0] - best(n, A[i0]['off'])[0] for n in range(lo, hi)]
        cross = None
        for k in range(len(d)-2):
            if d[k] > 0.01 and d[k+1] > 0.01 and d[k+2] > 0.01: cross = lo+k; break
        cuts.append((cross if cross is not None else nj, i0, i1, cross is not None, nj))
    # first run of the range: the one whose offset matches the first frames best
    starts = [a] + [c[0] for c in cuts]; ends = [c[0] for c in cuts] + [b]; rids = [ids[0]] + [c[2] for c in cuts]
    for s0, s1, ri in zip(starts, ends, rids):
        if s1 <= s0: continue
        off = A[ri]['off']
        frs = [best(n, off) for n in range(s0, s1)]
        sc = [v for v, _ in frs]
        # dominant framing per frame (kept per frame, the vertical's own crop is ours anyway)
        SEG.append(dict(n0=s0, n1=s1, t0=round(s0/HF,4), t1=round(s1/HF,4), off=round(off,4), run=ri,
                        src_in=round(s0/HF+off,4), rmin=round(min(sc),3), rmed=round(float(np.median(sc)),3),
                        framing=[list(map(float, fr)) for _, fr in frs]))
    for c in cuts:
        print(f'  range {a/HF:7.2f}-{b/HF:7.2f}: audio join {c[4]/HF:7.3f} -> picture cut {c[0]/HF:7.3f} ({c[0]-c[4]:+d} fr){"" if c[3] else "  NO CROSSOVER (kept audio join)"}')
for s in SEG:
    s['framing_mode'] = max(set(map(tuple, s['framing'])), key=[tuple(f) for f in s['framing']].count)
json.dump(SEG, open('edl_picture.json','w'))
print(len(TR), 'talk ranges,', len(SEG), 'picture segments')
for s in SEG:
    print(f"  {s['t0']:8.3f}-{s['t1']:8.3f}  off {s['off']:+8.3f}  src {s['src_in']:8.3f}  r med {s['rmed']:.3f} min {s['rmin']:.3f}  framing {tuple(round(v,2) for v in s['framing_mode'])}")
