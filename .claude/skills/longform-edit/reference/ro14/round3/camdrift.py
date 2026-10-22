"""camera drift of a take: ORB + RANSAC similarity on the background (outside x 560-1400) frame 0 vs every 12th frame; prints scale and shift."""
import sys, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
m = np.ones_like(fr[0]); m[:, 560:1400] = 0
orb = cv2.ORB_create(4000); k0, d0 = orb.detectAndCompute(fr[0], m); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
out = []
for i in range(12, len(fr), 12):
    k1, d1 = orb.detectAndCompute(fr[i], m); mt = bf.match(d0, d1)
    a = np.float32([k0[x.queryIdx].pt for x in mt]); b = np.float32([k1[x.trainIdx].pt for x in mt])
    M, inl = cv2.estimateAffinePartial2D(a, b, ransacReprojThreshold=2.0)
    s = np.hypot(M[0, 0], M[1, 0]); out.append(f"{i}:{(s-1)*100:+.1f}%/{M[0,2]:+.0f},{M[1,2]:+.0f}")
print(sys.argv[1].split('/')[-1], len(fr), " ".join(out))
