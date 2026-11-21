#!/usr/bin/env python3
"""SL-06 R7: QC for a no-face object take. Over the intro window (S's length, from --off frames):
  - motion map: per-pixel standard deviation across the window (what moves: should be only dust / light / steam),
  - drift: mean absolute difference of each frame against the window's first frame, inside and outside the motion areas,
  - a strip of 6 frames and the motion map side by side for eyes-on review.
  python3 obj_qc.py S TAKE.mp4 [--off 12] [--out DIR]"""
import argparse, os
import cv2, numpy as np
N = {"A": 99, "B": 111, "C": 68, "E": 76, "F": 60}
ap = argparse.ArgumentParser(); ap.add_argument("S"); ap.add_argument("take"); ap.add_argument("--off", type=int, default=12)
ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "qc")); a = ap.parse_args()
os.makedirs(a.out, exist_ok=True); n = N[a.S]
cap = cv2.VideoCapture(a.take); F = []; i = 0
while len(F) < n:
    ok, f = cap.read()
    if not ok: break
    if i >= a.off: F.append(cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_AREA))
    i += 1
X = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in F])
sd = X.std(0); moving = cv2.GaussianBlur((sd > 6).astype(np.float32), (31, 31), 0) > 0.2
d = np.abs(X - X[0]).mean(axis=(1, 2)); dstill = np.array([np.abs(x - X[0])[~moving].mean() for x in X])
tag = os.path.basename(a.take)[:-4] + (f"@{a.off}" if a.off else "")
heat = cv2.applyColorMap(np.clip(sd * 8, 0, 255).astype(np.uint8), cv2.COLORMAP_JET)
idx = np.linspace(0, len(F) - 1, 6).astype(int)
strip = np.hstack([cv2.resize(F[k], (240, 427)) for k in idx] + [cv2.resize(heat, (240, 427))])
cv2.imwrite(os.path.join(a.out, f"{tag}_strip.jpg"), strip)
print(f"{tag}: frames {len(F)}  moving area {100 * moving.mean():.1f}%  drift max {d.max():.2f}  still-area drift max {dstill.max():.2f}")
