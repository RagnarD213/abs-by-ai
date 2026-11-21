"""Remove the image model's wormy skin texture on the body (not the face): skin mask by colour, edge-preserving smoothing of
the 1-4 px band only, then a little fine grain back. Usage: deskin.py IN OUT [faceY1]"""
import sys, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src); h, w = im.shape[:2]
ycc = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
m = ((ycc[...,1] > 135) & (ycc[...,1] < 180) & (ycc[...,2] > 85) & (ycc[...,2] < 135) & (ycc[...,0] > 60)).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5,5),np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
fy = int(sys.argv[3]) if len(sys.argv) > 3 else 0
if fy: m[:fy] = 0
mf = cv2.GaussianBlur(m.astype(np.float32), (0,0), 3)[..., None]
f = im.astype(np.float32)
low = cv2.GaussianBlur(f, (0,0), 4.0)            # shape and shading
mid = cv2.GaussianBlur(f, (0,0), 0.8) - low       # the worm band lives here
sm = cv2.bilateralFilter(im, 0, 12, 6).astype(np.float32)
smid = cv2.GaussianBlur(sm, (0,0), 0.8) - cv2.GaussianBlur(sm, (0,0), 4.0)
clean = low + 0.45*mid + 0.55*smid
rng = np.random.default_rng(1); grain = rng.normal(0, 2.2, (h, w, 1)).astype(np.float32)
clean = clean + grain
res = f*(1-mf) + clean*mf
cv2.imwrite(out, np.clip(res+.5,0,255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95] if out.endswith('.jpg') else [])
cv2.imwrite(out.rsplit('.',1)[0]+'_mask.png', (m*255))
