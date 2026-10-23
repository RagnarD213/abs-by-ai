"""DS-44 R1 framing: the shot list on the film timeline, per-frame crop windows of Dan in the 0.75 key cache (1620x2618 =
source rows 0-3490, above the laptop), the clip's vertical crops, and the corner/transition placements.

Talk shots alternate W (1240 wide) and T (1000 wide), ratio 1.24, so every cut inside the take is a real size change (zoom
cut). W is as wide as the frame allows: a 9:16 window needs height 1.78x its width and must stop above the laptop line
(cache row 2618), with about 4 % of its height above the highest hair (VIDEO-RULES 2026-10-20), so W <= ~1250 on this take.
Vertical: crop top = the shot's highest hair row minus 4 % of the crop height, clamped inside the frame; never under 20 px at
1080. Horizontal: shared landing.vertical_dense (land on him at the cut, hold until he is 3.3 % off centre).
Person mask = the key's own matte (alpha > 0.5) from the stage 1 cache, every frame.

Clip phase: the clip fills the 1080x1920 frame (a fixed vertical window per camera shot, on the speaker's face; the caller's
webcam window starts below its "No card in camera" banner), Dan keyed small in the bottom-left corner (his real reaction while
he watched it on the laptop). Left, because the Shorts buttons sit on the right. TR: the clip shrinks toward the top and fades
while Dan grows from the corner into the W window, then the talk starts on a T shot (a size change at the first cut).
"""
from pathlib import Path
import json, subprocess, sys
import numpy as np, cv2
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0, str(R/'.claude/skills/_shared/cut')); import landing
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; SC = 0.75; KW, KH = 1620, 2618
edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json')); KEYS = edl['key']
SRC = edl['pieces'][0]['source']
def fr(t): return int(round(t*FPS))
SIZE = dict(W=1240, T=1000)
# R2 (Dan 2026-10-22): after the clip the interview keeps playing silently in a 16:9 frame at the top (CARD), behind Dan's head;
# his hair top sits at HAIR_Y, just under the frame's bottom edge (y 592), so the hair overlaps it. Through the end of S3.
CARD = [40, 30, 1000, 562]; HAIR_Y = 540
CARD_SHOTS = ('S1', 'S1b', 'S2', 'S3')
CARD_SCALE = dict(W=1080/1620, T=0.82)          # W = Dan's whole keyed frame across the screen; T = 1.23x tighter
CORNER_SCALE = 0.40*1080/1620                   # option B: 0.40 of full size (full-height key, laptop kept) = 432 x 768
HEAD = 0.035          # gate framing:headroom wants 30-70 px at 1080; 4 % read 76.8 (DS-33 used 3.5 %)

def measure(start, frames):
    ck = W/'framing-cache'/f'm_{start:.4f}_{frames}.npy'
    if ck.exists(): return np.load(ck)
    ck.parent.mkdir(exist_ok=True); m = _measure(start, frames); np.save(ck, m); return m

def _measure(start, frames):
    """per frame: hair top row and head centre x in the keyed 1620x2618 space, read from the stage 1 key cache (the matte
    itself, alpha > 0.5; rows above the garbage line are zero). Every frame of the shot is measured."""
    piece = min(KEYS, key=lambda k: abs(start - KEYS[k]) if start >= KEYS[k] - 1e-6 else 1e9)
    i0 = int(round((start - KEYS[piece])*FPS)); out = []
    if not (W/'key'/f'c1_{piece}'/f'f{i0 + frames - 1:04d}.npy').exists():
        return measure_src(start, frames)
    for i in range(i0, i0 + frames):
        a = np.load(W/'key'/f'c1_{piece}'/f'f{i:04d}.npy', mmap_mode='r')[..., 3]
        rows = np.where((np.asarray(a[:, 100:1520]) > 0.5).sum(1) > 6)[0]; top = int(rows[0]) if len(rows) else -1
        band = np.asarray(a[top:top + 120]) > 0.5
        cx = float(np.mean(np.where(band)[1])) if band.any() else np.nan
        out.append((float(top), cx))
    return np.array(out)

def measure_src(start, frames):
    """fallback before the key exists: not-screen pixels of the source (540x960 decode; rows 0-7 lens edge, laptop rows excluded)"""
    raw = subprocess.check_output([F, '-v', 'error', '-ss', f'{start:.4f}', '-i', SRC, '-frames:v', str(frames), '-an', '-vf',
                                   'scale=in_color_matrix=bt709:in_range=tv:out_range=pc,scale=540:960,format=rgb24', '-f', 'rawvideo', '-'])
    v = np.frombuffer(raw, np.uint8).reshape(-1, 960, 540, 3).astype(np.int16); out = []
    for f in v:
        r, g, b = f[..., 0], f[..., 1], f[..., 2]; fg = ~((g - r > 20) & (g - b > 20)); fg[:8] = False; fg[872:] = False
        rows = np.where(fg[:, 40:500].sum(1) > 4)[0]; top = int(rows[0]) if len(rows) else -1
        band = fg[top:top + 30, :]
        out.append((top*4*SC, float(np.mean(np.where(band)[1]))*4*SC if band.any() else np.nan))
    return np.array(out)

def at(phrase, piece=None, after=0.0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and (piece is None or words[i]['piece'] == piece) and \
           [x['w'].lower().strip('.,!?') for x in words[i:i+len(toks)]] == toks:
            return words[i]
    raise ValueError(phrase)
def cut_before(phrase, **k):
    """a cut in the pause before a word: midway between the previous word's end and this word's start, on a frame."""
    w = at(phrase, **k); i = words.index(w); prev = words[i - 1]
    return round(((prev['t1'] + w['t0'])/2)*FPS)/FPS

P0, PA, PB = edl['pieces']; CLIP_F = edl['clip']['frames']; TR = edl['tr']
a0 = P0['n0']/FPS; a1 = PA['n0']/FPS; b0 = PB['n0']/FPS; END = edl['total_frames']/FPS
c_already = cut_before('you already stopped'); c_youd = cut_before("you'd be 200"); c_so = cut_before('so you do know', piece='A')
c_fix = cut_before("so here's how to fix"); c_weigh = cut_before('weigh yourself'); c_notnext = cut_before('not next week')
c_losing = cut_before('losing 2 pounds is easy'); c_dial = cut_before('dial back'); c_sub = cut_before('subscribe')
SH = [dict(id='S0', kind='clip', a=0.0, b=CLIP_F/FPS),
      dict(id='TR', kind='transition', a=CLIP_F/FPS, b=a0),
      # build 3: read 1 (eyes on camera) "This is a critical insight", then read 2 from "from Alex Hormozi" at the wide size
      dict(id='S1', kind='talk', size='T', piece='A0', a=a0, b=a1),
      dict(id='S1b', kind='talk', size='W', piece='A', a=a1, b=c_already),
      dict(id='S2', kind='talk', size='T', piece='A', a=c_already, b=c_youd),
      # the caller from the clip (his silent thinking beat, clip 33.70-36.00, cut out of the opening) on "you'd be 200 pounds
      # heavier than you are right now": the cutaway shows the man the line is about (VIDEO-RULES 2026-10-10)
      dict(id='K1', kind='clipcut', a=c_youd, b=c_so, clip_in=33.70),
      dict(id='S3', kind='talk', size='T', piece='A', a=c_so, b=c_fix),
      dict(id='S4', kind='talk', size='W', piece='A', a=c_fix, b=c_weigh),
      # library A0197 (AI, approved in SL-07 "Weigh Yourself Every Morning"): a man on a bathroom scale, on "Weigh yourself every
      # morning, and the day you're 2 pounds over, you cut back that day."
      dict(id='B1', kind='broll', clip='A0197', ai=True, a=c_weigh, b=c_notnext, src_t0=0.30),
      dict(id='S5', kind='talk', size='T', piece='A', a=c_notnext, b=c_losing),
      dict(id='S6', kind='talk', size='W', piece='A', a=c_losing, b=c_dial),
      dict(id='S7', kind='talk', size='T', piece='A', a=c_dial, b=b0),
      # library B0351 (stock, used in "My Honest Zepbound Update"): hands holding an injection pen, from the take join (A|B) through
      # "...try taking Zepbound to make that easy." The cutaway covers the join and shows the thing he names.
      dict(id='B2', kind='broll', clip='B0351', ai=False, a=b0, b=c_sub, src_t0=0.6),
      dict(id='S8', kind='talk', size='W', piece='B', a=c_sub, b=END)]
for s in SH: s['n0'], s['n1'] = fr(s['a']), fr(s['b'])
SH[1]['n0'], SH[1]['n1'] = TR['n0'], TR['n0'] + TR['frames']
for x, y in zip(SH, SH[1:]): assert x['n1'] == y['n0'], (x['id'], y['id'], x['n1'], y['n0'])
assert SH[-1]['n1'] == edl['total_frames']
for s in SH: assert s['n1'] - s['n0'] >= 45 or s['kind'] == 'transition', (s['id'], s['n1'] - s['n0'])

def window(m, size):
    hmin = float(np.nanmin(m[:, 0]))
    w = SIZE[size]
    if size == 'W': w = int(min(w, (KH - hmin)/((1 - HEAD)*16/9)))//2*2      # narrow a wide shot just enough to stop above the laptop line
    h = round(w*16/9); y0 = hmin - HEAD*h; y0 = max(0.0, min(y0, KH - h))
    return w, h, y0, hmin
frames = {}; report = []
for s in SH:
    if s['kind'] != 'talk': continue
    pc = {'A0': P0, 'A': PA, 'B': PB}[s['piece']]
    off = s['n0'] - pc['n0']; n = s['n1'] - s['n0']
    m = measure(pc['start'] + off/FPS, n)
    if s['id'] in CARD_SHOTS:
        sc = CARD_SCALE[s['size']]; w = round(1080/sc); h = round(1920/sc)
        hmin = float(np.nanmin(m[:, 0])); y0 = hmin - HAIR_Y/sc
        assert (KH - y0)*sc >= 1920, (s['id'], 'laptop line would show')
        s['card'] = CARD
    else:
        w, h, y0, hmin = window(m, s['size'])
    clear_out = (hmin - y0)*1920/h          # card shots: = HAIR_Y (his hair sits under the card by design)
    dn, cx, heads, info = landing.vertical_dense(np.arange(n), m[:, 1], [dict(n0=0, n1=n)], w)
    xs = np.clip(cx - w/2, 0, max(0, KW - w))
    st = landing.motion_stats(np.arange(n), m[:, 1], xs + w/2, [dict(n0=0, n1=n)], w)
    s.update(crop_w=w, crop_h=h, y0=round(y0, 1), hair_top_min=round(hmin, 1), hair_clear_px_1080=round(clear_out, 1), motion=st)
    frames[s['id']] = [[round(float(x), 1), round(y0, 1), w, h] for x in xs]
    report.append(dict(id=s['id'], size=s['size'], hair_min=round(hmin), clear_px=round(clear_out, 1), headroom_pct=round(100*(hmin - y0)/h, 2), **st))

# --- watching piece: corner placement and the transition's W target
WT0 = edl['key']['watch']; RMC = edl['clip']['roll_minus_clip']
segs = edl['clip']['segs']
first_roll = segs[0]['clip_in'] + RMC; last_roll = TR['clip_in'] + RMC + TR['frames']/FPS
m = measure(first_roll, fr(last_roll - first_roll))
w_, h_, y0_, hmin_ = window(m, 'W')
cxm = float(np.nanmedian(m[-TR['frames']:, 1]))
# R2: option B corner from the full-height key (2880 cache rows, laptop kept): 432 x 768, flush left and bottom
corner = dict(scale=CORNER_SCALE, x0=0, y0=1920 - round(2880*CORNER_SCALE), full=True)
s_big = CARD_SCALE['W']
SH[1].update(corner=corner, card=CARD, target=dict(scale=s_big, x0=0.0, y0=HAIR_Y - hmin_*s_big))
SH[0].update(corner=corner)
report.append(dict(id='watch/TR', hair_min=round(hmin_), corner_hair_y=round(corner['y0'] + hmin_*CORNER_SCALE),
                   target=SH[1]['target']))

# --- the clip's vertical windows per camera shot (faces measured with OpenCV's frontal-face detector, median per shot)
CUTS = [0, 30.17, 32.961, 33.628, 38.878, 40.545, 43.42, 51.586, 99]
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
_clip = np.load(W/'src/clip_30-52_24fps.npy', mmap_mode='r')
# OpenCV here ships without the Haar face file: face centres measured on 960x540 stills of each camera shot (x in the 1920 frame)
FACE = {30.17: 1070.0, 33.628: 900.0, 38.878: 1080.0, 40.545: 940.0, 43.42: 1105.0}
def faces(t0, t1):
    if casc.empty():
        return next((v for k, v in FACE.items() if abs(k - t0) < 0.05 or (t0 == 30.0 and k == 30.17)), None)
    xs = []
    for t in np.arange(t0 + 0.1, t1 - 0.05, 0.4):
        g = cv2.cvtColor(np.asarray(_clip[int((t - 30.0)*24)]), cv2.COLOR_RGB2GRAY)
        d = casc.detectMultiScale(g, 1.1, 6, minSize=(140, 140))
        if len(d): x, y, w, h = max(d, key=lambda r: r[2]*r[3]); xs.append(x + w/2)
    return float(np.median(xs)) if xs else None
cams = []
for i, (s, e) in enumerate(zip(CUTS, CUTS[1:])):
    if e < 30.0 or s > 51.6: continue
    cx = faces(max(s, 30.0), min(e, 51.6))
    caller = cx is not None and cx < 1000 and s not in (30.17, 38.878, 43.42)
    kind = 'hormozi' if s in (30.17, 38.878, 43.42) else ('hosts' if s == 32.961 else 'caller')
    y0c = 150 if kind == 'caller' else 0       # below the webcam's "No card in camera" banner (rows 54-146)
    hc = 1080 - y0c; wc = hc*9/16
    cx = cx if cx is not None else 960
    x0c = float(np.clip(cx - wc/2, 0, 1920 - wc))
    cams.append(dict(a=s, b=e, kind=kind, face_x=round(cx, 1), crop=[round(x0c, 1), y0c, round(wc, 1), hc]))
SH[0]['cams'] = cams
(W/'shots.json').write_text(json.dumps(SH, indent=1)); (W/'framing-frames.json').write_text(json.dumps(frames))
(W/'framing-report.json').write_text(json.dumps(report, indent=1))
for r in report: print(r)
for c in cams: print(c)
