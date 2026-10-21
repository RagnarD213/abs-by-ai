"""Stage 1.5 (R2): steadier edges and clean edge colour, on the stage 1 cache at output scale.

    python3 stage15_temporal.py IN_CACHE SRC_U8.npy OUT_CACHE [watch_masks.json]

1. Motion-compensated temporal matte: each frame's alpha is averaged with its 2 neighbours on each side, warped into
   the frame with DIS optical flow on the source picture. A neighbour counts only where it agrees: picture match after
   warping, forward/backward flow consistency, and alpha agreement. Only the partly transparent edge band is touched;
   solid Dan and clear screen keep their own frame. Fast blurred hands lose confidence and keep their own blur.
2. Edge colour decontamination: the colour of a partly transparent pixel is pulled toward the colour of the nearest
   solid foreground (normalised convolution of alpha > 0.95 pixels), more as alpha falls, so no screen-subtraction
   error (the dark rim) is left in the edge.
3. Watch glass (optional JSON {"ranges": [[f0, f1, x0, y0, x1, y1], ...]}, hand-placed boxes in output pixels):
   inside the box, pixels darker than DARK x the screen that join the black case are made solid (1 px feather),
   colour = despilled source pixel, the same treatment the automatic hold-out gives the face seen square-on.
"""
import numpy as np, sys, os, glob, json, cv2, time
from multiprocessing import Pool
from scipy import ndimage as ndi
from keylib import despill

IN, SRCU8, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
MASKS = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
os.makedirs(OUT, exist_ok=True)
FILES = sorted(glob.glob(f"{IN}/f*.npy"))
N = len(FILES)
assert N > 200, f"{IN} has {N} frames"
R = int(os.environ.get("R", "3"))        # neighbours each side
TW = {1: 0.85, 2: 0.6, 3: 0.35}          # temporal weights
SIG_G, SIG_FB, SIG_A = 10.0, 1.0, 0.20   # confidence widths: grey levels, flow px, alpha
RIM = float(os.environ.get("RIM", "2"))  # px inside the outline whose colour is taken from deeper skin/hair
OY = 175                                 # output y of source row 0
GROW = 0.85                              # watch: brighter sliver allowed within 2 px of the glass
DARK = 0.65                              # watch: darker than this fraction of the screen = glass, not gap
BAND = 10                                # px each side of the edge that may be smoothed

_src = None
def src():
    global _src
    if _src is None:
        _src = np.load(SRCU8, mmap_mode="r")
    return _src

_plate = None
def plate():
    global _plate
    if _plate is None:
        _plate = np.load(os.path.join(os.path.dirname(SRCU8), "plate_out.npy"), mmap_mode="r")
    return _plate

def grey(i):
    return cv2.cvtColor(np.ascontiguousarray(src()[i]), cv2.COLOR_RGB2GRAY)

def load(i):
    d = np.load(FILES[i]).astype(np.float32)
    return d[..., :3], d[..., 3]

def fill_colour(F, w, sigmas=(1.5, 4, 12, 36)):
    """Normalised convolution: colour of nearby solid pixels, coarser scales only where finer ones see none."""
    out = np.zeros_like(F); done = np.zeros(w.shape, bool)
    for sg in sigmas:
        den = cv2.GaussianBlur(w, (0, 0), sg)
        num = cv2.GaussianBlur(F * w[..., None], (0, 0), sg)
        est = num / np.maximum(den, 1e-6)[..., None]
        sel = (~done) & (den > 0.08)
        out[sel] = est[sel]; done |= sel
    out[~done] = F[~done]
    return out

def work(i):
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    Fp, a = load(i)
    g = grey(i).astype(np.float32); gi = grey(i)
    h, w = a.shape
    yy, xx = np.mgrid[:h, :w].astype(np.float32)
    # edge band: within BAND px of a partly transparent pixel
    semi = (a > 0.004) & (a < 0.985)
    band = ndi.binary_dilation(semi, iterations=BAND)
    F = np.where(a[..., None] > 0.01, Fp / np.maximum(a[..., None], 1e-3), 0)
    acc = a.copy(); wsum = np.ones_like(a)
    accF = F * a[..., None]; wF = a.copy()       # colour averaged where each frame is actually foreground
    nb = []                                      # immediate neighbours, for the speck rule
    for j in range(max(0, i - R), min(N, i + R + 1)):
        if j == i: continue
        gj = grey(j)
        f = dis.calc(gi, gj, None)          # i -> j: where pixel of i sits in j
        b = dis.calc(gj, gi, None)
        mx, my = xx + f[..., 0], yy + f[..., 1]
        Fpj, aj = load(j)
        wa = cv2.remap(aj, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wFp = cv2.remap(Fpj, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wg = cv2.remap(gj.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wb = cv2.remap(b, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        fb = np.linalg.norm(f + wb, axis=2)
        c_track = np.exp(-((wg - g) / SIG_G) ** 2) * np.exp(-(fb / SIG_FB) ** 2)
        c = c_track * np.exp(-((wa - a) / SIG_A) ** 2)
        if abs(j - i) == 1:
            nb.append((ndi.maximum_filter(wa, 5), np.exp(-((wg - g) / SIG_G) ** 2)))
        c *= TW[abs(j - i)]
        acc += wa * c; wsum += c
        accF += wFp * c[..., None]; wF += wa * c
    a_t = acc / wsum
    F_t = accF / np.maximum(wF, 1e-4)[..., None]
    # only the edge band changes; solid detail (a near 1) is kept exactly
    keep_solid = np.clip((a - 0.92) / 0.06, 0, 1)
    a_new = np.where(band, a_t * (1 - keep_solid) + a * keep_solid, a).astype(np.float32)
    # speck rule: a pixel detached from Dan (2 px or more from anything over 0.9) cannot be much more solid than the
    # most solid pixel within 2 px of the same spot in BOTH neighbouring frames (flow is loose on flat screen, so only
    # the picture match is required). One-frame grain clumps go; real moving strands agree with a neighbour.
    if len(nb) == 2:
        (w1, c1), (w2, c2) = nb
        tracked = (c1 > 0.6) & (c2 > 0.6)
        detached = ndi.distance_transform_edt(a_new <= 0.9) >= 2
        # only islands: a blurred fingertip is one piece with its hand (alpha > 0.1 all the way); a grain clump is not
        lab, n = ndi.label(a_new > 0.1)
        if n:
            body = np.unique(lab[ndi.binary_dilation(a_new > 0.9)]); body = body[body > 0]
            detached &= ~np.isin(lab, body)
        cap = np.maximum(w1, w2) + 0.1
        a_new = np.where(tracked & detached & (a_new > cap), cap, a_new).astype(np.float32)
    # colour: unpremultiply, then decontaminate toward nearby solid colour as alpha falls
    F_t = F_t * (1 - keep_solid[..., None]) + F * keep_solid[..., None]
    F = np.where(band[..., None] & (wF[..., None] > 0.02), F_t, F)
    # colour source: solid pixels at least 3 px inside the outline (the outermost 'solid' pixels are themselves the
    # dark mixed edge: the positivity floor rates them opaque while they still hold screen-subtraction error)
    deep = ndi.binary_erosion(a > 0.97, iterations=3).astype(np.float32)
    Fn = fill_colour(F, deep)
    t_a = np.clip((0.95 - a_new) / 0.55, 0, 1)
    d_out = ndi.distance_transform_edt(a_new >= 0.5)
    t_z = np.clip((RIM + 2 - d_out) / 2, 0, 1) if RIM > 0 else 0 * t_a
    t = np.maximum(t_a, t_z)[..., None]
    F2 = F * (1 - t) + Fn * t
    # watch glass: hand-placed box per frame range; inside it, pixels clearly darker than the screen that join the
    # black case are solid (glass seen edge-on mirrors the screen dimly; real gaps show the screen at full brightness)
    for f0, f1, x0, y0, x1, y1 in MASKS.get("ranges", []):
        if not (f0 <= i <= f1): continue
        y0 -= OY; y1 -= OY
        P = np.asarray(src()[i][y0:y1, x0:x1]).astype(np.float32) / 255
        Sx = plate()[y0:y1, x0:x1]
        r = cv2.GaussianBlur(P.sum(-1), (0, 0), 0.8) / Sx.sum(-1)
        dark = r < DARK
        lab, n = ndi.label(dark)
        if not n: continue
        core = np.unique(lab[(r < 0.25) & dark]); core = core[core > 0]
        m = np.isin(lab, core)
        m = ndi.binary_fill_holes(ndi.binary_closing(m, iterations=2))
        # the glass's outermost sliver blends with the screen (up to ~0.85): grow into it, 2 px at most
        for _ in range(2):
            m |= ndi.binary_dilation(m) & (r < GROW)
        # glass at a grazing angle mirrors the screen at full brightness: close slits narrower than ~8 px between
        # solid pieces (case and forearm); real gaps between strap and hand are far wider
        sol = a_new[y0:y1, x0:x1] > 0.95
        disk = np.hypot(*np.mgrid[-4:5, -4:5]) <= 4
        m |= ndi.binary_closing(sol, structure=disk) & ~sol
        wm = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8) * 1.5, 0, 1)
        Pd, _ = despill(P)
        sub_a = a_new[y0:y1, x0:x1]; sub_F = F2[y0:y1, x0:x1]
        a_new[y0:y1, x0:x1] = np.maximum(sub_a, wm)
        F2[y0:y1, x0:x1] = sub_F * (1 - wm[..., None]) + Pd * wm[..., None]
    out = np.concatenate([np.clip(F2, 0, None) * a_new[..., None], a_new[..., None]], -1)
    np.save(f"{OUT}/f{i:04d}.npy", out.astype(np.float16))
    return i, float(np.abs(a_new - a)[band].mean()) if band.any() else 0.0

if __name__ == "__main__":
    only = [int(x) for x in os.environ.get("ONLY", "").split(",") if x]
    idx = only or list(range(N))
    t0 = time.time(); n = 0
    with Pool(int(os.environ.get("WORKERS") or os.environ.get("RENDERQ_CORES") or 4)) as pool:   # queue allowance
        for i, dch in pool.imap_unordered(work, idx):
            n += 1
            if n % 40 == 0: print(n, "frames", round(time.time() - t0), "s; mean band change", round(dch, 4), flush=True)
    print("done", n, round(time.time() - t0), "s")
    assert len(glob.glob(f"{OUT}/f*.npy")) >= len(idx)
