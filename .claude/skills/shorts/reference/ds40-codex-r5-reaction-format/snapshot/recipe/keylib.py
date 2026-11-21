"""DS-40 keyer v2: clean-plate colour-difference key (linear edges + solid core), screen subtraction,
average-limiter despill with neutral luminance restore, optional light wrap."""
import numpy as np, cv2
from scipy import ndimage as ndi

# Speed (2026-10-21, Handoffs/results-20261021-cheap-key.md), every change bit-identical to the approved R2 code
# (279 of 279 frames of the approved sample identical; the rendered sample hashes match approval.json): the blurs
# that do not depend on the plate are computed once per frame and shared by the inner and outer key, the coarse
# local-plate scales are skipped once every pixel is filled, channel min/max/sum and block means are written out
# elementwise in numpy's own order, erosion/hole fill/closing/the 70 px watch zone use exact OpenCV equivalents,
# the hole test runs on hole pixels only, and the local plate is upsampled by a separable float64 bilinear equal to
# scipy's zoom(order=1). The blurs stay scipy's: OpenCV's (float32 or float64) differ in the last bits, which moved
# the gate's speck count on the sample.
def _blur(x, sg):
    if x.ndim == 3:
        return np.stack([ndi.gaussian_filter(x[..., c], sg) for c in range(x.shape[-1])], -1)
    return ndi.gaussian_filter(x, sg)

def _cmin(x):
    return np.minimum(np.minimum(x[..., 0], x[..., 1]), x[..., 2])

def _cmax(x):
    return np.maximum(np.maximum(x[..., 0], x[..., 1]), x[..., 2])

def _blockmean(x, q):
    """x[:h//q*q, :w//q*q].reshape(h//q, q, w//q, q, ...).mean((1, 3)), bit-identical (numpy sums in this order)."""
    hq, wq = x.shape[0] // q, x.shape[1] // q
    r = x[:hq*q, :wq*q].reshape((hq, q, wq, q) + x.shape[2:])
    if x.ndim == 2:                  # numpy sums each row of the block first, then the rows
        rows = []
        for i in range(q):
            acc = r[:, i, :, 0].copy()
            for j in range(1, q):
                acc += r[:, i, :, j]
            rows.append(acc)
        acc = rows[0]
        for i in range(1, q):
            acc += rows[i]
    else:                            # with channels last: every element of the block in order
        acc = r[:, 0, :, 0].copy()
        for i in range(q):
            for j in range(q):
                if i or j:
                    acc += r[:, i, :, j]
    return acc / np.float32(q * q)

def _sum3(x):
    return x[..., 0] + x[..., 1] + x[..., 2]

def _erode_cross(m, n):
    """ndi.binary_erosion(m, iterations=n) (cross structure, outside = False): L1 distance to the nearest False > n."""
    return cv2.distanceTransform(np.pad(m, 1).astype(np.uint8), cv2.DIST_L1, 3)[1:-1, 1:-1] > n

def _fill_holes(m):
    """ndi.binary_fill_holes(m): everything except the background 4-connected to the frame border."""
    n, lab = cv2.connectedComponents((~m).astype(np.uint8), connectivity=4)
    lut = np.zeros(n, bool)
    lut[np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))] = True
    return m | ~lut[lab]

def _zoom_lin(img, h, w):
    """scipy.ndimage.zoom(order=1, grid_mode=False) of an (hq, wq, C) array to (h, w): corners aligned."""
    hq, wq = img.shape[:2]
    def axis(n_in, n_out):
        pos = np.arange(n_out, dtype=np.float64) * ((n_in - 1) / (n_out - 1))
        i0 = np.minimum(np.floor(pos).astype(np.int64), n_in - 2); t = pos - i0
        return i0, t
    i0, ty = axis(hq, h); j0, tx = axis(wq, w)
    x = img.astype(np.float64)
    out = np.empty((h, w) + img.shape[2:], np.float32)
    for r0 in range(0, h, 128):      # row blocks: same arithmetic per pixel, no 4K float64 temporaries
        r1 = min(h, r0 + 128); ia, ta = i0[r0:r1], ty[r0:r1]
        r = x[ia] * (1 - ta)[:, None, None] + x[ia + 1] * ta[:, None, None]
        out[r0:r1] = r[:, j0] * (1 - tx)[None, :, None] + r[:, j0 + 1] * tx[None, :, None]
    return out

_plate = None
def plate_full(shape):
    global _plate
    if _plate is None or _plate.shape[:2] != shape[:2]:
        q = np.load("/Volumes/Extreme/_edit_work/DS-40-codex/round5/recipe/plate_q.npy")
        zy, zx = shape[0] / q.shape[0], shape[1] / q.shape[1]
        _plate = np.stack([ndi.zoom(q[..., c], (zy, zx), order=1) for c in range(3)], -1).astype(np.float32)
        _plate_const.clear()
    return _plate

_plate_const = {}
def _consts(S):
    """max(excess(S), 0.03) and max(S, 1e-3): computed once per process for the global plate."""
    if S is _plate:
        if not _plate_const:
            _plate_const["ex"] = np.maximum(excess(S), 0.03); _plate_const["m"] = np.maximum(S, 1e-3)
        return _plate_const["ex"], _plate_const["m"]
    return np.maximum(excess(S), 0.03), np.maximum(S, 1e-3)

def excess(img):
    return img[..., 1] - np.maximum(img[..., 0], img[..., 2])

def local_plate(P, S, a0, q=4, sigma=6):
    """Per-frame plate: global plate times the frame's own screen/plate ratio, filled in from
    nearby pure-screen pixels (catches Dan's shadow and lighting drift next to the edges)."""
    h, w = a0.shape
    hq, wq = h // q, w // q
    Pq = _blockmean(P, q)
    Sq = _blockmean(S, q)
    scr = ~(a0[:hq*q, :wq*q] > 0.0).reshape(hq, q, wq, q).any(axis=(1, 3))     # = block max <= 0
    scr = ndi.binary_erosion(scr, iterations=1)
    ratio = np.where(scr[..., None], Pq / np.maximum(Sq, 1e-3), 0)
    wgt = scr.astype(np.float32)
    out = np.ones((hq, wq, 3), np.float32); done = np.zeros((hq, wq), bool)
    for sg in [sigma, sigma * 3, sigma * 9]:
        if done.all():
            break
        num = _blur(ratio, sg)
        den = _blur(wgt, sg)
        est = num / np.maximum(den, 1e-6)[..., None]
        sel = (~done) & (den > 0.05)
        out[sel] = est[sel]; done |= sel
    out = np.clip(out, 0.6, 1.4)
    up = _zoom_lin(out, h, w)
    return S * up[:h, :w]

def key(P, lo=0.12, core_t=0.85, core_erode=3, denoise=1.2, edge_gamma=1.0, refine=True, pos_lo=0.22, fill_holes=True, holdout=True, _pre=None):
    S = plate_full(P.shape)
    if _pre is None:                            # blurs that do not depend on the plate: once per frame
        ex = excess(P)
        if denoise:
            ex = _blur(ex, denoise)
        Pd = _blur(P, denoise or 1.0) if pos_lo is not None else None
        _pre = (ex, Pd)
    ex, Pd = _pre
    if refine:
        a0, _ = key(P, lo, core_t, core_erode, denoise, edge_gamma, refine=False, pos_lo=pos_lo, fill_holes=False, holdout=False, _pre=_pre)
        S = local_plate(P, S, a0)
    exS, Sm = _consts(S)
    e = ex / exS                                # 1 on screen, <=0 on subject
    a_lin = np.clip((1.0 - e - lo) / (1.0 - lo), 0, 1)
    if pos_lo is not None:
        # positivity: a pixel darker than the screen in any channel cannot be mostly screen
        rmin = _cmin(Pd / Sm)
        a_pos = np.clip((1.0 - rmin - pos_lo) / (1.0 - pos_lo), 0, 1)
        a_lin = np.maximum(a_lin, a_pos)
    if edge_gamma != 1.0:
        a_lin = a_lin ** edge_gamma
    core = _erode_cross(a_lin > core_t, core_erode)
    core = _blur(core.astype(np.float32), 1.5)
    a = np.maximum(a_lin, core)
    if fill_holes:
        a = fill_inner_holes(a, e, P, S)
    if holdout:
        a = watch_holdout(a, P, S)
    return a, S

def watch_holdout(a, P, S, y_min=2600, pad=70, dark_ratio=0.70):
    """Tracked hold-out for the Apple Watch: its glossy case side mirrors the screen as a dark green strip on the
    outside of the wrist, which keys half transparent. Find the grey band (neutral, mid luma, low on the frame),
    and inside a zone around band + black case treat pixels much darker than the screen as solid."""
    sub = P[y_min:]; Ssub = S[y_min:]
    mx, mn = _cmax(sub), _cmin(sub)
    Y = 0.2126 * sub[..., 0] + 0.7152 * sub[..., 1] + 0.0722 * sub[..., 2]
    band = ((mx - mn) < 0.07) & (Y > 0.25) & (Y < 0.62)
    band = ndi.binary_opening(band, iterations=2)
    lab, n = ndi.label(band)
    if not n:
        return a
    sizes = ndi.sum(np.ones_like(Y), lab, np.arange(1, n + 1))
    keep = np.zeros(n + 1, bool); keep[1:] = sizes > 1200
    if not keep.any():
        return a
    zone = cv2.distanceTransform((~keep[lab]).astype(np.uint8), cv2.DIST_L1, 3) <= pad   # = binary_dilation(iterations=pad)
    ratio = (_sum3(sub) + 1e-4) / (_sum3(Ssub) + 1e-4)
    solid = zone & (ratio < dark_ratio)
    solid = ndi.binary_closing(solid, iterations=2) & zone
    # the glass face seen side-on mirrors the screen exactly (screen colour, screen brightness): fill it by shape,
    # closing the black case outline so the glass strip inside it becomes solid
    case = zone & (Y < 0.12) & ((mx - mn) < 0.06)
    case = ndi.binary_opening(case, iterations=1)
    k25 = np.ones((25, 25), np.uint8)                    # = binary_closing(3x3 square, iterations=12), outside False
    closed = cv2.erode(cv2.dilate(case.astype(np.uint8), k25), k25, borderType=cv2.BORDER_CONSTANT, borderValue=0)
    hull = _fill_holes(closed.astype(bool)) & zone
    # convex outline of each sizeable case piece: the glass face can sit on the case's outer edge, unenclosed
    from PIL import Image as _I, ImageDraw as _D
    from scipy.spatial import ConvexHull
    labc, nc = ndi.label(case)
    if nc:
        szc = ndi.sum(np.ones_like(Y), labc, np.arange(1, nc + 1))
        for j in np.where(szc > 1500)[0] + 1:
            ys, xs = np.where(labc == j)
            pts = np.c_[xs, ys]
            try:
                hv = ConvexHull(pts).vertices
            except Exception:
                continue
            m = _I.new("L", (Y.shape[1], Y.shape[0]), 0)
            _D.Draw(m).polygon([tuple(map(int, pts[v])) for v in hv], fill=1)
            hull |= np.asarray(m, bool) & zone
    solid |= hull
    out = a.copy()
    out[y_min:][solid] = np.maximum(out[y_min:][solid], 1.0)
    return out

def fill_inner_holes(a, e, P=None, S=None, solid_t=0.95):
    """Fill see-through patches fully enclosed by Dan (or by Dan and the laptop) unless the patch looks like the
    screen itself. 'Looks like screen' = the same chromaticity as the local plate and a plausible brightness ratio,
    so a real gap between arm and torso stays open while the watch's green activity rings (much brighter, purer
    green) and shine reflecting the screen are filled."""
    solid = a > solid_t
    holes = _fill_holes(solid) & ~solid
    if not holes.any():
        return a
    lab, n = ndi.label(holes)
    # 'looks like screen' is only ever read inside the holes: test those pixels only (same per-pixel arithmetic;
    # per-hole fractions of 0/1 values are exact sums, so this equals ndi.mean over the whole frame)
    lh = lab[holes]
    if P is not None:
        Ph, Sh = P[holes], S[holes]
        sp = _sum3(Ph)[..., None] + 1e-4; ss = _sum3(Sh)[..., None] + 1e-4
        chroma_d = _cmax(np.abs(Ph / sp - Sh / ss))
        bright = sp[..., 0] / ss[..., 0]
        screenlike = (chroma_d < 0.06) & (bright > 0.4) & (bright < 1.5)
    else:
        screenlike = e[holes] > 0.85
    frac_screen = np.bincount(lh, screenlike.astype(np.float64), n + 1)[1:] / np.bincount(lh, None, n + 1)[1:]
    fill = np.zeros(n + 1, bool)
    fill[1:] = frac_screen < 0.5
    out = a.copy()
    out[fill[lab]] = 1.0
    return out

def despill(F, strength=1.0, lum_restore=0.35):
    r, g, b = F[..., 0], F[..., 1], F[..., 2]
    lim = 0.5 * (r + b)
    d = np.clip(g - lim, 0, None) * strength
    out = F.copy()
    out[..., 1] = g - d
    out += (d * lum_restore)[..., None]
    return out, d

def composite(P, a, S, B, despill_strength=1.0, lum_restore=0.35, wrap=0.0, wrap_sigma=24):
    A = a[..., None]
    Fp = np.clip(P - (1.0 - A) * S, 0, None)     # premultiplied foreground
    Fp *= np.clip(A * 25.0, 0, 1)                # no screen grain leaks where alpha is ~0
    Fp, _ = despill(Fp, despill_strength, lum_restore)
    out = Fp + (1.0 - A) * B
    if wrap > 0:
        inv = 1.0 - a
        bb = np.stack([ndi.gaussian_filter(B[..., c] * inv, wrap_sigma) for c in range(3)], -1)
        cover = ndi.gaussian_filter(inv, wrap_sigma)[..., None]
        out = out * (1 - wrap * cover * A) + wrap * bb * A
    return np.clip(out, 0, 1)
