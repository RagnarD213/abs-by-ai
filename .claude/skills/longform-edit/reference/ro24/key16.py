"""RO-24 key: the locked Bill Maher (DS-40) R2 body/arm matte + R3 motion-stable fine hair, adapted to the 16:9
C1726 green screen. Same maths as `_shared/chroma-key/reference/ds40-r3/round3-key_v2.py` (body) and
`round3-key_v3.py` (hair); only the geometry is re-measured for this source:

  * the portrait sample's fixed hair ROI (x350:1850, y400:1300), hair band (top+470, fade 180) and handover rows
    (960..1120) become per-piece / per-frame values measured from Dan's own hair top on THIS roll, scaled by the
    measured head-size ratio S (C1726 head is about 0.75 of the DS-40 portrait head in native pixels);
  * the screen field is either the locked shot-stable 6-term quadratic ('quad') or a per-pixel clean plate of this
    screen ('plate': the 16:9 screen has vertical folds and low creases the quadratic misses by up to 0.03 green
    excess near the head, ~17% of the screen's own excess);
  * a garbage matte: only the connected foreground that is Dan survives (screen spots and creases far from him are 0),
    and processing is restricted to a per-piece box around him.

Output per piece: FFV1 gbrap16le (lossless RGB + alpha) at 2880x1620 holding UNPREMULTIPLIED foreground colour F and alpha a
(composite later: grade(F)*a + (1-a)*background). Temporal neighbours come only from the same continuous source range
(+/- 2 handle frames read past each end of the range, never across a cut).

usage: key16.py <start_s> <frames> <out.mov> [--screen plate|quad] [--box x0,y0,x1,y1] [--roi x0,y0,x1,y1]
"""
import sys, os, json, time, subprocess, argparse
import numpy as np, cv2
from scipy.ndimage import distance_transform_edt, label

SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4'
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
W = '/Volumes/Expansion/_edit_work/RO-24/round1'
FPS = 30000 / 1001
H, WD = 2160, 3840
OUT_W, OUT_H = 2880, 1620
S = 0.75                        # C1726 head size / DS-40 portrait head size (native px), measured 2026-10-20
DEC = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb48le'

# ---------------------------------------------------------------- screen fields
def quad_basis(h, w, y0=0, x0=0, fh=H, fw=WD):
    y, x = np.mgrid[y0:y0 + h, x0:x0 + w].astype(np.float32); x /= fw; y /= fh
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], -1)

def fit_quad_piece(start, frames):
    """R3/R4 shot-stable screen: per-sample quadratic fits at 1/16 scale with 3 trimming passes, median coefficients."""
    cs = []
    for i in range(0, max(frames, 1), 45):
        raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{start + i / FPS:.4f}', '-i', SRC, '-frames:v', '1', '-an', '-vf',
                                       DEC.replace(',format=rgb48le', '') + ',scale=240:135,format=rgb48le', '-f', 'rawvideo', '-'])
        s = np.frombuffer(raw, '<u2').reshape(135, 240, 3).astype(np.float32) / 65535
        M = quad_basis(135, 240, fh=135, fw=240); r, g, b = s.transpose(2, 0, 1); sel = (g - r > .14) & (g - b > .14)
        c = np.linalg.lstsq(M[sel], s[sel], rcond=None)[0]
        for _ in range(3):
            res = np.linalg.norm(s - M @ c, axis=2); keep = sel & (res < np.percentile(res[sel], 85))
            c = np.linalg.lstsq(M[keep], s[keep], rcond=None)[0]
        cs.append(c)
    return np.median(cs, axis=0)

def screen_field(kind, start, frames, box):
    x0, y0, x1, y1 = box
    if kind == 'quad':
        c = fit_quad_piece(start, frames)
        return (quad_basis(y1 - y0, x1 - x0, y0, x0) @ c).astype(np.float32)
    p = np.load(f'{W}/key/plate_half.npy')
    full = cv2.resize(p, (WD, H), interpolation=cv2.INTER_CUBIC)
    return np.ascontiguousarray(full[y0:y1, x0:x1]).astype(np.float32)

# ---------------------------------------------------------------- R2 body / arm matte (round3-key_v2.py maths)
def body_key(im, bg, prev_top=None):
    r, g, b = im.transpose(2, 0, 1)
    ex = np.maximum(g - np.maximum(r, b), 0); be = np.maximum(bg[:, :, 1] - np.maximum(bg[:, :, 0], bg[:, :, 2]), .08)
    a0 = np.clip(1 - ex / be, 0, 1)
    core = (a0 > .97).astype('uint8'); core = cv2.erode(core, np.ones((3, 3), np.uint8))
    # garbage matte: Dan is the large connected foreground; isolated screen spots / creases are not
    n, lab = cv2.connectedComponents(core, connectivity=8)
    if n > 1:
        sizes = np.bincount(lab.ravel()); sizes[0] = 0
        keep = sizes >= max(40000, 0.02 * sizes.max())
        core = keep[lab].astype('uint8')
    dist, inds = distance_transform_edt(1 - core, return_indices=True); near = im[inds[0], inds[1]]; delta = near - bg
    solved = np.sum((im - bg) * delta, axis=2) / np.maximum(np.sum(delta * delta, axis=2), .001)
    a = np.where((dist < 16) & (a0 < .995), solved, a0)
    a = np.clip((a - .055) / .92, 0, 1); a[dist >= 16] = 0
    a = cv2.ximgproc.guidedFilter(im, a, 2, .000015); a = np.clip(a, 0, 1)
    # hair top from real opaque foreground (v2), then the hair band; geometry scaled by S
    rows = np.where(core.sum(1) > 24 * S)[0]
    top = int(rows[0]) if len(rows) else (prev_top if prev_top is not None else 200)
    y = np.arange(im.shape[0])[:, None]
    hair = np.broadcast_to(np.clip((top + 470 * S - y) / (180 * S), 0, 1).astype(np.float32), a.shape)
    hair_a = np.clip((solved - .018) / .975, 0, 1); hair_a[dist >= 20] = 0
    hair_a = cv2.ximgproc.guidedFilter(im, hair_a, 3, .00004); hair_a = np.clip(hair_a, 0, 1)
    a = a * (1 - hair) + hair_a * hair
    return a.astype(np.float32), hair, top, near.astype(np.float32)

def foreground(im, a, bg):
    f = np.clip(im - (1 - a[:, :, None]) * bg, 0, a[:, :, None])
    f[:, :, 1] = np.minimum(f[:, :, 1], np.maximum(f[:, :, 0], f[:, :, 2]))
    return f

# ---------------------------------------------------------------- R3 fine hair (round3-key_v3.py maths)
def hair_key(im, bg):
    chroma = lambda x: x[:, :, 1] - .5 * (x[:, :, 0] + x[:, :, 2])
    bc = chroma(bg); ic = chroma(im)
    a0 = np.clip(1 - ic / np.maximum(bc, .08), 0, 1)
    core = (a0 > .98).astype(np.float32)
    sig = 22 * S
    den = cv2.GaussianBlur(core, (0, 0), sig)
    col = cv2.GaussianBlur(im * core[:, :, None], (0, 0), sig)
    near = (col + np.array([.105, .105, .095], np.float32) * .025) / (den[:, :, None] + .025)
    fc = chroma(near)
    a = np.clip((bc - ic) / np.maximum(bc - fc, .08), 0, 1)
    a = np.clip((a - .012) / .988, 0, 1)
    a = cv2.ximgproc.guidedFilter(im, a, 2, .000025); a = np.clip(a, 0, 1)
    d = distance_transform_edt(a0 < .7)
    a *= np.clip((75 * S - d) / (25 * S), 0, 1)
    gray = cv2.cvtColor((np.clip(im, 0, 1) * 255).astype('uint8'), cv2.COLOR_RGB2GRAY)
    return {'im': im, 'a': a.astype(np.float32), 'gray': gray, 'near': near}

FLOWS = {}                       # directed DIS flows by (frame, frame): each pair is needed by both frames' stabilizers
def _flow(maker, a, b):
    k = (a['n'], b['n'])
    if k not in FLOWS:
        FLOWS[k] = maker.calc(a['gray'], b['gray'], None)
    return FLOWS[k]

def align(other, cur, maker):
    h, w = cur['a'].shape; y, x = np.mgrid[:h, :w].astype(np.float32)
    flow = _flow(maker, cur, other)
    back = _flow(maker, other, cur)
    mx = x + flow[:, :, 0]; my = y + flow[:, :, 1]
    wa = cv2.remap(other['a'], mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wg = cv2.remap(other['gray'], mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(back, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    fb = np.linalg.norm(flow + wb, axis=2)
    cf = np.exp(-((wg.astype(np.float32) - cur['gray']) / 12) ** 2) * np.exp(-(fb / 1.5) ** 2)
    cf *= np.exp(-((wa - cur['a']) / .25) ** 2)
    return wa, cf

def stabilize(items, idx, maker):
    cur = items[idx]; acc = cur['a'].copy(); weights = np.ones_like(acc)
    for j in range(max(0, idx - 2), min(len(items), idx + 3)):
        if j == idx: continue
        a, c = align(items[j], cur, maker); c *= .85 if abs(j - idx) == 1 else .45
        acc += a * c; weights += c
    a = acc / weights
    blend = np.clip((1 - cur['a']) / .15, 0, 1)
    return cur['a'] * (1 - blend) + a * blend

def hair_premult(cur, a, bg):
    """round3-key_v3.composite() up to (not including) the grade and field: premultiplied hair foreground."""
    aa = a[:, :, None]; fg = np.clip(cur['im'] - (1 - aa) * bg, 0, aa)
    n = cur['near'].copy(); n[:, :, 1] = np.minimum(n[:, :, 1], .5 * (n[:, :, 0] + n[:, :, 2]))
    t = (1 - a) * .92
    fg = fg * (1 - t[:, :, None]) + n * aa * t[:, :, None]
    fg[:, :, 1] = np.minimum(fg[:, :, 1], np.maximum(fg[:, :, 0], fg[:, :, 2]))
    return fg

# ---------------------------------------------------------------- refinement (RO-24 'refined' variant, on top of the approved maths)
def refine(im, a, f, near_fallback, bg=None, hairband=None, motion=None):
    """Two residual flaws of the approved key, measured on C1726 (2026-10-20): (1) solid hair and forehead sit at alpha
    0.83-0.99 inside the head (19 % of interior head pixels below 0.99), so the background tints them (the grey halo Dan
    accepted on DS-40); (2) body and hand edges keep an olive outline where the despilled screen residue sits in the edge
    colour. Fix (1): deep inside the silhouette (9 px erosion of a > 0.5) alpha above 0.80 is lifted smoothly to 1; real
    gaps below 0.80 are untouched. Fix (2): every semitransparent pixel takes a continuous local foreground colour (the
    opaque core, Gaussian-normalised, sigma 6 px; the approved near colour where no core is close), weighted by its
    transparency. Fix (3): edge-band spill limit (below). Alpha shape outside the interior is unchanged."""
    F = f / np.maximum(a[:, :, None], 1e-4)
    inner = cv2.erode((a > .5).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    lift = np.clip((a - .80) / .15, 0, 1)
    a2 = np.where(inner, a + (1 - a) * lift, a).astype(np.float32)
    core = cv2.erode((a2 > .98).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
    den = cv2.GaussianBlur(core, (0, 0), 6)
    col = cv2.GaussianBlur(im * core[:, :, None], (0, 0), 6)
    eps = .02
    nearc = (col + near_fallback * eps) / (den[:, :, None] + eps)
    nearc[:, :, 1] = np.minimum(nearc[:, :, 1], np.maximum(nearc[:, :, 0], nearc[:, :, 2]))
    w = (np.clip((1 - a2) / .5, 0, 1) * .9)[:, :, None]
    F2 = F * (1 - w) + nearc * w
    # (3) green light wrapping onto OPAQUE skin at the silhouette (an olive line on arms and hands): inside a 14 px band
    # along the edge, green may not exceed the mean of red and blue (skin, hair, the tank and the watch all sit below it)
    d = distance_transform_edt(a2 > .02)
    wb = np.clip(1 - d / 14, 0, 1) * (a2 > .02)
    g_lim = np.minimum(F2[:, :, 1], .5 * (F2[:, :, 0] + F2[:, :, 2]) + .01)
    F2[:, :, 1] = F2[:, :, 1] * (1 - wb) + g_lim * wb
    if bg is not None:                                      # (4) moving hands
        a2, F2 = hands(im, a2, np.clip(F2, 0, 1), bg, hairband if hairband is not None else np.zeros_like(a2), motion)
    return a2, np.clip(F2, 0, 1) * a2[:, :, None]

# ---------------------------------------------------------------- moving hands (RO-24 refined, independent review F1/F2, 2026-10-20)
def hands(im, a, F, bg, hairband, motion=None):
    """Fast hand moves (independent review F1/F2, 2026-10-20, frames K2 423, 626-633, K3 168). The approved body key measures green
    as G - max(R, B); skin is red-heavy, so a 50/50 blur of skin and screen (R .52, G .50, B .32) still reads 0 green and counts
    as SOLID: the blurred hand edge and the screen seen through the gaps between fingers come out opaque and olive. Here, next
    to skin, each pixel's chromaticity (colour / its sum, so brightness and the screen's shadow between fingers drop out) is
    projected onto the line from the local skin colour to the screen colour: t = 0 skin, t = 1 screen. Only pixels that lie on
    that line (residual < 0.03: a real skin/screen mix, not the watch, the tank or a highlight) and read greener than the skin
    are changed, and alpha only goes DOWN (min with the approved alpha): a = (1-t)S_b / ((1-t)S_b + t S_f) with S the colour sums.
    Their colour becomes the local skin colour. Opaque skin, the tank, the watch and the hair band are untouched."""
    lum = lambda x: .2126 * x[..., 0] + .7152 * x[..., 1] + .0722 * x[..., 2]
    r, g, b = F[..., 0], F[..., 1], F[..., 2]
    opaque = a > .98
    skin = opaque & (r > g + .05) & (g > b) & (r - b > .10) & (lum(F) > .12)
    skin = cv2.erode(skin.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    if skin.sum() < 500: return a, F
    dark = opaque & (lum(F) < .12)
    d_sk = distance_transform_edt(~skin); d_dk = distance_transform_edt(~dark) if dark.any() else np.full(a.shape, 1e9, np.float32)
    sf = skin.astype(np.float32); den = cv2.GaussianBlur(sf, (0, 0), 12)
    Fs = cv2.GaussianBlur(F * sf[..., None], (0, 0), 12) / np.maximum(den[..., None], 1e-4)
    cs = lambda x: x / np.maximum(x.sum(-1, keepdims=True), 1e-3)
    ims = cv2.GaussianBlur(np.clip(im, 1e-4, 1), (0, 0), 1.2)       # chromaticity is noisy pixel to pixel; read it lightly smoothed
    ci, cf, cb = cs(ims), cs(Fs), cs(bg)
    dv = cb - cf; dd = np.maximum((dv * dv).sum(-1), 1e-6)
    t = ((ci - cf) * dv).sum(-1) / dd
    res = np.linalg.norm(ci - cf - t[..., None] * dv, axis=-1)
    t = np.clip(t, 0, 1)
    Sf, Sb = Fs.sum(-1), bg.sum(-1)
    ac = (1 - t) * Sb / np.maximum((1 - t) * Sb + t * Sf, 1e-4)
    ac = np.clip(cv2.ximgproc.guidedFilter(np.clip(im, 0, 1), ac.astype(np.float32), 3, .0002), 0, 1)
    zone = (d_sk < 40) & (d_sk <= d_dk) & (den > .02) & (hairband <= 0) & (res < .03) & (t > .06)
    wz = (np.clip((40 - d_sk) / 12, 0, 1) * np.clip((.03 - res) / .01, 0, 1) * np.clip((t - .06) / .06, 0, 1) * zone).astype(np.float32)
    wz = cv2.GaussianBlur(wz, (0, 0), 2.0)
    if motion is not None:          # only where something moved: green light bouncing onto a STILL arm reads like transparency too
        wz = wz * motion
    a3 = np.minimum(a, a * (1 - wz) + ac * wz)
    a3 = np.minimum(a, cv2.GaussianBlur(a3.astype(np.float32), (0, 0), .8))
    wF = np.clip((a - a3) / .25, 0, 1)[..., None]
    # colour from the NEAREST opaque skin (keeps its shading: a shaded inner arm stays shaded, no light rim), lightly smoothed
    _, ix = distance_transform_edt(~skin, return_indices=True)
    Fn = cv2.GaussianBlur(np.ascontiguousarray(F[ix[0], ix[1]]), (0, 0), 2.0)
    Fn[..., 1] = np.minimum(Fn[..., 1], .5 * (Fn[..., 0] + Fn[..., 2]) + .01)
    F3 = F * (1 - wF) + Fn * wF
    return a3.astype(np.float32), np.clip(F3, 0, 1).astype(np.float32)

# ---------------------------------------------------------------- piece renderer
def measure_box(start, frames):
    """Dan's extent over the piece at 1/8 scale (plus margins): processing box and a hair ROI."""
    xs0, xs1, tops, ys1 = [], [], [], []
    for i in list(range(0, frames, 15)) + [frames - 1]:
        raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{start + i / FPS:.4f}', '-i', SRC, '-frames:v', '1', '-an', '-vf',
                                       DEC.replace(',format=rgb48le', '') + ',scale=480:270,format=rgb48le', '-f', 'rawvideo', '-'])
        s = np.frombuffer(raw, '<u2').reshape(270, 480, 3).astype(np.float32) / 65535
        r, g, b = s.transpose(2, 0, 1); fg = (g - np.maximum(r, b)) < .06
        n, lab = cv2.connectedComponents(fg.astype('uint8'))
        sizes = np.bincount(lab.ravel()); sizes[0] = 0; fg = lab == sizes.argmax()
        cols = np.where(fg.any(0))[0]; rows = np.where(fg.any(1))[0]
        xs0.append(cols[0] * 8); xs1.append(cols[-1] * 8 + 8); tops.append(rows[0] * 8)
        hc = np.where(fg[rows[0]:rows[0] + 6].any(0))[0]
        ys1.append((hc[0] * 8, hc[-1] * 8 + 8))
    box = (max(0, min(xs0) - 220), 0, min(WD, max(xs1) + 220), H)
    hx0 = min(a for a, b in ys1); hx1 = max(b for a, b in ys1)
    cx = (hx0 + hx1) // 2; half = int(max(560 * S * 1.0, (hx1 - hx0) / 2 + 560 * S))
    roi = (max(box[0], cx - half), max(0, min(tops) - int(245 * S)), min(box[2], cx + half), min(H, max(tops) + int(655 * S) + 40))
    return box, roi, int(np.median(tops))

def encoder(path):
    # lossless, matrix-free: planar 16-bit RGB + alpha in FFV1 (no YUV round trip on the keyed foreground)
    return subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-s', f'{OUT_W}x{OUT_H}', '-r', '30000/1001',
                             '-i', '-', '-an', '-c:v', 'ffv1', '-level', '3', '-slices', '16', '-threads', '4', '-pix_fmt', 'gbrap16le',
                             str(path)], stdin=subprocess.PIPE)

def render(start, frames, out, screen='plate', box=None, roi=None, handles=2, log=None, variant='both'):
    cv2.setNumThreads(3)
    if box is None or roi is None:
        mb, mr, _ = measure_box(start, frames); box = box or mb; roi = roi or mr
    x0, y0, x1, y1 = box; rx0, ry0, rx1, ry1 = roi
    bg = screen_field(screen, start, frames, box)
    bgr = np.ascontiguousarray(bg[ry0 - y0:ry1 - y0, rx0 - x0:rx1 - x0])
    maker = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    flowbody = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    f0 = int(round(start * FPS))                 # frame-exact: frame f has pts f*1001/30000; seek 0.3 frame early
    lead = min(handles, f0)
    total = frames + lead + handles
    dec = subprocess.Popen([FF, '-v', 'error', '-ss', f'{(f0 - lead - 0.3) / FPS:.5f}', '-i', SRC, '-frames:v', str(total), '-an', '-vf', DEC,
                            '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    enc = encoder(out) if variant in ('approved', 'both') else None
    enc2 = encoder(out.replace('.mkv', '_refined.mkv')) if variant in ('refined', 'both') else None
    if enc is None: enc, enc2 = enc2, None; _refine_only = True
    else: _refine_only = False
    bh, bw = y1 - y0, x1 - x0
    sh, sw = bh // 2, bw // 2
    Ys, Xs = np.mgrid[:sh, :sw].astype(np.float32)
    cache = {}; nxt = 0; prev_top = None; stats = []; t = time.time(); got = 0
    def read(j):
        nonlocal prev_top, got
        raw = dec.stdout.read(H * WD * 6)
        if len(raw) < H * WD * 6:
            return None
        got += 1
        full = np.frombuffer(raw, '<u2').reshape(H, WD, 3)
        im = full[y0:y1, x0:x1].astype(np.float32) / 65535
        a, hair, top, near = body_key(im, bg, prev_top); prev_top = top
        gray = cv2.cvtColor((cv2.resize(np.clip(im, 0, 1), (sw, sh), interpolation=cv2.INTER_AREA) * 255).astype('uint8'), cv2.COLOR_RGB2GRAY)
        hh = hair_key(np.ascontiguousarray(im[ry0 - y0:ry1 - y0, rx0 - x0:rx1 - x0]), bgr); hh['n'] = j
        return dict(im=im, a=a, hair=hair, top=top, near=near, gray=gray, hh=hh)
    speed = {}
    def body_align(other, cur):
        flow = flowbody.calc(cur['gray'], other['gray'], None)
        m = np.linalg.norm(flow, axis=2); speed['m'] = m if 'm' not in speed else np.maximum(speed['m'], m)
        sa = cv2.resize(other['a'], (sw, sh), interpolation=cv2.INTER_AREA)
        wa = cv2.remap(sa, Xs + flow[:, :, 0], Ys + flow[:, :, 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wg = cv2.remap(other['gray'], Xs + flow[:, :, 0], Ys + flow[:, :, 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        return cv2.resize(wa, (bw, bh)), cv2.resize(np.exp(-((wg.astype(np.float32) - cur['gray']) / 14) ** 2), (bw, bh))
    tops = []; geo = []
    for i in range(total):
        lo = max(0, i - 2); hi = min(total, i + 3)
        while nxt < hi:
            it = read(nxt)
            if it is None:
                total = nxt; hi = min(hi, total); break
            cache[nxt] = it; nxt += 1
        if i >= total: break
        for j in list(cache):
            if j < lo: del cache[j]
        for k2 in [k2 for k2 in FLOWS if min(k2) < lo]: del FLOWS[k2]
        if i < lead or i >= lead + frames:
            continue
        cur = cache[i]
        # R2 temporal body smoothing inside the hair band (prev/next, flow-aligned, confidence-weighted)
        a = cur['a'].copy(); band = cur['hair'] > 0
        rows = np.where(band.any(1))[0]; rb = int(rows[-1]) + 1 if len(rows) else 0
        acc = a[:rb].copy(); weights = np.ones_like(acc)
        for j in (i - 1, i + 1):
            if j not in cache: continue
            wa, cf = body_align(cache[j], cur); wa, cf = wa[:rb], cf[:rb]
            cf *= np.clip(1 - abs(wa - a[:rb]) / .22, 0, 1) * .55; acc += cf * wa; weights += cf
        a[:rb] = a[:rb] * (1 - cur['hair'][:rb]) + (acc / weights) * cur['hair'][:rb]
        f = foreground(cur['im'], a, bg)
        blend = (1 - a[:rb]) * cur['hair'][:rb] * .8
        nn = cur['near'][:rb].copy(); nn[:, :, 1] = np.minimum(nn[:, :, 1], np.maximum(nn[:, :, 0], nn[:, :, 2]))
        f[:rb] = f[:rb] * (1 - blend[:, :, None]) + nn * a[:rb, :, None] * blend[:, :, None]
        # R3 five-frame hair in the ROI, handed over above the forehead (rows relative to this frame's hair top)
        items = [cache[j]['hh'] for j in range(lo, hi)]
        ah = stabilize(items, i - lo, maker)
        fh = hair_premult(cur['hh'], ah, bgr)
        tops.append(cur['top']); top_s = int(np.median(tops[-9:]))
        yy = np.arange(ry0, ry1, dtype=np.float32)[:, None] - y0
        full_above = top_s + 315 * S; ho = np.clip((full_above + 160 * S - yy) / (160 * S), 0, 1)
        ho = np.broadcast_to(ho, ah.shape)[:, :, None]
        sy, sx = slice(ry0 - y0, ry1 - y0), slice(rx0 - x0, rx1 - x0)
        a[sy, sx] = a[sy, sx] * (1 - ho[:, :, 0]) + ah * ho[:, :, 0]
        f[sy, sx] = f[sy, sx] * (1 - ho) + fh * ho
        # into the full frame, then the 2880x1620 intermediate (premultiplied downscale, then unpremultiply)
        sc = OUT_W / WD
        X0, Y0 = int(round(x0 * sc)), int(round(y0 * sc)); X1, Y1 = int(round(x1 * sc)), int(round(y1 * sc))
        nf = np.where(cur['hair'][:, :, None] > 0, np.array([.105, .105, .095], np.float32), cur['near'])
        # how fast each pixel moved to the neighbouring frames (DIS flow at half res, from the body smoothing above; same take only):
        # motion blur is only wide enough to matter above ~2.5 half-res px a frame (~5 native px); a sway of a pixel or two is not
        mv = speed.pop('m', np.zeros(cur['gray'].shape, np.float32))
        mv = cv2.dilate(cv2.GaussianBlur(mv, (0, 0), 3), np.ones((15, 15), np.uint8))
        motion = cv2.resize(np.clip((mv - 2.5) / 3, 0, 1), (bw, bh), interpolation=cv2.INTER_LINEAR)
        if _refine_only: variants = [(enc,) + refine(cur['im'], a, f, nf, bg, cur['hair'], motion)]
        else: variants = [(enc, a, f)] + ([(enc2,) + refine(cur['im'], a, f, nf, bg, cur['hair'], motion)] if enc2 is not None else [])
        for e, av, fv in variants:
            fs = cv2.resize(fv, (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_AREA)
            as_ = np.clip(cv2.resize(av, (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_AREA), 0, 1)
            Fo = np.zeros((OUT_H, OUT_W, 3), np.float32); Ao = np.zeros((OUT_H, OUT_W), np.float32)
            Fo[Y0:Y1, X0:X1] = np.clip(fs / np.maximum(as_[:, :, None], 1e-4), 0, 1) * (as_[:, :, None] > 1e-4)
            Ao[Y0:Y1, X0:X1] = as_
            rgba = np.concatenate([Fo, Ao[:, :, None]], 2)
            e.stdin.write((rgba * 65535 + .5).astype('<u2').tobytes())
        k = i - lead
        # per-frame head geometry in the 2880 intermediate (hair top = first row with >= 3 px of alpha > 0.35)
        rr = np.where((Ao > .35).sum(1) >= 3)[0]; htop = int(rr[0]) if len(rr) else -1
        band = Ao[max(htop, 0):max(htop, 0) + 260] > .5; cols = np.where(band.any(0))[0]
        geo.append([k, htop, int((cols[0] + cols[-1]) // 2) if len(cols) else -1, int(cols[0]) if len(cols) else -1, int(cols[-1]) if len(cols) else -1])
        if k % 30 == 0:
            stats.append({'frame': k, 'hair_top': int(cur['top']), 'sec': round(time.time() - t, 1)})
            print(out.split('/')[-1], k, frames, round(time.time() - t, 1), flush=True)
    enc.stdin.close(); assert enc.wait() == 0
    if enc2 is not None: enc2.stdin.close(); assert enc2.wait() == 0
    dec.stdout.close(); dec.wait()
    meta = {'src': SRC, 'start': start, 'f0': f0, 'frames': frames, 'screen': screen, 'box': box, 'roi': roi, 'S': S, 'variant': variant, 'stats': stats, 'geo': geo,
            'seconds': round(time.time() - t, 1)}
    json.dump(meta, open(out + '.json', 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    print('KEY DONE', out, meta['seconds'], flush=True)
    return meta

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('start', type=float); ap.add_argument('frames', type=int); ap.add_argument('out')
    ap.add_argument('--screen', default='plate'); ap.add_argument('--box'); ap.add_argument('--roi'); ap.add_argument('--variant', default='both')
    A = ap.parse_args()
    pb = lambda s: tuple(int(v) for v in s.split(',')) if s else None
    render(A.start, A.frames, A.out, A.screen, pb(A.box), pb(A.roi), variant=A.variant)
