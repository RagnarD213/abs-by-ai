#!/usr/bin/env python3
"""RA-07 round 3: lock an AI END frame's background to START with no tone step where START's person used to be.

lockstill.py copies START outside both people and keeps END inside; the area START's person covered then shows END's own
redraw, a few levels off START (the I4a reviews found a 10-level patch with a seam on the rack upright). Here END is first
shifted by the SMOOTH difference START - END measured on the shared background (masked Gaussian, sigma 22 px), everywhere
except END's own person, then blended into START with a 15 px feather.
  python3 lock_tone.py START END OUT [x0,y0,x1,y1 ...]   (boxes forced into the person area)
"""
import sys
import cv2, numpy as np
import mediapipe as mp


def person(img):
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True) as P:
        r = P.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return (r.segmentation_mask > 0.3).astype(np.uint8)


S = cv2.imread(sys.argv[1]).astype(np.float32); E = cv2.imread(sys.argv[2]).astype(np.float32)
pS, pE = person(S.astype(np.uint8)), person(E.astype(np.uint8))
el = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
union = cv2.dilate(np.maximum(pS, pE), el(18))
for b in sys.argv[4:]:                                    # extra boxes START's person covers that the segmenter misses (frame edges)
    x0, y0, x1, y1 = map(int, b.split(",")); union[y0:y1, x0:x1] = 1
bg = (1 - cv2.dilate(union, el(12))).astype(np.float32)
bg *= (np.abs(S - E).max(2) < 30).astype(np.float32)        # sample tone drift only: a real object difference (a leftover sleeve) is not drift
sig = 22
num = cv2.GaussianBlur((S - E) * bg[..., None], (0, 0), sig); den = cv2.GaussianBlur(bg, (0, 0), sig)[..., None]
Ds = num / np.maximum(den, 1e-3)
keepE = cv2.GaussianBlur(cv2.dilate(pE, el(3)).astype(np.float32), (0, 0), 3)[..., None]
Ec = E + Ds * (1 - keepE)
w = cv2.GaussianBlur(union.astype(np.float32), (0, 0), 7)[..., None]          # ~15 px feather
O = np.clip(Ec * w + S * (1 - w), 0, 255).round().astype(np.uint8)
cv2.imwrite(sys.argv[3], O)
print("done", sys.argv[3], "fill px", int(((pS > 0) & (pE == 0)).sum()))
