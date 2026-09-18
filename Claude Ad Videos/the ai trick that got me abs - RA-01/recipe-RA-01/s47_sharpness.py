#!/usr/bin/env python3
"""Rebuild sharpness.json on the ROUND-3 files.

Round 2 left `/framing/face_sharpness_lapvar` at the ROUND-1 numbers. This recomputes it with the
method its own `_method` string names -- variance of the Laplacian over the FaceMesh bounding box,
median of four frames -- on the graded native source, the delivered 9:16 master, and the approved
Ad 1 vertical. (The scale-normalised face256 version of the same comparison, which is the one to
judge by, is s33_verify.py's `face_sharpness_lapvar_face256` in r2/verify_9x16.json.)
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp

MASTER = sys.argv[1] if len(sys.argv) > 1 else "master_9x16.mp4"
AD1 = (f"{L.REPO}/Zeeshan Ad Videos/this picture got me abs - ad 1/"
       "this picture got me abs | claude | 9x16 | ad 1.mp4")
OURS_T = [13.0, 22.6, 34.0, 49.0]                 # four talking-head moments, both levels
AD1_T = [24.0, 36.0, 96.0, 135.0]
SRC_T = [57.5, 60.0, 70.0, 85.0]                  # source seconds inside kept spans
K = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)


def grab(path, t, vf=None):
    cmd = [L.FF, "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1"]
    if vf: cmd += ["-vf", vf]
    cmd += ["-f", "image2pipe", "-vcodec", "png", "-"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    import io
    return np.asarray(Image.open(io.BytesIO(out)).convert("RGB"))


def lapvar(a):
    H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a))
    if not r.multi_face_landmarks: return None, None
    xs = [p.x*W for p in r.multi_face_landmarks[0].landmark]
    ys = [p.y*H for p in r.multi_face_landmarks[0].landmark]
    x0, x1 = int(max(0, min(xs))), int(min(W, max(xs)))
    y0, y1 = int(max(0, min(ys))), int(min(H, max(ys)))
    c = a[y0:y1, x0:x1]
    if c.size < 400: return None, None
    g = np.asarray(Image.fromarray(c).convert("L"), float)
    return float(convolve2d(g, K, mode="valid").var()), (x1-x0)


def med(path, times, vf=None):
    vals, ws = [], []
    for t in times:
        v, w = lapvar(grab(path, t, vf))
        if v: vals.append(v); ws.append(w)
    return (round(float(np.median(vals)), 1) if vals else None,
            round(float(np.median(ws)), 0) if ws else None, len(vals))


GRADE = L.grade()
src, src_w, src_n = med(L.ROLL, SRC_T, f"{L.DECODE},{GRADE}")
our, our_w, our_n = med(MASTER, OURS_T)
ad1, ad1_w, ad1_n = med(AD1, AD1_T)
fm.close()
out = {"source_native": src, "delivered_9x16": our, "ad1_vertical_reference": ad1,
       "delivered_over_ad1": round(our/ad1, 3) if (our and ad1) else None,
       "face_box_px_wide": {"source_native": src_w, "delivered_9x16": our_w,
                            "ad1_vertical_reference": ad1_w},
       "frames_used": {"source": src_n, "delivered": our_n, "ad1": ad1_n},
       "measured_on": {"delivered": os.path.abspath(MASTER), "round": 3},
       "_method": "variance of the Laplacian over the FaceMesh bounding box, median of four frames "
                  "(NOT scale-normalised; the normalised face256 comparison is "
                  "r2/verify_9x16.json -> face_sharpness_lapvar_face256)"}
json.dump(out, open("sharpness.json", "w"), indent=1)
print(json.dumps(out, indent=1))
