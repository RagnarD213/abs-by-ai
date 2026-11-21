#!/usr/bin/env python3
"""THE PICTURE for the Ad 3 vertical: a Python frame compositor on HIS 29.97 fps grid (frame n here == frame n of
Muhammad's v6 HD). Built on render5.py (Ad 5), with Ad 3's beat kinds:
  talk       the conform through crop.json (hair-anchored NEAR/FAR, torso/head track)
  window     Dan above in a full-width window, his text-left screen below: body 'blocks' (bullets that blur in, block
             swaps) or 'phone' (his app screenshot scrolling on HIS measured offsets)
  card       a still in his olive card (blur-in, slow push, optional AI chip)
  cardv      a 16:9 clip in his olive card: a lift from his render at his frames, or a library clip on a time map
  bleedv     a NATIVE 9:16 AI clip filling the frame on his time map, the big low AI chip, a caption scrim
  phonecard  a phone in his olive card: a png on his scroll offsets, a recording on his time map, or a still
  photoseq   his rapid photo-shoot stills on the field
Per-frame state is Python (skill A6.9); every cache is keyed on content; the frame count is asserted.
  python3 render3.py [--from N --to M] [--out picture.mp4] [--preview]
  python3 render3.py --stills 100,200,300 --dir stills
  python3 render3.py --cutplan cut_plan.json --out cut/picture.mp4"""
import json, os, subprocess, sys, numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g3 as G, beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FP = FF.replace('ffmpeg', 'ffprobe')
VW, VH, FPS, NTOT = 1080, 1920, B.FPS, B.NTOT
args = sys.argv[1:]
def arg(k, d): return args[args.index(k)+1] if k in args else d
N0, N1 = int(arg('--from', 0)), int(arg('--to', NTOT))
OUT = arg('--out', 'picture.mp4'); PREVIEW = '--preview' in args
tl, ov = B.timeline()
CROP = {int(k): v for k, v in json.load(open('crop.json'))['frames'].items()} if os.path.exists('crop.json') else {}
FLASH = B.FLASH

# ------------------------------------------------------------------ readers
READERS = []
def close_media_readers(keep):
    for r in list(READERS):
        if r is not keep: r.close(); READERS.remove(r)

def _probe(path):
    o = subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height,r_frame_rate',
                        '-of', 'csv=p=0:s=x', path], capture_output=True, text=True).stdout.strip().split('\n')[0].split('x')
    nu, de = map(int, o[2].split('/')); return int(o[0]), int(o[1]), nu/de

def _vf(w, h, cover, crop):
    vf = ['format=rgb24']                      # rgb first: an odd crop is never rounded by chroma subsampling (A7.3)
    if crop: vf.append(f'crop=iw*{crop[2]-crop[0]:.4f}:ih*{crop[3]-crop[1]:.4f}:iw*{crop[0]:.4f}:ih*{crop[1]:.4f}')
    if w and cover: vf.append(f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h}")
    elif w: vf.append(f'scale={w}:{h}:flags=lanczos')
    vf.append('scale=in_color_matrix=bt709:in_range=tv')
    return vf

class Reader:
    """Sequential RGB frames at 29.97 (a lift from his render, or the base), optional cover size / crop / rate."""
    def __init__(self, path, w=None, h=None, ss=0.0, cover=False, crop=None, rate=1.0):
        READERS.append(self); self.path = path
        vf = _vf(w, h, cover, crop)
        vf.insert(1, f'fps={FPS:.6f}')
        if rate != 1.0: vf.insert(1, f'setpts=PTS*{rate:.5f}')
        sw, sh, _ = _probe(path); self.w, self.h = (w, h) if w else (sw, sh)
        self.p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-ss', f'{ss:.4f}', '-i', path, '-vf', ','.join(vf),
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
        self.last = None
    def read(self):
        b = self.p.stdout.read(self.w*self.h*3)
        if len(b) == self.w*self.h*3: self.last = np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3)
        elif len(b) not in (0,): raise RuntimeError(f'short raw frame from {self.path}: {len(b)} bytes')
        return self.last                                   # past the end: hold the last frame (never loop)
    def close(self):
        try: self.p.kill()
        except Exception: pass

class NativeReader:
    """A clip at its OWN frame rate, read forward to any native index j (his time maps retime and cut the clip)."""
    def __init__(self, path, w, h, cover=True, crop=None):
        READERS.append(self); self.path, self.w, self.h, self.cover, self.crop = path, w, h, cover, crop
        self.fps = _probe(path)[2]; self._open(0)
    def _open(self, j0):
        self.p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-ss', f'{j0/self.fps:.4f}', '-i', self.path, '-vf',
                                   ','.join(_vf(self.w, self.h, self.cover, self.crop)), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                  stdout=subprocess.PIPE, bufsize=10**8)
        self.idx = j0 - 1; self.last = None
    def get(self, j):
        j = max(0, int(j))
        if j < self.idx: self.close(); self._open(j)
        while self.idx < j:
            b = self.p.stdout.read(self.w*self.h*3)
            if len(b) < self.w*self.h*3: break
            self.last = np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3); self.idx += 1
        return self.last
    def close(self):
        try: self.p.kill()
        except Exception: pass

def still(path): return ImageOps.exif_transpose(Image.open(path)).convert('RGB')

# ------------------------------------------------------------------ his time maps
def tmap_t(M, n, fps_src=None):
    """source time at his frame n from matched samples [(n, t, score)]: interpolate between neighbours that belong to the
    same shot (slope 0.4-2.5 src s per his s), else step from the nearer one at the median slope."""
    S = [(a, t) for a, t, sc in M if sc is not None and sc > 0.55]
    if not S: raise ValueError('empty time map')
    ns = np.array([a for a, _ in S]); ts = np.array([t for _, t in S])
    sl = np.diff(ts)/np.maximum(np.diff(ns)/FPS, 1e-6); good = sl[(sl > 0.4) & (sl < 2.5)]
    med = float(np.median(good)) if len(good) else 1.0
    i = int(np.searchsorted(ns, n))
    if i < len(ns) and ns[i] == n: return float(ts[i])
    if 0 < i < len(ns):
        s = (ts[i]-ts[i-1])/((ns[i]-ns[i-1])/FPS)
        if 0.0 <= s < 2.5: return float(ts[i-1] + (n-ns[i-1])/FPS*s)   # slope 0 = HIS HELD FRAME: hold it (0.4 here extrapolated +1 source frame on every odd frame -> flicker across the clip's own cut, 82.2 s)
        k = i-1 if n - ns[i-1] <= ns[i] - n else i
        return float(ts[k] + (n-ns[k])/FPS*med)
    k = 0 if i == 0 else len(ns)-1
    return float(ts[k] + (n-ns[k])/FPS*med)

# ------------------------------------------------------------------ helpers
def warp_crop(img, x0, y0, w, h, W=VW, H=VH, interp=cv2.INTER_LANCZOS4):
    sx, sy = W/w, H/h
    M = np.float32([[sx, 0, -x0*sx], [0, sy, -y0*sy]])
    return cv2.warpAffine(img, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)
def unsharp(img, amount=0.7, sigma=1.2):
    b = cv2.GaussianBlur(img, (0, 0), sigma); return cv2.addWeighted(img, 1+amount, b, -amount, 0)
# ⚠ FINAL COLOUR TRIM, AFTER THE UNSHARP (zgrade4.py, fitted on the DELIVERED render 10 against his file read as BT.709).
# The unsharp raises local contrast after every colour stage: render 10 read saturation 0.436 vs his 0.414 and shadows p5
# 9 vs 12. Only Dan's picture (talk + window) passes through here -- graphics and captions are composed afterwards.
_FINAL = json.load(open('grade_final.json')) if os.path.exists('grade_final.json') else None
_FLUT = [np.array(c, np.uint8) for c in _FINAL['curves']] if _FINAL else None
_LW = np.array([0.2126, 0.7152, 0.0722], np.float32)
def final_trim(img):
    if _FINAL is None: return img
    x = np.dstack([cv2.LUT(img[..., c], _FLUT[c]) for c in range(3)]).astype(np.float32)
    L = (x @ _LW)[..., None]
    return np.clip(L + _FINAL['sat']*(x - L) + 0.5, 0, 255).astype(np.uint8)
def compose(base_rgb, rgba):
    bb = rgba.getchannel('A').getbbox()
    if not bb: return base_rgb
    x0, y0, x1, y1 = bb
    o = np.asarray(rgba.crop(bb), dtype=np.uint16); a = o[..., 3:4]
    r = base_rgb[y0:y1, x0:x1].astype(np.uint16)
    base_rgb[y0:y1, x0:x1] = ((r*(255-a) + o[..., :3]*a + 127)//255).astype(np.uint8)
    return base_rgb
def push_cover(pil, i, n, w, h, ox=0.5, oy=0.5, amt=0.05):
    k = i/max(1, n-1); z = 1.0 + amt*k
    W0, H0 = pil.size; s = max(w/W0, h/H0)*z; cw, ch = w/s, h/s
    return warp_crop(np.asarray(pil), (W0-cw)*ox, (H0-ch)*oy, cw, ch, w, h)
def blur_in(arr, t, dur=0.40, top=22):
    s = top*(1 - G.ease_out_cubic(G.clamp01(t/dur)))
    return cv2.GaussianBlur(arr, (0, 0), s) if s > 0.4 else arr
def field_np(): return np.asarray(G.field()).copy()
def slow_push(arr, i, n, amt=0.025):
    z = 1.0 + amt*(i/max(1, n-1)); H, W = arr.shape[:2]; cw, ch = W/z, H/z
    return warp_crop(arr, (W-cw)/2, (H-ch)/2, cw, ch, W, H, cv2.INTER_LINEAR)

_VIG = None
def vignette(f, n=None):
    global _VIG
    if _VIG is None:
        V = json.load(open('vignette.json')); rr = [v[0] for v in V]; gg = [v[1] for v in V]
        ys, xs = np.mgrid[0:1080, 0:1920]; rad = np.hypot((xs-960)/960, (ys-540)/540)
        _VIG = np.clip(np.interp(rad, rr, gg), 0.3, 1.05).astype(np.float32)[..., None]
    out = np.clip(f.astype(np.float32)*_VIG + 0.5, 0, 255).astype(np.uint8)
    # ⚠ HIS GRADE AS A PLAYER SHOWS IT (2026-09-13). Dan rejected render 9's colour side by side in VLC: "Muhammad's look
    # brighter, like the colors are more vivid. I look more tan." His file has NO colour tags; ffmpeg reads untagged video
    # with the BT.601 matrix, VLC and browsers read untagged HD as BT.709, and the grade had been fitted to the 601 reading.
    # zlut.py now reads BT.709, and zgrade2.py --post matches each channel's distribution to his, over the pixels inside our
    # vertical crop, AFTER this vignette (correcting before it cannot lift a highlight the vignette then darkens).
    if _CURVES is not None:
        out = np.stack([_CURVES[c][out[..., c]] for c in range(3)], -1)
    # ...then his grade SECTION BY SECTION (zgrade3.py): his opening 0-43 s is warmer than the rest of his ad (skin R-G
    # 58-60 against 52-54 elsewhere), which one global table cannot follow. A 3x3 colour transfer per EDL segment,
    # smoothed over 5 s and interpolated per frame, so no join can pop colour.
    if _SEG is not None and n is not None:
        A, t = _seg_at(n)
        out = np.clip(out.astype(np.float32) @ A.T + t + 0.5, 0, 255).astype(np.uint8)
    return out
_SEG = None
if os.path.exists('grade_seg.json'):
    _SEG = np.array(json.load(open('grade_seg.json'))['keys'], dtype=np.float64)
def _seg_at(n):
    ks = _SEG[:, 0]
    if n <= ks[0]: p = _SEG[0, 1:]
    elif n >= ks[-1]: p = _SEG[-1, 1:]
    else:
        j = int(np.searchsorted(ks, n)); a = (n - ks[j-1])/(ks[j] - ks[j-1]); p = _SEG[j-1, 1:]*(1-a) + _SEG[j, 1:]*a
    return p[:9].reshape(3, 3).astype(np.float32), p[9:].astype(np.float32)
LABEL_PLACE = json.load(open('label_place.json')) if os.path.exists('label_place.json') else {}
_CURVES = None
if os.path.exists('grade_post.json'):
    _CURVES = np.array(json.load(open('grade_post.json'))['curves'], dtype=np.uint8)
WIN_PAD = 90            # source rows of headroom added above the frame (see below)


def window_src(f, c, win_h, pad=WIN_PAD):
    """Dan inside a window, with HEADROOM.

    The window box is nearly the source's own aspect, so filling it from y=0 shows the whole frame -- and in the
    whole frame his hair top sits only 15-100 px down (measure.json), which put his hair 12-35 px under the
    window's rounded top edge and held the assessment window at 12-25 px for 12 s (independent audit, 2026-09-11,
    item 12). The talk crops anchor to the hair and give 29-70 px; the window ignored the anchor entirely.

    Take the source rect from y = -pad instead. warpAffine's BORDER_REPLICATE extends row 0 upward -- the same
    trick the opening hold already uses (zcrop Y0_EXTEND) -- and the rect widens to keep the box's aspect, which
    also shrinks him slightly. `pad` is capped so the widened rect still fits inside the 1920-px frame.
    """
    pad = int(max(0, min(pad, 1920.0*win_h/VW - 1080)))
    hs = 1080.0 + pad
    ws = hs*VW/win_h
    x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, max(0.0, 1920 - ws)))
    return final_trim(unsharp(warp_crop(f, x0c, -pad, ws, hs, VW, win_h), 0.5))

# ------------------------------------------------------------------ beat renderers
def r_talk(b, base):
    for n in range(b['n0'], b['n1']):
        # a default crop ONLY for graphics test stills before crop.json exists; once it exists a missing frame raises
        f = base(n); x0, y0, w, h = CROP[n] if CROP else [656, 0, 576, 1024]
        yield final_trim(unsharp(warp_crop(f, x0, y0, w, h)))

def _mono_offsets(offs):
    """zmatch3 scroll entries: (n, offset, box, score) -> the samples that describe ONE FORWARD SCROLL.

    A phone screen scrolls one way. So the honest filter is not the match score, it is MONOTONICITY: keep the
    longest non-decreasing run of offsets and drop what cannot belong to it. That removes the workout phone's
    first sample (6834, offset 1265 at score 0.246, against ~51 for its neighbours) which held the screenshot at
    its BOTTOM for 14 frames and then snapped to the top (audit 1, item 8).

    ⚠ Do NOT filter on the score instead. That was tried, and the scores decay along every one of these scrolls
    (they fall below 0.55 after 22 / 16 / 12 frames): dropping them stranded the interpolation on its last kept
    sample and FROZE all three phones -- the assessment screen for 347 frames, 11.6 s, where his keeps moving
    (audit 2, item 5). One bad sample became three dead screens.
    """
    P = [(r[0], r[1]) for r in offs if r[1] is not None]
    if len(P) < 3: return P
    best, cur = [], []
    for i, (n, o) in enumerate(P):
        if cur and o < cur[-1][1] - 2:                     # a step backwards: this run ends here
            if len(cur) > len(best): best = cur
            cur = []
        cur.append((n, o))
    if len(cur) > len(best): best = cur
    if len(best) < 3: return P
    # ...and drop a LEAP. The assessment phone's last sample reads 1533 px where the 41 before it all read 651 --
    # his screen has stopped and held for 3.7 s. Kept, it snapped the screen 354 px in the final three frames.
    steps = [abs(best[i+1][1] - best[i][1]) for i in range(len(best)-1)]
    if steps:
        med = float(np.median([s for s in steps if s > 0]) or 1.0)
        out = [best[0]]
        for (n, o) in best[1:]:
            if abs(o - out[-1][1]) > max(40.0, 12*med): continue
            out.append((n, o))
        if len(out) >= 3: best = out
    return best


def _off_series(offs, n0, n1, cap):
    """Every offset the beat needs, as a dict, fitted ONCE so the scroll fills the beat and the asset exactly.

    Two separate failures made these phones stand still, and both are fixed here rather than per frame:
      * the samples stop before the beat does (33 frames early on the workout phone), and
      * his screen scrolls further than our screenshot has content for (1533 px measured against 617 available).
    So: filter to one forward scroll, extend at the trailing rate to the beat's last frame, then scale the whole
    thing so its end lands exactly on the asset's last row. Where his screen genuinely stops -- the assessment
    phone holds a flat 651 px for its final 3.7 s -- the trailing rate is zero and it still stops."""
    P = _mono_offsets(offs)
    if len(P) < 2: return {n: (P[0][1] if P else 0.0) for n in range(n0, n1)}
    xs = [a for a, _ in P]; ys = [o for _, o in P]
    tail = P[-min(8, len(P)):]
    span = tail[-1][0] - tail[0][0]
    rate = (tail[-1][1] - tail[0][1])/span if span else 0.0
    def raw(n):
        if n > xs[-1]: return ys[-1] + rate*(n - xs[-1])
        return float(np.interp(n, xs, ys))
    lo = min(ys[0], raw(n0)); hi = max(raw(n1-1), max(ys))
    k = (cap - lo)/(hi - lo) if (cap is not None and hi > lo and hi > cap) else 1.0
    return {n: float(min(max(lo + (raw(n) - lo)*k, 0.0), cap if cap is not None else 1e9)) for n in range(n0, n1)}


def _interp_off(offs, n, cap=None):
    """cap: the furthest this screenshot can scroll (its height minus the visible strip).

    His assessment phone scrolls further than our screenshot has content for -- the measured offsets run to 1533 px
    against a 617 px limit -- so clamping at the limit froze the phone for the last 150 frames (5 s). COMPRESS the
    whole scroll into what the asset has instead: it keeps moving for the full beat, at a slightly slower rate than
    his, which is invisible, where a dead screen is not."""
    P = _mono_offsets(offs)
    ys = [o for _, o in P]
    if cap is not None and ys and max(ys) > cap > 0:
        lo = min(ys); k = (cap - lo)/(max(ys) - lo) if max(ys) > lo else 1.0
        P = [(a, lo + (o - lo)*k) for a, o in P]
    # PAST the last sample, keep going at the rate it was going. The matcher's samples stop 33 frames before the
    # workout phone's beat ends and 17 before the second one's; holding the last value froze those screens for the
    # last second (audit 2, item 5). Where his screen has genuinely STOPPED the trailing rate is ~0, so this holds
    # by itself -- the assessment phone reads a flat 651 px for its last 3.7 s and stays flat.
    if n > P[-1][0] and len(P) >= 4:
        tail = P[-min(8, len(P)):]
        span = tail[-1][0] - tail[0][0]
        rate = (tail[-1][1] - tail[0][1])/span if span else 0.0
        v = P[-1][1] + rate*(n - P[-1][0])
        return float(min(v, cap) if cap is not None else v)
    return float(np.interp(n, [a for a, _ in P], [o for _, o in P]))

def r_window(b, base):
    body = b['body']; n = b['n1']-b['n0']
    if body == 'blocks':
        blocks = [dict(t0=(bl['n'] - b['n0'])/FPS, items=[dict(it, t=(it['n'] - b['n0'])/FPS) for it in bl['items']])
                  for bl in b['blocks']]
        fn, th = G.blocks_body(blocks); rect = G.window_rect(th)
    elif body == 'phone':
        rect = (0, 60, VW, 720); png = still(b['media']); offs = b['offsets']
        _mh, _mw = 878, 404
        OFFS = _off_series(offs, b['n0'], b['n1'], png.height - int(png.width*_mh/_mw))
    else: raise ValueError(body)
    win_h = rect[3]-rect[1]; cache = {}
    for i in range(n):
        t = i/FPS; nn = b['n0']+i
        f = base(nn); c = CROP.get(nn, [656, 0, 608, 1080])
        out = field_np()
        if body == 'blocks':
            sk = fn.settled_key(t) if t >= 0.42 else None
            key = ('s', sk) if sk is not None else ('t', round(t, 4))
            if key not in cache:
                if len(cache) > 40: cache.clear()          # memory: a full-frame RGBA plate is 8.3 MB
                cache[key] = G.window_plate(rect, t, lambda d, im, tt, ty: fn(d, im, tt, ty), in_dur=0.42)
            plate = cache[key]
        else:
            plate = G.window_plate(rect, t, in_dur=0.30, grow=0.03)
            k = G.ease_out_back(G.clamp01(t/0.42)); mh, mw = 878, 404
            sh_ = int(png.width*mh/mw); off = OFFS[nn]
            scr = png.crop((0, int(off), png.width, int(off) + sh_))
            phone = G.phone_frame(scr, mw, notch=False)
            hy0 = 762; hw2, hh2 = int(phone.width*(0.94+0.06*k)), int(phone.height*(0.94+0.06*k))
            G.rrect(plate, [VW//2-hw2//2-16, hy0-12, VW//2+hw2//2+16, hy0+hh2+12], 30, fill=G.CARD_OL+(255,), glow=22)
            plate.alpha_composite(phone.resize((hw2, hh2), Image.LANCZOS), (VW//2-hw2//2, hy0))
        out[rect[1]:rect[3]] = window_src(f, c, win_h)
        yield compose(out, plate)

def r_card(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    hole = G.card_hole(b.get('ar') or pil.width/pil.height, has_text=False)
    hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    for i in range(n):
        t = i/FPS
        m = push_cover(pil, i, n, hw, hh, b.get('ox', 0.5), b.get('oy', 0.5), 0.05)
        if b.get('blur'): m = blur_in(m, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = m
        pl = G.card_plate(hole, t)
        if b.get('label'): G.ai_chip(pl, hole[2]-18, hole[3]-12)
        yield compose(out, pl)

def r_cardv(b, base):
    n = b['n1']-b['n0']; hole = G.card_hole(b.get('ar', 16/9)); hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    if b.get('tmap'):                                       # library clips on his time map: [(n, name, t, score)]
        rds = {k: NativeReader(p, hw, hh, cover=True, crop=b.get('crop')) for k, p in b['srcs'].items()}
        M = b['tmap']
    else:
        rd = Reader(b['media'], hw, hh, ss=b.get('ss', 0)/FPS, cover=True, crop=b.get('crop'), rate=b.get('rate', 1.0))
    for i in range(n):
        t = i/FPS; nn = b['n0']+i
        if b.get('tmap'):
            near = min(M, key=lambda r: abs(r[0]-nn)); name = near[1]
            sub = [(a, tt, sc) for a, nm, tt, sc in M if nm == name]
            m = rds[name].get(round(tmap_t(sub, nn)*rds[name].fps))
        else: m = rd.read()
        if b.get('blur'): m = blur_in(m, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = unsharp(m, 0.3)
        pl = G.card_plate(hole, t)
        if b.get('label'): G.ai_chip(pl, hole[2]-18, hole[3]-12)
        yield compose(out, pl)

def r_bleedv(b, base):
    n = b['n1']-b['n0']; rd = NativeReader(b['media'], VW, VH, cover=True); M = b['tmap']
    chip = G.blank(); G.ai_chip_low(chip, cy=b.get('chip_y', 1240)); last_j = -1
    for i in range(n):
        nn = b['n0']+i
        j = max(round(tmap_t(M, nn)*rd.fps), last_j); last_j = j                  # never backwards
        fr = unsharp(rd.get(j).copy(), 0.25)
        if b.get('blur'): fr = blur_in(fr, i/FPS, dur=b.get('blur_dur', 0.30), top=b.get('blur_top', 16))
        yield compose(fr, chip)

def r_phonecard(b, base):
    n = b['n1']-b['n0']; hole = (120, 150, 960, 1330)
    PW = 500
    if b['src'] == 'png':
        png = still(b['media']); offs = b['offsets']
        OFFS = _off_series(offs, b['n0'], b['n1'], png.height - int(png.width*19.5/9))
    elif b['src'] == 'video': rd = NativeReader(b['media'], 886, 1920, cover=True); M = b['tmap']; last_j = -1
    else: img = still(b['media'])
    for i in range(n):
        t = i/FPS; nn = b['n0']+i
        if b['src'] == 'png':
            sh_ = int(png.width*19.5/9); off = OFFS[nn]
            scr = png.crop((0, int(off), png.width, int(off) + sh_))
        elif b['src'] == 'video':
            j = max(round(tmap_t(M, nn)*rd.fps), last_j); last_j = j
            scr = Image.fromarray(rd.get(j))
        else: scr = img
        phone = G.phone_frame(scr, PW, notch=False)
        z = 1.0 + 0.03*(i/max(1, n-1)); pw, ph = int(phone.width*z), int(phone.height*z)
        phone = phone.resize((pw, ph), Image.LANCZOS)
        if b.get('chip'):                                    # his AI-GENERATED tag on the goal picture inside the phone
            cx0, cy0, cx1, cy1 = b['chip']                    # fractions of the phone image
            G.ai_chip(phone, int(pw*cx1), int(ph*cy1), size=int(30*z))
        inner = Image.new('RGB', (hole[2]-hole[0], hole[3]-hole[1]), G.CARD_OL)
        inner.paste(phone, ((inner.width-pw)//2, (inner.height-ph)//2), phone)
        arr = np.asarray(inner).copy()
        if b.get('blur'): arr = blur_in(arr, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = arr
        yield compose(out, G.card_plate(hole, t))

def r_photoseq(b, base):
    """His rapid stills on the field. `pop=(n0, n1, scale)` reproduces the POP-ZOOM he puts on the last one:
    his flag still grows 1487 -> 1678 px over three frames (4881-4883) and holds into his flash. Ours was flat
    (audit 2026-09-11, item 18)."""
    cache = {}; pop = b.get('pop')
    BOX = (60, 170, VW-60, 1330)
    for i in range(b['n1']-b['n0']):
        nn = b['n0']+i; cur = [p for s, p in b['stills'] if s <= nn][-1]
        z = 1.0
        if pop and nn >= pop[0]:
            z = 1.0 + (pop[2]-1.0)*min(1.0, (nn-pop[0])/max(1, pop[1]-pop[0]))
        key = (cur, round(z, 4))
        if key not in cache:
            if len(cache) > 12: cache.clear()
            box = BOX
            if z != 1.0:
                cx, cy = (BOX[0]+BOX[2])/2, (BOX[1]+BOX[3])/2
                hw, hh = (BOX[2]-BOX[0])/2*z, (BOX[3]-BOX[1])/2*z
                box = (int(cx-hw), int(cy-hh), int(cx+hw), int(cy+hh))
            # every one of these four is a REAL photo-shoot after picture of Dan -> the standing label (AGENTS.md, 09-11)
            # placement OFF HIS BODY, measured per still by zlabelplace.py (Dan's 09-12 rule: never over face or abs)
            lab = LABEL_PLACE.get(os.path.basename(cur))
            assert lab is not None, f'no measured label placement for {cur} -- run zlabelplace.py'
            cache[key] = np.asarray(G.photo_on_field(still(cur), box=box, real_label=True, label=lab))
        yield cache[key].copy()

R = dict(talk=r_talk, window=r_window, card=r_card, cardv=r_cardv, bleedv=r_bleedv, phonecard=r_phonecard, photoseq=r_photoseq)

# ------------------------------------------------------------------ overlays
_OVC = {}
def overlay_img(o, n):
    t = (n - o['n0'])/FPS; dur = (o['n1'] - o['n0'])/FPS
    settle = (G.LT_LEAD + G.LT_STAGGER*(len(o.get('lines', [])) - 1) + G.LT_SPAN + 0.05) if o['kind'] == 'lt' else 0.45   # every line typed (A6.19a)
    key = (id(o), round(t, 3) if (t < settle or t > dur - 0.35) else 'settled')
    if key in _OVC: return _OVC[key]
    if o['kind'] == 'lt': im = G.lower_third(o['lines'], t, dur, y_bottom=o.get('y_bottom', 1600), num=o.get('num'))
    elif o['kind'] == 'pill': im = G.cta_pill(o['top'], o['big'], t, dur)
    else: raise ValueError(o['kind'])
    if len(_OVC) > 60: _OVC.clear()               # memory: 400 full-frame overlays was ~3.3 GB (encoder killed 2026-09-11)
    _OVC[key] = im
    return im

# ------------------------------------------------------------------ captions (the gated layout: captions.py)
def caption_schedule(path='cap/list.txt'):
    L = [l.strip() for l in open(path)]; out, t = [], 0.0
    for a, bb in zip(L[0::2], L[1::2]):
        if not a.startswith('file') or not bb.startswith('duration'): continue
        p = a.split("'")[1]; d = float(bb.split()[1]); out.append((t, t+d, p)); t += d
    return out
CAPS = caption_schedule() if os.path.exists('cap/list.txt') else []
_CAPC = {}
def caption_at(n):
    t = (n + 0.5)/FPS
    for a, bb, p in CAPS:
        if a <= t < bb:
            if p.endswith('_blank.png'): return None
            if p not in _CAPC:
                if len(_CAPC) > 32: _CAPC.clear()
                _CAPC[p] = Image.open(p).convert('RGBA')
            return _CAPC[p]
    return None
_y = np.arange(VH, dtype=np.float32)
SCRIM = np.clip(np.minimum((_y - 1230)/140, (1640 - _y)/120), 0, 1)[:, None, None]*0.62     # soft dark band under the captions
SCRIM_N = {n for bb in tl if bb.get('scrim') for n in range(bb['n0'], bb['n1'])}

def finish(fr, n, ovs, capn):
    fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
    for o in ovs:
        if o['n0'] <= n < o['n1']: fr = compose(fr, overlay_img(o, n))
    c = caption_at(capn)
    if c is not None:
        if n in SCRIM_N: fr = (fr.astype(np.float32)*(1 - SCRIM)).astype(np.uint8)
        fr = compose(fr, c)
    if n in FLASH: fr = G.flash(fr, FLASH[n])
    return fr

def encoder(out, w=VW, h=VH, preview=False):
    return subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}',
                             '-r', '30000/1001', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                             '-c:v', 'libx264', '-preset', 'veryfast' if preview else 'slow', '-crf', '20' if preview else '15',
                             '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                             '-color_range', 'tv', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
def count_frames(f):
    return int(subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-count_frames', '-show_entries',
                               'stream=nb_read_frames', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())
def make_base():
    if not os.path.exists('base.mp4'):
        class _Z:
            def close(self): pass
        return _Z(), (lambda n: np.zeros((1080, 1920, 3), np.uint8))
    base_rd = Reader('base.mp4'); cur = [-1, None, None]
    def base(n):
        while cur[0] < n:
            cur[1] = base_rd.read(); cur[0] += 1; cur[2] = None
        if cur[2] is None: cur[2] = vignette(cur[1], cur[0])
        return cur[2]
    return base_rd, base

# ------------------------------------------------------------------ modes
def stills(ns, outdir):
    os.makedirs(outdir, exist_ok=True); base_rd, base = make_base(); want = set(ns)
    for b in tl:
        hit = [n for n in range(b['n0'], b['n1']) if n in want]
        if not hit: continue
        gen = R[b['kind']](b, base)
        for n in range(b['n0'], max(hit)+1):
            fr = next(gen)
            if n in want: Image.fromarray(finish(fr, n, ov, n)).save(f'{outdir}/f{n:05d}.png')
        gen.close(); close_media_readers(base_rd)
    base_rd.close()

def cutdown(planfile, out):
    global CROP, CAPS
    P = json.load(open(planfile))
    CC = {int(k): v for k, v in json.load(open('cut/crop.json'))['frames'].items()}
    m2c = {}
    for p in P:
        for n in range(p['p0'], p['p1']): m2c[n] = p['c0'] + n - p['p0']
    CROP = {n: CC[c] for n, c in m2c.items() if c in CC}
    CAPS = caption_schedule('cut/cap/list.txt')
    base_rd, base = make_base(); enc = encoder(out); written = 0
    for p in P:
        for b in tl:
            a, z = max(p['p0'], b['n0']), min(p['p1'], b['n1'])
            if a >= z: continue
            bb = dict(b, n0=a) if b['kind'] == 'talk' else b
            gen = R[b['kind']](bb, base)
            for n in range(bb['n0'], z):
                fr = next(gen)
                if n < a: continue
                ovs = [o for o in ov if o['n0'] >= p['p0'] or o['n0'] >= a]
                enc.stdin.write(finish(fr, n, ovs, m2c[n]).tobytes()); written += 1
            gen.close(); close_media_readers(base_rd)
    enc.stdin.close(); enc.wait(); base_rd.close()
    got = count_frames(out); print(f'{out}: {got} frames written / {P[-1]["c1"]} planned'); assert got == written == P[-1]['c1']

def main():
    if '--stills' in args:
        stills([int(x) for x in arg('--stills', '').split(',')], arg('--dir', 'stills')); return
    if '--cutplan' in args:
        cutdown(arg('--cutplan', 'cut_plan.json'), arg('--out', 'cut/picture.mp4')); return
    base_rd, base = make_base()
    ow, oh = (540, 960) if PREVIEW else (VW, VH)
    enc = encoder(OUT, ow, oh, PREVIEW); written = 0
    for b in tl:
        if b['n1'] <= N0 or b['n0'] >= N1: continue
        gen = R[b['kind']](b, base)
        for n in range(b['n0'], b['n1']):
            fr = next(gen)
            if n < N0 or n >= N1: continue
            assert fr.shape == (VH, VW, 3), (b['kind'], n, fr.shape)
            fr = finish(fr, n, ov, n)
            if PREVIEW: fr = cv2.resize(fr, (ow, oh), interpolation=cv2.INTER_AREA)
            enc.stdin.write(np.ascontiguousarray(fr).tobytes()); written += 1
            if n % 300 == 0: print(f'  frame {n} ({n/FPS:6.2f}s) {b["kind"]}', flush=True)
        gen.close(); close_media_readers(base_rd)
    enc.stdin.close(); enc.wait(); base_rd.close()
    want = min(N1, NTOT) - N0; got = count_frames(OUT)
    print(f'{OUT}: {got} frames written / {want} planned'); assert got == want == written, (got, want, written)

if __name__ == '__main__':
    main()
