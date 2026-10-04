#!/usr/bin/env python3
"""WHICH RAW FRAME DOES HIS FRAME n SHOW, read off HIS FACE (FaceMesh on both): mouth opening, mouth width, head tilt and
yaw are scale-free, so they hold under his punch-in ramp where whole-frame matching fails; with --abs (his frame is the
raw frame, framing 1.0) the face position and size are compared too, which pins a walk-out or a slow-down.
A Viterbi path over frames gives k(n): real time is free, a hold or a jump costs.
  python3 zlips.py N0 N1 D0 LO HI [--abs]   -> prints runs, writes kmap_N0_N1.json"""
import json, subprocess, sys, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
N0, N1, D0, LO, HI = (int(x) for x in sys.argv[1:6]); ABS = '--abs' in sys.argv
W, H = 1920, 1080
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.3)
def feats(src, k0, n):
    p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-ss', f'{max(0, k0/FPS - 0.0002):.5f}', '-i', src, '-frames:v', str(n), '-vf',
                          'scale=in_color_matrix=bt709:flags=accurate_rnd,format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=10**8)
    out = []
    for _ in range(n):
        b = p.stdout.read(W*H*3)
        if len(b) < W*H*3: break
        r = fm.process(np.frombuffer(b, np.uint8).reshape(H, W, 3))
        if not r.multi_face_landmarks: out.append(None); continue
        L = np.array([(l.x*W, l.y*H) for l in r.multi_face_landmarks[0].landmark])
        fh = np.linalg.norm(L[10] - L[152]); fw = np.linalg.norm(L[234] - L[454])
        eye = L[263] - L[33]
        out.append(dict(open=np.linalg.norm(L[13] - L[14])/fh, width=np.linalg.norm(L[61] - L[291])/fw,
                        tilt=float(np.arctan2(eye[1], eye[0])), yaw=float((L[1][0] - L[234][0])/fw),
                        pitch=float((L[1][1] - L[10][1])/fh), brow=float(np.linalg.norm(L[105] - L[159])/fh),
                        cx=float(L[1][0]), cy=float(L[1][1]), fh=float(fh)))
    p.kill(); return out
A = feats('reference.mp4', N0, N1 - N0); k_lo = N0 + D0 + LO; k_hi = N1 + D0 + HI
R = feats('raw.mp4', k_lo, k_hi - k_lo)
print(f'faces: his {sum(a is not None for a in A)}/{len(A)}, raw {sum(a is not None for a in R)}/{len(R)}', flush=True)
KEYS = [('open', 0.025), ('width', 0.03), ('tilt', 0.03), ('yaw', 0.03), ('pitch', 0.02), ('brow', 0.01)] + ([('cx', 14.0), ('cy', 10.0), ('fh', 8.0)] if ABS else [])
ks = np.arange(LO, HI + 1); C0 = np.full((len(A), len(ks)), 3.0, np.float32)
for i, a in enumerate(A):
    if a is None: C0[i] = 1.0; continue
    for j, dk in enumerate(ks):
        k = N0 + i + D0 + dk - k_lo
        if 0 <= k < len(R) and R[k] is not None:
            C0[i, j] = float(np.mean([min(abs(a[f] - R[k][f])/s, 3.0) for f, s in KEYS]))
C = np.full_like(C0, 1e9); B = np.zeros(C0.shape, int); C[0] = C0[0]
pen = lambda a, b: 0.0 if a == b else 0.25 + 0.03*abs(a - b)
for i in range(1, len(C0)):
    for j in range(len(ks)):
        c = [C[i-1, q] + pen(q, j) for q in range(len(ks))]; q = int(np.argmin(c)); C[i, j] = c[q] + C0[i, j]; B[i, j] = q
path = [int(np.argmin(C[-1]))]
for i in range(len(C0) - 1, 0, -1): path.append(B[i, path[-1]])
path = path[::-1]; d = [D0 + int(ks[j]) for j in path]
runs = []
for i, v in enumerate(d):
    if runs and runs[-1][2] == v: runs[-1][1] = N0 + i + 1
    else: runs.append([N0 + i, N0 + i + 1, v])
for a, b, v in runs:
    j = list(ks).index(v - D0); j0 = list(ks).index(0)
    print(f'  his {a:5d}-{b:5d}  d {v}  ({b-a} frames)  cost {C0[a-N0:b-N0, j].mean():.2f}  (at the nominal d {D0}: {C0[a-N0:b-N0, j0].mean():.2f})')
json.dump(dict(n0=N0, n1=N1, d=d, runs=runs), open(f'kmap_{N0}_{N1}.json', 'w'))
