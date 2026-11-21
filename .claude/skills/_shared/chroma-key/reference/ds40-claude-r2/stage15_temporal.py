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

Speed (2026-10-21, Handoffs/results-20261021-cheap-key.md), output bit-identical to the approved R2 code: each worker
keys a run of consecutive frames and keeps the frames, greys and DIS flows of its window, so every flow is computed
once instead of twice; the neighbour warps and confidences are computed only on the edge band (plus 2 px for the speck
rule's 5x5 maximum), the only pixels they can change; cv2 runs one thread per worker and the pool is RENDERQ_CORES
workers (the render queue's allowance, default 4). ONLY=f1,f2,... re-keys just those frames (a failing piece).
MIN_FRAMES (default 200) guards against a partial cache; calibrate.py sets it low for its 2-3 s excerpts.
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
assert N > int(os.environ.get("MIN_FRAMES", "200")), f"{IN} has {N} frames"
R = int(os.environ.get("R", "3"))        # neighbours each side
TW = {1: 0.85, 2: 0.6, 3: 0.35}          # temporal weights
SIG_G, SIG_FB, SIG_A = 10.0, 1.0, 0.20   # confidence widths: grey levels, flow px, alpha
RIM = float(os.environ.get("RIM", "2"))  # px inside the outline whose colour is taken from deeper skin/hair
OY = 175                                 # output y of source row 0
GROW = 0.85                              # watch: brighter sliver allowed within 2 px of the glass
DARK = 0.65                              # watch: darker than this fraction of the screen = glass, not gap
BAND = 10                                # px each side of the edge that may be smoothed
CORES = int(os.environ.get("WORKERS") or os.environ.get("RENDERQ_CORES") or 4)
K = 2048                                 # points per row when warping a point list (cv2 needs rows < 32767)
FLOW_CACHE = int(os.environ.get("FLOW_CACHE", "2"))   # flows kept for neighbours this close; farther ones are recomputed

_src = None
def src_frame(i):
    """Source frame i of SRC_U8.npy, read with pread: no memory map, so a worker's resident memory does not grow
    with every frame it has touched (same bytes as np.load(..., mmap_mode="r")[i])."""
    global _src
    if _src is None:
        f = open(SRCU8, "rb")
        v = np.lib.format.read_magic(f)
        shape, _fo, dt = (np.lib.format.read_array_header_1_0 if v == (1, 0) else np.lib.format.read_array_header_2_0)(f)
        _src = (f, shape, dt, f.tell(), int(np.prod(shape[1:])) * dt.itemsize)
    f, shape, dt, off, n = _src
    return np.frombuffer(os.pread(f.fileno(), n, off + i * n), dt).reshape(shape[1:])

_plate = None
def plate():
    global _plate
    if _plate is None:
        _plate = np.load(os.path.join(os.path.dirname(SRCU8), "plate_out.npy"), mmap_mode="r")
    return _plate

def grey(i):
    return cv2.cvtColor(src_frame(i), cv2.COLOR_RGB2GRAY)

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

class Window:
    """Frames, greys and flows of the frames around the one being keyed. A flow i->j is computed once and serves
    both frame i (forward) and frame j (its backward check), exactly as the per-frame code computed it twice."""
    def __init__(self):
        self.dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        self.g, self.d, self.fl = {}, {}, {}
    def grey(self, j):
        if j not in self.g: self.g[j] = grey(j)
        return self.g[j]
    def frame(self, j):                   # (H, W, 4) float32: premultiplied colour + alpha, one remap for both
        if j not in self.d: self.d[j] = np.load(FILES[j])     # kept as stored (float16): half the memory
        return self.d[j].astype(np.float32)
    def flow(self, i, j):
        if abs(i - j) > FLOW_CACHE:
            return self.dis.calc(self.grey(i), self.grey(j), None)
        if (i, j) not in self.fl: self.fl[(i, j)] = self.dis.calc(self.grey(i), self.grey(j), None)
        return self.fl[(i, j)]
    def forget(self, i):                  # keying frame i next, in increasing order
        for c in (self.g, self.d):
            for k in [k for k in c if k < i - R]: del c[k]
        for k in [k for k in self.fl if max(k) < i]: del self.fl[k]

def warp(img, mx, my):
    """cv2.remap of img at the point lists mx, my: the same value cv2.remap gives at those pixels of a full map."""
    n = len(mx); pad = (-n) % K
    px = np.concatenate([mx, np.zeros(pad, np.float32)]).reshape(-1, K)
    py = np.concatenate([my, np.zeros(pad, np.float32)]).reshape(-1, K)
    r = cv2.remap(img, px, py, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return r.reshape((-1,) + img.shape[2:])[:n]

def work(i, win):
    d = win.frame(i)
    Fp, a = d[..., :3], np.ascontiguousarray(d[..., 3])
    gi = win.grey(i)
    h, w = a.shape
    # edge band: within BAND px of a partly transparent pixel (= binary_dilation(semi, iterations=BAND): L1 ball)
    semi = (a > 0.004) & (a < 0.985)
    band = cv2.distanceTransform((~semi).astype(np.uint8), cv2.DIST_L1, 3) <= BAND if semi.any() else np.zeros_like(semi)
    F = np.where(a[..., None] > 0.01, Fp / np.maximum(a[..., None], 1e-3), 0)
    # neighbour work happens only on the band plus 2 px (the speck rule's 5x5 maximum reads that far)
    reg = cv2.dilate(band.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    ys, xs = np.nonzero(reg)
    inb = band[ys, xs]
    xr, yr = xs.astype(np.float32), ys.astype(np.float32)
    a_r = a[ys, xs]; g_r = gi[ys, xs].astype(np.float32); F_r = F[ys, xs]
    acc = a_r.copy(); wsum = np.ones_like(a_r)
    accF = F_r * a_r[..., None]; wF = a_r.copy()  # colour averaged where each frame is actually foreground
    nb = []                                       # immediate neighbours, for the speck rule (band pixels)
    for j in range(max(0, i - R), min(N, i + R + 1)):
        if j == i: continue
        gj = win.grey(j)
        f = win.flow(i, j)[ys, xs]                # i -> j: where pixel of i sits in j
        b = win.flow(j, i)
        mx, my = xr + f[..., 0], yr + f[..., 1]
        wd = warp(win.frame(j), mx, my)
        wFp, wa = wd[..., :3], wd[..., 3]
        wg = warp(gj.astype(np.float32), mx, my)
        wb = warp(b, mx, my)
        fb = np.linalg.norm(f + wb, axis=-1)
        c_track = np.exp(-((wg - g_r) / SIG_G) ** 2) * np.exp(-(fb / SIG_FB) ** 2)
        c = c_track * np.exp(-((wa - a_r) / SIG_A) ** 2)
        if abs(j - i) == 1:
            full = np.zeros((h, w), np.float32); full[ys, xs] = wa
            mxf = cv2.dilate(full, np.ones((5, 5), np.uint8))[ys, xs]   # = ndi.maximum_filter(wa, 5) on the band
            nb.append((mxf, np.exp(-((wg - g_r) / SIG_G) ** 2)))
        c *= TW[abs(j - i)]
        acc += wa * c; wsum += c
        accF += wFp * c[..., None]; wF += wa * c
    a_t = acc / wsum
    F_t = accF / np.maximum(wF, 1e-4)[..., None]
    # only the edge band changes; solid detail (a near 1) is kept exactly
    keep_solid = np.clip((a_r - 0.92) / 0.06, 0, 1)
    a_new = a.copy()
    a_new[ys[inb], xs[inb]] = (a_t * (1 - keep_solid) + a_r * keep_solid)[inb]
    # speck rule: a pixel detached from Dan (2 px or more from anything over 0.9) cannot be much more solid than the
    # most solid pixel within 2 px of the same spot in BOTH neighbouring frames (flow is loose on flat screen, so only
    # the picture match is required). One-frame grain clumps go; real moving strands agree with a neighbour.
    # Off the band nothing can change: there a is solid (never detached) or under 0.004 (below any cap).
    if len(nb) == 2:
        (w1, c1), (w2, c2) = nb
        tracked = np.zeros((h, w), bool); tracked[ys, xs] = (c1 > 0.6) & (c2 > 0.6) & inb
        # distance_transform_edt(a_new <= 0.9) >= 2 is "no pixel over 0.9 in the 3x3 around"
        detached = ~cv2.dilate((a_new > 0.9).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        # only islands: a blurred fingertip is one piece with its hand (alpha > 0.1 all the way); a grain clump is not
        lab, n = ndi.label(a_new > 0.1)
        if n:
            body = np.unique(lab[ndi.binary_dilation(a_new > 0.9)]); body = body[body > 0]
            isb = np.zeros(n + 1, bool); isb[body] = True
            detached &= ~isb[lab]
        cap = np.zeros((h, w), np.float32); cap[ys, xs] = np.maximum(w1, w2) + 0.1
        a_new = np.where(tracked & detached & (a_new > cap), cap, a_new).astype(np.float32)
    # colour: unpremultiply, then decontaminate toward nearby solid colour as alpha falls
    F_t = F_t * (1 - keep_solid[..., None]) + F_r * keep_solid[..., None]
    sel = inb & (wF > 0.02)
    F[ys[sel], xs[sel]] = F_t[sel]
    # colour source: solid pixels at least 3 px inside the outline (the outermost 'solid' pixels are themselves the
    # dark mixed edge: the positivity floor rates them opaque while they still hold screen-subtraction error)
    deep = ndi.binary_erosion(a > 0.97, iterations=3).astype(np.float32)
    Fn = fill_colour(F, deep)
    t_a = np.clip((0.95 - a_new) / 0.55, 0, 1)
    d_out = ndi.distance_transform_edt(a_new >= 0.5)
    t_z = np.clip((RIM + 2 - d_out) / 2, 0, 1) if RIM > 0 else 0 * t_a
    t = np.maximum(t_a, t_z)
    del d_out, t_z
    # F2 = F * (1 - t) + Fn * t is built in row blocks at the end (it is float64: a full frame of it and its
    # temporaries was ~0.2 GB per worker); the watch boxes work on a patch of it covering their union
    boxes = [(f0, f1, x0, y0 - OY, x1, y1 - OY) for f0, f1, x0, y0, x1, y1 in MASKS.get("ranges", []) if f0 <= i <= f1]
    patch = None
    if boxes:
        py0, py1 = max(0, min(b[3] for b in boxes)), min(h, max(b[5] for b in boxes))
        px0, px1 = max(0, min(b[2] for b in boxes)), min(w, max(b[4] for b in boxes))
        tt = t[py0:py1, px0:px1][..., None]
        patch = F[py0:py1, px0:px1] * (1 - tt) + Fn[py0:py1, px0:px1] * tt
    # watch glass: hand-placed box per frame range; inside it, pixels clearly darker than the screen that join the
    # black case are solid (glass seen edge-on mirrors the screen dimly; real gaps show the screen at full brightness)
    for f0, f1, x0, y0, x1, y1 in boxes:
        P = np.asarray(src_frame(i)[y0:y1, x0:x1]).astype(np.float32) / 255
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
        sub_a = a_new[y0:y1, x0:x1]; sub_F = patch[y0 - py0:y1 - py0, x0 - px0:x1 - px0]
        a_new[y0:y1, x0:x1] = np.maximum(sub_a, wm)
        patch[y0 - py0:y1 - py0, x0 - px0:x1 - px0] = sub_F * (1 - wm[..., None]) + Pd * wm[..., None]
    out = np.empty((h, w, 4), np.float16)
    for r0 in range(0, h, 256):
        r1 = min(h, r0 + 256)
        tt = t[r0:r1][..., None]
        F2 = F[r0:r1] * (1 - tt) + Fn[r0:r1] * tt
        if patch is not None and r0 < py1 and r1 > py0:
            q0, q1 = max(r0, py0), min(r1, py1)
            F2[q0 - r0:q1 - r0, px0:px1] = patch[q0 - py0:q1 - py0]
        out[r0:r1] = np.concatenate([np.clip(F2, 0, None) * a_new[r0:r1, :, None], a_new[r0:r1, :, None]], -1).astype(np.float16)
    tmp = f"{OUT}/.tmp_f{i:04d}.npy"; np.save(tmp, out); os.replace(tmp, f"{OUT}/f{i:04d}.npy")
    return i, float(np.abs(a_new - a)[band].mean()) if band.any() else 0.0

def init():
    cv2.setNumThreads(1)                 # one core per worker: the pool is the allowance (outputs are identical)

def run(frames_):
    """Key a run of consecutive frames with one window of cached frames and flows."""
    win = Window(); res = []
    for i in frames_:
        win.forget(i)
        res.append(work(i, win))
    return res

def chunks(idx, workers):
    """Consecutive runs of idx, cut into about two pieces per worker (a cut costs one frame's flows again)."""
    runs, cur = [], [idx[0]]
    for i in idx[1:]:
        if i == cur[-1] + 1: cur.append(i)
        else: runs.append(cur); cur = [i]
    runs.append(cur)
    size = max(8, -(-len(idx) // (2 * workers)))
    return [r[k:k + size] for r in runs for k in range(0, len(r), size)]

if __name__ == "__main__":
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ.setdefault(v, "1")
    only = [int(x) for x in os.environ.get("ONLY", "").split(",") if x]
    idx = sorted(only) or list(range(N))
    t0 = time.time(); n = 0
    with Pool(CORES, initializer=init) as pool:
        for res in pool.imap_unordered(run, chunks(idx, CORES)):
            for i, dch in res:
                n += 1
                if n % 40 == 0: print(n, "frames", round(time.time() - t0), "s; mean band change", round(dch, 4), flush=True)
    print("done", n, round(time.time() - t0), "s")
    assert len(glob.glob(f"{OUT}/f*.npy")) >= len(idx)
