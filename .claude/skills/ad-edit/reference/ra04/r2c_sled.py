#!/usr/bin/env python3
"""RA-04 round 2c: build the leg press END frame so the machine is physically exact.

Image models redraw the whole picture on every edit, so across three generated END frames the sled never moved as one piece
(platform sliding 16-24 px against its own plates), the static frame stretched or jogged, and three independent reviews failed it.
So the machine is built in code, the man comes from the generated frame:
  1. canvas = START (every static machine and background pixel exact)
  2. where START's man and START's sled were, fill from the generated END (it renders what is behind them; measured 0-1 px off START)
  3. the sled (platform + horn + plates + bracket) cut from START as ONE sprite, moved T px exactly along the 45-degree rails
  4. the man from the generated END (extended legs, feet on the platform, face, phone) on top, by pose segmentation
usage: r2c_sled.py START GEN_END OUT [--t 115]
"""
import argparse, math
import cv2, numpy as np
import mediapipe as mp

def person(img):
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True) as P:
        r = P.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return (r.segmentation_mask > 0.5).astype(np.uint8)

def legskin(img, pm):
    """Soften the image model's net-like 'cracked' texture on bare leg skin (both reviews flagged it): an edge-preserving
    filter on skin-coloured person pixels below the waist only, blended at 85 % so hair and shading stay."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); skin = ((hsv[..., 0] < 25) & (hsv[..., 1] > 40) & (hsv[..., 2] > 70)).astype(np.uint8)
    ys = np.where(pm.any(1))[0]; legs = np.zeros_like(skin); legs[:, :] = 0
    lm = skin & pm; lm[:int(img.shape[0] * 0.30)] = 0
    lm[:, :int(img.shape[1] * 0.33)] = 0                       # torso/arms/face sit left of x~310 here; legs run right of it
    sm = cv2.bilateralFilter(img, 9, 40, 6); w = cv2.GaussianBlur(lm.astype(np.float32), (7, 7), 0)[..., None] * 0.85
    return (img * (1 - w) + sm * w).round().astype(np.uint8)

ap = argparse.ArgumentParser(); ap.add_argument("start"); ap.add_argument("gen"); ap.add_argument("out"); ap.add_argument("--t", type=float, default=115); ap.add_argument("--legskin", action="store_true")
ap.add_argument("--footfix", help="cx,cy,dx,dy,sigma: nudge one generated foot by (dx,dy) with a Gaussian falloff so it rides the platform")
a = ap.parse_args()
S = cv2.imread(a.start); G = cv2.imread(a.gen); H, W = S.shape[:2]
T = (int(round(a.t)), -int(round(a.t)))                      # exactly 45 degrees: as far up as across
# sled sprite in START (measured on a 3x gridded crop, F4f_c): platform quad, the two stacked plates, the hinge bracket
sled = np.zeros((H, W), np.uint8); plate_poly = np.zeros_like(sled); brk = np.zeros_like(sled)
# platform outline traced at 5x on F4h (6th review: the loose outline carried background and rail, smearing the top corner)
cv2.fillPoly(plate_poly, [np.array([(501, 530), (550, 489), (557, 484), (572, 484), (580, 491), (747, 772), (655, 747), (630, 742)], np.int32)], 1)
cv2.rectangle(brk, (604, 516), (650, 578), 1, -1)
lum = cv2.cvtColor(S, cv2.COLOR_BGR2GRAY)
k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
# the bracket box also held the pillar's dark face (5th review: a dark patch on the pillar once moved): keep black metal + bolts only
metal = ((lum < 55) | (lum > 170)).astype(np.uint8)
brk = cv2.morphologyEx(brk & metal, cv2.MORPH_OPEN, k(1))
cv2.circle(sled, (777, 641), 105, 1, -1); cv2.circle(sled, (756, 641), 104, 1, -1)
sled = np.maximum(sled, np.maximum(plate_poly, brk))
if a.footfix:
    # the image model slid the near foot down the platform (5th review: (47,-14) against the sled's (33,-33)); a local warp moves it back
    cx, cy, ddx, ddy, sg = map(float, a.footfix.split(","))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); w = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sg * sg))
    G = cv2.remap(G, xx - ddx * w, yy - ddy * w, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
pS, pG = person(S), person(G)
# START's feet rest on the platform: cut them out of the sled piece and fill the platform face under them (5th review: phantom toe)
near_feet = cv2.dilate(pS, k(14))                           # shoe highlights the segmentation missed, but only next to the feet,
feet = cv2.dilate(((pS > 0) | ((lum > 85) & (near_feet > 0))).astype(np.uint8), k(3)) & plate_poly   # never the platform rim
S_sled = cv2.inpaint(S, feet, 9, cv2.INPAINT_TELEA)
fill = cv2.dilate(np.maximum(pS, sled), k(10))
fill[515:715, 495:700] = 1                                   # START's shoes: the segmentation missed a lace loop (536,630)
fill[615:725, 235:325] = 1                                   # START's phone and hand: a phone is not 'person' (4th review: floating phone)
moved = np.zeros_like(sled); M = np.float32([[1, 0, T[0]], [0, 1, T[1]]])
spr = cv2.warpAffine(S_sled, M, (W, H)); moved = cv2.warpAffine(sled, M, (W, H), flags=cv2.INTER_NEAREST)
man = cv2.dilate(pG, k(2))
# shoes are not reliably 'person' to the segmenter (the far shoe vanished under the moved platform): on the dark platform near
# the generated feet, anything bright (grey suede, white sole, sock) is shoe; close it and fill its holes (laces, shadows)
lumG = cv2.cvtColor(G, cv2.COLOR_BGR2GRAY)
face_new = cv2.erode(cv2.warpAffine(plate_poly, M, (W, H), flags=cv2.INTER_NEAREST), k(2))   # the platform face only, not the bracket bolts
zone = cv2.dilate(pG, k(40)) & face_new
shoe = ((lumG > 72) & (zone > 0)).astype(np.uint8)
shoe = cv2.morphologyEx(shoe, cv2.MORPH_CLOSE, k(6))
cnt, _ = cv2.findContours(shoe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
shoe = np.zeros_like(shoe)                                     # keep shoe-sized blobs only: rim highlights are specks
for c in cnt:
    if cv2.contourArea(c) > 400: cv2.drawContours(shoe, [c], -1, 1, -1)
man = np.maximum(man, cv2.dilate(shoe, k(1)))
f = lambda m, s: cv2.GaussianBlur(m.astype(np.float32), (s, s), 0)[..., None]
O = S.astype(np.float32)
O = O * (1 - f(fill, 9)) + G.astype(np.float32) * f(fill, 9)          # what is behind the old man and old sled
O = O * (1 - f(moved, 3)) + spr.astype(np.float32) * f(moved, 3)       # the rigid sled, crisp edge
O = O * (1 - f(man, 5)) + G.astype(np.float32) * f(man, 5)             # the man on top (feet over the platform)
O = O.round().clip(0, 255).astype(np.uint8)
if a.legskin: O = legskin(O, pG)
cv2.imwrite(a.out, O)
cv2.imwrite(a.out.replace(".png", "_layers.png"), np.dstack([fill * 255, moved * 255, man * 255]).astype(np.uint8))
print({"out": a.out, "T": T, "travel_deg": round(math.degrees(math.atan2(-T[1], T[0])), 1)})
