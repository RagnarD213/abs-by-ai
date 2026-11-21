#!/usr/bin/env python3
"""ROUND 2 verification, measured on the DELIVERED file.  s33_verify.py 9x16|16x9 <master>

Three things the build plan can only promise and the delivered pixels have to prove:

  R2  his FACE BOX stays inside 8-92 % of the frame width on every talking-head frame (round 1
      reached 98.2 %), sampled at 6 Hz -- denser than the 5 Hz crop track;
  R2  delivered face sharpness against the approved Ad 1 vertical, the same Laplacian-variance
      measure normalised to a 256 px face;
  R5  delivered face luma and CIELAB chroma against the Ad 1 vertical.

Writes r2/verify_<key>.json.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect
import mediapipe as mp

KEY, MASTER = sys.argv[1], sys.argv[2]
A = Aspect(KEY)
B = json.load(open("beats.json"))
TL = json.load(open(f"timeline_{KEY}.json"))
OUT = "r2"; os.makedirs(OUT, exist_ok=True)
AD1 = (f"{L.REPO}/Zeeshan Ad Videos/this picture got me abs - ad 1/"
       "this picture got me abs | claude | 9x16 | ad 1.mp4")
AD1_T = [21, 24, 33, 36, 42, 48, 90, 96, 132, 135]
FPS_S = 6.0

fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)


def landmarks(a):
    H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a))
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark
        return [(p.x*W, p.y*H) for p in Lm]
    d = fd.process(np.ascontiguousarray(a))
    if not d.detections: return None
    b = d.detections[0].location_data.relative_bounding_box
    cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
    s_ = max(b.width*W, b.height*H)*2.2
    x0, y0 = int(max(0, cx-s_/2)), int(max(0, cy-s_/2))
    x1, y1 = int(min(W, cx+s_/2)), int(min(H, cy+s_/2))
    rr = fm.process(np.ascontiguousarray(a[y0:y1, x0:x1]))
    if not rr.multi_face_landmarks: return None
    Lm = rr.multi_face_landmarks[0].landmark
    cw, ch = x1-x0, y1-y0
    return [(p.x*cw+x0, p.y*ch+y0) for p in Lm]


def lapvar_face(a, box):
    x0, y0, x1, y1 = [int(v) for v in box]
    c = a[max(0, y0):y1, max(0, x0):x1]
    if c.size < 400: return None
    g = np.asarray(Image.fromarray(c).convert("L").resize((256, 256), Image.LANCZOS), float)
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
    from scipy.signal import convolve2d
    return float(convolve2d(g, k, mode="valid").var())


def rgb2lab(px):
    c = px/255.0
    c = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787*xyz + 16/116)
    return 116*f[:, 1] - 16, 500*(f[:, 0]-f[:, 1]), 200*(f[:, 1]-f[:, 2])


def skin(a, box):
    x0, y0, x1, y1 = [int(v) for v in box]
    c = a[max(0, y0):y1, max(0, x0):x1].astype(np.float32)
    if c.size < 300: return None
    R, G, Bb = c[..., 0], c[..., 1], c[..., 2]
    m = (R > G+8) & (G > Bb) & (R > 55)
    if m.sum() < 200: return None
    px = c[m]
    Lv, av, bv = rgb2lab(px)
    luma = 0.2126*px[:, 0] + 0.7152*px[:, 1] + 0.0722*px[:, 2]
    return {"face_luma": float(np.median(luma)), "chroma": float(np.median(np.hypot(av, bv))),
            "a": float(np.median(av)), "b": float(np.median(bv))}


def frames_of(video, times, w, h):
    """One decoded frame per time, native size."""
    for t in times:
        raw = subprocess.run([L.FF, "-v", "error", "-nostdin", "-ss", f"{t:.3f}", "-i", video,
                              "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        if len(raw) < w*h*3:
            yield t, None; continue
        yield t, np.frombuffer(raw[:w*h*3], np.uint8).reshape(h, w, 3)


dan = [(p["beat"], p["end"], p["level"]) for p in TL["punch"]]
times = []
for a, b, lvl in dan:
    t = a + 0.12
    while t < b - 0.12:
        times.append((round(t, 3), lvl)); t += 1.0/FPS_S

W, H = A.VW, A.VH
rows, miss = [], 0
for (t, lvl), (_, a) in zip(times, frames_of(MASTER, [x[0] for x in times], W, H)):
    if a is None: miss += 1; continue
    P = landmarks(a)
    if P is None: miss += 1; continue
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    fx0, fx1 = min(xs), max(xs)
    rows.append({"t": t, "level": lvl,
                 "fx0_frac": round(fx0/W, 4), "fx1_frac": round(fx1/W, 4),
                 "fc_frac": round((fx0+fx1)/2/W, 4),
                 "lapvar": lapvar_face(a, (fx0, min(ys), fx1, max(ys))),
                 "skin": skin(a, (fx0, min(ys), fx1, max(ys)))})
worst_lo = min(r["fx0_frac"] for r in rows)
worst_hi = max(r["fx1_frac"] for r in rows)
bad = [r for r in rows if r["fx0_frac"] < 0.08 or r["fx1_frac"] > 0.92]

ref = []
for t, a in frames_of(AD1, AD1_T, 1080, 1920):
    if a is None: continue
    P = landmarks(a)
    if P is None: continue
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    ref.append({"lapvar": lapvar_face(a, (min(xs), min(ys), max(xs), max(ys))),
                "skin": skin(a, (min(xs), min(ys), max(xs), max(ys)))})
ref = [r for r in ref if r["lapvar"] and r["skin"]]

ours_lap = [r["lapvar"] for r in rows if r["lapvar"]]
ours_chr = [r["skin"]["chroma"] for r in rows if r["skin"]]
ours_lum = [r["skin"]["face_luma"] for r in rows if r["skin"]]
ref_lap = [r["lapvar"] for r in ref]
ref_chr = [r["skin"]["chroma"] for r in ref]
ref_lum = [r["skin"]["face_luma"] for r in ref]

out = {
 "file": os.path.abspath(MASTER), "samples": len(rows), "misses": miss, "sample_hz": FPS_S,
 "face_box_8_92": {"rule": "the face box stays inside 8-92 % of the frame width on every frame",
                   "worst_left_frac": round(worst_lo, 4), "worst_right_frac": round(worst_hi, 4),
                   "violations": len(bad), "worst": bad[:8],
                   "pass": not bad},
 "face_centre_frac": {"min": round(min(r["fc_frac"] for r in rows), 4),
                      "max": round(max(r["fc_frac"] for r in rows), 4),
                      "median": round(float(np.median([r["fc_frac"] for r in rows])), 4)},
 "face_sharpness_lapvar_face256": {
     "delivered_median": round(float(np.median(ours_lap)), 1),
     "ad1_vertical_median": round(float(np.median(ref_lap)), 1),
     "ratio": round(float(np.median(ours_lap)/np.median(ref_lap)), 3)},
 "face_colour": {
     "delivered_luma": round(float(np.median(ours_lum)), 1),
     "delivered_chroma": round(float(np.median(ours_chr)), 2),
     "ad1_vertical_luma": round(float(np.median(ref_lum)), 1),
     "ad1_vertical_chroma": round(float(np.median(ref_chr)), 2),
     "chroma_pct_of_ad1": round(100*float(np.median(ours_chr))/float(np.median(ref_chr)), 1),
     "floor_pct": 85.0},
}
json.dump(out, open(f"{OUT}/verify_{KEY}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "face_box_8_92"}, indent=1))
print("face box 8-92 %:", "PASS" if out["face_box_8_92"]["pass"] else "FAIL",
      out["face_box_8_92"]["worst_left_frac"], out["face_box_8_92"]["worst_right_frac"],
      f"({len(bad)} violation(s) of {len(rows)} samples)")
