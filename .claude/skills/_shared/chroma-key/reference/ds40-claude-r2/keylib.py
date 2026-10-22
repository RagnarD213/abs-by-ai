"""DS-40 keyer v2: clean-plate colour-difference key (linear edges + solid core), screen subtraction,
average-limiter despill with neutral luminance restore, optional light wrap."""
import numpy as np
from scipy import ndimage as ndi

_plate = None
def plate_full(shape):
    global _plate
    if _plate is None or _plate.shape[:2] != shape[:2]:
        q = np.load("/Volumes/Extreme/_edit_work/ds40/r1/key/plate_q.npy")
        zy, zx = shape[0] / q.shape[0], shape[1] / q.shape[1]
        _plate = np.stack([ndi.zoom(q[..., c], (zy, zx), order=1) for c in range(3)], -1).astype(np.float32)
    return _plate

def excess(img):
    return img[..., 1] - np.maximum(img[..., 0], img[..., 2])

def local_plate(P, S, a0, q=4, sigma=6):
    """Per-frame plate: global plate times the frame's own screen/plate ratio, filled in from
    nearby pure-screen pixels (catches Dan's shadow and lighting drift next to the edges)."""
    h, w = a0.shape
    hq, wq = h // q, w // q
    Pq = P[:hq*q, :wq*q].reshape(hq, q, wq, q, 3).mean((1, 3))
    Sq = S[:hq*q, :wq*q].reshape(hq, q, wq, q, 3).mean((1, 3))
    scr = (a0[:hq*q, :wq*q].reshape(hq, q, wq, q).max((1, 3)) <= 0.0)
    scr = ndi.binary_erosion(scr, iterations=1)
    ratio = np.where(scr[..., None], Pq / np.maximum(Sq, 1e-3), 0)
    wgt = scr.astype(np.float32)
    out = np.ones((hq, wq, 3), np.float32); done = np.zeros((hq, wq), bool)
    for sg in [sigma, sigma * 3, sigma * 9]:
        num = np.stack([ndi.gaussian_filter(ratio[..., c], sg) for c in range(3)], -1)
        den = ndi.gaussian_filter(wgt, sg)
        est = num / np.maximum(den, 1e-6)[..., None]
        sel = (~done) & (den > 0.05)
        out[sel] = est[sel]; done |= sel
    out = np.clip(out, 0.6, 1.4)
    up = np.stack([ndi.zoom(out[..., c], (h / hq, w / wq), order=1) for c in range(3)], -1)
    return S * up[:h, :w]

def key(P, lo=0.12, core_t=0.85, core_erode=3, denoise=1.2, edge_gamma=1.0, refine=True, pos_lo=0.22, fill_holes=True, holdout=True):
    S = plate_full(P.shape)
    if refine:
        a0, _ = key(P, lo, core_t, core_erode, denoise, edge_gamma, refine=False, pos_lo=pos_lo, fill_holes=False, holdout=False)
        S = local_plate(P, S, a0)
    ex = excess(P)
    if denoise:
        ex = ndi.gaussian_filter(ex, denoise)
    e = ex / np.maximum(excess(S), 0.03)        # 1 on screen, <=0 on subject
    a_lin = np.clip((1.0 - e - lo) / (1.0 - lo), 0, 1)
    if pos_lo is not None:
        # positivity: a pixel darker than the screen in any channel cannot be mostly screen
        Pd = np.stack([ndi.gaussian_filter(P[..., c], denoise or 1.0) for c in range(3)], -1)
        rmin = (Pd / np.maximum(S, 1e-3)).min(-1)
        a_pos = np.clip((1.0 - rmin - pos_lo) / (1.0 - pos_lo), 0, 1)
        a_lin = np.maximum(a_lin, a_pos)
    if edge_gamma != 1.0:
        a_lin = a_lin ** edge_gamma
    core = ndi.binary_erosion(a_lin > core_t, iterations=core_erode)
    core = ndi.gaussian_filter(core.astype(np.float32), 1.5)
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
    mx, mn = sub.max(-1), sub.min(-1)
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
    zone = ndi.binary_dilation(keep[lab], iterations=pad)
    ratio = (sub.sum(-1) + 1e-4) / (Ssub.sum(-1) + 1e-4)
    solid = zone & (ratio < dark_ratio)
    solid = ndi.binary_closing(solid, iterations=2) & zone
    # the glass face seen side-on mirrors the screen exactly (screen colour, screen brightness): fill it by shape,
    # closing the black case outline so the glass strip inside it becomes solid
    case = zone & (Y < 0.12) & ((mx - mn) < 0.06)
    case = ndi.binary_opening(case, iterations=1)
    hull = ndi.binary_fill_holes(ndi.binary_closing(case, structure=np.ones((3, 3), bool), iterations=12)) & zone
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
    holes = ndi.binary_fill_holes(solid) & ~solid
    if not holes.any():
        return a
    lab, n = ndi.label(holes)
    idx = np.arange(1, n + 1)
    if P is not None:
        sp = P.sum(-1, keepdims=True) + 1e-4; ss = S.sum(-1, keepdims=True) + 1e-4
        chroma_d = np.abs(P / sp - S / ss).max(-1)
        bright = sp[..., 0] / ss[..., 0]
        screenlike = (chroma_d < 0.06) & (bright > 0.4) & (bright < 1.5)
    else:
        screenlike = e > 0.85
    frac_screen = ndi.mean(screenlike.astype(np.float32), lab, idx)
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
