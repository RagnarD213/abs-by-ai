#!/usr/bin/env python3
"""THE PICTURE for Ad 4: the Ad 5 Python frame compositor (render5.py, approved 2026-09-11) on HIS 29.97 grid (frame n here
== frame n of Muhammad's V4 HD), plus the beat kinds Ad 4 needs:

  robot      his portrait AI clip in a portrait olive card, his "AI-generated video" tag + dashed arrow pointing DOWN at it
  shot/bleed full-bleed portrait with a slow push; label='real' draws the standing real-picture chip (Dan, 2026-09-11)
  app/phonecard/dl   a phone in his olive card playing an asset already on his time map (or a still screen)
  window body 'phonev'   Dan above, the audit phone below (his phone beside Dan's head, translated to above/below)
  cardv 'crop'   the card hole takes the crop's aspect (the label clip, cropped to the tub -- still a downscale)
  overlays 'numlt'   his numbered point lower thirds

Per-frame state is Python (skill A6.9): the crop comes straight from crop.json, every overlay is composited on the frame its
measured in/out says, the output frame count is asserted. No filter-graph expressions, no index-keyed caches.

  python3 render8.py [--from N --to M] [--out picture.mp4] [--preview]
  python3 render8.py --stills 100,200,300 --dir stills
  python3 render8.py --cutplan cut_plan.json --out cut/picture.mp4
"""
import json, os, subprocess, sys, numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
def arg(k, d): return args[args.index(k)+1] if k in args else d
# AV-03 / AS-02 (2026-10-03): ONE compositor for the 9:16 and the 1:1. --aspect 1x1 re-points the graphics library's
# geometry (same 1080 width, 1080 tall, captions at 880, text ending by 1030: skill S1 START HERE) before anything draws.
ASPECT = arg('--aspect', '9x16'); SQ = ASPECT == '1x1'; SFX = '_sq' if SQ else ''
import g5 as G5, g8 as G, beats as B
if SQ:
    G5.TITLE_UP = G.TITLE_UP = 0
    G.HDR_F, G.BUL_F, G.TAIL_F = 42, 42, 46        # the square's text ladder (S1 B: one bullet size, 42 px)
    for _m in (G5, G):
        _m.VH = 1080; _m.CAP_Y = 880; _m.TOP_SAFE = 40; _m.BOT_SAFE = 1030
    G5.field.__defaults__ = (1080, 1080, True)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VW, VH, FPS, NTOT = 1080, (1080 if SQ else 1920), B.FPS, B.NTOT
CAP_Y = G5.CAP_Y
N0, N1 = int(arg('--from', 0)), int(arg('--to', NTOT))
OUT = arg('--out', 'picture.mp4'); PREVIEW = '--preview' in args
tl, ov = B.timeline()
CROPF = f'crop{SFX}.json'
CROP = {int(k): v for k, v in json.load(open(CROPF))['frames'].items()} if os.path.exists(CROPF) else {}
PLACE = json.load(open('label_place.json')) if os.path.exists('label_place.json') else {}
MEAS = [m for m in json.load(open('measure.json')) if m.get('ok')] if os.path.exists('measure.json') else []
NOLABEL = '--nolabel' in args
FLASH = B.FLASH

# ------------------------------------------------------------------ readers
READERS = []
def close_media_readers(keep):
    for r in list(READERS):
        if r is not keep: r.close(); READERS.remove(r)

class Reader:
    """Sequential RGB frames from any video, converted to 29.97 fps, optional cover-size."""
    def __init__(self, path, w=None, h=None, ss=0.0, cover=False, crop=None, rate=1.0):
        READERS.append(self); self.path = path
        vf = ['scale=in_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=rgb24'] + ([f'setpts=PTS*{rate:.5f}'] if rate != 1.0 else []) + [f'fps={FPS:.6f}']   # 709 read first, then rgb: no chroma-subsampling rounding of an odd crop; rate > 1 = slower   # rgb first: no chroma-subsampling rounding of an odd crop; rate > 1 = slower
        if crop:                                             # (x0, y0, x1, y1) fractions of the source
            vf.append(f'crop=iw*{crop[2]-crop[0]:.4f}:ih*{crop[3]-crop[1]:.4f}:iw*{crop[0]:.4f}:ih*{crop[1]:.4f}')
        if w and cover: vf.append(f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h}")
        elif w: vf.append(f'scale={w}:{h}:flags=lanczos')
        probe = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries',
                                'stream=width,height', '-of', 'csv=p=0:s=x', path], capture_output=True, text=True).stdout.strip()
        sw, sh = (int(v) for v in probe.split('\n')[0].split('x')[:2])
        self.sw, self.sh = sw, sh
        self.w, self.h = (w, h) if w else (sw, sh)
        if crop and not w: self.w, self.h = int(sw*(crop[2]-crop[0]))//2*2, int(sh*(crop[3]-crop[1]))//2*2
        self.p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-ss', f'{ss:.4f}', '-i', path, '-vf', ','.join(vf),
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
        self.last = None
    def read(self):
        b = self.p.stdout.read(self.w*self.h*3)
        if len(b) == self.w*self.h*3: self.last = np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3)
        elif len(b) not in (0,):
            raise RuntimeError(f'short raw frame from {self.path}: {len(b)} bytes for {self.w}x{self.h}')
        return self.last                                   # past the end: hold the last frame (never loop)
    def close(self):
        try: self.p.kill()
        except Exception: pass

def still(path): return ImageOps.exif_transpose(Image.open(path)).convert('RGB')

# ------------------------------------------------------------------ helpers
def warp_crop(img, x0, y0, w, h, W=VW, H=VH, interp=cv2.INTER_LANCZOS4):
    sx, sy = W/w, H/h
    M = np.float32([[sx, 0, -x0*sx], [0, sy, -y0*sy]])
    return cv2.warpAffine(img, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)

def unsharp(img, amount=0.7, sigma=1.2):
    b = cv2.GaussianBlur(img, (0, 0), sigma)
    return cv2.addWeighted(img, 1+amount, b, -amount, 0)

def compose(base_rgb, rgba):
    bb = rgba.getchannel('A').getbbox()
    if not bb: return base_rgb
    x0, y0, x1, y1 = bb
    o = np.asarray(rgba.crop(bb), dtype=np.uint16); a = o[..., 3:4]
    r = base_rgb[y0:y1, x0:x1].astype(np.uint16)
    base_rgb[y0:y1, x0:x1] = ((r*(255-a) + o[..., :3]*a + 127)//255).astype(np.uint8)
    return base_rgb

def push_cover(pil, i, n, w, h, ox=0.5, oy=0.5, amt=0.05):
    """cover-fill (w,h) with a slow push over the beat (nothing sits dead-frozen)."""
    k = i/max(1, n-1); z = 1.0 + amt*k
    W0, H0 = pil.size; s = max(w/W0, h/H0)*z; cw, ch = w/s, h/s
    x0 = (W0-cw)*ox; y0 = (H0-ch)*oy
    return warp_crop(np.asarray(pil), x0, y0, cw, ch, w, h)

def blur_in(arr, t, dur=0.40, top=22):
    """his blur-in on a card's media: gaussian settling to sharp over `dur` s"""
    s = top*(1 - G.ease_out_cubic(G.clamp01(t/dur)))
    return cv2.GaussianBlur(arr, (0, 0), s) if s > 0.4 else arr

def field_np(): return np.asarray(G.field()).copy()

# ---- HIS GRADE, READ AS A PLAYER SHOWS IT (BT.709): vignette -> per-channel curves (zgrade2 --post) -> section-by-section
# colour transfer (zgrade3) on the base frame; a final trim after the unsharp (zgrade4). Skill A12.12.
_VIG = None
_CURVES = np.array(json.load(open('grade_post.json'))['curves'], dtype=np.uint8) if os.path.exists('grade_post.json') and '--nopost' not in args else None
_SEG = np.array(json.load(open('grade_seg.json'))['keys'], dtype=np.float64) if os.path.exists('grade_seg.json') and '--noseg' not in args else None
_FINAL = json.load(open(f'grade_final{SFX}.json')) if os.path.exists(f'grade_final{SFX}.json') and '--nofinal' not in args else None
_FLUT = [np.array(c, np.uint8) for c in _FINAL['curves']] if _FINAL else None
_LW = np.array([0.2126, 0.7152, 0.0722], np.float32)
def _seg_at(n):
    ks = _SEG[:, 0]
    if n <= ks[0]: p = _SEG[0, 1:]
    elif n >= ks[-1]: p = _SEG[-1, 1:]
    else:
        j = int(np.searchsorted(ks, n)); a = (n - ks[j-1])/(ks[j] - ks[j-1]); p = _SEG[j-1, 1:]*(1-a) + _SEG[j, 1:]*a
    return p[:9].reshape(3, 3).astype(np.float32), p[9:].astype(np.float32)
def vignette(f, n=None):
    global _VIG
    if _VIG is None:
        V = json.load(open('vignette.json')); rr = [v[0] for v in V]; gg = [v[1] for v in V]
        ys, xs = np.mgrid[0:1080, 0:1920]; rad = np.hypot((xs-960)/960, (ys-540)/540)
        _VIG = np.clip(np.interp(rad, rr, gg), 0.3, 1.05).astype(np.float32)[..., None]
    out = np.clip(f.astype(np.float32)*_VIG + 0.5, 0, 255).astype(np.uint8)
    if _CURVES is not None: out = np.dstack([cv2.LUT(out[..., c], _CURVES[c]) for c in range(3)])
    if _SEG is not None and n is not None:
        A, t = _seg_at(n); out = np.clip(out.astype(np.float32) @ A.T + t + 0.5, 0, 255).astype(np.uint8)
    return out
def final_trim(img):
    if _FINAL is None: return img
    x = np.dstack([cv2.LUT(np.ascontiguousarray(img[..., c]), _FLUT[c]) for c in range(3)]).astype(np.float32)
    L = (x @ _LW)[..., None]
    return np.clip(L + _FINAL['sat']*(x - L) + 0.5, 0, 255).astype(np.uint8)

def sp_of(b):
    """the beat's spec for this aspect: b['sq'] overrides the vertical values in the square"""
    return dict(b, **b.get('sq', {})) if SQ else b

WIN_PAD = 24            # (at most) source rows of headroom added above the frame, and only in a window whose hair top comes within 34 px of the source's top: he rises to 10 px under the source's own top edge (frame 984), and
                        # in a window that put his hair on the edge (review round 3). warp_crop replicates the top row (plain wall) upward (skill A12.7)
def padded(f, pad):
    """`pad` rows of headroom above the source frame: the top rows' own colour, smoothed along x (a repeated single row turns
    the wall's grain into vertical streaks: round 4), with a little grain so it does not read as a flat band."""
    if pad <= 0: return f
    top = cv2.GaussianBlur(f[:6].astype(np.float32).mean(0, keepdims=True), (0, 0), 14)
    band = np.repeat(top, pad, 0) + np.random.RandomState(7).normal(0, 1.6, (pad, f.shape[1], 1)).astype(np.float32)
    out = np.vstack([np.clip(band, 0, 255).astype(np.uint8), f])
    out[pad-3:pad+5] = cv2.GaussianBlur(out[pad-6:pad+8], (0, 0), 2)[3:11]      # no hard line where the fill meets the picture
    return out
def window_src(f, c, win_h, pad=0):
    """Dan's window above the text. 9:16: the FULL source height in a full-width window (a downscale), centred on the crop
    track. 1:1: sized by MAGNIFICATION (skill S1.3) -- a 1400 px wide source rect from the source's own top (his hair has
    22-50 px above it on this roll), so the track keeps travel and he is not shrunk to a third of his 16:9 size."""
    if SQ:
        ws = 1400.0; hs = ws*win_h/VW
        x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, 1920 - ws))
        return final_trim(unsharp(warp_crop(padded(f, pad), x0c, 0, ws, hs, VW, win_h), 0.3))
    ws = (1080.0 + pad)*VW/win_h
    x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, 1920 - ws))
    return final_trim(unsharp(warp_crop(padded(f, pad), x0c, 0, ws, 1080 + pad, VW, win_h), 0.5))

def phone_in(scr, pw, r):
    """a phone mockup whose screen has the MEDIA's aspect (r = h/w): a 9:16 recording in a 19.5:9 phone would be
    cover-cropped at the sides and lose the list's text edges"""
    bz = 14; ph = int(round(pw*r))
    im = Image.new("RGBA", (pw+2*bz, ph+2*bz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw+2*bz-1, ph+2*bz-1], radius=int(pw*0.13), fill=(18, 18, 20, 255))
    sc = G.cover(scr, pw, ph); m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, pw-1, ph-1], radius=int(pw*0.10), fill=255)
    im.paste(sc, (bz, bz), m)
    return im

_WH = {}
def probe_wh(path):
    if path not in _WH:
        o = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries',
                            'stream=width,height', '-of', 'csv=p=0:s=x', path], capture_output=True, text=True).stdout.strip()
        _WH[path] = tuple(int(v) for v in o.split('\n')[0].split('x')[:2])
    return _WH[path]

def cover_window(sw, sh, cx, cy, tw, th, zoom=1.0):
    """the largest window of the target's aspect inside the source (shrunk by `zoom` > 1), centred on the (cx, cy)
    fractions and clamped to the source"""
    ta = tw/th
    if sw/sh > ta: wf, hf = (sh*ta)/sw, 1.0
    else: wf, hf = 1.0, (sw/ta)/sh
    wf, hf = wf/zoom, hf/zoom
    x0 = min(max(cx - wf/2, 0.0), 1.0-wf); y0 = min(max(cy - hf/2, 0.0), 1.0-hf)
    return (x0, y0, x0+wf, y0+hf)

# ------------------------------------------------------------------ labels (placed by MEASUREMENT: zlabel9.py -> label_place.json)
REAL_LINES = {1: ["Real picture of me - not AI-generated"], 2: ["Real picture of me", "not AI-generated"],
              3: ["Real picture", "of me", "not AI-generated"]}
AI_LINES = {1: ["AI-GENERATED"]}
def chip_lines(kind, lines): return (REAL_LINES if kind == 'real' else AI_LINES)[lines]
def chip_size(kind, lines, size):
    fl = G.font(size, "SemiBold"); tx = chip_lines(kind, lines)
    return max(G.text_size(t, fl)[0] for t in tx) + 40, int(size*1.24)*len(tx) + 26
def chip_at(im, kind, x, y, lines=1, size=40):
    """the standing label chip (black rounded box, white Manrope SemiBold), top-left at (x, y)"""
    fl = G.font(size, "SemiBold"); tx = chip_lines(kind, lines); w, h = chip_size(kind, lines, size)
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=(0, 0, 0, 215))
    for k, t in enumerate(tx):
        d.text((x + (w - G.text_size(t, fl)[0])//2, y + 13 + k*int(size*1.24)), t, font=fl, fill=(255, 255, 255, 255), anchor="lt")
    return w, h
def label_layer(b):
    kind = b.get('label')
    if not kind or NOLABEL: return None
    key = f"{ASPECT}:{b['n0']}"; p = PLACE.get(key)
    assert p is not None, f'no measured label placement for {key} -- run zlabel9.py'
    lay = G.blank(); chip_at(lay, kind, p['x'], p['y'], p['lines'], p['size'])
    return lay

# ------------------------------------------------------------------ beat renderers
def r_talk(b, base):
    for n in range(b['n0'], b['n1']):
        f = base(n); x0, y0, w, h = CROP[n]; up = VH/h
        yield final_trim(unsharp(warp_crop(f, x0, y0, w, h), 0.7 if up > 1.6 else (0.4 if up > 1.2 else 0.2)))

GAP = 40 if SQ else 74
def win_plate(rect, t, body=None, in_dur=0.42, grow=0.045):
    im = G.field().convert("RGBA"); d = ImageDraw.Draw(im)
    if body: body(d, im, t, rect[3] + GAP)
    return G5.punch(im, G5._hole_at(rect, t, in_dur, grow), 0)
def win_rect(text_h):
    if SQ: return (0, 0, VW, int(max(420, min(820, G5.BOT_SAFE - GAP - text_h)))//2*2)      # text ends by 1030, no dead band (S1 B)
    return G.window_rect(text_h)

def r_window(b, base):
    body = b['body']; n = b['n1']-b['n0']
    plate_cache = {}; rd = None; tails = []; it = []; hdr_delay = 0.0; pad = 0
    DEF = [420, 0, 1080, 1080] if SQ else [656, 0, 608, 1080]
    if body == 'bullets':
        it = [(x - b['n0'])/FPS for x in b['item_n']]
        hdr_delay = ((b.get('t_hdr', b['n0']) - b['n0'])/FPS)
        tails = [(tx, (tn - b['n0'])/FPS - hdr_delay) for tx, tn in b.get('tails', [])]
        fn, th = G.bullets_body2(0, b['header'], b['items'], [x - hdr_delay for x in it], tails=tails)
        rect = win_rect(th); win_h = rect[3]-rect[1]
        _h = [m['hair'] for m in MEAS if b['n0'] <= m['n'] < b['n1']]
        pad = int(np.clip(34 - min(_h), 0, WIN_PAD)) if _h else 0          # only text screen 1 needs it (he rises to 10 px under the source top at 984)
    elif body == 'phonev':
        rd = Reader(b['media'])
        rect = (0, 0, 600, VH) if SQ else (0, 60, VW, 640); win_h = rect[3]-rect[1]
    for i in range(n):
        t = i/FPS
        f = base(b['n0']+i); c = CROP.get(b['n0']+i, DEF)
        out = field_np()
        if body == 'bullets':
            tb = t - hdr_delay
            settle = max([x - hdr_delay for x in it] + [tc for _, tc in tails]) + 1.6     # every sub-element typed on (A7.5)
            key = round(tb, 3) if tb < settle else 'settled'
            if key not in plate_cache:
                if len(plate_cache) > 300: plate_cache.clear()
                plate_cache[key] = win_plate(rect, t, lambda d, im, tt, ty: fn(d, im, tb, ty), in_dur=0.42)
            plate = plate_cache[key]
            out[rect[1]:rect[3]] = window_src(f, c, win_h, pad)
        elif body == 'phonev':
            k = G.ease_out_back(G.clamp01(t/0.42))
            if SQ:      # a 1:1 frame has the width for his own split: Dan in a 600 px window at 1.00x, the phone beside him
                plate = win_plate(rect, t, in_dur=0.30, grow=0.02)
                x0c = float(np.clip(c[0] + c[2]/2 - 300, 0, 1920 - 600))
                out[:, 0:600] = final_trim(unsharp(warp_crop(f, x0c, 0, 600, 1080, 600, VH), 0.2))
                phone = phone_in(Image.fromarray(rd.read()), 400, rd.h/rd.w); pcx, hy0 = 840, 84
            else:
                # review round 1: the uncropped 16:9 put his head at 7 % of the frame beside a small phone. Now a 760 px
                # wide source rect from his hold's hair-anchored top (1.42x: head and shoulders) and the phone as large as fits.
                plate = win_plate(rect, t, in_dur=0.30, grow=0.03)
                # Round 2 review: his chin was at the panel's edge with the bar on it, and his own FAR -> NEAR punch at 6157
                # read as a same-size jump. The panel shows the source from its top (hair 22-50 px down) at the hold's own
                # level: 1080 px wide at FAR (head and shoulders, 1.00x), 940 at NEAR. The bar sits wholly on the field under it.
                ws = float(np.interp(c[3], [832.0, 1024.0], [960.0, 1080.0])); hs = ws*win_h/VW      # NEAR shows 515 px of source height: his chin (about 455) keeps 60 px under it
                x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, 1920 - ws))
                out[rect[1]:rect[3]] = final_trim(unsharp(warp_crop(f, x0c, 0.0, ws, hs, VW, win_h), 0.2))
                phone = phone_in(Image.fromarray(rd.read()), 452, rd.h/rd.w); pcx, hy0 = VW//2, 824
            hw2, hh2 = int(phone.width*(0.94+0.06*k)), int(phone.height*(0.94+0.06*k))
            G.rrect(plate, [pcx-hw2//2-16, hy0-12, pcx+hw2//2+16, hy0+hh2+12], 30, fill=G.CARD_OL+(255,), glow=22)
            plate.alpha_composite(phone.resize((hw2, hh2), Image.LANCZOS), (pcx-hw2//2, hy0))
        else: raise ValueError(body)
        yield compose(out, plate)
    if rd: rd.close()

def slow_push(arr, i, n, amt=0.025):
    """a settled graphic never sits dead-frozen (skill A3.6): a slow centred push over the beat"""
    z = 1.0 + amt*(i/max(1, n-1)); H, W = arr.shape[:2]
    cw, ch = W/z, H/z
    return warp_crop(arr, (W-cw)/2, (H-ch)/2, cw, ch, W, H, cv2.INTER_LINEAR)

def r_fillv(b, base):
    """A clip that FILLS the frame (Dan 2026-10-01/02: fill unless the sides hold something the clip needs). The window is
    the largest one of the frame's aspect, centred on the subject (cx, cy), never on the middle by default."""
    sp = sp_of(b); n = b['n1']-b['n0']; sw, sh = probe_wh(sp['media'])
    if sp.get('card_ar'):       # 1:1 only: a PORTRAIT clip whose action runs top to bottom keeps its full height, in his card
        hole = G.card_hole(sp['card_ar'], top=30, bot=(CAP_Y - 40 if sp['card_ar'] > 1 else VH-30)); hw, hh = hole[2]-hole[0], hole[3]-hole[1]     # a landscape card ends above the caption line
        rd = Reader(sp['media'], hw, hh, ss=sp.get('ss', 0)/FPS, cover=True, crop=cover_window(sw, sh, sp.get('cx', 0.5), sp.get('cy', 0.5), hw, hh)); lay = label_layer(b)
        for i in range(n):
            out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = unsharp(slow_push(rd.read(), i, n, 0.03), 0.2)
            fr = compose(out, G.card_plate(hole, i/FPS))
            if lay is not None: fr = compose(fr, lay)
            yield fr
        rd.close(); return
    cr = cover_window(sw, sh, sp.get('cx', 0.5), sp.get('cy', 0.5), VW, VH, sp.get('zoom', 1.0))
    rd = Reader(sp['media'], VW, VH, ss=sp.get('ss', 0)/FPS, cover=True, crop=cr, rate=sp.get('rate', 1.0))
    up = VH/((cr[3]-cr[1])*sh); lay = label_layer(b)
    for i in range(n):
        fr = unsharp(slow_push(rd.read(), i, n, 0.04), 0.5 if up > 1.3 else 0.25)
        if sp.get('blur'): fr = blur_in(fr, i/FPS)
        if lay is not None: fr = compose(np.ascontiguousarray(fr).copy(), lay)
        yield fr
    rd.close()

def r_sqv(b, base):
    """A clip whose subject spreads across the frame (the stack pan, the overhead meal prep): the centre SQUARE, in his
    olive card as wide as the phone frame allows. In the 1:1 the same square simply fills the frame."""
    if SQ:
        yield from r_fillv(b, base); return
    sp = b; n = b['n1']-b['n0']; sw, sh = probe_wh(sp['media'])
    hole = G.card_hole(sp.get('ar', 1.0)); hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    cr = cover_window(sw, sh, sp.get('cx', 0.5), sp.get('cy', 0.5), hw, hh)
    rd = Reader(sp['media'], hw, hh, ss=sp.get('ss', 0)/FPS, cover=True, crop=cr, rate=sp.get('rate', 1.0))
    for i in range(n):
        t = i/FPS; m = slow_push(rd.read(), i, n, 0.04)
        if sp.get('blur'): m = blur_in(m, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = unsharp(m, 0.25)
        yield compose(out, G.card_plate(hole, t))
    rd.close()

def r_bleed(b, base):
    """A photo that fills the frame, with a slow push. fit='fith' (1:1 only): the whole photo at full height on the field,
    for a portrait whose 1:1 cover crop would cut his head or his shorts (skill S1.5)."""
    sp = sp_of(b); pil = still(sp['media']); n = b['n1']-b['n0']; lay = label_layer(b)
    for i in range(n):
        if sp.get('fit', 'cover') == 'cover':
            fr = unsharp(push_cover(pil, i, n, VW, VH, sp.get('ox', 0.5), sp.get('oy', 0.5), sp.get('amt', 0.05)), 0.3)
        else:
            hh = int(sp.get('fith_h', VH))//2*2; w = int(hh*pil.width/pil.height)//2*2; y0 = 10 if hh < VH else 0
            # the push is anchored at the TOP of the photo: a centred push took his hair out of the frame (review round 3)
            fr = field_np(); fr[y0:y0+hh, (VW-w)//2:(VW-w)//2+w] = unsharp(push_cover(pil, i, n, w, hh, 0.5, 0.0, 0.03), 0.3)
        if sp.get('blur'): fr = blur_in(fr, i/FPS)
        if lay is not None: fr = compose(np.ascontiguousarray(fr).copy(), lay)
        yield fr

def r_shot(b, base):
    return r_bleed(dict(b, label=b.get('label', 'real')), base)

def r_sqcard(b, base):
    """A photo that cannot fill a 9:16 frame without cutting a person: a square (or `ar`) crop in his olive card, as wide
    as the phone frame allows. In the 1:1 the photo fills the frame."""
    if SQ:
        yield from r_bleed(b, base); return
    pil = still(b['media']); n = b['n1']-b['n0']
    hole = G.card_hole(b.get('ar', 1.0)); hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    for i in range(n):
        t = i/FPS
        m = push_cover(pil, i, n, hw, hh, b.get('ox', 0.5), b.get('oy', 0.5), 0.05)
        if b.get('blur'): m = blur_in(m, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = m
        yield compose(out, G.card_plate(hole, t))

def r_title(b, base):
    n = b['n1']-b['n0']
    # 8 % over the beat: at 2.5 % the settled YOU LOCK IN card read as 76 frozen frames (watch scan, render 1); his own
    # card is never still (per-frame change 0.24 on his 256x144 cut)
    for i in range(n): yield slow_push(np.asarray(G.title_card(b['headline'], b['sub'], i/FPS).convert('RGB')), i, n, 0.08)

def r_phonecard(b, base):
    """app / phonecard / dl: a phone on his olive card, AS LARGE AS FITS (Dan 2026-10-02: a phone demo is as large as
    fits), the screen from an asset already on his time map (or a still)."""
    n = b['n1']-b['n0']; hole = (40, 40, 1040, 1040) if SQ else (60, 150, 1020, 1660); media = b['media']
    hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    static = media.endswith('.png')
    img = still(media) if static else None; rd = None if static else Reader(media)
    ar = (img.height/img.width) if static else (rd.h/rd.w)
    pw = int(min(hw - 140, ((hh - 40)/1.03 - 28)/ar))//2*2
    for i in range(n):
        t = i/FPS
        scr = img if static else Image.fromarray(rd.read())
        phone = phone_in(scr, pw, ar)
        z = 1.0 + 0.03*(i/max(1, n-1)); pw2, ph2 = int(phone.width*z), int(phone.height*z)       # slow push: held screens never freeze
        phone = phone.resize((pw2, ph2), Image.LANCZOS)
        inner = Image.new('RGB', (hw, hh), G.CARD_OL)
        inner.paste(phone, ((inner.width-phone.width)//2, (inner.height-phone.height)//2), phone)
        arr = np.asarray(inner).copy()
        if b.get('blur'): arr = blur_in(arr, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = arr
        out[hole[3], hole[0]:hole[2]+1] = G.CARD_OL; out[hole[1]:hole[3]+1, hole[2]] = G.CARD_OL     # the plate's hole includes its last row and column: a 1 px dark line showed (review round 2)
        yield compose(out, G.card_plate(hole, t))
    if rd: rd.close()

R = dict(talk=r_talk, window=r_window, fillv=r_fillv, sqv=r_sqv, bleed=r_bleed, shot=r_shot, sqcard=r_sqcard, title=r_title,
         app=r_phonecard, phonecard=r_phonecard, dl=r_phonecard)
KIND = {}
for _b in tl:
    for _n in range(_b['n0'], _b['n1']): KIND[_n] = _b['kind']
PLATE_KINDS = {'fillv', 'bleed', 'shot'} | ({'sqv', 'sqcard'} if SQ else set())     # full-frame pictures behind the captions

# ------------------------------------------------------------------ overlays
def lt_y(o): return o.get('sq_y', 985) if SQ else o.get('y_bottom', 1600)
_OVC = {}
def overlay_img(o, n):
    t = (n - o['n0'])/FPS; dur = (o['n1'] - o['n0'])/FPS
    settle = 1.9 if o['kind'] in ('lt', 'numlt') else 1.2
    key = (id(o), round(t, 3) if (t < settle or t > dur - 0.4) else 'settled')
    if key in _OVC: return _OVC[key]
    k = o['kind']
    if k == 'lt': im = G.lower_third(o['lines'], t, dur, y_bottom=lt_y(o), weights=o.get('weights'), sizes=o.get('sizes'))
    elif k == 'numlt': im = G.num_lower_third(o['num'], o['lines'], t, dur, y_bottom=lt_y(o))
    elif k == 'pill': im = G.cta_pill(o['top'], o['big'], t, dur + (9.0 if o['n1'] >= B.NTOT else 0.0))      # his closing pill is at full strength on his last frame
    else: raise ValueError(k)
    if len(_OVC) > 400: _OVC.clear()
    _OVC[key] = im
    return im

# ------------------------------------------------------------------ captions (the gated layout: captions.py)
def caption_schedule(path='cap/list.txt'):
    L = [l.strip() for l in open(path)]
    out, t = [], 0.0
    for a, bb in zip(L[0::2], L[1::2]):
        if not a.startswith('file') or not bb.startswith('duration'): continue
        p = a.split("'")[1]; d = float(bb.split()[1])
        out.append((t, t+d, p)); t += d
    return out
CAPS = caption_schedule(f'cap{SFX}/list.txt') if os.path.exists(f'cap{SFX}/list.txt') else []
_CAPC = {}
def caption_at(n):
    t = (n + 0.5)/FPS
    for a, bb, p in CAPS:
        if a <= t < bb:
            if p.endswith('_blank.png'): return None
            if p not in _CAPC:
                if len(_CAPC) > 64: _CAPC.clear()
                _CAPC[p] = Image.open(p).convert('RGBA')
            return p, _CAPC[p]
    return None

_PLC = {}
def cap_plate(p, im):
    """A caption-LOCAL black plate, sized to this caption line, in the chip language of the labels: the olive lit word is
    unreadable over a bright full-frame photo or clip, and a full-width gradient fogs a white backdrop (skill A9.4)."""
    if p not in _PLC:
        if len(_PLC) > 64: _PLC.clear()
        a = np.asarray(im.getchannel('A')) > 235; xs = np.where(a.any(0))[0]
        x0, x1 = int(xs.min()), int(xs.max()); w = max(x1 - x0 + 64, 280); cx = (x0 + x1)//2
        pl = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(pl).rounded_rectangle([cx - w//2, CAP_Y - 12, cx + w//2, CAP_Y + 96], radius=14, fill=(0, 0, 0, 205))
        _PLC[p] = pl
    return _PLC[p]

_TINT_LOW = np.array([0.55, 0.95, 1.45], np.float32)   # the leak's colour where it is faint (the decay)
_TINT = np.array([0.81, 1.0, 1.25], np.float32)        # his light leak is BLUE-white: fitted per channel on 60 of his flash frames against ours (round 3: ours read neutral, B-R -22 against his +38)
def flash9(fr, k):
    a = fr.astype(np.float32)/255.0
    c = _TINT_LOW + (1.0 - _TINT_LOW)*min(1.0, k/0.85)**1.5          # his leak is WHITE at its peak and blue as it decays (round 4: ours was cyan at the peak, neutral in the decay)
    return ((1 - (1 - a)*(1 - np.minimum(k*c, 1.0)))*255 + 0.5).clip(0, 255).astype(np.uint8)

def finish(fr, n, ovs, capn):
    fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
    for o in ovs:
        if o['n0'] <= n < o['n1'] and not (o['kind'] == 'pill' and o['n1'] < B.NTOT and o['n1'] - n <= 2): fr = compose(fr, overlay_img(o, n))     # a pill's last two fading frames are a dark ghost of its glow
    if n in FLASH: fr = flash9(fr, FLASH[n])      # his light leak washes the PICTURE; our caption layer sits over it (round 4: the
    c = caption_at(capn)                           # blue leak washed the lit word out and the gate could not find it)
    if c is not None:
        if KIND.get(n) in PLATE_KINDS: fr = compose(fr, cap_plate(*c))
        fr = compose(fr, c[1])
    return fr

def encoder(out, w=VW, h=VH, preview=False):
    return subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}',
                             '-r', '30000/1001', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                             '-c:v', 'libx264', '-preset', 'veryfast' if preview else 'slow', '-crf', '20' if preview else '15',
                             '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                             '-color_range', 'tv', '-movflags', '+faststart', out], stdin=subprocess.PIPE)

def count_frames(f):
    return int(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-count_frames',
                               '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())

def make_base():
    if not os.path.exists('base.mp4'):                       # graphics-only test stills before the conform exists
        class _Z:
            def close(self): pass
        return _Z(), (lambda n: np.zeros((1080, 1920, 3), np.uint8))
    base_rd = Reader('base.mp4'); cur = [-1, None, None]
    def base(n):
        while cur[0] < n:
            cur[1] = base_rd.read(); cur[0] += 1; cur[2] = None
        if cur[2] is None: cur[2] = vignette(cur[1], cur[0]) if os.path.exists('vignette.json') else cur[1]
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
    CC = {int(k): v for k, v in json.load(open(f'cut{SFX}/crop.json'))['frames'].items()}
    m2c = {}
    for p in P:
        for n in range(p['p0'], p['p1']): m2c[n] = p['c0'] + n - p['p0']
    CROP = {n: CC[c] for n, c in m2c.items() if c in CC}
    CAPS = caption_schedule(f'cut{SFX}/cap/list.txt')
    base_rd, base = make_base(); enc = encoder(out); written = 0
    # per range: only overlays that START inside it, each ENDING at the seam if it would run past it, so its own fade-out
    # plays before the cut instead of the bar being sliced off at full strength (review round 1, seam 3)
    OVP = {p['p0']: [dict(o, n1=min(o['n1'], p['p1'])) for o in ov if p['p0'] <= o['n0'] < p['p1']] for p in P}
    for cutf, f0, f1 in B.FLASH_CUTS:                      # round 3: one frame of his flash ramp was left before two seams
        for p in P:
            if f0 < p['p1'] <= cutf:
                for n in range(f0, p['p1']): FLASH.pop(n, None)
    for p in P:
        for b in tl:
            a, z = max(p['p0'], b['n0']), min(p['p1'], b['n1'])
            if a >= z: continue
            bb = dict(b, n0=a) if b['kind'] == 'talk' else b
            gen = R[b['kind']](bb, base)
            for n in range(bb['n0'], z):
                fr = next(gen)
                if n < a: continue
                enc.stdin.write(finish(fr, n, OVP[p['p0']], m2c[n]).tobytes()); written += 1
            gen.close(); close_media_readers(base_rd)
    enc.stdin.close(); enc.wait(); base_rd.close()
    got = count_frames(out); print(f'{out}: {got} frames written / {P[-1]["c1"]} planned'); assert got == written == P[-1]['c1']

def main():
    if '--stills' in args:
        stills([int(x) for x in arg('--stills', '').split(',')], arg('--dir', 'stills')); return
    if '--cutplan' in args:
        cutdown(arg('--cutplan', 'cut_plan.json'), arg('--out', 'cut/picture.mp4')); return
    base_rd, base = make_base()
    ow, oh = (VW//2, VH//2) if PREVIEW else (VW, VH)
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
