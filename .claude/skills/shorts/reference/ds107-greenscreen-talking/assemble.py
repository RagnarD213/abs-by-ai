"""DS-107 R1 assembly (from DS-41 R1): one RGB pass over the film timeline -> base.mp4 (no graphics, no title band) +
composite.mp4 (graphics + title band), then the master with burned captions and the chosen mix, and the SRT.
    python3 assemble.py [--voice house_bass15] [--look r5warm] [--stills 1.0,5.0,...] [--mux-only] [--pink]
Soft Blue shorts standard: the title band (field y 0-310, cyan eyebrow + two-line headline, 2 px glass line) on screen for the whole
short and laid over everything last; the picture area 1080 x 1610 under it. Shots (framing.py): talk = Dan keyed (house key, stage 2
finishing, grade on Dan only, light wrap) on the moving Soft Blue field; card = the full-screen HyperFrames study card; broll =
library clips filling the picture area (or a square card where two people must stay in shot), AI chip where AI; still = Dan's
real photos with a slow push-in and the real-photo chip."""
from pathlib import Path
import json, subprocess, sys, hashlib, re, os
import numpy as np, cv2
from scipy import ndimage as ndi
from multiprocessing import Pool
W = Path(__file__).resolve().parents[1]; RC = Path(__file__).resolve().parent; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); sys.path.insert(0, str(HF.parent)); sys.path.insert(0, str(RC))
import composite as CM, softblue as B
from grade import LOOKS_DAN
from PIL import Image, ImageDraw
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
O = W/'main'
NAME = 'Metabolism Not The Reason SFC R2'
Q = O/'review'; Q.mkdir(exist_ok=True)
args = sys.argv[1:]
VOICE = args[args.index('--voice') + 1] if '--voice' in args else 'house_bass15'
LOOK = args[args.index('--look') + 1] if '--look' in args else os.environ.get('LOOK', 'r5warm')
STILLS = [float(x) for x in args[args.index('--stills') + 1].split(',')] if '--stills' in args else None
PINK = '--pink' in args
GRADE = LOOKS_DAN[LOOK]
edl = json.load(open(O/'edl.json')); shots = json.load(open(O/'shots.json'))
crops = json.load(open(O/'framing-frames.json')); man = json.load(open(O/'graphics-manifest.json')) if (O/'graphics-manifest.json').exists() else []
TOTAL = edl['total_frames']; fr = lambda t: int(round(t*FPS))
TSUB = edl['key']['T']
def tsub(t_roll):
    for name, t0, d in TSUB:
        if t0 - 1e-6 <= t_roll < t0 + d - 3.5/FPS: return name, t0
    raise ValueError(f'roll {t_roll:.3f} is not inside a keyed stretch {TSUB}')
MIN_FRAG, EDGE, HAZE = 900, 4, 4.5
WRAP, WRAP_SIG = 0.12, 10
CW, CH = 1080, 1920; DROP = 310
def u8(x): return (np.clip(x, 0, 1)*255 + 0.5).astype(np.uint8)

# ---------- keyed layer (house stage 2, scaled for the 0.75 cache)
def key_frame(t_roll):
    name, t0 = tsub(t_roll); i = int(round((t_roll - t0)*FPS)); p = W/'key'/f'c2_{name}'/f'f{i:04d}.npy'
    d = np.load(p).astype(np.float32); Fp, a = d[..., :3], d[..., 3]
    a[2600:, :300] = 0; Fp[2600:, :300] = 0     # garbage matte: the green screen's dark bottom-left vignette keys to 30 % (measure/islands_alpha.json); Dan's legs sit at x 480-1200
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
    G = GRADE(np.clip(G, 0, 1))
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

# ---------- the moving field (keyframes every 0.5 s, blended per frame) and the title band laid over it
TITLE = ('METABOLISM MYTH', ["Your Metabolism Is Not", "The Reason You're Fat"])
_fk = {}
def field_key(k):
    if k not in _fk:
        ck = W/'cache'/f'field_{k:04d}.npy'
        if ck.exists(): _fk[k] = np.load(ck)
        else:
            ck.parent.mkdir(exist_ok=True); a = np.asarray(B.field(k*0.5, CW, CH).convert('RGB')); np.save(ck, a); _fk[k] = a
    return _fk[k]
def field(t):
    if PINK: return np.ones((CH, CW, 3), np.float32)*np.array([0.95, 0.25, 0.62], np.float32)
    k = int(t/0.5); u = t/0.5 - k
    return (field_key(k).astype(np.float32)*(1 - u) + field_key(k + 1).astype(np.float32)*u)/255
def band_layer():
    """the SL-21 title band (lib.band geometry): eyebrow Poppins 34 cyan letter-spaced with the slim accent at x 64, headline Poppins
    Bold 88 (shrunk to fit 64 px margins), lines at y 86 and 182, glass line at y 309; as an RGBA layer over the field"""
    im = Image.new('RGBA', (CW, DROP + 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); eyebrow, lines = TITLE
    fe = B.font(34); size = 88
    while max(B.text_w(l, B.font(size)) for l in lines) > CW - 2*64: size -= 2
    fh = B.font(size)
    d.rounded_rectangle((64, 50, 71, 86), 3, fill=B.CYAN); x = 88
    for ch in eyebrow: d.text((x, 44), ch, font=fe, fill=B.CYAN); x += B.text_w(ch, fe) + 4
    y = 86
    for line in lines: d.text((64, y), line, font=fh, fill=B.WHITE); y += 96
    assert y <= DROP + 2
    d.line((0, DROP - 1, CW, DROP - 1), fill=B.GLASS_LINE, width=2)
    a = np.asarray(im).astype(np.float32)/255
    return a[..., :3], a[..., 3:]
BAND = band_layer()
def with_band(f8, t):
    """lay the title band (its own moving field + text) over rows 0-310 of a finished uint8 frame"""
    fl = field(t)[:DROP + 2]; col, al = BAND
    top = fl*(1 - al) + col*al
    out = f8.copy(); out[:DROP - 1] = u8(top[:DROP - 1]); out[DROP - 1:DROP + 1] = u8(top[DROP - 1:DROP + 1]*al[DROP - 1:DROP + 1] + f8[DROP - 1:DROP + 1]/255*(1 - al[DROP - 1:DROP + 1]))
    return out

# ---------- chips
def chip(text_lines, xy, px=28, anchor='lt'):
    """the dark disclosure chip (softblue.disclosure style: CHIP fill, radius 12 u, 20 u side padding), one or two lines; returns
    (colour, alpha, box) on the full canvas"""
    f = B.font(px, False); lh = round(px*1.28); u = px/23
    tw = max(B.text_w(s_, f) for s_ in text_lines); bw, bh = tw + 40*u, lh*len(text_lines) + 17*u
    x, y = xy
    if anchor == 'rt': x -= bw
    blk = Image.new('RGB', (CW, CH), (0, 0, 0)); wht = Image.new('RGB', (CW, CH), (255, 255, 255))
    for im in (blk, wht):
        B.rr(im, (x, y, x + bw, y + bh), B.CHIP, 12*u); d = ImageDraw.Draw(im)
        for i, s_ in enumerate(text_lines): d.text((x + 20*u, y + 7*u + i*lh), s_, font=f, fill=B.WHITE)
    a0 = np.asarray(blk).astype(np.float32)/255; a1 = np.asarray(wht).astype(np.float32)/255
    al = 1 - (a1 - a0).max(2).clip(0, 1); col = np.where(al[..., None] > 0, a0/np.maximum(al[..., None], 1e-3), 0)
    return col, al, (round(x), round(y), round(x + bw), round(y + bh))
CHIPS = {}
AI_XY = {'A0063': (40, DROP + 30), 'A0072': (40, DROP + 30), 'A0182': (40, DROP + 30), 'A0242': (40, DROP + 30)}
REAL_XY = {'before': ((24, DROP + 110), 'lt'), 'today': ((1056, DROP + 110), 'rt')}
def get_chip(key):
    if key not in CHIPS:
        if key in AI_XY: CHIPS[key] = chip(['AI-GENERATED'], AI_XY[key], px=37)
        else: xy, an = REAL_XY[key]; CHIPS[key] = chip(['Real Photo Of Me,', 'Not AI-Generated'], xy, px=30, anchor=an)
    return CHIPS[key]
def lay(f, key):
    col, al, _ = get_chip(key); return f*(1 - al[..., None]) + col*al[..., None]

# ---------- B-roll and stills
BOX = {'A0063': 'square', 'A0072': 'square'}
GB = json.load(open(W/'broll-grade.json')) if (W/'broll-grade.json').exists() else {}
def broll_grade(x, clip):
    g = GB.get(clip)
    if not isinstance(g, dict): return x
    f = np.clip(x, 0, 1)**g['gamma']; y = (f*np.array([.2126, .7152, .0722], np.float32)).sum(-1, keepdims=True)
    f = y + g['sat']*(f - y); f = f*np.array(g['rgb'], np.float32)
    return np.clip(f, 0, 1)
NFPS = {'A0063': 24.0, 'A0072': 25.0, 'A0182': 24.0, 'A0242': 24.0, 'B0559': 25.0, 'B0042': 25.0, 'B0448': 30000/1001, 'B0542': 30000/1001}
_br = {}
def broll(clip, src_t0, j, speed=1.0):
    """one native frame per film frame from the clip's start frame (DS-41: no fps resampling, no doubled frames); speed > 1 skips source
    frames (R2 opener: never blends, so no ghosting)"""
    if clip not in _br: _br[clip] = np.load(W/f'src/{clip}.npy', mmap_mode='r')
    a = _br[clip]; k = int(round(src_t0*NFPS[clip])) + int(round(j*speed))
    assert k < a.shape[0], (clip, k, a.shape)
    return a[k].astype(np.float32)/255
_st = {}
def photo(name, u):
    """a real photo filling the picture area, pushing in 100 % -> 105 % over the shot (u 0..1) about his head"""
    if name not in _st: _st[name] = np.load(W/f'src/{name}.npy')[0].astype(np.float32)/255
    z = 1.0 + 0.05*u; cx, cy = {'before': (560, 330), 'today': (460, 260)}[name]
    M = np.array([[z, 0, cx - z*cx], [0, z, cy - z*cy]], np.float32)
    return cv2.warpAffine(_st[name], M, (CW, CH - DROP), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def render(g):
    """frame g of the film, float RGB 0..1, no graphics, no title band"""
    s = next(x for x in shots if x['n0'] <= g < x['n1']); j = g - s['n0']; t = g/FPS
    if s['kind'] == 'talk':
        pc = next(p for p in edl['pieces'] if p['id'] == s['piece']); t_roll = pc['start'] + (g - pc['n0'])/FPS
        x, y, cw, ch = crops[s['id']][j]; sc = CW/cw
        Fp, a = key_frame(t_roll)
        return place(field(t), Fp, a, sc, -x*sc, DROP - y*sc)
    if s['kind'] == 'card':
        return field(t)
    if s['kind'] == 'broll':
        f = broll_grade(broll(s['clip'], s['src_t0'], j, s.get('speed', 1.0)), s['clip']); out = field(t)
        if BOX.get(s['clip']) == 'square': out[DROP + 10:DROP + 10 + 1080] = f
        else: out[DROP:] = f
        return lay(out, s['clip']) if s.get('ai') else out
    if s['kind'] == 'still':
        out = field(t); out[DROP:] = photo(s['photo'], j/max(1, s['n1'] - s['n0'] - 1))
        return lay(out, s['photo'])
    raise ValueError(s)

C = CM.Compositor(man, wh=(CW, CH)) if man else None
def gfx(f8, g): return with_band(C.apply(f8.copy(), g) if C else f8, g/FPS)

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
    # review copy: the 1080p master itself (VIDEO-RULES 2026-11-02, no 540p duplicate)
    def secs(x): h, m, s_ = x.split(':'); return int(h)*3600 + int(m)*60 + float(s_)
    def stamp(x): ms = round(x*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    cues = []
    for line in (O/'captions.ass').read_text().splitlines():
        if line.startswith('Dialogue:'): f_ = line.split(',', 9); cues.append((secs(f_[1]), secs(f_[2]), re.sub(r'\{[^}]*\}', '', f_[9])))
    (Q/f'{NAME}.srt').write_text(''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(cues)))
    print('FINISHED', hashlib.sha256(master.read_bytes()).hexdigest(), flush=True)
