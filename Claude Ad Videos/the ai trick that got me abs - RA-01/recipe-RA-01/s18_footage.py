#!/usr/bin/env python3
"""Eyeline, lighting and face sharpness for the footage report (plan section 8)."""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
K = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)

def landmarks(a):
    H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a))
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark
        return {i: (Lm[i].x*W, Lm[i].y*H) for i in range(468)}, (0, 0, W, H)
    d = fd.process(np.ascontiguousarray(a))
    if not d.detections: return None, None
    b = d.detections[0].location_data.relative_bounding_box
    cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
    s = max(b.width*W, b.height*H)*2.2
    x0, y0 = int(max(0, cx-s/2)), int(max(0, cy-s/2)); x1, y1 = int(min(W, cx+s/2)), int(min(H, cy+s/2))
    rr = fm.process(np.ascontiguousarray(a[y0:y1, x0:x1]))
    if not rr.multi_face_landmarks: return None, None
    Lm = rr.multi_face_landmarks[0].landmark; cw, ch = x1-x0, y1-y0
    return {i: (Lm[i].x*cw+x0, Lm[i].y*ch+y0) for i in range(468)}, (x0, y0, x1, y1)

yaws, pitches, ratios, shadows, sharp = [], [], [], [], []
for p in sorted(glob.glob("probe/g*.png")):
    a = np.asarray(Image.open(p).convert("RGB"))
    P, _ = landmarks(a)
    if P is None: continue
    l, r, nose, fore, chin = P[234], P[454], P[1], P[10], P[152]
    cx = (l[0]+r[0])/2
    halfw = abs(r[0]-l[0])/2
    yaws.append(float(np.degrees(np.arcsin(np.clip((nose[0]-cx)/max(halfw, 1), -1, 1)))))
    mid = (fore[1]+chin[1])/2
    pitches.append(float(np.degrees(np.arcsin(np.clip((nose[1]-mid)/max(chin[1]-fore[1], 1)*2, -1, 1)))))
    g = np.asarray(Image.open(p).convert("L"), float)
    fb = (int(l[0]), int(fore[1]), int(r[0]), int(chin[1]))
    face = g[fb[1]:fb[3], fb[0]:fb[2]]
    if face.size > 400: sharp.append(float(convolve2d(face, K, mode="valid").var()))
    sky = g[0:500, :]
    ratios.append(float(sky.mean()/max(face.mean(), 1)))
    half = face.shape[1]//2
    shadows.append("camera-left" if face[:, :half].mean() < face[:, half:].mean() else "camera-right")
json.dump({"method": "mediapipe FaceMesh on the graded source frames: yaw from the nose tip against "
                     "the cheek-edge midpoint, pitch from the nose against the forehead-chin midpoint",
           "yaw_deg_est": round(float(np.median(yaws)), 1),
           "yaw_range": [round(min(yaws), 1), round(max(yaws), 1)],
           "pitch_deg_est": round(float(np.median(pitches)), 1),
           "notes": "a small consistent yaw with no drift is a teleprompter just off the lens axis; "
                    "the sign says which side"},
          open("eyeline.json", "w"), indent=1)
json.dump({"sky_vs_face_luma_ratio": round(float(np.median(ratios)), 2),
           "shadow_side": max(set(shadows), key=shadows.count),
           "notes": "overcast key from the open sky; the pool and the pale limestone wall fill from "
                    "below and behind, so the face carries little modelling"},
          open("lighting.json", "w"), indent=1)
json.dump({"source_native": round(float(np.median(sharp)), 1),
           "_why_delivered": "filled by s18_footage.py delivered <master 9x16> after the render"},
          open("sharpness.json", "w"), indent=1)
print("eyeline", json.load(open("eyeline.json")))
print("lighting", json.load(open("lighting.json")))
print("sharpness source", json.load(open("sharpness.json")))
