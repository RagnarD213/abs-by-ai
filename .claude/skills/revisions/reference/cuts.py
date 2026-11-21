"""Per-cut shot-size report for a 1080x1920 short.
usage: cuts.py VIDEO OUTDIR
Finds hard cuts, then for each: background scale across the cut (SIFT, person/captions/graphic masked),
eye-distance ratio (mediapipe face mesh) and hair top y (selfie segmentation) on both sides."""
import sys, os, cv2, numpy as np, json
import mediapipe as mp
V, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
cap = cv2.VideoCapture(V); fps = cap.get(cv2.CAP_PROP_FPS)
frames = []; small = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(cv2.imencode('.jpg', f, [cv2.IMWRITE_JPEG_QUALITY, 92])[1])
    g = cv2.cvtColor(cv2.resize(f, (135, 240)), cv2.COLOR_BGR2GRAY).astype(np.float32)
    small.append(g[40:160])  # skip top graphic band and captions band
N = len(frames)
d = np.array([0] + [float(np.mean(np.abs(small[i] - small[i-1]))) for i in range(1, N)])
cuts = [i for i in range(2, N-2) if d[i] > 12 and d[i] > 3*max(d[i-1], 0.5) and d[i] > 3*max(d[i+1], 0.5)]
get = lambda i: cv2.imdecode(frames[i], 1)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)
seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
def face(im):
    h, w = im.shape[:2]; r = fm.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    if not r.multi_face_landmarks: return None
    l = r.multi_face_landmarks[0].landmark; p = lambda i: np.array([l[i].x*w, l[i].y*h])
    return float(np.linalg.norm(p(33)-p(263))), float(np.linalg.norm(p(10)-p(152))), float(p(168)[0]), float(p(168)[1])
def hairtop(im):
    r = seg.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)); m = r.segmentation_mask > 0.5
    m[:, :300] = False; m[:, 780:] = False
    rows = np.where(m.sum(1) > 25)[0]
    return int(rows[0]) if len(rows) else None
sift = cv2.SIFT_create(4000)
def bg(a, b):
    A = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY); B = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    def mask(im):
        m = np.full(im.shape, 255, np.uint8); m[:330, :] = 0; m[1000:, :] = 0; m[:, 330:750] = 0; return m
    ka, da = sift.detectAndCompute(A, mask(A)); kb, db = sift.detectAndCompute(B, mask(B))
    if da is None or db is None or len(ka) < 10 or len(kb) < 10: return None
    mm = cv2.BFMatcher().knnMatch(da, db, k=2)
    good = [x[0] for x in mm if len(x) == 2 and x[0].distance < 0.7*x[1].distance]
    if len(good) < 10: return None
    pa = np.float32([ka[m.queryIdx].pt for m in good]); pb = np.float32([kb[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=4)
    if M is None: return None
    return round(float(np.hypot(M[0,0], M[1,0])), 3), int(inl.sum()), len(good)
rows = []
print(f"{V}\nframes {N} fps {fps:.3f}\ncut_time  d   bgscale(inl/good)   eye a->b ratio   faceH ratio  nose jump   hairtop a->b")
for c in cuts:
    a, b = get(c-1), get(c)
    fa, fb = face(a), face(b); s = bg(a, b); ha, hb = hairtop(a), hairtop(b)
    er = f"{fa[0]:.0f}->{fb[0]:.0f} x{fb[0]/fa[0]:.3f}  fH x{fb[1]/fa[1]:.3f}  ({fb[2]-fa[2]:+.0f},{fb[3]-fa[3]:+.0f})" if fa and fb else f"face {'Y' if fa else 'n'}/{'Y' if fb else 'n'}"
    print(f"{c/fps:6.2f} (f{c}) d={d[c]:5.1f}  bg={s}  {er}  hair {ha}->{hb}")
    rows.append(dict(frame=c, t=c/fps, bg=s, fa=fa, fb=fb, ha=ha, hb=hb))
    pair = np.hstack([cv2.resize(a, (540, 960)), cv2.resize(b, (540, 960))])
    cv2.putText(pair, f"{c/fps:.2f}", (10, 940), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 3)
    cv2.imwrite(f"{OUT}/cut_{c:04d}.jpg", pair, [cv2.IMWRITE_JPEG_QUALITY, 80])
# per-shot: hair top min over the shot (every 3rd frame), zoom within shot
bounds = [0] + cuts + [N]
print("\nshot  start-end   face?  hairtop min/median   in-shot bg scale first->last")
for i in range(len(bounds)-1):
    a, b = bounds[i], bounds[i+1]-1
    if b - a < 4: continue
    hs = [hairtop(get(j)) for j in range(a+1, b, 3)]; hs = [h for h in hs if h is not None]
    f = face(get((a+b)//2)); s = bg(get(a+1), get(b-1))
    print(f"{a/fps:6.2f}-{(b+1)/fps:6.2f}  {'cam eye %.0f'%f[0] if f else 'noface'}  hair min {min(hs) if hs else None} med {int(np.median(hs)) if hs else None}  zoom {s}")
json.dump(rows, open(f"{OUT}/cuts.json", "w"))
