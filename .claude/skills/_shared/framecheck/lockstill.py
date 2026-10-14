#!/usr/bin/env python3
"""Make everything that should stand still in an AI END frame pixel-identical to its START frame.

usage: lockstill.py START END OUT [--box x0,y0,x1,y1 ...] [--grow 18] [--maskout mask.png]
Keeps END's pixels only where something is meant to move: the person in either frame (MediaPipe pose segmentation of
START and END, grown by --grow px) plus every --box (moving props, e.g. a sled, in BOTH its positions). Everything else is
copied from START, feathered over 6 px. Image models redraw the whole frame on an "edit", so a machine frame or background
drifts by tens of pixels (RA-04, 2026-10-14: the leg press top grew 55-75 px between frames; an independent review caught it).
"""
import argparse
import cv2, numpy as np
import mediapipe as mp

def person(img):
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True) as P:
        r = P.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return (r.segmentation_mask > 0.3).astype(np.uint8) if r.segmentation_mask is not None else np.zeros(img.shape[:2], np.uint8)

ap = argparse.ArgumentParser(); ap.add_argument("start"); ap.add_argument("end"); ap.add_argument("out")
ap.add_argument("--box", action="append", default=[]); ap.add_argument("--grow", type=int, default=18); ap.add_argument("--maskout")
a = ap.parse_args()
S = cv2.imread(a.start); E = cv2.imread(a.end); assert S.shape == E.shape, (S.shape, E.shape)
m = np.maximum(person(S), person(E))
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.grow + 1, 2 * a.grow + 1)); m = cv2.dilate(m, k)
for b in a.box:
    x0, y0, x1, y1 = map(int, b.split(",")); m[y0:y1, x0:x1] = 1
w = cv2.GaussianBlur(m.astype(np.float32), (13, 13), 0)[..., None]
O = (E.astype(np.float32) * w + S.astype(np.float32) * (1 - w)).round().astype(np.uint8)
cv2.imwrite(a.out, O)
if a.maskout: cv2.imwrite(a.maskout, (w[..., 0] * 255).astype(np.uint8))
print({"out": a.out, "moving_fraction": round(float(m.mean()), 3)})
