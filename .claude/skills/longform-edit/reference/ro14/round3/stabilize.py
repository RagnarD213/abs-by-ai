"""Lock an AI take's camera in code (RO-14 round 3, A1): Veo 3.1 creeps in 2-5 % over 8 s even with 'locked camera' in the prompt.
Fit a similarity (scale, rotation, shift) from frame A to every frame on the background only (outside x 520-1440, which holds the
man and the scale), smooth it over time, then warp every frame onto the window's middle frame, with the smallest uniform zoom that
leaves no frame edge inside the picture. Output: 24 fps x264 crf 12, frames A..B only.
usage: stabilize.py TAKE A B OUT"""
import os, sys, subprocess, cv2, numpy as np
take, A, B, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cap = cv2.VideoCapture(take); fr = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if A <= i <= B: fr.append(f)
    i += 1
g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
m = np.full_like(g[0], 255); m[:, 520:1440] = 0
orb = cv2.ORB_create(5000); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
k0, d0 = orb.detectAndCompute(g[0], m)
P = []
for x in g:
    k1, d1 = orb.detectAndCompute(x, m); mt = bf.match(d0, d1)
    a = np.float32([k0[t.queryIdx].pt for t in mt]); b = np.float32([k1[t.trainIdx].pt for t in mt])
    M, _ = cv2.estimateAffinePartial2D(a, b, ransacReprojThreshold=2.0)
    s = np.hypot(M[0, 0], M[1, 0]); r = np.arctan2(M[1, 0], M[0, 0]); P.append([s, r, M[0, 2], M[1, 2]])
P = np.array(P)
k = 9; pad = np.pad(P, ((k//2, k//2), (0, 0)), mode="edge")
S = np.array([np.median(pad[j:j+k], 0) for j in range(len(P))])          # smooth: median over 9 frames
def mat(p):
    s, r, tx, ty = p; c, n = s*np.cos(r), s*np.sin(r); return np.array([[c, -n, tx], [n, c, ty], [0, 0, 1]])
REF = int(sys.argv[5]) if len(sys.argv) > 5 else len(S)//2
TN = mat(S[REF])                             # align every frame to the reference frame (default: the window's middle)
Ws = [TN @ np.linalg.inv(mat(p)) for p in S]
# the smallest uniform zoom about the centre that keeps every warped frame's edge outside the picture (no border, no smear)
C = np.array([[1, 0, 960], [0, 1, 540], [0, 0, 1.]]); Ci = np.linalg.inv(C)
def covered(z):
    Z = C @ np.diag([z, z, 1]) @ Ci
    for W in Ws:
        Wi = np.linalg.inv(Z @ W)                 # output pixel -> source pixel; every output corner must land inside the source
        for x, y in ((0, 0), (1919, 0), (0, 1079), (1919, 1079)):
            u, v, _ = Wi @ [x, y, 1]
            if not (0 <= u <= 1919 and 0 <= v <= 1079): return False
    return True
z = 1.0
NOZOOM = os.environ.get('STAB_NOZOOM') == '1'   # extend edge pixels instead of zooming (keeps head room when the take framed the head at the top)
while not NOZOOM and not covered(z): z += 0.0005
if os.environ.get('STAB_ZOOM'):                # a fixed zoom about an anchor point, e.g. '1.043@960,78': covers the bottom and
    zs, xy = os.environ['STAB_ZOOM'].split('@')  # sides while the top (head room) stays where it is
    z = float(zs); ax, ay = map(float, xy.split(','))
    C = np.array([[1, 0, ax], [0, 1, ay], [0, 0, 1.]]); Ci = np.linalg.inv(C)
Z = C @ np.diag([z, z, 1]) @ Ci; Ws = [Z @ W for W in Ws]
edge = dict(left=0, right=0, top=0, bottom=0)
for W in Ws:
    c = W[:2] @ np.array([[0, 1919, 0, 1919], [0, 0, 1079, 1079], [1, 1, 1, 1]])
    edge['left'] = max(edge['left'], c[0, 0], c[0, 2]); edge['right'] = max(edge['right'], 1919 - c[0, 1], 1919 - c[0, 3])
    edge['top'] = max(edge['top'], c[1, 0], c[1, 1]); edge['bottom'] = max(edge['bottom'], 1079 - c[1, 2], 1079 - c[1, 3])
ff = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
enc = subprocess.Popen([ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-framerate", "24", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-frames:v", str(len(fr)), "-t", f"{len(fr)/24:.3f}", out], stdin=subprocess.PIPE)   # -frames/-t: the render queue sees a short clip (quick lane)
for f, W in zip(fr, Ws):
    enc.stdin.write(cv2.warpAffine(f, W[:2], (1920, 1080), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
enc.stdin.close(); enc.wait()
print(out, "frames", len(fr), "drift removed: scale %.2f%% -> 0, shift %+.0f,%+.0f px; cover zoom %.2f%%; edge pixels extended at most %s" % ((S[-1, 0]/S[0, 0]-1)*100, S[-1, 2]-S[0, 2], S[-1, 3]-S[0, 3], (z-1)*100, {k: round(max(v, 0)) for k, v in edge.items()}))
