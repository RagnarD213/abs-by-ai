#!/usr/bin/env python3
"""ROUND 2 carried work: one head measurement on the EXACT first frame of every hold (and its last frame).

Round 1's crop landed 5 to 20 source px off his head at a cut because the track samples him 5 times a second and the
landing interpolated between two samples. Same measurement as s04_track.py (graded half-scale frame, face mesh + person
mask, hair top = first row the mask fills above the forehead), written to framing_holdstart.json; s60_plan.py merges it
into the track. framing.json (locked, d798e48e) is not touched.

  s04b_holdstart.py beats.json [beats_camopen.json ...]
"""
import json, os, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/round2")
import ra01lib as L
import mediapipe as mp
CUT = json.load(open("cut.json")); FPS = L.FPS; fr = lambda t: int(round(t*FPS)); HALF = 2.0
GRADE = L.grade()


def src_frame(t, last=False):
    """source frame index of output time t (first frame of a hold), or of the frame just before t (last=True)."""
    f = fr(t) - (1 if last else 0); tt = f/FPS + 1e-4
    for p in CUT["pieces"]:
        if fr(p["t_in"]) <= f < fr(p["t_out"]):
            return fr(p["src_in"] + (f/FPS - p["t_in"])*(CUT.get("speed") or 1.0)), f/FPS   # RA-05 r2: speed-aware
    return None, None


want = {}
for bp in sys.argv[1:]:
    for p in json.load(open(bp))["punch"]:
        for t, last in ((p["beat"][0], False), (min(p["beat"][1], CUT["dur"]), True)):
            sf, tt = src_frame(t, last)
            if sf is not None: want[sf] = tt
tmp = tempfile.mkdtemp(prefix="ra14hs_"); paths = {}
for sf in sorted(want):
    p = os.path.join(tmp, "%06d.png" % sf)
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{sf/FPS + 0.002:.4f}", "-i", L.ROLL, "-frames:v", "1",
                    "-vf", f"{L.DECODE},{GRADE},scale=1080:1920:flags=lanczos", "-y", p], check=True)
    paths[sf] = p
mdir = os.path.join(tmp, "m")
subprocess.run([L.PERSONMASK, mdir] + list(paths.values()), capture_output=True, text=True)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
out, miss = [], 0
for sf in sorted(want):
    a = np.asarray(Image.open(paths[sf]).convert("RGB")); H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a)); P = None
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark; P = {k: (Lm[k].x*W, Lm[k].y*H) for k in (10, 152, 234, 454)}
    if P is None:
        d = fd.process(np.ascontiguousarray(a))
        if d.detections:
            b = d.detections[0].location_data.relative_bounding_box
            cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H; s = max(b.width*W, b.height*H)*2.2
            x0, y0 = int(max(0, cx-s/2)), int(max(0, cy-s/2)); x1, y1 = int(min(W, cx+s/2)), int(min(H, cy+s/2))
            rr = fm.process(np.ascontiguousarray(a[y0:y1, x0:x1]))
            if rr.multi_face_landmarks:
                Lm = rr.multi_face_landmarks[0].landmark; cw, ch = x1-x0, y1-y0
                P = {k: (Lm[k].x*cw+x0, Lm[k].y*ch+y0) for k in (10, 152, 234, 454)}
    mp_ = os.path.join(mdir, os.path.basename(paths[sf])[:-4] + ".mask.png")
    if P is None or not os.path.exists(mp_): miss += 1; continue
    m = np.asarray(Image.open(mp_).convert("L"), dtype=np.float32)/255.0
    cx = (P[234][0]+P[454][0])/2; fw = abs(P[454][0]-P[234][0]); fore, chin = P[10][1], P[152][1]; fh = chin-fore
    b0, b1 = int(max(0, cx-0.40*fw)), int(min(W, cx+0.40*fw))
    idx = np.where((m[:, b0:b1] > 0.5).mean(1) >= 0.20)[0]
    if not len(idx): miss += 1; continue
    top = int(idx[0]); climb = (fore-top)/fh
    if not (0.10 <= climb <= 0.60): miss += 1; continue
    fx0, fx1 = min(P[234][0], P[454][0]), max(P[234][0], P[454][0])
    out.append({"src": round(sf/FPS, 4), "src_frame": sf, "t": round(want[sf], 4), "hair": round(top*HALF, 1), "cx": round(cx*HALF, 1),
                "chin": round(chin*HALF, 1), "head_h": round((chin-top)*HALF, 1), "climb": round(climb, 3),
                "fx0": round(fx0*HALF, 1), "fx1": round(fx1*HALF, 1), "fw": round((fx1-fx0)*HALF, 1), "holdstart": True})
fm.close(); fd.close(); shutil.rmtree(tmp, ignore_errors=True)
json.dump({"samples": out, "misses": miss, "n": len(want)}, open("framing_holdstart.json", "w"), indent=1)
print(f"framing_holdstart.json: {len(out)} of {len(want)} hold edges measured ({miss} misses)")
