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
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01-sq")
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


fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)


def _mesh(a):
    """FaceMesh, with the detect-then-crop fallback s04_track.py uses for a small face."""
    H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a))
    if r.multi_face_landmarks:
        return [(p.x*W, p.y*H) for p in r.multi_face_landmarks[0].landmark]
    d = fd.process(np.ascontiguousarray(a))
    if not d.detections: return None
    b = d.detections[0].location_data.relative_bounding_box
    cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
    s_ = max(b.width*W, b.height*H)*2.2
    x0, y0 = int(max(0, cx-s_/2)), int(max(0, cy-s_/2))
    x1, y1 = int(min(W, cx+s_/2)), int(min(H, cy+s_/2))
    rr = fm.process(np.ascontiguousarray(a[y0:y1, x0:x1]))
    if not rr.multi_face_landmarks: return None
    cw, ch = x1-x0, y1-y0
    return [(p.x*cw+x0, p.y*ch+y0) for p in rr.multi_face_landmarks[0].landmark]


def lapvar(a):
    H, W = a.shape[:2]
    P = _mesh(a)
    if P is None: return None, None
    xs = [q[0] for q in P]
    ys = [q[1] for q in P]
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
# ⚠ scale the source grab to the delivered height before detection: mediapipe returns no face on a
# 2160x3840 frame (the round-2 tracker scaled to 1080x1920 for the same reason). The measure is a
# per-pixel Laplacian variance, so this reports the source at the SAME scale as the delivered file.
src, src_w, src_n = med(L.ROLL, SRC_T, f"{L.DECODE},{GRADE},scale=1080:1920:flags=lanczos")
our, our_w, our_n = med(MASTER, OURS_T)
ad1, ad1_w, ad1_n = med(AD1, AD1_T)
fm.close(); fd.close()
out = {"source_native": src, "delivered_9x16": our, "ad1_vertical_reference": ad1,
       "delivered_over_ad1": round(our/ad1, 3) if (our and ad1) else None,
       "face_box_px_wide": {"source_native": src_w, "delivered_9x16": our_w,
                            "ad1_vertical_reference": ad1_w},
       "frames_used": {"source": src_n, "delivered": our_n, "ad1": ad1_n},
       "source_native_note": (None if src_n else "NOT MEASURED: no face detected on the graded "
                              "source frames at 1080x1920 (the face is ~120 px wide there); the "
                              "delivered-vs-Ad1 comparison below is the one the plan asks for"),
       "measured_on": {"delivered": os.path.abspath(MASTER), "round": 3},
       "_method": "variance of the Laplacian over the FaceMesh bounding box, median of four frames "
                  "(NOT scale-normalised; the normalised face256 comparison is "
                  "r2/verify_9x16.json -> face_sharpness_lapvar_face256)"}
json.dump(out, open("sharpness.json", "w"), indent=1)
print(json.dumps(out, indent=1))
