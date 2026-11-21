"""Map each exercise clip in a delivered vertical cut to its time in the raw roll (static camera, static background).
usage: rawmatch.py CUT RAW 'a-b,a-b,...' RAW_T0 RAW_T1 [CACHE_DIR]
For each cut span it prints the three best raw ranges (mean correlation of edge images along the diagonal, so it is
robust to the grade) and the per-frame best raw time. A span whose per-frame times jump to another part of the roll
half way through is two takes joined by a dissolve (revisions lesson 75). Then check each range against what Dan
SAYS on the roll before that take (boost the roll sound, it can sit at -72 dB)."""
import sys, cv2, numpy as np, subprocess, os
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
CUT, RAW, spans, T0, T1 = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
CACHE = sys.argv[6] if len(sys.argv) > 6 else os.path.dirname(os.path.abspath(CUT))
W, H, FPS = 480, 270, 10
cache = os.path.join(CACHE, f"rawlo_{os.path.basename(RAW)}_{int(T0)}_{int(T1)}.npy")
if os.path.exists(cache): raw = np.load(cache)
else:
    p = subprocess.run([FF, "-v", "error", "-ss", str(T0), "-t", str(T1-T0), "-i", RAW, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True)
    raw = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W); np.save(cache, raw)
print("raw frames", raw.shape, file=sys.stderr)
cap = cv2.VideoCapture(CUT); fps = cap.get(cv2.CAP_PROP_FPS)
def cutframe(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*fps))); ok, f = cap.read(); return cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) if ok else None
sift = cv2.SIFT_create(3000)
def affine(cf, rf):
    m = np.zeros(cf.shape, np.uint8); m[330:1250, :] = 255
    k1, d1 = sift.detectAndCompute(cf, m); k2, d2 = sift.detectAndCompute(rf, None)
    mm = cv2.BFMatcher().knnMatch(d1, d2, k=2); g = [a for a, b in mm if a.distance < 0.7*b.distance]
    if len(g) < 12: return None
    M, inl = cv2.estimateAffinePartial2D(np.float32([k1[x.queryIdx].pt for x in g]), np.float32([k2[x.trainIdx].pt for x in g]), method=cv2.RANSAC, ransacReprojThreshold=3)
    return M, int(inl.sum())
for sp in spans.split(','):
    a, b = map(float, sp.split('-'))
    # affine from cut coords to raw lo-res coords, using a mid frame against a mid raw frame (background is static)
    cf = cutframe((a+b)/2); best = None
    for ri in (0, len(raw)//2, len(raw)-1):
        r = affine(cf, cv2.resize(raw[ri], (W*2, H*2)))
        if r and (best is None or r[1] > best[1]): best = r
    if best is None: print(sp, "no affine"); continue
    M = best[0].copy(); M /= 2.0   # to lo-res coords
    sc = np.hypot(M[0,0], M[1,0])
    # raw window covered by the cut frame, in raw 3840 px
    x0 = M[0,2]*8; xw = 1080*sc*8; print(f"span {sp}: cut px = {sc*8:.3f} raw px; raw window x {x0:.0f}..{x0+xw:.0f} ({xw:.0f} wide), inliers {best[1]}")
    def feat(im):
        g = cv2.GaussianBlur(im.astype(np.float32), (0, 0), 1.2)
        gx = cv2.Sobel(g, cv2.CV_32F, 1, 0); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1)
        f = np.concatenate([gx[40:175, 150:352].ravel(), gy[40:175, 150:352].ravel()])
        f -= f.mean(); return f / (np.linalg.norm(f) + 1e-6)
    global RF
    try: RF
    except NameError: RF = np.stack([feat(r) for r in raw])
    ts = np.arange(a + 0.05, b - 0.05, 1.0 / FPS)
    C = np.stack([feat(cv2.warpAffine(cutframe(t), M, (W, H))) for t in ts])
    S = C @ RF.T                       # n_cut x n_raw
    n = len(ts); offs = []
    for o in range(0, len(raw) - n):
        offs.append(float(np.mean(S[np.arange(n), o + np.arange(n)])))
    offs = np.array(offs); order = np.argsort(-offs)
    picks = []
    for o in order:
        if all(abs(o - p) > 20 for p in picks): picks.append(o)
        if len(picks) == 3: break
    for p in picks: print(f"   raw {T0 + p/FPS:7.1f} .. {T0 + (p+n)/FPS:7.1f}  mean corr {offs[p]:.3f}")
    fr = S.argmax(1); print("   per-frame best raw time (every 0.5 s):", ' '.join(f"{T0 + fr[k]/FPS:.1f}" for k in range(0, n, 5)))
