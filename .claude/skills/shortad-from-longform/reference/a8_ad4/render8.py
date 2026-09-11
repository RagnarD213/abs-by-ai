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
import g8 as G, beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
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

class Reader:
    """Sequential RGB frames from any video, converted to 29.97 fps, optional cover-size."""
    def __init__(self, path, w=None, h=None, ss=0.0, cover=False, crop=None, rate=1.0):
        READERS.append(self); self.path = path
        vf = ['format=rgb24'] + ([f'setpts=PTS*{rate:.5f}'] if rate != 1.0 else []) + [f'fps={FPS:.6f}']   # rgb first: no chroma-subsampling rounding of an odd crop; rate > 1 = slower
        if crop:                                             # (x0, y0, x1, y1) fractions of the source
            vf.append(f'crop=iw*{crop[2]-crop[0]:.4f}:ih*{crop[3]-crop[1]:.4f}:iw*{crop[0]:.4f}:ih*{crop[1]:.4f}')
        if w and cover: vf.append(f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h}")
        elif w: vf.append(f'scale={w}:{h}:flags=lanczos')
        vf.append('scale=in_color_matrix=bt709:in_range=tv')
        probe = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries',
                                'stream=width,height', '-of', 'csv=p=0:s=x', path], capture_output=True, text=True).stdout.strip()
        sw, sh = (int(v) for v in probe.split('\n')[0].split('x')[:2])
        self.w, self.h = (w, h) if w else (sw, sh)
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

_VIG = None
def vignette(f):
    """His radial falloff (vignette.json: median his/ours after the LUT, in 1920x1080 source coordinates) applied to the
    conform before any crop -- so the talking head and the windows carry exactly his edge darkening (skill rule 12)."""
    global _VIG
    if _VIG is None:
        V = json.load(open('vignette.json')); rr = [v[0] for v in V]; gg = [v[1] for v in V]
        ys, xs = np.mgrid[0:1080, 0:1920]; rad = np.hypot((xs-960)/960, (ys-540)/540)
        _VIG = np.clip(np.interp(rad, rr, gg), 0.3, 1.05).astype(np.float32)[..., None]
    return np.clip(f.astype(np.float32)*_VIG + 0.5, 0, 255).astype(np.uint8)

def window_src(f, c, win_h):
    """Dan's window: the FULL source height in a full-width window of win_h (a downscale), centred on the crop track."""
    ws = 1080.0*VW/win_h
    x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, 1920 - ws))
    return unsharp(warp_crop(f, x0c, 0, ws, 1080, VW, win_h), 0.5)

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

# ------------------------------------------------------------------ beat renderers
def r_talk(b, base):
    for n in range(b['n0'], b['n1']):
        f = base(n); x0, y0, w, h = CROP[n]
        yield unsharp(warp_crop(f, x0, y0, w, h))

def r_window(b, base):
    body = b['body']; n = b['n1']-b['n0']
    rect = (0, 60, VW, 720)
    win_h = rect[3]-rect[1]
    plate_cache = {}; rd = None; tails = []; it = []; hdr_delay = 0.0
    if body == 'bullets':
        it = [(x - b['n0'])/FPS for x in b['item_n']]
        hdr_delay = ((b.get('t_hdr', b['n0']) - b['n0'])/FPS)
        tails = [(tx, (tn - b['n0'])/FPS - hdr_delay) for tx, tn in b.get('tails', [])]
        fn, th = G.bullets_body2(0, b['header'], b['items'], [x - hdr_delay for x in it], tails=tails)
        rect = G.window_rect(th); win_h = rect[3]-rect[1]
    elif body == 'phonev':
        rd = Reader(b['media'])
    for i in range(n):
        t = i/FPS
        f = base(b['n0']+i); c = CROP.get(b['n0']+i, [656, 0, 608, 1080])
        out = field_np()
        if body == 'bullets':
            tb = t - hdr_delay
            settle = max([x - hdr_delay for x in it] + [tc for _, tc in tails]) + 1.6     # every sub-element typed on (A7.5)
            key = round(tb, 3) if tb < settle else 'settled'
            if key not in plate_cache:
                if len(plate_cache) > 300: plate_cache.clear()
                plate_cache[key] = G.window_plate(rect, t, lambda d, im, tt, ty: fn(d, im, tb, ty), in_dur=0.42)
            plate = plate_cache[key]
        elif body == 'phonev':
            plate = G.window_plate(rect, t, in_dur=0.30, grow=0.03)
            k = G.ease_out_back(G.clamp01(t/0.42))
            phone = phone_in(Image.fromarray(rd.read()), 440, 16/9)
            hy0 = 770; hw2, hh2 = int(phone.width*(0.94+0.06*k)), int(phone.height*(0.94+0.06*k))
            G.rrect(plate, [VW//2-hw2//2-16, hy0-12, VW//2+hw2//2+16, hy0+hh2+12], 30, fill=G.CARD_OL+(255,), glow=22)
            plate.alpha_composite(phone.resize((hw2, hh2), Image.LANCZOS), (VW//2-hw2//2, hy0))
        else: raise ValueError(body)
        out[rect[1]:rect[3]] = window_src(f, c, win_h)
        yield compose(out, plate)
    if rd: rd.close()

def r_card(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    ar = b.get('ar') or (pil.width/pil.height); hole = G.card_hole(ar)
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
    n = b['n1']-b['n0']; cr = b.get('crop')
    ar = (16/9)*((cr[2]-cr[0])/(cr[3]-cr[1])) if cr else 16/9
    hole = G.card_hole(ar); hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    rd = Reader(b['media'], hw, hh, ss=b.get('ss', 0)/FPS, cover=True, crop=cr, rate=b.get('rate', 1.0))
    for i in range(n):
        t = i/FPS; m = slow_push(rd.read(), i, n, 0.04)        # his near-static stock (pill bottles) read as a 12-frame freeze
        if b.get('blur'): m = blur_in(m, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = unsharp(m, 0.3)
        pl = G.card_plate(hole, t)
        if b.get('label'): G.ai_chip(pl, hole[2]-18, hole[3]-12)
        yield compose(out, pl)
    rd.close()

def r_robot(b, base):
    n = b['n1']-b['n0']; hole = G.card_hole(9/16, top=350); hw, hh = hole[2]-hole[0], hole[3]-hole[1]
    rd = Reader('assets/robot.mp4', hw, hh, cover=True); FADE = 10
    for i in range(n):
        t = i/FPS; m = rd.read()
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = unsharp(m, 0.3)
        pl = G.card_plate(hole, t)
        # his tag is ON from the card's first frame (audit 1: typing it on left the AI clip unlabelled for 5 frames and
        # half-labelled for 10 -- Dan r1: an AI clip is labelled for its whole time on screen)
        G.robot_label(pl, VW//2, 150, hole[1]-28, 10.0)
        fr = compose(out, pl)
        if i < FADE:                                                 # his card fades up from the field over 85-95, tag already on
            a = (i + 1)/(FADE + 1); fr = (field_np().astype(np.float32)*(1 - a) + fr.astype(np.float32)*a + 0.5).astype(np.uint8)
        yield fr
    rd.close()

def r_bleed(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    lay = None
    if b.get('label') == 'real': lay = G.blank(); G.real_chip(lay)
    elif b.get('label') == 'ai': lay = G.blank(); G.ai_chip_bleed(lay)
    for i in range(n):
        fr = unsharp(push_cover(pil, i, n, VW, VH, b.get('ox', 0.5), b.get('oy', 0.5), 0.05), 0.3)
        if b.get('blur'): fr = blur_in(fr, i/FPS)
        if lay is not None: fr = compose(np.ascontiguousarray(fr).copy(), lay)
        yield fr

def r_shot(b, base):
    return r_bleed(dict(b, label=b.get('label', 'real')), base)

def slow_push(arr, i, n, amt=0.025):
    """a settled graphic never sits dead-frozen (skill A3.6): a slow centred push over the beat"""
    z = 1.0 + amt*(i/max(1, n-1)); H, W = arr.shape[:2]
    cw, ch = W/z, H/z
    return warp_crop(arr, (W-cw)/2, (H-ch)/2, cw, ch, W, H, cv2.INTER_LINEAR)

def r_title(b, base):
    n = b['n1']-b['n0']
    # 8 % over the beat: at 2.5 % the settled YOU LOCK IN card read as 76 frozen frames (watch scan, render 1); his own
    # card is never still (per-frame change 0.24 on his 256x144 cut)
    for i in range(n): yield slow_push(np.asarray(G.title_card(b['headline'], b['sub'], i/FPS).convert('RGB')), i, n, 0.08)

def r_phonecard(b, base):
    """app / phonecard / dl: a phone on his olive card, the screen from an asset already on his time map (or a still)."""
    n = b['n1']-b['n0']; hole = (120, 150, 960, 1330); media = b['media']
    static = media.endswith('.png')
    img = still(media) if static else None; rd = None if static else Reader(media)
    ar = (img.height/img.width) if static else (rd.h/rd.w)
    pw = b.get('pw', 500 if ar > 2.0 else 560)
    for i in range(n):
        t = i/FPS
        scr = img if static else Image.fromarray(rd.read())
        phone = phone_in(scr, pw, ar)
        z = 1.0 + 0.03*(i/max(1, n-1)); pw2, ph2 = int(phone.width*z), int(phone.height*z)       # slow push: held screens never freeze
        phone = phone.resize((pw2, ph2), Image.LANCZOS)
        inner = Image.new('RGB', (hole[2]-hole[0], hole[3]-hole[1]), G.CARD_OL)
        inner.paste(phone, ((inner.width-phone.width)//2, (inner.height-phone.height)//2), phone)
        arr = np.asarray(inner).copy()
        if b.get('blur'): arr = blur_in(arr, t)
        out = field_np(); out[hole[1]:hole[3], hole[0]:hole[2]] = arr
        yield compose(out, G.card_plate(hole, t))
    if rd: rd.close()

R = dict(talk=r_talk, window=r_window, card=r_card, cardv=r_cardv, bleed=r_bleed, shot=r_shot, title=r_title,
         robot=r_robot, app=r_phonecard, phonecard=r_phonecard, dl=r_phonecard)

# ------------------------------------------------------------------ overlays
_OVC = {}
def overlay_img(o, n):
    t = (n - o['n0'])/FPS; dur = (o['n1'] - o['n0'])/FPS
    settle = 1.9 if o['kind'] in ('lt', 'numlt') else 1.2
    key = (id(o), round(t, 3) if (t < settle or t > dur - 0.4) else 'settled')
    if key in _OVC: return _OVC[key]
    k = o['kind']
    if k == 'lt': im = G.lower_third(o['lines'], t, dur, y_bottom=o.get('y_bottom', 1600), weights=o.get('weights'), sizes=o.get('sizes'))
    elif k == 'numlt': im = G.num_lower_third(o['num'], o['lines'], t, dur, y_bottom=o.get('y_bottom', 1600))
    elif k == 'pill': im = G.cta_pill(o['top'], o['big'], t, dur)
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
CAPS = caption_schedule() if os.path.exists('cap/list.txt') else []
_CAPC = {}
def caption_at(n):
    t = (n + 0.5)/FPS
    for a, bb, p in CAPS:
        if a <= t < bb:
            if p.endswith('_blank.png'): return None
            if p not in _CAPC:
                if len(_CAPC) > 64: _CAPC.clear()
                _CAPC[p] = Image.open(p).convert('RGBA')
            return _CAPC[p]
    return None

def finish(fr, n, ovs, capn):
    fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
    for o in ovs:
        if o['n0'] <= n < o['n1']: fr = compose(fr, overlay_img(o, n))
    c = caption_at(capn)
    if c is not None: fr = compose(fr, c)
    if n in FLASH: fr = G.flash(fr, FLASH[n])
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
        if cur[2] is None: cur[2] = vignette(cur[1]) if os.path.exists('vignette.json') else cur[1]
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
                ovs = [o for o in ov if o['n0'] >= p['p0'] or o['n0'] >= a]      # only overlays that START inside the range
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
