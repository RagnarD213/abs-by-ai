#!/usr/bin/env python3
"""blend_head.py original.jpg edited.png out.jpg
Keep the original photo and take only the head and hair from the AI-aged version: align the edit to the original
(ORB features + similarity transform), find the face, blend a feathered head-and-hair region, and match the edit's
colour tint (a/b in Lab) to the original so skin tone does not shift. Body, background and framing stay original pixels."""
import sys
import numpy as np, cv2

orig = cv2.imread(sys.argv[1]); edit = cv2.imread(sys.argv[2]); out_path = sys.argv[3]
H, W = orig.shape[:2]

# 1. align the edit onto the original
g1 = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
e0 = cv2.resize(edit, (W, round(edit.shape[0] * W / edit.shape[1])))
g2 = cv2.cvtColor(e0, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create(4000)
k1, d1 = orb.detectAndCompute(g1, None); k2, d2 = orb.detectAndCompute(g2, None)
m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d2, d1), key=lambda x: x.distance)[:400]
src = np.float32([k2[x.queryIdx].pt for x in m]); dst = np.float32([k1[x.trainIdx].pt for x in m])
M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=4)
al = cv2.warpAffine(e0, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

# 2. head region from the face box
# where the edit changed things, in the top half (the head), not the body
d = cv2.absdiff(cv2.GaussianBlur(orig, (0, 0), 3), cv2.GaussianBlur(al, (0, 0), 3)).max(axis=2).astype(np.float32)
d[int(H * 0.5):] = 0
d = cv2.GaussianBlur(d, (0, 0), W / 40)
ys, xs = np.where(d > d.max() * 0.35)
fx, fy = int(xs.min()), int(ys.min()); fw, fh = int(xs.max() - xs.min()), int(ys.max() - ys.min())
mask = np.zeros((H, W), np.float32)
cx, cy, ax, ay = [int(v) for v in sys.argv[4:8]]   # head ellipse set by eye per photo
fw = ax * 2
cv2.ellipse(mask, (cx, cy), (ax, ay), 0, 0, 360, 1.0, -1)
mask = cv2.GaussianBlur(mask, (0, 0), fw * 0.08)

# 3. keep the original tint inside the head (match a/b only, so the gray in the hair stays)
lo = cv2.cvtColor(orig, cv2.COLOR_BGR2LAB).astype(np.float32)
le = cv2.cvtColor(al, cv2.COLOR_BGR2LAB).astype(np.float32)
sel = mask > 0.5
for c in (1, 2):
    le[..., c] += lo[..., c][sel].mean() - le[..., c][sel].mean()
al = cv2.cvtColor(np.clip(le, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

out = orig.astype(np.float32) * (1 - mask[..., None]) + al.astype(np.float32) * mask[..., None]
cv2.imwrite(out_path, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
print(out_path, 'inliers', int(inl.sum()), 'changed region', (fx, fy, fw, fh), 'of', (W, H))
