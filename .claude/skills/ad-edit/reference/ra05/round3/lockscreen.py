#!/usr/bin/env python3
"""Hold the phone picture still in a Veo take (Veo animates the photo on the screen like a live photo).
1. track: SIFT on the phone region of frame 0 against every frame (no chaining, so no drift), RANSAC homography, falling back
   to a similarity when the homography jumps; ECC refinement on the bezel ring kept only when it agrees within 3 px
2. smooth: the four bezel corners over time (Gaussian, sigma `smooth` frames); each warp rebuilt from the smoothed corners
3. paste: frame 0's screen picture into the tracked screen, feathered, leaving out the strip where his fingers overlap it
4. check: correlation of the bezel ring between the warped frame 0 and frame n (ring_ncc), per frame
usage: lockscreen.py <take.mp4> <out.mp4> <n_frames> <cfg.json>
cfg: {"outer": [[x,y]x4], "inner": [[x,y]x4], "exclude": [[x,y],...] (optional), "smooth": 1.6}  corners TL, TR, BR, BL"""
import json, subprocess, sys, numpy as np, cv2
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
src, out, N, cfg = sys.argv[1], sys.argv[2], int(sys.argv[3]), json.load(open(sys.argv[4]))
W, H = 1080, 1920
p = subprocess.Popen([FF, "-v", "error", "-i", src, "-vf", "scale=in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24",
                      "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
fr = []
for _ in range(N):
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    fr.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
p.wait(); N = len(fr)
outer = np.float32(cfg["outer"]); inner = np.float32(cfg["inner"])
x0, y0 = np.int32(outer.min(0) - 60); x1, y1 = np.int32(outer.max(0) + 60)
ring = np.zeros((H, W), np.uint8)
cv2.fillPoly(ring, [np.int32(outer)], 255); cv2.fillPoly(ring, [np.int32(inner)], 0)
ring = cv2.dilate(ring, np.ones((9, 9), np.uint8))
if cfg.get("exclude"): cv2.fillPoly(ring, [np.int32(cfg["exclude"])], 0)
paste = np.zeros((H, W), np.uint8); cv2.fillPoly(paste, [np.int32(inner)], 255)
paste = cv2.erode(paste, np.ones((5, 5), np.uint8))
if cfg.get("exclude"): cv2.fillPoly(paste, [np.int32(cfg["exclude"])], 0)
paste = cv2.GaussianBlur(paste.astype(np.float32) / 255, (7, 7), 2)
cx0, cy0, cx1, cy1 = max(0, x0 - 80), max(0, y0 - 80), min(W, x1 + 80), min(H, y1 + 80)
g = lambda a: cv2.GaussianBlur(cv2.cvtColor(a[cy0:cy1, cx0:cx1], cv2.COLOR_RGB2GRAY), (5, 5), 1).astype(np.float32)
ringc = np.ascontiguousarray(ring[cy0:cy1, cx0:cx1])
Sh = np.float32([[1, 0, cx0], [0, 1, cy0], [0, 0, 1]]); Shi = np.linalg.inv(Sh)
cor = lambda M: cv2.perspectiveTransform(outer[None], np.linalg.inv(M))[0]
T = g(fr[0]); Wp = np.eye(3, dtype=np.float32)
sift = cv2.SIFT_create(4000)
fm = np.zeros((H, W), np.uint8); cv2.fillPoly(fm, [np.int32(outer)], 255); fm = cv2.dilate(fm, np.ones((41, 41), np.uint8))
if cfg.get("exclude"): cv2.fillPoly(fm, [np.int32(cfg["exclude"])], 0)
k0, d0 = sift.detectAndCompute(cv2.cvtColor(fr[0], cv2.COLOR_RGB2GRAY), fm)
bf = cv2.BFMatcher(cv2.NORM_L2)
WPS, INF = [Wp.copy()], [(1.0, 0)]
for n in range(1, N):
    a = fr[n]; Gn = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    sm = cv2.dilate(cv2.warpPerspective(fm, np.linalg.inv(Wp), (W, H)), np.ones((61, 61), np.uint8))
    kn, dn = sift.detectAndCompute(Gn, sm)
    mt = [m for m, m2 in bf.knnMatch(d0, dn, k=2) if m.distance < 0.75 * m2.distance]
    A = np.float32([k0[m.queryIdx].pt for m in mt]); Bp = np.float32([kn[m.trainIdx].pt for m in mt])
    Hs, inl = cv2.findHomography(A, Bp, cv2.RANSAC, 2.5)
    Af, _ = cv2.estimateAffinePartial2D(A, Bp, method=cv2.RANSAC, ransacReprojThreshold=2.5)
    cand = [np.linalg.inv(Hs).astype(np.float32), np.linalg.inv(np.vstack([Af, [0, 0, 1]])).astype(np.float32)]
    jump = [float(np.abs(cor(M) - cor(Wp)).max()) for M in cand]
    Wp = cand[0] if jump[0] <= 12 or jump[0] <= jump[1] else cand[1]
    cc = -2.0
    try:
        Wc = (Shi @ Wp @ Sh).astype(np.float32)
        c2, Wc = cv2.findTransformECC(T, g(a), Wc, cv2.MOTION_HOMOGRAPHY,
                                      (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6), ringc, 5)
        We = (Sh @ Wc @ Shi).astype(np.float32)
        if c2 > 0.95 and float(np.abs(cor(We) - cor(Wp)).max()) <= 3: Wp, cc = We, c2
    except cv2.error:
        pass
    WPS.append(Wp.copy()); INF.append((round(float(cc), 4), int(inl.sum())))
C = np.array([cor(M) for M in WPS]); Cs = C.copy(); sg = float(cfg.get("smooth", 1.6))
if sg > 0:
    k = np.exp(-0.5 * (np.arange(-4, 5) / sg) ** 2); k /= k.sum()
    P = np.pad(C, ((4, 4), (0, 0), (0, 0)), mode="edge")
    Cs = np.stack([np.tensordot(k, P[i:i + 9], axes=(0, 0)) for i in range(len(C))])
enc = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "24",
                        "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "12",
                        "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-color_range", "tv", out], stdin=subprocess.PIPE)
log = []
for n, a in enumerate(fr):
    Wp = np.linalg.inv(cv2.getPerspectiveTransform(outer, np.float32(Cs[n]))).astype(np.float32) if n else np.eye(3, dtype=np.float32)
    warped = cv2.warpPerspective(fr[0], Wp, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
    m = cv2.warpPerspective(paste, Wp, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)[..., None]
    o = (a * (1 - m) + warped * m + 0.5).astype(np.uint8)
    rm = cv2.warpPerspective(ring, Wp, (W, H), flags=cv2.INTER_NEAREST | cv2.WARP_INVERSE_MAP) > 0
    ga = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)[rm].astype(float); gw = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)[rm].astype(float)
    log.append({"n": n, "ecc": INF[n][0], "inliers": INF[n][1], "ring_ncc": round(float(np.corrcoef(ga, gw)[0, 1]), 4),
                "corners": cor(Wp).round(1).tolist()})
    enc.stdin.write(o.tobytes())
enc.stdin.close(); assert enc.wait() == 0
json.dump(log, open(out + ".lock.json", "w"), indent=0)
Cl = np.array([l["corners"] for l in log])
print(out, N, "frames | inliers min", min(l["inliers"] for l in log[1:]), "| ring ncc min", min(l["ring_ncc"] for l in log),
      "| corner 2nd-diff max px", round(float(np.abs(np.diff(Cl, 2, axis=0)).max()), 1))
