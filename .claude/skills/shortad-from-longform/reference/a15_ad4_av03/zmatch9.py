#!/usr/bin/env python3
"""WHICH RAW FRAME DOES HIS FRAME n SHOW? A precise per-frame match for the stretches where pic.json (256x144, whole-frame
NCC) is too coarse: the hook under his punch-in ramp and the closing shot under his pill. 640x360, high-passed (edges:
mouth, eyes, hands), warped by his fitted framing, scored over the head-and-torso box, then a Viterbi path over frames so
the answer is a clean k(n): advancing one raw frame per frame is free, a hold or a jump costs.
  python3 zmatch9.py N0 N1 D0 LO HI   -> prints the path as runs; writes kmap_N0_N1.json"""
import json, subprocess, sys, numpy as np, cv2
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
N0, N1, D0, LO, HI = (int(x) for x in sys.argv[1:6])
W, H = 640, 360
def dec(src, k0, n):
    b = subprocess.run([FF, '-nostdin', '-v', 'error', '-ss', f'{max(0, k0/FPS - 0.0002):.5f}', '-i', src, '-frames:v', str(n), '-vf',
                        f'scale={W}:{H}:flags=area:in_color_matrix=bt709,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, H, W).astype(np.float32)
def hp(a): return a - cv2.GaussianBlur(a, (0, 0), 6)
his = dec('reference.mp4', N0, N1 - N0)
k_lo, k_hi = N0 + D0 + LO, N1 + D0 + HI
raw = dec('raw.mp4', k_lo, k_hi - k_lo)
assert len(his) == N1 - N0 and len(raw) == k_hi - k_lo, (len(his), len(raw))
F = sorted(json.load(open('fit.json')), key=lambda o: o['n'])
def framing(n):
    c = [o for o in F if o.get('r', 0) >= 0.55 and abs(o['n'] - n) <= 9]
    o = min(c, key=lambda o: abs(o['n'] - n)) if c else dict(s=1.0, x=0.0, y=0.0)
    return o['s'], o['x'], o['y']
ks = np.arange(LO, HI + 1); S = np.full((N1 - N0, len(ks)), -1.0, np.float32)
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5)
def ncc(a, b):
    a = a - a.mean(); b = b - b.mean(); return float((a*b).sum()/max(np.sqrt((a*a).sum()*(b*b).sum()), 1e-6))
Mprev = None
for i in range(N1 - N0):
    n = N0 + i; Hi = his[i]
    # REGISTER his frame to the raw by ECC (scale + shift), seeded by the fitted framing or the previous frame's answer:
    # the fitted framing is too coarse under his punch ramp, and a 2 % scale error swamps a 2-frame mouth difference
    s0, x0, y0 = framing(n)
    seeds = ([Mprev] if Mprev is not None else []) + [np.float32([[s0, 0, -x0*s0/3], [0, s0, -y0*s0/3]])]
    k0 = int(np.clip(n + D0 - k_lo, 0, len(raw) - 1)); best = (-9, None)
    for M0 in seeds:
        try:
            cc, M = cv2.findTransformECC(cv2.GaussianBlur(Hi, (0, 0), 2), cv2.GaussianBlur(raw[k0], (0, 0), 2), M0.copy(), cv2.MOTION_AFFINE, crit, None, 5)
            if cc > best[0]: best = (cc, M)
        except cv2.error: pass
    M = best[1] if best[1] is not None else seeds[-1]; Mprev = M
    Hh = hp(Hi)[30:330, 120:520]
    for j, dk in enumerate(ks):
        k = n + D0 + dk - k_lo
        if 0 <= k < len(raw):
            R = hp(cv2.warpAffine(raw[k], M, (W, H), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE))[30:330, 120:520]
            S[i, j] = ncc(Hh, R)
# Viterbi: state = dk; from frame to frame staying on the same dk (real time) is free
C = np.full_like(S, 1e9); B = np.zeros(S.shape, int); C[0] = -S[0]
pen = lambda a, b: 0.0 if a == b else 0.03 + 0.004*abs(a - b)
for i in range(1, len(S)):
    for j in range(len(ks)):
        c = [C[i-1, q] + pen(q, j) for q in range(len(ks))]; q = int(np.argmin(c)); C[i, j] = c[q] - S[i, j]; B[i, j] = q
path = [int(np.argmin(C[-1]))]
for i in range(len(S) - 1, 0, -1): path.append(B[i, path[-1]])
path = path[::-1]; d = [D0 + int(ks[j]) for j in path]
runs = []
for i, v in enumerate(d):
    if runs and runs[-1][2] == v: runs[-1][1] = N0 + i + 1
    else: runs.append([N0 + i, N0 + i + 1, v])
for a, b, v in runs: print(f'  his {a:5d}-{b:5d}  d {v}  ({b-a} frames)  mean score {S[a-N0:b-N0, list(ks).index(v-D0)].mean():.3f}')
print('  raw argmax per frame (no smoothing), every 4th:', [(N0+i, D0+int(ks[int(np.argmax(S[i]))]), round(float(S[i].max()), 2)) for i in range(0, len(S), 4)])
json.dump(dict(n0=N0, n1=N1, d=d), open(f'kmap_{N0}_{N1}.json', 'w'))
