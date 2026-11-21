"""DS-43 R1 assembly for ONE version: one RGB pass over the film timeline -> base.mp4 (no graphics) + composite.mp4 (graphics
in), then the master with burned captions and the chosen mix, the phone review copy and the SRT.
    python3 assemble.py scripted|offcuff [--voice house_bass15] [--stills 1.0,5.0,...] [--mux-only] [--pink]
Shots (framing.py): S0 clip full screen + Dan's corner; PW titled panel + Dan large watching; PR the same panel, clip silent,
Dan's response; talk on the moving Soft Blue field; broll (AI chip where AI); still (the clip's photo of Terry, slow push-in).
Keyed layers: the house key's stage 2 finishing (DS-44 recipe, scaled for the 0.75 cache), Codex R5 warm grade on Dan only,
light wrap. The clip keeps its own BT.709 decode (no grade), as R5."""
from pathlib import Path
import json, subprocess, sys, hashlib, re, os
import numpy as np, cv2
from scipy import ndimage as ndi
from multiprocessing import Pool
W = Path(__file__).resolve().parents[1]; RC = Path(__file__).resolve().parent; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); sys.path.insert(0, str(HF.parent)); sys.path.insert(0, str(RC))
import composite as CM, softblue as B
from grade import grade_r5_warm
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
VERSION = sys.argv[1]; O = W/VERSION
NAME = {'scripted': 'Terry Crews Fasting SFC R2 - scripted', 'offcuff': 'Terry Crews Fasting SFC R2 - off the cuff'}[VERSION]
Q = O/'review'; Q.mkdir(exist_ok=True)
args = sys.argv[2:]
VOICE = args[args.index('--voice') + 1] if '--voice' in args else 'house_bass15'
STILLS = [float(x) for x in args[args.index('--stills') + 1].split(',')] if '--stills' in args else None
PINK = '--pink' in args
edl = json.load(open(O/'edl.json')); shots = json.load(open(O/'shots.json'))
crops = json.load(open(O/'framing-frames.json')); man = json.load(open(O/'graphics-manifest.json')) if (O/'graphics-manifest.json').exists() else []
TOTAL = edl['total_frames']; fr = lambda t: int(round(t*FPS))
KP = dict(scripted='S', offcuff='O')[VERSION]
KEYS = {'watchF': W/'key'/'c2_watchF', 'T': W/'key'/f'c2_{KP}'}
KSTART = dict(watchF=edl['key']['watchF'], T=edl['key']['T']); RMC = edl['clip']['roll_minus_clip']
SILENT0 = edl['clip']['panel_silent_from']; CL0 = 0.0
MIN_FRAG, EDGE, HAZE = 900, 4, 4.5
WRAP, WRAP_SIG = 0.12, 10
CW, CH = 1080, 1920
PLATE = CM.Compositor(json.load(open(O/'plate-manifest.json')), wh=(CW, CH)) if (O/'plate-manifest.json').exists() else None
HOLE = (0, 92, 1080, 608)
def u8(x): return (np.clip(x, 0, 1)*255 + 0.5).astype(np.uint8)
def plate_under(base, g):
    """base: float RGB with the media in the hole; returns the plate (moving field, title, frame) over it"""
    return PLATE.apply(u8(base), g).astype(np.float32)/255

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
    return Fp, a_new

FEDGE, FEATHER = 54, 180     # the corner's soft right/top edge (DS-44 option B) in cache px
def feather(Fp, a, fw=FEDGE):
    """Fade the small corner Dan toward the camera's right and top edges (a hand leaving the camera fades, never a straight line)."""
    h, w = a.shape
    rx = np.clip((w - 1 - np.arange(w, dtype=np.float32))/max(fw, 1.0), 0, 1); ry = np.clip(np.arange(h, dtype=np.float32)/FEATHER, 0, 1)
    ramp = rx[None, :]*ry[:, None]
    return Fp*ramp[..., None], a*ramp
def corner_fw(Fp, a):
    """R5: the right-edge fade widens only while a hand or arm reaches the camera edge (alpha in the last 40 px columns)"""
    edge = float((a[:, -40:] > 0.5).mean())
    return FEDGE + (FEATHER - FEDGE)*min(1.0, edge*12)

def place(out, Fp, a, s, x0, y0, wrap=WRAP, wrap_sig=WRAP_SIG):
    """Composite a premultiplied keyed layer scaled by s with its top-left at (x0, y0) (output px); grade after the resize."""
    h, w = a.shape
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
    G = grade_r5_warm(np.clip(G, 0, 1))
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
_clip = None; _lid = None
CLIP_FPS = 24000/1001
def clip_frame(t):
    global _clip
    if _clip is None: _clip = np.load(W/'src/clip_0-32_24fps.npy', mmap_mode='r')
    k = int(np.floor((t - CL0)*CLIP_FPS + 1e-6))
    if k >= SILENT_K0:                         # the silent panel's frames (clip from frame 576, src/clip_silent_24fps.npy)
        global _silent
        if _silent is None: _silent = np.load(W/'src/clip_silent_24fps.npy', mmap_mode='r')
        return _silent[min(k - SILENT_K0, _silent.shape[0] - 1)].astype(np.float32)/255
    return _clip[min(max(k, 0), _clip.shape[0] - 1)].astype(np.float32)/255
SILENT_K0 = 576; _silent = None
def clip_view(t):
    """the clip at clip time t in the S0 portrait window, 1080 x 1920 (gentle unsharp: enlarged 1.78x)"""
    fr_ = clip_frame(t); x0, y0, cw, ch = shots[0]['cams'][0]['crop']
    M = np.array([[CW/cw, 0, -x0*CW/cw], [0, CH/ch, -y0*CH/ch]], np.float32)
    v = cv2.warpAffine(fr_, M, (CW, CH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    bl = cv2.GaussianBlur(v, (0, 0), 1.6); return np.clip(v + 0.45*(v - bl), 0, 1)
def panel_bg(tc, g):
    """the plate with the clip (clip time tc) full width in its hole, 1080 x 608 (full 16:9 height)"""
    base = np.zeros((CH, CW, 3), np.float32); x_, y_, w_, h_ = HOLE
    base[y_:y_ + h_, x_:x_ + w_] = cv2.resize(clip_frame(tc), (w_, h_), interpolation=cv2.INTER_AREA)
    return plate_under(base, g) if PLATE else base

_reel = None
REEL0 = next(x['n0'] for x in shots if x['id'] == 'PR')
def reel_bg(g):
    """R2: the plate with the Terry flex reel in its hole (src/flex_reel.npy, one frame per film frame from PR on)"""
    global _reel
    if _reel is None: _reel = np.load(W/'src/flex_reel.npy', mmap_mode='r')
    base = np.zeros((CH, CW, 3), np.float32); x_, y_, w_, h_ = HOLE
    base[y_:y_ + h_, x_:x_ + w_] = _reel[min(g - REEL0, _reel.shape[0] - 1)].astype(np.float32)/255
    return plate_under(base, g) if PLATE else base

# ---------- B-roll and the still
def broll_grade(x, clip):
    """VIDEO-RULES 2026-10-11: every B-roll is graded to sit with the presenter (measured per clip, broll-grade.json)"""
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
_still = None
def still(u):
    """the NYSE photo, pushing in from 100 % to 108 % over the shot (u 0..1), centred high so his head stays in frame"""
    global _still
    if _still is None: _still = np.load(W/'src/NYSE.npy')[0].astype(np.float32)/255
    z = 1.0 + 0.08*u; cx, cy = CW/2, CH*0.30
    M = np.array([[z, 0, cx - z*cx], [0, z, cy - z*cy]], np.float32)
    return cv2.warpAffine(_still, M, (CW, CH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
CHIP_XY = {'A0210': (40, 120), 'A0086': (40, 120)}
def chip_layer(xy):
    from PIL import Image
    base = Image.new('RGB', (CW, CH), (0, 0, 0)); wh = Image.new('RGB', (CW, CH), (255, 255, 255))
    B.disclosure(base, 'AI-GENERATED', xy, 1.6, anchor='lt', size=23); B.disclosure(wh, 'AI-GENERATED', xy, 1.6, anchor='lt', size=23)
    x = np.asarray(base).astype(np.float32)/255; y = np.asarray(wh).astype(np.float32)/255
    al = 1 - (y - x).max(2).clip(0, 1); col = np.where(al[..., None] > 0, x/np.maximum(al[..., None], 1e-3), 0)
    return col, al
CHIPS = {}

def render(g):
    """frame g of the film, float RGB 0..1, no graphics"""
    s = next(x for x in shots if x['n0'] <= g < x['n1']); j = g - s['n0']; t = g/FPS
    if s['kind'] in ('clip', 'panelwatch'):
        seg = next(x for x in edl['clip']['segs'] if x['n0'] <= g < x['n0'] + x['frames'])
        tc = seg['clip_in'] + (g - seg['n0'])/FPS
        Fp, a = key_frame('watchF', tc + RMC)
        if s['kind'] == 'clip':
            out = np.ones((CH, CW, 3), np.float32)*np.array([0.95, 0.25, 0.62], np.float32) if PINK else clip_view(tc)
            Fp, a = feather(Fp, a, fw=corner_fw(Fp, a)); c = s['corner']
            return place(out, Fp, a, c['scale'], c['x0'], c['y0'])
        # the last two panel frames would show the clip's next subtitle card ('My first meal...', the repeat of the hook): hold the frame before it
        hold = seg['clip_in'] + (min(g, s['n1'] - 3) - seg['n0'])/FPS
        out = panel_bg(hold, g) if not PINK else field(t); c = s['place']
        out = place(out, Fp, a, c['scale'], c['x0'], c['y0'])
        # R2 (Dan): the laptop stays visible while he watches, so he reads as watching his screen, not looking at the ground. The real lid
        # (still, median of the watching piece, key/laptop_layer.npy) sits at its true scale flush to the frame bottom, in front of his hands.
        global _lid
        if _lid is None: _lid = np.load(W/'key/laptop_layer.npy')
        return place(out, _lid[..., :3], _lid[..., 3], c['scale'], 0, CH - _lid.shape[0]*c['scale'], wrap=0)
    if s['kind'] == 'panelresp':
        pc = next(p for p in edl['pieces'] if p['id'] == s['piece']); t_roll = pc['start'] + (g - pc['n0'])/FPS
        out = reel_bg(g) if not PINK else field(t); c = s['place']
        Fp, a = key_frame('T', t_roll)
        return place(out, Fp, a, c['scale'], c['x0'], c['y0'])
    if s['kind'] == 'talk':
        pc = next(p for p in edl['pieces'] if p['id'] == s['piece']); t_roll = pc['start'] + (g - pc['n0'])/FPS
        x, y, cw, ch = crops[s['id']][j]; sc = CW/cw
        Fp, a = key_frame('T', t_roll)
        return place(field(t), Fp, a, sc, -x*sc, -y*sc)
    if s['kind'] == 'broll':
        f = broll_grade(broll(s['clip'], s['src_t0'] + j/FPS), s['clip'])
        if s.get('ai'):
            if s['clip'] not in CHIPS: CHIPS[s['clip']] = chip_layer(CHIP_XY[s['clip']])
            col, al = CHIPS[s['clip']]; f = f*(1 - al[..., None]) + col*al[..., None]
        return f
    if s['kind'] == 'still':
        return still(j/max(1, s['n1'] - s['n0'] - 1))
    raise ValueError(s)

C = CM.Compositor(man, wh=(CW, CH)) if man else None
def gfx(f8, g): return C.apply(f8.copy(), g) if C else f8

if __name__ == '__main__':
    if STILLS:
        (O/'stills').mkdir(exist_ok=True)
        for t in STILLS:
            g = fr(t); f8 = u8(render(g))
            cv2.imwrite(str(O/'stills'/f'g{g:05d}{"_pink" if PINK else ""}.png'), cv2.cvtColor(gfx(f8, g), cv2.COLOR_RGB2BGR))
        print('STILLS', [fr(t) for t in STILLS]); sys.exit()
    comp = O/('composite_pink.mp4' if PINK else 'composite.mp4'); base = O/'base.mp4'
    MUX_ONLY = '--mux-only' in args and comp.exists() and base.exists()
    enc = lambda p: subprocess.Popen([F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-framerate', '30000/1001', '-i', '-', '-an',
                                       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15',
                                       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(p)], stdin=subprocess.PIPE)
    if not MUX_ONLY:
        pc_ = enc(comp); pb_ = None if PINK else enc(base); n = 0
        with Pool(int(os.environ.get('RENDERQ_CORES', '4'))) as pool:
            for f in pool.imap(render, range(TOTAL), chunksize=4):
                f8 = u8(f)
                if pb_: pb_.stdin.write(f8.tobytes())
                pc_.stdin.write(np.ascontiguousarray(gfx(f8, n)).tobytes()); n += 1
                if n % 150 == 0: print(n, 'frames', flush=True)
        for p in (pc_, pb_):
            if p: p.stdin.close(); assert p.wait() == 0
        assert n == TOTAL
    if PINK: print('PINK DONE', comp); sys.exit()
    master = Q/f'{NAME}.mp4'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-i', str(comp), '-i', str(O/f'mix-{VOICE}.wav'), '-map', '0:v', '-map', '1:a', '-vf', f"ass='{O}/captions.ass'",
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-frames:v', str(TOTAL),
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', str(master)], check=True)
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-i', str(master), '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-c:a', 'aac', '-b:a', '160k',
                    '-movflags', '+faststart', str(Q/f'{NAME} - REVIEW 540p.mp4')], check=True)
    def secs(x): h, m, s_ = x.split(':'); return int(h)*3600 + int(m)*60 + float(s_)
    def stamp(x): ms = round(x*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    cues = []
    for line in (O/'captions.ass').read_text().splitlines():
        if line.startswith('Dialogue:'): f_ = line.split(',', 9); cues.append((secs(f_[1]), secs(f_[2]), re.sub(r'\{[^}]*\}', '', f_[9])))
    (Q/f'{NAME}.srt').write_text(''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(cues)))
    print('FINISHED', hashlib.sha256(master.read_bytes()).hexdigest(), flush=True)
