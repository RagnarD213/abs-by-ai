#!/usr/bin/env python3
"""THE PICTURE: a Python frame compositor on HIS 24 fps grid (frame n here == frame n of his cut).

Why a compositor and not an ffmpeg filter graph: every filter-graph trap in this skill's history -- the crop
expression evaluated in the wrong order (316 px off for twelve seconds), overlays gated but not shifted (nothing
appeared), a truncated plate shortening a beat, a stale index-keyed cache -- came from expressing per-frame state as
filter expressions. Here the per-frame state IS Python: the crop comes straight from crop.json, every overlay is
composited on the frame its measured in/out says, and the output frame count is asserted.

  python3 zrender.py [--from N --to M] [--out picture.mp4] [--preview]   (--preview: 540x960, fast)
"""
import json, os, subprocess, sys, hashlib, numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0, '.')
import zgfx as G, beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VW, VH, FPS, NTOT = 1080, 1920, 24.0, B.NTOT
args = sys.argv[1:]
def arg(k, d):
    return args[args.index(k)+1] if k in args else d
N0, N1 = int(arg('--from', 0)), int(arg('--to', NTOT))
OUT = arg('--out', 'picture.mp4')
PREVIEW = '--preview' in args
tl, ov = B.timeline()
CROP = {int(k): v for k, v in json.load(open('crop.json'))['frames'].items()}
FLASH = set(B.FLASHES)

# ------------------------------------------------------------------ readers
READERS = []
def close_media_readers(keep):
    """A media beat's generator is abandoned after its last frame, so its ffmpeg reader would sit blocked on a full
    pipe until the render exits (seen: five idle readers holding decoded frames at the end of the master render)."""
    for r in list(READERS):
        if r is not keep: r.close(); READERS.remove(r)

class Reader:
    """Sequential RGB frames from any video, converted to 24 fps, with an optional size."""
    def __init__(self, path, w=None, h=None, ss=0.0, vf_extra=''):
        READERS.append(self)
        vf = [f'fps=24']
        if w: vf.append(f'scale={w}:{h}:flags=lanczos')
        vf.append('scale=in_color_matrix=bt709:in_range=tv')
        if vf_extra: vf.insert(0, vf_extra)
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
        return self.last                                   # past the end: hold the last frame (never loop)
    def close(self):
        try: self.p.kill()
        except Exception: pass

def still(path):
    return ImageOps.exif_transpose(Image.open(path)).convert('RGB')

# ------------------------------------------------------------------ helpers
def warp_crop(img, x0, y0, w, h, W=VW, H=VH, interp=cv2.INTER_LANCZOS4):
    sx, sy = W/w, H/h
    M = np.float32([[sx, 0, -x0*sx], [0, sy, -y0*sy]])
    return cv2.warpAffine(img, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)

def unsharp(img, amount=0.7, sigma=1.2):
    b = cv2.GaussianBlur(img, (0, 0), sigma)
    return cv2.addWeighted(img, 1+amount, b, -amount, 0)

def push_still(pil, n_local, n_total, ox=0.5, oy=0.5, amt=0.05, pop=False):
    """Cover-fill 1080x1920 with a slow push (nothing sits dead-frozen); `pop` = his card pop-in over 3 frames."""
    k = n_local/max(1, n_total-1)
    z = 1.0 + amt*k
    if pop and n_local < 3: z *= 0.93 + 0.07*(n_local/3)
    W0, H0 = pil.size
    s = max(VW/W0, VH/H0)*z
    cw, ch = VW/s, VH/s
    x0 = (W0 - cw)*ox; y0 = (H0 - ch)*oy
    return warp_crop(np.asarray(pil), x0, y0, cw, ch)

def compose(base_rgb, rgba):
    """Alpha-composite a full-frame RGBA PIL image onto an RGB numpy frame, inside its bounding box only."""
    bb = rgba.getchannel('A').getbbox()
    if not bb: return base_rgb
    x0, y0, x1, y1 = bb
    o = np.asarray(rgba.crop(bb), dtype=np.uint16)
    a = o[..., 3:4]
    r = base_rgb[y0:y1, x0:x1].astype(np.uint16)
    base_rgb[y0:y1, x0:x1] = ((r*(255-a) + o[..., :3]*a + 127)//255).astype(np.uint8)
    return base_rgb

_ys = np.arange(VH, dtype=np.float32)
SCRIM = 1.0 - np.interp(_ys, [0, 1200, 1370, 1560, 1920], [0, 0, 0.65, 0.65, 0.40]).astype(np.float32)

def field_np():
    return np.full((VH, VW, 3), G.FIELD, np.uint8)

# ------------------------------------------------------------------ beat renderers (each a generator of frames)
def r_talk(b, base):
    for n in range(b['n0'], b['n1']):
        f = base(n)
        x0, y0, w, h = CROP[n]
        yield unsharp(warp_crop(f, x0, y0, w, h))

def r_split(b, base):
    """Dan above (a window from the top of the camera frame, a DOWNSCALE of the conform), the photo on the door below
    with his lime box. The door card sits BETWEEN Dan and the caption band (1385-1495) so the hook's key line -- "I
    generated this picture with AI back when..." -- is captioned (the first build muted it under a card that covered
    the band), and at 360 px tall the print is drawn at 0.87x instead of blown up 1.45x (audit 2026-09-10: soft)."""
    WIN_H = 960
    hs = 1024.0*WIN_H/1000; ws = hs*VW/WIN_H        # the same 0.977x scale as before; the window just ends higher
    P = (130, 175, 300, 415)                       # the door photo in base pixels (x, y, w, h), static camera
    ph = 360; pw = round(ph*P[2]/P[3]); px0 = (VW - pw)//2; py0 = 985
    for i, n in enumerate(range(b['n0'], b['n1'])):
        f = base(n)
        c = CROP[n]; x0c = float(np.clip(c[0] + c[2]/2 - ws/2, 0, 1920 - ws))
        out = field_np()
        out[:WIN_H] = unsharp(warp_crop(f, x0c, 0, ws, hs, VW, WIN_H), 0.5)
        pc = warp_crop(f, P[0], P[1], P[2], P[3], pw, ph)
        cv2.rectangle(out, (px0-10, py0-10), (px0+pw+9, py0+ph+9), (0, 0, 0), -1)
        out[py0:py0+ph, px0:px0+pw] = unsharp(pc, 0.4)
        im = Image.fromarray(out).convert('RGBA')
        t = i/FPS - b['t_box']
        if t >= 0:                                     # his box sits just around the print: base (160,212)-(400,550)
            sx, sy = pw/P[2], ph/P[3]
            G.callout_stroke(im, (px0 + (160-P[0])*sx, py0 + (212-P[1])*sy, px0 + (400-P[0])*sx, py0 + (550-P[1])*sy), t, width=8)
        yield np.asarray(im.convert('RGB'))

def r_card(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    for i in range(n):
        k = G.ease_out_cubic(i/max(1, n-1))
        w = round(b['w0'] + (b['w1']-b['w0'])*k)
        im = G.field(); box = G.card_on(im, pil, VW/2, b['cy'], w)
        if b.get('label'): G.ai_label(im, box[2]-18, box[3]-12, size=48)
        yield np.asarray(im.convert('RGB'))

def r_cardv(b, base):
    rd = Reader(b['media']); n = b['n1']-b['n0']
    for i in range(n):
        f = Image.fromarray(rd.read())
        k = i/max(1, n-1); w = round(1000 + 40*k)
        cy = 760 if f.width/f.height > 1.5 else 740
        im = G.field(); box = G.card_on(im, f, VW/2, cy, w)
        if b.get('label'): G.ai_label(im, box[2]-18, box[3]-12, size=44)
        yield np.asarray(im.convert('RGB'))
    rd.close()

def r_bleed(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    for i in range(n):
        yield unsharp(push_still(pil, i, n, b.get('ox', 0.5), b.get('oy', 0.5), 0.05, b.get('pop', False)), 0.3)

def r_bleedv(b, base):
    rd = Reader(b['media']); n = b['n1']-b['n0']
    for i in range(n):
        f = rd.read()
        W0, H0 = rd.w, rd.h
        z = 1.0 + 0.04*(i/max(1, n-1))                    # slow push over the whole beat (also covers a hold)
        s = max(VW/W0, VH/H0)*z; cw, ch = VW/s, VH/s
        fr = warp_crop(f, (W0-cw)/2, (H0-ch)/2, cw, ch)
        if (W0, H0) != (VW, VH): fr = unsharp(fr, 0.4)
        if b.get('scrim'):
            # A soft dark gradient behind the caption band. On his phone-on-marble clip the goal photo's pool deck and
            # green shorts fill the band with thousands of pixels within 40 levels of the lime highlight (measured:
            # 3,600-4,300 of 6,400-7,500 green px), so neither a viewer nor caption_sync_check could find the lit word
            # (2026-09-10: 3 of the cutdown's 4 misses). 0 -> 0.65 over y 1200-1370, held to 1560, easing to 0.40.
            fr = (fr.astype(np.float32) * SCRIM[:, None, None]).astype(np.uint8)
        if b.get('label'):
            # above his CTA bar and off the face
            im = Image.fromarray(fr).convert('RGBA'); G.ai_label(im, VW-44, 1180, size=54); fr = np.asarray(im.convert('RGB'))
        yield fr
    rd.close()

def r_app(b, base):
    rd = Reader(b['media']); n = b['n1']-b['n0']
    PH = 1520; PW = round(PH*rd.w/rd.h); x0 = (VW-PW)//2; y0 = 110
    mask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW-1, PH-1], radius=44, fill=255)
    for i in range(n):
        f = Image.fromarray(rd.read()).resize((PW, PH), Image.LANCZOS)
        im = G.field(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([x0-9, y0-9, x0+PW+8, y0+PH+8], radius=52, fill=(0, 0, 0, 255))
        im.paste(f, (x0, y0), mask)
        yield np.asarray(im.convert('RGB'))
    rd.close()

def r_appres(b, base):
    """The app's result as a PLAIN result card: the after image alone (assets/after_still.png, the photo cut out of the
    app recording with nothing of the email screen around it), in his black-bordered card with a slow push, under his
    "Final Result AI" label. The first build showed the screen itself cropped above the form; the independent audit
    (2026-09-10) found its heading and confetti still made it recognisably the banned email-capture screen."""
    pil = still(b['media']); n = b['n1']-b['n0']
    for i in range(n):
        w = round(660 + 20*i/max(1, n-1))
        im = G.field(); box = G.card_on(im, pil, VW/2, 690, w)
        # the app's after image is an AI result: standing rule, burned label (his style), bottom-right, off the face
        G.ai_label(im, box[2]-18, box[3]-14, size=44)
        yield np.asarray(im.convert('RGB'))

def r_png(b, base):
    pil = still(b['media']); n = b['n1']-b['n0']
    crop = pil.crop((0, 0, pil.width, 2040))
    for i in range(n):
        w = round(660 + 24*i/max(1, n-1))
        im = G.field(); G.card_on(im, crop, VW/2, 90 + round(w*2040/900)/2, w, border=8)
        yield np.asarray(im.convert('RGB'))

def r_title1(b, base):
    cues = [(c - b['n0'])/FPS for c in B.TITLE1_CUES]
    fo0, fo1 = [(c - b['n0'])/FPS for c in B.TITLE1_FADEOUT]
    for i in range(b['n1']-b['n0']):
        t = i/FPS
        fr = np.asarray(G.title_visualizing(t, cues).convert('RGB')).astype(np.float32)
        if t > fo0:
            k = G.ease_in_out(min(1, (t-fo0)/(fo1-fo0)))
            fr = fr*(1-k) + np.array(G.FIELD, np.float32)*k
        yield fr.astype(np.uint8)

def r_title2(b, base):
    for i in range(b['n1']-b['n0']): yield np.asarray(G.title_free(i/FPS).convert('RGB'))

def r_end(b, base):
    for i in range(b['n1']-b['n0']): yield np.asarray(G.endcard(i/FPS, b['t_second']).convert('RGB'))

R = dict(talk=r_talk, split=r_split, card=r_card, cardv=r_cardv, bleed=r_bleed, bleedv=r_bleedv, app=r_app,
         appres=r_appres, png=r_png, title1=r_title1, title2=r_title2, end=r_end)

# ------------------------------------------------------------------ overlays
_OVC = {}
def overlay_img(o, n):
    t = (n - o['n0'])/FPS; dur = (o['n1'] - o['n0'])/FPS
    # an overlay's image is cached once it has SETTLED -- after its LAST element has drawn on. The problem lower third
    # draws its subtitle 1.83 s in; settling it at 0.45 s baked "No Time, No Motivation." out of 4.96 s of the beat
    # (independent audit, 2026-09-10), so it settles on its subtitle like the checklist settles on its last item
    settle = 0.45
    if o['kind'] == 'checklist': settle = max((x - o['n0'])/FPS for x in o['items']) + 0.45
    elif o['kind'] == 'problem': settle = (o['sub'] - o['n0'])/FPS + 0.45
    key = (id(o), round(t, 3) if (t < settle or t > dur - 0.2) else 'settled')
    if key in _OVC: return _OVC[key]
    k = o['kind']
    if k == 'checklist': im = G.checklist(t, [(x - o['n0'])/FPS for x in o['items']], dur)
    elif k == 'problem': im = G.problem_lt(t, (o['sub'] - o['n0'])/FPS, dur)
    elif k == 'ifyousaw': im = G.ifyousaw_lt(t, dur)
    elif k == 'num': im = G.num_lt(t, o['num'], o['text'], dur)
    elif k == 'cta': im = G.cta_bar(t, dur)
    elif k == 'final': im = G.final_label(t, dur)
    else: raise ValueError(k)
    if len(_OVC) > 400: _OVC.clear()
    _OVC[key] = im
    return im

# ------------------------------------------------------------------ captions (the gated layout: captions.py)
def caption_schedule(path='cap/list.txt'):
    """(start, end, png) from cap/list.txt -- the exact states captions.py rendered, so the burned captions are the
    ones caption_sync_check.py measures against."""
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

# ------------------------------------------------------------------ main loop
def stills(ns, outdir):
    """Render only the listed frames to PNG (full resolution) for inspection -- beats with no requested frame are
    skipped; the base is decoded sequentially up to each talk frame."""
    os.makedirs(outdir, exist_ok=True)
    base_rd = Reader('base.mp4'); cur = [-1, None]
    def base(n):
        while cur[0] < n:
            cur[1] = base_rd.read(); cur[0] += 1
        return cur[1]
    want = set(ns)
    for b in tl:
        hit = [n for n in range(b['n0'], b['n1']) if n in want]
        if not hit: continue
        gen = R[b['kind']](b, base)
        for n in range(b['n0'], max(hit)+1):
            fr = next(gen)
            if n not in want: continue
            fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
            for o in ov:
                if o['n0'] <= n < o['n1']: fr = compose(fr, overlay_img(o, n))
            c = caption_at(n)
            if c is not None: fr = compose(fr, c)
            if n in FLASH: fr = np.asarray(G.flash(fr, B.FLASH_K))
            Image.fromarray(fr).save(f'{outdir}/f{n:05d}.png')
        gen.close(); close_media_readers(base_rd)
    base_rd.close()

def cutdown(planfile, out):
    """The <=0:59: HIS master frames, range by range (cut_plan.json), with the cutdown's own captions (cut/cap, re-timed
    through the audio windows) and the cutdown's crop (cut/crop.json: talk-to-talk seams flipped FAR<->NEAR)."""
    global CROP, CAPS
    P = json.load(open(planfile))
    CC = {int(k): v for k, v in json.load(open('cut/crop.json'))['frames'].items()}
    m2c = {}
    for p in P:
        for n in range(p['p0'], p['p1']): m2c[n] = p['c0'] + n - p['p0']
    CROP = {n: CC[c] for n, c in m2c.items() if c in CC}
    CAPS = caption_schedule('cut/cap/list.txt')
    base_rd = Reader('base.mp4'); cur = [-1, None]
    def base(n):
        while cur[0] < n:
            cur[1] = base_rd.read(); cur[0] += 1
        return cur[1]
    enc = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{VW}x{VH}',
                            '-r', '24', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709',
                            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', out],
                           stdin=subprocess.PIPE)
    written = 0
    for p in P:
        for b in tl:
            a, z = max(p['p0'], b['n0']), min(p['p1'], b['n1'])
            if a >= z: continue
            # a talk frame depends only on its frame number, so its generator starts AT the range (a talk beat the
            # cutdown re-enters for a later range would otherwise walk frames that are in no range and have no crop);
            # every other beat is animated from its own first frame, so it is played from there and skipped to `a`
            bb = dict(b, n0=a) if b['kind'] == 'talk' else b
            gen = R[b['kind']](bb, base)
            for n in range(bb['n0'], z):
                fr = next(gen)
                if n < a: continue
                fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
                for o in ov:
                    if o['n0'] <= n < o['n1'] and (o['kind'] == 'cta' or o['n0'] >= p['p0']):
                        fr = compose(fr, overlay_img(o, n))
                c = caption_at(m2c[n])
                if c is not None: fr = compose(fr, c)
                if n in FLASH: fr = np.asarray(G.flash(fr, B.FLASH_K))
                enc.stdin.write(np.ascontiguousarray(fr).tobytes()); written += 1
            gen.close(); close_media_readers(base_rd)
    enc.stdin.close(); enc.wait(); base_rd.close()
    got = int(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-count_frames',
                              '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip())
    print(f'{out}: {got} frames written / {P[-1]["c1"]} planned'); assert got == written == P[-1]['c1']

def main():
    if '--stills' in args:
        stills([int(x) for x in arg('--stills', '').split(',')], arg('--dir', 'stills')); return
    if '--cutplan' in args:
        cutdown(arg('--cutplan', 'cut_plan.json'), arg('--out', 'cut/picture.mp4')); return
    base_rd = Reader('base.mp4')
    cur = [-1, None]
    def base(n):
        while cur[0] < n:
            cur[1] = base_rd.read(); cur[0] += 1
        return cur[1]
    ow, oh = (540, 960) if PREVIEW else (VW, VH)
    enc = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{ow}x{oh}',
                            '-r', '24', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                            '-c:v', 'libx264', '-preset', 'veryfast' if PREVIEW else 'slow', '-crf', '20' if PREVIEW else '15',
                            '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                            '-color_range', 'tv', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    written = 0
    for b in tl:
        if b['n1'] <= N0 or b['n0'] >= N1: continue
        gen = R[b['kind']](b, base)
        for n in range(b['n0'], b['n1']):
            fr = next(gen)
            if n < N0 or n >= N1: continue
            fr = np.ascontiguousarray(fr, dtype=np.uint8).copy()
            assert fr.shape == (VH, VW, 3), (b['kind'], n, fr.shape)
            for o in ov:
                if o['n0'] <= n < o['n1']: fr = compose(fr, overlay_img(o, n))
            c = caption_at(n)
            if c is not None: fr = compose(fr, c)
            if n in FLASH: fr = np.asarray(G.flash(fr, B.FLASH_K))
            if PREVIEW: fr = cv2.resize(fr, (ow, oh), interpolation=cv2.INTER_AREA)
            enc.stdin.write(np.ascontiguousarray(fr).tobytes()); written += 1
            if n % 240 == 0: print(f'  frame {n} ({n/FPS:6.2f}s) {b["kind"]}', flush=True)
        gen.close(); close_media_readers(base_rd)
    enc.stdin.close(); enc.wait(); base_rd.close()
    want = min(N1, NTOT) - N0
    got = int(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-count_frames',
                              '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', OUT], capture_output=True, text=True).stdout.strip())
    print(f'{OUT}: {got} frames written / {want} planned')
    assert got == want == written, (got, want, written)

if __name__ == '__main__':
    main()
