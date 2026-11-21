#!/usr/bin/env python3
"""Eye-openness over a frame range of a delivered master.  s40_blink.py <master> <f0> <f1>

Round 1 added a 0.60 s tail to the macro card because the cut back to camera landed on a 0.58 s
eye-squeeze. Round 2's R3 caps the card at the recording's stable window, so the tail had to be
measured instead of guessed: this reports the FaceMesh eye-aspect-ratio per frame so the card's
out-point can be put on a frame where his eyes are open.
"""
import subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from PIL import Image
import mediapipe as mp
M, F0, F1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
pr = subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v",
                     "-show_entries", "stream=width,height", "-of", "csv=p=0", M],
                    capture_output=True, text=True).stdout.strip().split(",")
W, H = int(pr[0]), int(pr[1])
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
raw = subprocess.run([L.FF, "-v", "error", "-nostdin", "-i", M, "-vf",
                      f"select='between(n\\,{F0}\\,{F1})'", "-vsync", "0",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
n = len(raw)//(W*H*3)
out = []
for i in range(n):
    a = np.frombuffer(raw[i*W*H*3:(i+1)*W*H*3], np.uint8).reshape(H, W, 3)
    r = fm.process(np.ascontiguousarray(a))
    if not r.multi_face_landmarks:
        out.append((F0+i, None)); continue
    lm = r.multi_face_landmarks[0].landmark
    # right eye: 159 upper / 145 lower / 33,133 corners; left eye: 386/374, 362,263
    def ear(up, lo, c0, c1):
        v = abs(lm[up].y - lm[lo].y)*H
        w = abs(lm[c1].x - lm[c0].x)*W
        return v/max(w, 1e-6)
    out.append((F0+i, round((ear(159, 145, 33, 133) + ear(386, 374, 362, 263))/2, 4)))
vals = [v for _, v in out if v is not None]
open_thr = 0.20
print(f"frames {F0}..{F1}   median EAR {np.median(vals):.3f}   open threshold {open_thr}")
for f, v in out:
    mark = "" if v is None else ("  <== eyes closed" if v < open_thr else "")
    print(f"  f{f}  t={f*L.FD:7.3f}s  EAR {v}{mark}")
run = 0
for f, v in out:
    if v is not None and v >= open_thr:
        run += 1
        if run >= 5:
            print(f"\nFIRST frame with the eyes open for 5 consecutive frames: f{f-4} "
                  f"(t={(f-4)*L.FD:.3f}s)")
            break
    else:
        run = 0
