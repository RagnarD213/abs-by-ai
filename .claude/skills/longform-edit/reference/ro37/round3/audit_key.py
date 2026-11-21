"""RO-37 round 3: measure the key on the delivered film, shot by shot. Every 10th film frame of every presenter run: pixels on his
edge brighter than both his skin and the scene (the pale line Dan saw), darker than both (a rim), and green hedge left on the edge.
Writes r3/audit/key.json and keeps the worst frame of each shot as a png with its cut-out mask for the zoom sheets."""
import json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
from assemble import main_body
FILM = sys.argv[1]; OUT = "r3/audit"; STEP = 10
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
runs = []
for i in range(6): runs += json.load(open(f"r3/full/c{i}.build.json"))["runs"]
P = [r for r in runs if r["kind"] == "presenter"]
by_f = {}
for ri, r in enumerate(P):
    for f in range(r["f0"], r["f1"]): by_f[f] = ri
rd = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", FILM, "-map", "0:v", "-vf", f"select=not(mod(n\\,{STEP}))", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
res = {}; OW, OH = 1920, 1080
def score(img, a):
    L = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    hard = (a > 0.5).astype(np.uint8)
    di = cv2.distanceTransform(hard, cv2.DIST_L2, 3); do = cv2.distanceTransform(1 - hard, cv2.DIST_L2, 3)
    edge = (di < 2.5) & (do < 2.5) & (np.minimum(cv2.GaussianBlur(a, (0, 0), 2), 1) > 0)
    def ring(m):
        w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 8); return cv2.GaussianBlur(L * m, (0, 0), 8) / np.maximum(w, 1e-3)
    Li = ring((di > 5) & (di < 11)); Lo = ring((do > 5) & (do < 11))
    bright = edge & (L > np.maximum(Li, Lo) + 24)
    dark = edge & (L < np.minimum(Li, Lo) - 24)
    b, g, r = [img[..., c].astype(np.float32) for c in range(3)]
    green = edge & (g > r + 14) & (g > b + 14)
    def longest(m):
        n, _, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)), connectivity=8)
        if n < 2: return 0, None
        i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); x, y, w, h = st[i][:4]
        return int(max(w, h)), (int(x + w / 2), int(y + h / 2))
    return dict(bright=int(bright.sum()), dark=int(dark.sum()), green=int(green.sum()), bl=longest(bright), dl=longest(dark), gl=longest(green))
n = 0
while True:
    buf = rd.stdout.read(OW * OH * 3)
    if len(buf) < OW * OH * 3: break
    f = n * STEP; n += 1
    if f not in by_f: continue
    ri = by_f[f]; r = P[ri]; x, y, w, h = r["rect"]
    if w < 300: pass
    k = r["src_k0"] + f - r["f0"]; lo, hi = r["src_k0"], r["src_k0"] + r["f1"] - r["f0"] - 1
    a = r2.alpha(r["roll"], k, lo, hi); a = main_body(cv2.resize(a, (w, h), interpolation=cv2.INTER_LINEAR))
    A = np.zeros((OH, OW), np.float32); X0, Y0, X1, Y1 = max(0, x), max(0, y), min(OW, x + w), min(OH, y + h)
    A[Y0:Y1, X0:X1] = a[Y0 - y:Y1 - y, X0 - x:X1 - x]
    img = np.frombuffer(buf, np.uint8).reshape(OH, OW, 3)
    s = score(img, A); s["f"] = f
    d = res.setdefault(ri, dict(shot=r["shot"], f0=r["f0"], f1=r["f1"], roll=r["roll"], framing=r["framing"], placement=r["placement"], bg=r["bg"], bg_type=r["bg_type"], rect=r["rect"], frames=[]))
    d["frames"].append(s)
    worst = s["bl"][0] + s["dl"][0] * .5 + s["gl"][0]
    if worst >= d.get("worst", -1):
        d["worst"] = worst; d["wf"] = f; cv2.imwrite(f"{OUT}/s{ri:03d}.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 93])
        d["w_bl"], d["w_dl"], d["w_gl"] = s["bl"], s["dl"], s["gl"]
    if n % 100 == 0: print(n, flush=True)
json.dump(res, open(f"{OUT}/key.json", "w"), indent=0)
print("AUDIT DONE", len(res))
