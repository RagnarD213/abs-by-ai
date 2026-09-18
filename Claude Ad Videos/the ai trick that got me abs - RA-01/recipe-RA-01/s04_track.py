#!/usr/bin/env python3
"""Hair-top and head-centre track over the kept source spans, at 4 samples/s.

Measured on the GRADED picture at half scale (1080x1920) and reported in SOURCE pixels, so the
crop is anchored to the same thing the delivered-frame gate measures (website rev 3 lesson 106:
the sampler that gates the delivery is the sampler that anchors the crop).

A climb shorter than 0.10 or longer than 0.60 of the face height is a MISS and reads LOW, the
dangerous direction — discarded, and the count is printed.
"""
import json, os, subprocess, sys, tempfile, shutil
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp

CUT = json.load(open("cut.json"))
# ROUND 2, R2: the crop now has to keep his FACE BOX inside 8-92 % of the frame width on every
# frame, so the track records the face box as well as its centre, and samples 5x a second instead
# of 4 -- round 1's worst lean (face at 98.2 % of frame width) fell between two 4 Hz samples.
SAMPLE_FPS = 5.0
HALF = 2.0                      # 1080x1920 measurement scale -> source pixels
GRADE = L.grade()               # grade.json: the one exposure + saturation (R5)

pieces = CUT["pieces"]
times = []
for p in pieces:
    t = p["src_in"] + 0.06
    while t < p["src_out"] - 0.06:
        times.append((round(t, 3), p["t_in"] + (t - p["src_in"])))
        t += 1.0/SAMPLE_FPS
print(f"{len(times)} samples over {len(pieces)} source pieces")

tmp = tempfile.mkdtemp(prefix="ra01trk_")
paths = []
for i, (st, tt) in enumerate(times):
    p = os.path.join(tmp, "%04d.png" % i)
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{st:.3f}", "-i", L.ROLL,
                    "-frames:v", "1", "-vf", f"{L.DECODE},{GRADE},scale=1080:1920:flags=lanczos",
                    "-y", p], check=True)
    paths.append(p)
mdir = os.path.join(tmp, "m")
for i in range(0, len(paths), 150):
    subprocess.run([L.PERSONMASK, mdir] + paths[i:i+150], capture_output=True, text=True)

fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
out, miss = [], 0
for i, (st, tt) in enumerate(times):
    a = np.asarray(Image.open(paths[i]).convert("RGB")); H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a)); P = None
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark
        P = {k: (Lm[k].x*W, Lm[k].y*H) for k in (10, 152, 234, 454)}
    if P is None:
        d = fd.process(np.ascontiguousarray(a))
        if d.detections:
            b = d.detections[0].location_data.relative_bounding_box
            cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
            s = max(b.width*W, b.height*H)*2.2
            x0, y0 = int(max(0, cx-s/2)), int(max(0, cy-s/2))
            x1, y1 = int(min(W, cx+s/2)), int(min(H, cy+s/2))
            cr = np.ascontiguousarray(a[y0:y1, x0:x1]); rr = fm.process(cr)
            if rr.multi_face_landmarks:
                Lm = rr.multi_face_landmarks[0].landmark; cw, ch = x1-x0, y1-y0
                P = {k: (Lm[k].x*cw+x0, Lm[k].y*ch+y0) for k in (10, 152, 234, 454)}
    mp_ = os.path.join(mdir, os.path.basename(paths[i])[:-4] + ".mask.png")
    if P is None or not os.path.exists(mp_):
        miss += 1; continue
    m = np.asarray(Image.open(mp_).convert("L"), dtype=np.float32)/255.0
    cx = (P[234][0]+P[454][0])/2; fw = abs(P[454][0]-P[234][0])
    fore, chin = P[10][1], P[152][1]; fh = chin-fore
    b0, b1 = int(max(0, cx-0.40*fw)), int(min(W, cx+0.40*fw))
    frac = (m[:, b0:b1] > 0.5).mean(1); idx = np.where(frac >= 0.20)[0]
    if not len(idx): miss += 1; continue
    top = int(idx[0]); climb = (fore-top)/fh
    if not (0.10 <= climb <= 0.60):
        miss += 1; continue
    fx0, fx1 = min(P[234][0], P[454][0]), max(P[234][0], P[454][0])
    out.append({"src": st, "t": round(tt, 3), "hair": round(top*HALF, 1),
                "cx": round(cx*HALF, 1), "chin": round(chin*HALF, 1),
                "head_h": round((chin-top)*HALF, 1), "climb": round(climb, 3),
                "fx0": round(fx0*HALF, 1), "fx1": round(fx1*HALF, 1),
                "fw": round((fx1-fx0)*HALF, 1)})
fm.close(); fd.close(); shutil.rmtree(tmp, ignore_errors=True)
hs = np.array([s["hair"] for s in out]); cs = np.array([s["cx"] for s in out])
hh = np.array([s["head_h"] for s in out]); fw = np.array([s["fw"] for s in out])
print(f"valid {len(out)}/{len(times)}  ({miss} discarded misses)")
print(f"hair top  min {hs.min():.0f}  med {np.median(hs):.0f}  max {hs.max():.0f}  (source px)")
print(f"head_h    min {hh.min():.0f}  med {np.median(hh):.0f}  max {hh.max():.0f}")
print(f"face cx   min {cs.min():.0f}  med {np.median(cs):.0f}  max {cs.max():.0f}")
print(f"face w    min {fw.min():.0f}  med {np.median(fw):.0f}  max {fw.max():.0f}")
json.dump({"samples": out, "misses": miss, "n": len(times), "sample_fps": SAMPLE_FPS,
           "grade": GRADE,
           "hair_min": float(hs.min()), "hair_med": float(np.median(hs)),
           "head_med": float(np.median(hh)), "cx_med": float(np.median(cs)),
           "face_w_med": float(np.median(fw)), "face_w_max": float(fw.max())},
          open("framing.json", "w"), indent=1)
print("framing.json written")
