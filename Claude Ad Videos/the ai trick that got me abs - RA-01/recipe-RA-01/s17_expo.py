#!/usr/bin/env python3
"""Exposure test: which 8/28 LUT exposure puts Dan's FACE where an approved graded frame puts it.

The LUT was fitted indoors (the kitchen set); this roll is outdoors and overcast, so the plan
allows testing 1.30 / 1.45 / 1.60 and picking by MEASUREMENT against an approved website-video
frame. Face pixels are selected by mediapipe, not by a fixed crop (ad-edit lesson 39: a fixed crop
measures the background when the two shots are framed differently).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp
REF = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Website Videos/"
       "Website Conversion Video (post-generation)/website_video_16x9.mp4")
os.makedirs("probe/expo", exist_ok=True)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

def face_stats(path):
    a = np.asarray(Image.open(path).convert("RGB")); H, W = a.shape[:2]
    # FaceMesh's own short-range finder misses a small face in a 4K portrait frame; the
    # full-range detector locates it and FaceMesh runs on the crop (deliver/checks/framing.py).
    r = fm.process(np.ascontiguousarray(a)); box = None
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark
        xs = [p.x*W for p in Lm]; ys = [p.y*H for p in Lm]
    else:
        d = fd.process(np.ascontiguousarray(a))
        if not d.detections: return None
        b = d.detections[0].location_data.relative_bounding_box
        cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
        s_ = max(b.width*W, b.height*H)*2.2
        cx0, cy0 = int(max(0, cx-s_/2)), int(max(0, cy-s_/2))
        cx1, cy1 = int(min(W, cx+s_/2)), int(min(H, cy+s_/2))
        rr = fm.process(np.ascontiguousarray(a[cy0:cy1, cx0:cx1]))
        if not rr.multi_face_landmarks: return None
        Lm = rr.multi_face_landmarks[0].landmark
        cw, ch = cx1-cx0, cy1-cy0
        xs = [p.x*cw+cx0 for p in Lm]; ys = [p.y*ch+cy0 for p in Lm]
    x0, x1 = int(max(0, min(xs))), int(min(W, max(xs)))
    y0, y1 = int(max(0, min(ys))), int(min(H, max(ys)))
    c = a[y0:y1, x0:x1].astype(np.float32)
    if c.size < 300: return None
    R, G, Bc = c[..., 0], c[..., 1], c[..., 2]
    skin = (R > G+8) & (G > Bc) & (R > 55)
    if skin.sum() < 200: skin = np.ones(R.shape, bool)
    px = c[skin]
    luma = 0.2126*px[:, 0] + 0.7152*px[:, 1] + 0.0722*px[:, 2]
    return {"face_luma": round(float(np.median(luma)), 1),
            "face_rgb": [round(float(np.median(px[:, i])), 1) for i in range(3)],
            "face_chroma_ab": [round(float(np.median(px[:, 0]-px[:, 1])), 1),
                               round(float(np.median(px[:, 1]-px[:, 2])), 1)],
            "n": int(skin.sum())}

ref = {}
for t in (30, 60, 95):
    p = f"probe/expo/ref{t}.png"
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", str(t), "-i", REF, "-frames:v", "1",
                    "-y", p], check=True)
    s = face_stats(p)
    if s: ref[t] = s
R = {"face_luma": float(np.median([v["face_luma"] for v in ref.values()])),
     "face_chroma_ab": [float(np.median([v["face_chroma_ab"][i] for v in ref.values()])) for i in (0, 1)],
     "frames": ref}
print("approved website-video reference face:", R["face_luma"], R["face_chroma_ab"])

tests = {}
for e in ("1.30", "1.45", "1.60"):
    cube = L.LUT % e
    vals = []
    for t in (33, 58, 80):
        p = f"probe/expo/e{e}_{t}.png"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", str(t), "-i", L.ROLL,
                        "-frames:v", "1", "-vf",
                        f"{L.DECODE},lut3d=file={cube}:interp=tetrahedral,eq=saturation=0.88",
                        "-y", p], check=True)
        s = face_stats(p)
        if s: vals.append(s)
    tests[e] = {"face_luma": round(float(np.median([v["face_luma"] for v in vals])), 1),
                "face_chroma_ab": [round(float(np.median([v["face_chroma_ab"][i] for v in vals])), 1)
                                   for i in (0, 1)],
                "frames": len(vals)}
    d = abs(tests[e]["face_luma"] - R["face_luma"])
    tests[e]["luma_err"] = round(d, 1)
    tests[e]["chroma_err"] = round(float(np.hypot(tests[e]["face_chroma_ab"][0]-R["face_chroma_ab"][0],
                                                  tests[e]["face_chroma_ab"][1]-R["face_chroma_ab"][1])), 1)
    print(f"  e{e}: face luma {tests[e]['face_luma']:6.1f} (err {d:5.1f})  "
          f"chroma {tests[e]['face_chroma_ab']} (err {tests[e]['chroma_err']})")
best = min(tests, key=lambda e: tests[e]["luma_err"] + tests[e]["chroma_err"])
print("PICK exposure", best)

# sky clipping and tree grain on the chosen exposure
p = f"probe/expo/e{best}_58.png"
a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
sky = a[0:600, :, :]
clip = float(((sky > 250).all(2)).mean())
patch = a[300:420, 1200:1320, :].mean(2)
json.dump({"reference": R, "tests": tests, "chosen": best,
           "sky_clip_pct": round(clip*100, 3),
           "tree_noise_sd_flat_patch": round(float(patch.std()), 2)},
          open("expo.json", "w"), indent=1)
print(f"sky clipped {clip*100:.3f}%   tree patch sd {patch.std():.2f}")
