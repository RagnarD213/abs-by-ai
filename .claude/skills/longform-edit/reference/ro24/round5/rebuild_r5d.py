"""A7 redo 3: inputs from fix_start_r5d.py (hair, garment colour, shoe, strip). A7 redo 2 (review 2 FAIL): START regenerated from END with identity locked (start_v3: same hair, shoes, shirts); the landing
spot / steps hole grown 25 px before its feather (review 2: a ghost of END's shoe on step 4); the rim clamp only on the calm man
against the sky (review 2: it smeared the jumper's hair); no shoe blur (review 2: a grey box). Redo 1 note follows.
A7 redo 1 (after review 1 FAIL): one shared background for both frames (END's own trees and sky), each frame's men from its
own generation inside a tight Apple Vision person mask (2 px grow, 2 px feather), the same edge-preserving softening on every
background pixel, START's empty landing spot / steps colour-matched to the shared background, and the 1-2 px bright rim
around the men clamped to the local background estimate + 2 (round 4 A8 method). Inputs: masks/S.png (start_v1), masks/E.png
(end_v4), masks/S.full.mask.png, masks/E.mask.png. Writes start.png, end.png."""
import cv2, numpy as np
D = '/Volumes/Expansion/_edit_work/RO-24/round5/ai/A7/'
S = cv2.imread(D + 'masks/S3fix.png').astype(np.float32); E = cv2.imread(D + 'masks/E.png').astype(np.float32)
def soft(I, strong=True):
    o = cv2.bilateralFilter(I.astype(np.uint8), 7, 28, 5).astype(np.float32)
    return cv2.GaussianBlur(o, (0, 0), 0.8 if strong else 0.45)
def mask(p, grow=2, feather=2):
    m = (cv2.imread(p, 0) > 110).astype(np.uint8)
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1, 2 * grow + 1)))
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), feather)[..., None].clip(0, 1)
mS, mE = mask(D + 'masks/S3.full.mask2.png'), mask(D + 'masks/E.mask.png')
bg = soft(E)                                                     # the shared background (END's pines, sky, wall, lawn, steps)
# what is behind END's men in START: START's own empty lawn / steps, colour-matched to the shared background around them
hole = (cv2.dilate((mE[..., 0] > 0.01).astype(np.uint8), np.ones((51, 51), np.uint8)) > 0) & (mS[..., 0] < 0.5)
ring = (cv2.dilate(hole.astype(np.uint8), np.ones((41, 41), np.uint8)) > 0) & ~hole & (mS[..., 0] < 0.02)
Ss = soft(S); fill = Ss.copy()
n, lab = cv2.connectedComponents(hole.astype(np.uint8))
for i in range(1, n):
    h = lab == i; r = ring & (cv2.dilate(h.astype(np.uint8), np.ones((61, 61), np.uint8)) > 0)
    if r.sum() < 200: r = (cv2.dilate(h.astype(np.uint8), np.ones((121, 121), np.uint8)) > 0) & ~hole & (mS[..., 0] < 0.02)
    if r.sum() < 200: continue                                   # nothing to match against: keep START's own pixels
    for c in range(3):
        a, b = Ss[..., c][r], bg[..., c][r]
        fill[..., c][h] = (Ss[..., c][h] - a.mean()) * (b.std() / max(a.std(), 1e-3)) + b.mean()
hf = cv2.GaussianBlur(cv2.erode(hole.astype(np.uint8), np.ones((13, 13), np.uint8)).astype(np.float32), (0, 0), 4)[..., None]
hf = np.maximum(hf, (cv2.dilate((mE[..., 0] > 0.01).astype(np.uint8), np.ones((23, 23), np.uint8)) > 0)[..., None] * 1.0)
bgS = bg * (1 - hf) + fill * hf                                  # START's background: shared, with the landing spot emptied
SKYBOX = (1080, 60, 1340, 470)                                    # calm man against the sky only
def rimfix(img, m, base):
    """clamp the bright halo just outside the men to the background estimate + 2"""
    core = (m[..., 0] > 0.5).astype(np.uint8)
    band = (cv2.dilate(core, np.ones((7, 7), np.uint8)) > 0) & (cv2.erode(core, np.ones((3, 3), np.uint8)) == 0)
    est = cv2.inpaint(base.clip(0, 255).astype(np.uint8), cv2.dilate(core, np.ones((9, 9), np.uint8)), 7, cv2.INPAINT_TELEA).astype(np.float32)
    L, Le = img.mean(-1), est.mean(-1)
    sky = np.zeros_like(band); x0, y0, x1, y1 = SKYBOX; sky[y0:y1, x0:x1] = True
    hot = band & sky & (L > Le + 4)
    out = img.copy(); out[hot] = est[hot] + 2
    return out, int(hot.sum())
Sp, Ep = soft(S, False), soft(E, False)                          # the men themselves: a lighter softening (AI crunch)
St = bgS * (1 - mS) + Sp * mS; Et = bg * (1 - mE) + Ep * mE
St, nS = rimfix(St, mS, bgS); Et, nE = rimfix(Et, mE, bg)
cv2.imwrite(D + 'start.png', St.round().clip(0, 255).astype(np.uint8)); cv2.imwrite(D + 'end.png', Et.round().clip(0, 255).astype(np.uint8))
a, b = St, Et; outside = (mS[..., 0] < 0.01) & (mE[..., 0] < 0.01) & ~hole
print('rim px clamped', nS, nE, '| outside men+hole max diff', float(np.abs(a - b)[outside].max()), 'mean', float(np.abs(a - b)[outside].mean()))
