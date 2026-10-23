"""DS-44 R1 assembly: one RGB pass over the film timeline -> base.mp4 (no graphics) + composite.mp4 (graphics in), then the master
with burned captions and the chosen mix, the phone review copy and the SRT.
  S0  the clip full screen (fixed vertical window per camera shot, on the speaker), Dan keyed small in the bottom-left corner
  TR  16 frames: the clip shrinks toward the top and fades, Dan grows from the corner into the W window (Soft Blue field)
  talk shots: keyed C1730 from the 0.75 cache (key/c2_A, c2_B), per-frame windows from framing-frames.json, on the Soft Blue field
  K1  the caller from the clip, full screen (his silent thinking beat)
  B1  library A0197 (AI, 9:16) full screen + the AI-GENERATED chip;  B2  library B0351 (stock) vertical window on the pen
Keyed layers: the house key's stage 2 (DS-40 Claude R2 stage2_comp.py) despeckle, haze clip, grade, light wrap, with its pixel
distances scaled x1.5 for the 0.75 cache (fragments >= 900 px, 4 px edge zone, haze beyond 4.5 px); wrap 0.12, sigma 10 at output.
usage: assemble.py [--voice house_bass15] [--look B_warmvivid] [--stills 12.0,30.5,...] [--mux-only] [--pink]"""
from pathlib import Path
import json, subprocess, sys, hashlib, re, os
import numpy as np, cv2
from scipy import ndimage as ndi
from multiprocessing import Pool
W = Path(__file__).resolve().parents[1]; RC = Path(__file__).resolve().parent; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); sys.path.insert(0, str(HF.parent)); sys.path.insert(0, str(RC))
import composite as CM, buildcap, softblue as B
from grade import grade, LOOKS
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
NAME = 'Hormozi Fat Guy SFC R2'; Q = W/'review'; Q.mkdir(exist_ok=True)
args = sys.argv[1:]
VOICE = args[args.index('--voice') + 1] if '--voice' in args else 'house_bass15'
LOOK = args[args.index('--look') + 1] if '--look' in args else 'B_warmvivid'
STILLS = [float(x) for x in args[args.index('--stills') + 1].split(',')] if '--stills' in args else None
PINK = '--pink' in args
edl = json.load(open(W/'edl.json')); shots = json.load(open(W/'shots.json'))
crops = json.load(open(W/'framing-frames.json')); man = json.load(open(W/'graphics-manifest.json')) if (W/'graphics-manifest.json').exists() else []
TOTAL = edl['total_frames']; fr = lambda t: int(round(t*FPS))
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
CLIPS = {'A0197': LIB + '/04 AI-Generated Clips/concepts-and-gags/A0197_man-on-analog-scale-needle-swings-metronome_9x16_6s.mp4',
         'B0351': LIB + '/03 B-Roll - Real Footage/stock/other/B0351_hands-hold-insulin-pen-blue-backdrop_16x9_12s.mp4'}
KEYS = {p: W/'key'/f'c2_{p}' for p in ('watch', 'watchF', 'A0', 'A', 'B')}
KSTART = dict(edl['key'], watchF=2192.30); RMC = edl['clip']['roll_minus_clip']
CLIPF = edl['clip']['file']; CL0 = 30.0          # clip frames cached from 30.0 s (24 fps) of the clip file
MIN_FRAG, EDGE, HAZE = 900, 4, 4.5
WRAP, WRAP_SIG = 0.12, 10
CW, CH = 1080, 1920
CHIP_XY = (40, 120)     # AI-GENERATED on A0197: top-left, on the bathroom wall above the man's head (checked on the person mask)

# ---------- keyed layer (house stage 2, scaled for the 0.75 cache)
def key_frame(piece, t_roll):
    i = int(round((t_roll - KSTART[piece])*FPS)); p = KEYS[piece]/f'f{i:04d}.npy'
    d = np.load(p).astype(np.float32); Fp, a = d[..., :3], d[..., 3]
    lab, n = ndi.label(a > 0.03)
    if n:
        sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= MIN_FRAG
        m = ndi.binary_dilation(keep[lab], iterations=EDGE)
        a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
    far = ndi.distance_transform_edt(a < 0.25) > HAZE
    a_new = np.where(far, np.clip((a - 0.15)/0.85, 0, 1), a)
    Fp = Fp*np.where(a > 1e-4, a_new/np.maximum(a, 1e-4), 0)[..., None]
    return Fp, a_new                                   # premultiplied, 1620 x 2618

EDGE, FEATHER = 54, 180      # option B's soft right edge (DS-40 R4: 36 / 120 px at 0.5 scale) in 0.75-cache px
def feather(Fp, a, fw=EDGE, amount=1.0):
    """Fade the keyed footage toward its right and top edges, for the small Dan whose frame edge sits inside the screen
    (a hand or shoulder that leaves the camera fades instead of stopping on a straight line). Premultiplied."""
    if amount <= 0: return Fp, a
    h, w = a.shape
    rx = np.clip((w - 1 - np.arange(w, dtype=np.float32))/max(fw, 1.0), 0, 1); ry = np.clip(np.arange(h, dtype=np.float32)/FEATHER, 0, 1)
    ramp = 1 - amount + amount*(rx[None, :]*ry[:, None])
    return Fp*ramp[..., None], a*ramp

ELBOW = (138, 222, 8)        # R2 review: frames where his left elbow reaches the camera's edge (4.6-7.4 s), plus ramp frames
def elbow_fw(g):
    """Right-edge fade width for clip-phase frame g: option B's wide fade (FEATHER) while the elbow sits on the camera edge,
    the narrow EDGE elsewhere (DS-40 R4 comp_opening.shrug_fw), so the arm never ends on a straight line."""
    a_, b_, r = ELBOW
    w = min(1.0, max(0.0, (g - (a_ - r))/r), max(0.0, ((b_ + r) - g)/r))
    return EDGE + (FEATHER - EDGE)*w

def place(out, Fp, a, s, x0, y0, wrap=WRAP, wrap_sig=WRAP_SIG):
    """Composite a premultiplied keyed layer scaled by s with its top-left at (x0, y0) (output px); grade after the resize."""
    h, w = a.shape
    sw, sh = max(1, int(round(w*s))), max(1, int(round(h*s)))
    # crop to the visible part first (cheaper), with a small margin for the resize
    vx0, vy0 = max(0, int(np.floor(-x0/s)) - 2), max(0, int(np.floor(-y0/s)) - 2)
    vx1, vy1 = min(w, int(np.ceil((CW - x0)/s)) + 2), min(h, int(np.ceil((CH - y0)/s)) + 2)
    if vx1 <= vx0 or vy1 <= vy0: return out
    Fc, ac = Fp[vy0:vy1, vx0:vx1], a[vy0:vy1, vx0:vx1]
    ox, oy = x0 + vx0*s, y0 + vy0*s
    tw, th = max(1, int(round((vx1 - vx0)*s))), max(1, int(round((vy1 - vy0)*s)))
    interp = cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC
    Fr = cv2.resize(Fc, (tw, th), interpolation=interp); ar = np.clip(cv2.resize(ac, (tw, th), interpolation=interp), 0, 1)
    Fr = np.clip(Fr, 0, None)
    G = np.where(ar[..., None] > 0.01, Fr/np.maximum(ar[..., None], 1e-3), 0)
    G = grade(np.clip(G, 0, 1), **LOOKS[LOOK]) if LOOK != 'none' else G
    X0, Y0 = int(round(ox)), int(round(oy)); X1, Y1 = min(CW, X0 + tw), min(CH, Y0 + th)
    sx, sy = max(0, -X0), max(0, -Y0); X0, Y0 = max(0, X0), max(0, Y0)
    if X1 <= X0 or Y1 <= Y0: return out
    ga = G[sy:sy + Y1 - Y0, sx:sx + X1 - X0]; aa = ar[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    reg = out[Y0:Y1, X0:X1]; A = aa[..., None]; comp = ga*A + reg*(1 - A)
    if wrap:
        sg = max(2.0, wrap_sig*min(1.0, s/0.87)); inv = 1 - aa
        bb = cv2.GaussianBlur(reg*inv[..., None], (0, 0), sg); cover = cv2.GaussianBlur(inv, (0, 0), sg)[..., None]
        wm = wrap*cover*A; comp = comp*(1 - wm) + bb/np.maximum(cover, 1e-3)*wm
    out[Y0:Y1, X0:X1] = comp
    return out

def field(t):
    if PINK: return np.ones((CH, CW, 3), np.float32)*np.array([0.95, 0.25, 0.62], np.float32)
    return np.asarray(B.field(t, CW, CH).convert('RGB')).astype(np.float32)/255

# ---------- the clip
_clip = None
def clip_frame(t):
    global _clip
    if _clip is None: _clip = np.load(W/'src/clip_30-52_24fps.npy', mmap_mode='r')
    k = int(np.floor((t - CL0)*24 + 1e-6)); return _clip[min(max(k, 0), _clip.shape[0] - 1)].astype(np.float32)/255
def cam_at(t):
    cams = shots[0]['cams']
    return next(c for c in cams if c['a'] <= t + 1e-6 < c['b'])
def clip_view(t, w=CW, h=CH):
    """The clip's frame at clip time t in the camera shot's fixed vertical window, resized to w x h (gentle unsharp when enlarged)."""
    fr_ = clip_frame(t); x0, y0, cw, ch = cam_at(t)['crop']
    M = np.array([[w/cw, 0, -x0*w/cw], [0, h/ch, -y0*h/ch]], np.float32)
    v = cv2.warpAffine(fr_, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    if w/cw > 1.5:
        bl = cv2.GaussianBlur(v, (0, 0), 1.6); v = np.clip(v + 0.45*(v - bl), 0, 1)
    return v

# ---------- B-roll
def broll_grade(x, clip):
    """VIDEO-RULES 2026-10-11: every B-roll is graded to sit with the presenter. Measured per clip (grade_broll in notes)."""
    g = GB.get(clip)
    if not g: return x
    f = np.clip(x, 0, 1)**g['gamma']; y = (f*np.array([.2126, .7152, .0722], np.float32)).sum(-1, keepdims=True)
    f = y + g['sat']*(f - y); f = f*np.array(g['rgb'], np.float32)
    return np.clip(f, 0, 1)
GB = json.load(open(W/'broll-grade.json')) if (W/'broll-grade.json').exists() else {}
_br = {}
def broll(clip, t):
    if clip not in _br: _br[clip] = np.load(W/f'src/{clip}_30fps.npy', mmap_mode='r')
    a = _br[clip]; return a[min(int(round(t*FPS)), a.shape[0] - 1)].astype(np.float32)/255
def chip_layer():
    from PIL import Image, ImageDraw
    base = Image.new('RGB', (CW, CH), (0, 0, 0)); wh = Image.new('RGB', (CW, CH), (255, 255, 255))
    xy = tuple(next(s for s in shots if s['id'] == 'B1').get('chip', CHIP_XY))
    B.disclosure(base, 'AI-GENERATED', xy, 1.6, anchor='lt', size=23); B.disclosure(wh, 'AI-GENERATED', xy, 1.6, anchor='lt', size=23)
    x = np.asarray(base).astype(np.float32)/255; y = np.asarray(wh).astype(np.float32)/255
    al = 1 - (y - x).max(2).clip(0, 1); col = np.where(al[..., None] > 0, x/np.maximum(al[..., None], 1e-3), 0)
    return col, al
CHIP = None

def render(g):
    """frame g of the film, float RGB 0..1, no graphics"""
    global CHIP
    s = next(x for x in shots if x['n0'] <= g < x['n1']); j = g - s['n0']; t = g/FPS
    if s['kind'] == 'clip':
        seg = next(x for x in edl['clip']['segs'] if x['n0'] <= g < x['n0'] + x['frames'])
        tc = seg['clip_in'] + (g - seg['n0'])/FPS
        out = np.ones((CH, CW, 3), np.float32)*np.array([0.95, 0.25, 0.62], np.float32) if PINK else clip_view(tc)
        Fp, a = key_frame('watchF', tc + RMC); c = s['corner']
        Fp, a = feather(Fp, a, fw=elbow_fw(g))
        return place(out, Fp, a, c['scale'], c['x0'], c['y0'])
    if s['kind'] == 'transition':
        tc = edl['tr']['clip_in'] + j/FPS; u = (j + 1)/(s['n1'] - s['n0']); u = u*u*(3 - 2*u)
        out = field(t)
        if not PINK:
            # R2: the clip shrinks from full screen into the card at the top (its own 9:16 window easing to the full 16:9 frame)
            x, y, w, h = s['card']; X = u*x; Y = u*y; Wd = CW + (w - CW)*u; Hd = CH + (h - CH)*u
            # the largest window of the card's current shape, on the speaker's face (9:16 at u=0 easing to the full 16:9 frame)
            A_ = Wd/Hd; chh = 1080.0 if A_ <= 1920/1080 else 1920/A_; cww = chh*A_
            cx_ = float(np.clip(cam_at(tc)['face_x'], cww/2, 1920 - cww/2)); fr_ = clip_frame(tc)
            win = fr_[int(round(540 - chh/2)):int(round(540 + chh/2)), int(round(cx_ - cww/2)):int(round(cx_ + cww/2))]
            img = cv2.resize(win, (int(round(Wd)), int(round(Hd))), interpolation=cv2.INTER_AREA if Wd < cww else cv2.INTER_CUBIC)
            out = draw_card(out, img, (X, Y, Wd, Hd), r=22*u, shadow=u)
        Fp, a = key_frame('watchF', tc + RMC); c, d = s['corner'], s['target']
        Fp, a = feather(Fp, a, amount=1 - u)
        sc = c['scale'] + (d['scale'] - c['scale'])*u
        return place(out, Fp, a, sc, c['x0'] + (d['x0'] - c['x0'])*u, c['y0'] + (d['y0'] - c['y0'])*u)
    if s['kind'] == 'talk':
        pc = next(p for p in edl['pieces'] if p['id'] == s['piece']); t_roll = pc['start'] + (g - pc['n0'])/FPS
        x, y, cw, ch = crops[s['id']][j]; sc = CW/cw
        Fp, a = key_frame(s['piece'], t_roll)
        bg = field(t)
        if s.get('card') and not PINK: bg = draw_card(bg, card_frame(card_time(g)), s['card'])
        return place(bg, Fp, a, sc, -x*sc, -y*sc)
    if s['kind'] == 'clipcut':
        return clip_view(s['clip_in'] + j/FPS)
    if s['kind'] == 'broll':
        f = broll(s['clip'], s['src_t0'] + j/FPS)
        f = broll_grade(f, s['clip'])
        if s.get('ai'):
            if CHIP is None: CHIP = chip_layer()
            col, al = CHIP; f = f*(1 - al[..., None]) + col*al[..., None]
        return f
    raise ValueError(s)

_card = None
def card_frame(tc):
    global _card
    if _card is None: _card = np.load(W/'src/card_58-74_24fps.npy', mmap_mode='r')
    return _card[min(int(np.floor(tc*24 + 1e-6)), _card.shape[0] - 1)].astype(np.float32)/255
from PIL import Image as _Im, ImageDraw as _Dr
def _rr(w, h, r):
    m = _Im.new('L', (max(1, w), max(1, h)), 0); _Dr.Draw(m).rounded_rectangle((0, 0, max(1, w) - 1, max(1, h) - 1), max(0, int(r)), fill=255)
    return np.asarray(m, np.float32)[..., None]/255
def draw_card(out, img, rect, r=22, shadow=1.0):
    """A 16:9 picture as a rounded card with a soft shadow and a hairline Soft Blue border (the DS-40 R3 card)."""
    x, y, w, h = [int(round(v)) for v in rect]
    if w < 4 or h < 4: return out
    if shadow > 0:
        sh = np.zeros(out.shape[:2], np.float32); sh[max(0, y + 14):y + 14 + h, max(0, x + 6):x + 6 + w] = 0.59*shadow
        out *= 1 - cv2.GaussianBlur(sh, (0, 0), 18)[..., None]
    if img.shape[:2] != (h, w): img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    m = _rr(w, h, r); X0, Y0, X1, Y1 = max(0, x), max(0, y), min(CW, x + w), min(CH, y + h)
    sx, sy = X0 - x, Y0 - y; reg = out[Y0:Y1, X0:X1]; mm = m[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    out[Y0:Y1, X0:X1] = img[sy:sy + Y1 - Y0, sx:sx + X1 - X0]*mm + reg*(1 - mm)
    b = np.zeros((h, w, 1), np.float32); bm = _rr(w, h, r) - np.pad(_rr(w - 4, h - 4, r - 2), ((2, 2), (2, 2), (0, 0)))
    bc = np.array([150, 200, 255], np.float32)/255; ba = np.clip(bm, 0, 1)*0.47
    reg = out[Y0:Y1, X0:X1]; bb = ba[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    out[Y0:Y1, X0:X1] = reg*(1 - bb) + bc*bb
    return out
CARD_SHOTS = [x for x in shots if x.get('card') and x['kind'] == 'talk']
def card_time(g):
    """seconds of interview shown so far in the card (it only advances while the card is on screen)"""
    t = 0.0
    for x in CARD_SHOTS:
        if g >= x['n1']: t += (x['n1'] - x['n0'])/FPS
        elif g >= x['n0']: return t + (g - x['n0'])/FPS
    return t

def u8(x): return (np.clip(x, 0, 1)*255 + 0.5).astype(np.uint8)
C = CM.Compositor(man, wh=(CW, CH)) if man else None
def gfx(f8, g): return C.apply(f8.copy(), g) if C else f8

if __name__ == '__main__':
    if STILLS:
        (W/'stills').mkdir(exist_ok=True)
        for t in STILLS:
            g = fr(t); f8 = u8(render(g))
            cv2.imwrite(str(W/'stills'/f'g{g:05d}{"_pink" if PINK else ""}.png'), cv2.cvtColor(gfx(f8, g), cv2.COLOR_RGB2BGR))
        print('STILLS', [fr(t) for t in STILLS]); sys.exit()
    comp = W/('composite_pink.mp4' if PINK else 'composite.mp4'); base = W/'base.mp4'
    MUX_ONLY = '--mux-only' in args and comp.exists() and base.exists()
    enc = lambda p: subprocess.Popen([F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-framerate', '30000/1001', '-i', '-', '-an',
                                       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15',
                                       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(p)], stdin=subprocess.PIPE)
    if not MUX_ONLY:
        pc_ = enc(comp); pb_ = None if PINK else enc(base); n = 0
        with Pool(int(os.environ.get('WORKERS', '5'))) as pool:
            for f in pool.imap(render, range(TOTAL), chunksize=4):
                f8 = u8(f)
                if pb_: pb_.stdin.write(f8.tobytes())
                pc_.stdin.write(np.ascontiguousarray(gfx(f8, n)).tobytes()); n += 1
                if n % 150 == 0: print(n, 'frames', flush=True)
        for p in (pc_, pb_):
            if p: p.stdin.close(); assert p.wait() == 0
        assert n == TOTAL
    if PINK: print('PINK DONE', comp); sys.exit()
    master = Q/f'{NAME} - complete Short.mp4'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-i', str(comp), '-i', str(W/f'mix-{VOICE}.wav'), '-map', '0:v', '-map', '1:a', '-vf', f"ass='{W}/captions.ass'",
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-frames:v', str(TOTAL),
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', str(master)], check=True)
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-i', str(master), '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-c:a', 'aac', '-b:a', '160k',
                    '-movflags', '+faststart', str(Q/f'{NAME} - REVIEW 540p.mp4')], check=True)
    def secs(x): h, m, s_ = x.split(':'); return int(h)*3600 + int(m)*60 + float(s_)
    def stamp(x): ms = round(x*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    cues = []
    for line in (W/'captions.ass').read_text().splitlines():
        if line.startswith('Dialogue:'): f_ = line.split(',', 9); cues.append((secs(f_[1]), secs(f_[2]), re.sub(r'\{[^}]*\}', '', f_[9])))
    (Q/f'{NAME}.srt').write_text(''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(cues)))
    print('FINISHED', hashlib.sha256(master.read_bytes()).hexdigest(), flush=True)
