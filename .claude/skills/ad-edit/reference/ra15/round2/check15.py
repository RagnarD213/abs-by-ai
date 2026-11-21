"""RA-15 round 2: the measured sense check on an AI take, before anyone looks at it in the ad (VIDEO-RULES 2026-10-13 / 10-14).
usage: check15.py <take.mp4> [a_s b_s]       (a..b: the part of the take that would be used; default the whole take)
Writes beside the take:
  <take>.sheet.jpg      every 4th frame of the used part, numbered (watch the action step by step)
  <take>.ends.jpg       every 2nd frame of the first and the last second of the used part
  <take>.selfchange.jpg first frame against its tenth AND tenth-last against last, people masked (Vision person mask grown 40 px):
                        anything bright outside the blue mask changed by itself
  <take>.check.json     frame-to-frame change per frame (a baked cut or dissolve shows as a spike or a ramp) and the self-change blobs"""
import sys, os, json, subprocess, numpy as np, cv2, tempfile
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
src = sys.argv[1]; base = src[:-4]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(f)
n = len(F); a = int(round(float(sys.argv[2])*fps)) if len(sys.argv) > 3 else 0; b = min(n, int(round(float(sys.argv[3])*fps))) if len(sys.argv) > 3 else n
U = F[a:b]; H, W = U[0].shape[:2]
def lab(img, t):
    img = img.copy(); cv2.rectangle(img, (0, 0), (300, 70), (0, 0, 0), -1); cv2.putText(img, t, (10, 52), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 3); return img
def grid(frames, idx, cols, w):
    th = [cv2.resize(lab(f, f"{i} {i/fps:.2f}s"), (w, int(w*H/W))) for f, i in zip(frames, idx)]
    while len(th) % cols: th.append(np.zeros_like(th[0]))
    return np.vstack([np.hstack(th[r:r+cols]) for r in range(0, len(th), cols)])
idx = list(range(a, b, 4)); cv2.imwrite(base + ".sheet.jpg", grid([F[i] for i in idx], idx, 8, 240), [cv2.IMWRITE_JPEG_QUALITY, 85])
k = int(round(fps)); i1 = list(range(a, min(b, a+k), 2)); i2 = list(range(max(a, b-k), b, 2))
cv2.imwrite(base + ".ends.jpg", np.vstack([grid([F[i] for i in i1], i1, len(i1), 200), grid([F[i] for i in i2], i2, len(i2), 200)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
# frame-to-frame change over the whole take
diff = [0.0] + [float(np.abs(F[i].astype(np.int16) - F[i-1]).mean()) for i in range(1, n)]
med = float(np.median(diff[1:])); spikes = [(i, round(d, 2)) for i, d in enumerate(diff) if i and d > max(6.0, 4*med)]
# self change: pair (p, q), people of both frames masked
td = tempfile.mkdtemp()
def people(i):
    p = f"{td}/f{i}.png"; cv2.imwrite(p, F[i]); subprocess.run([PM, td, p], capture_output=True)
    m = cv2.imread(f"{td}/f{i}.mask.png", 0); return (m > 60).astype(np.uint8) if m is not None else np.zeros((H, W), np.uint8)
def selfchange(p, q):
    A = cv2.GaussianBlur(F[p], (0, 0), 1.5).astype(np.float32); B = cv2.GaussianBlur(F[q], (0, 0), 1.5).astype(np.float32); kk = np.ones((7, 7), np.uint8)
    d = np.maximum(np.maximum(A - cv2.dilate(B, kk), cv2.erode(B, kk) - A), 0).max(2)
    man = cv2.dilate(np.maximum(people(p), people(q)), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81)))
    m = ((d > 10) & (man == 0)).astype(np.uint8); nn, l2, s2, _ = cv2.connectedComponentsWithStats(m)
    blobs = sorted(((int(s2[j, 4]), int(s2[j, 0]), int(s2[j, 1]), int(s2[j, 2]), int(s2[j, 3])) for j in range(1, nn) if s2[j, 4] >= 30), reverse=True)[:8]
    vis = cv2.cvtColor(np.clip(d*10, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR); vis[man > 0] = (vis[man > 0]*0.3 + np.array([90, 0, 0])).astype(np.uint8)
    for ar, x, y, w, h in blobs: cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 255), 3)
    return blobs, cv2.resize(lab(vis, f"{p}>{q}"), (W//2, H//2))
s1, v1 = selfchange(a, min(b-1, a+9)); s2, v2 = selfchange(max(a, b-10), b-1)
mid = (a + b)//2; s3, v3 = selfchange(mid, min(b-1, mid+9))
cv2.imwrite(base + ".selfchange.jpg", np.hstack([v1, v3, v2]), [cv2.IMWRITE_JPEG_QUALITY, 85])
R = {"take": src, "fps": fps, "frames": n, "used": [a, b], "diff_median": round(med, 2), "spikes": spikes,
     "self_change_first": s1, "self_change_mid": s3, "self_change_last": s2}
json.dump(R, open(base + ".check.json", "w"), indent=1)
print(json.dumps({k: R[k] for k in ("fps", "frames", "used", "diff_median", "spikes", "self_change_first", "self_change_mid", "self_change_last")}))
