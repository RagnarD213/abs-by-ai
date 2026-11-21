"""DS-41 R1 framing (from DS-36 R1 / DS-43 R2) for ONE version (python3 framing.py scripted|offcuff; SHOTS_ONLY=1 writes shot times only).
The Bill Maher Codex R5 sequence, adapted to the 0.75 key cache (1620 wide; talk pieces 2618 rows = source rows 0-3490, above
the laptop; the watching piece 2880 rows, laptop kept):
  S0  clip full screen (fixed portrait window on Kevin James), Dan lower left at 0.40 of full size (432 x 768, flush left/bottom)
  PW  titled panel (clip full width at y 92-700, title above it), Dan large (full width = R5 scale 1.0) still watching; one
      fixed placement for the whole stretch with his LOWEST hair 28 px over the panel's bottom edge (R5)
  PR  the same panel, clip continuing silently; Dan's response at R5 scale 1.25 (1350 px wide), horizontally centred on his
      median head position, again one fixed placement with the lowest hair 28 px over the panel edge
  then Dan on the moving Soft Blue field: fixed W/T windows (zoom cuts), cutaways.
Talk windows: crop top = the shot's highest hair minus 3.5 % of the crop height (VIDEO-RULES 2026-10-20, >= 20 px at 1080),
W as wide as the laptop line allows, T = W / 1.17; horizontal landing: shared landing.vertical_dense.
"""
from pathlib import Path
import json, subprocess, sys, os
import numpy as np
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0, str(R/'.claude/skills/_shared/cut')); import landing
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; KW, KH, KHF = 1620, 2618, 2880
VERSION = sys.argv[1]; O = W/VERSION
edl = json.load(open(O/'edl.json')); words = json.load(open(O/'words_out.json'))
KP = dict(scripted='S', offcuff='O')[VERSION]          # key piece folder for this version's talk take
SRC = edl['pieces'][0]['source']
def fr(t): return int(round(t*FPS))
SIZE = dict(W=1240, T=1060)
PANEL = [0, 92, 1080, 608]; PANEL_BOTTOM = 700; OVERLAP = 28
CORNER_SCALE = 0.40*1080/KW; WATCH_SCALE = 1080/KW; RESP_SCALE = 1.25*1080/KW
HEAD = 0.035

def measure(piece, start, frames):
    """per frame: hair top row and head centre x in the cache space, from the stage 1 key matte (alpha > 0.5), every frame.
    DS-36: a raised hand above the head is not hair. Each frame's column tops are cached; the head column is a running median
    (31 frames) of the frame's alpha-weighted top-band centre, and the hair top is read only within +-330 cache px of it."""
    from scipy.ndimage import median_filter
    ck = W/'framing-cache'/f'c_{piece}_{start:.4f}_{frames}.npy'
    if ck.exists(): ct = np.load(ck)
    else:
        ck.parent.mkdir(exist_ok=True)
        if piece.startswith('watch'): t0, kdir = edl['key'][piece], f'c1_{piece}'
        else:                          # the talk take: the keyed stretch that holds this shot (prep.py KEY['T'])
            name, t0, d_ = next(x for x in edl['key']['T'] if x[1] - 1e-6 <= start and start + frames/FPS <= x[1] + x[2] - 3/FPS)
            kdir = f'c1_{name}'
        i0 = int(round((start - t0)*FPS)); ct = np.full((frames, KW), KHF, np.int16)
        for j, i in enumerate(range(i0, i0 + frames)):
            m_ = np.asarray(np.load(W/'key'/kdir/f'f{i:04d}.npy', mmap_mode='r')[..., 3]) > 0.5
            has = m_.any(0); ct[j, has] = m_[:, has].argmax(0)
        np.save(ck, ct)
    ct = ct.astype(np.float32); ct[:, :100] = KHF; ct[:, 1520:] = KHF
    raw = []
    for r in ct:
        s7 = np.sort(r)[6]; cols = np.where(r <= s7 + 120)[0]
        raw.append(float(np.median(cols)) if len(cols) else np.nan)
    raw = np.array(raw); ok = ~np.isnan(raw)
    cxm = median_filter(np.where(ok, raw, np.nanmedian(raw)), size=min(31, len(raw) | 1), mode='nearest')
    out = []
    for r, c in zip(ct, cxm):
        lo, hi = int(max(0, c - 330)), int(min(KW, c + 330)); win = r[lo:hi]
        top = float(np.sort(win)[6]) if (win < KHF).sum() > 6 else -1.0
        cols = lo + np.where(win <= top + 120)[0]
        out.append((top, float(np.mean(cols)) if len(cols) else np.nan))
    return np.array(out)

def at(phrase, piece=None, after=0.0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and words[i]['speaker'] == 'dan' and (piece is None or words[i]['piece'] == piece) and \
           [x['w'].lower().strip('.,!?…') for x in words[i:i+len(toks)]] == toks:
            return words[i]
    raise ValueError(phrase)
def cut_before(phrase, **k):
    """a cut in the pause before a word: midway between the previous word's end and this word's start, on a frame"""
    w = at(phrase, **k); i = words.index(w); prev = words[i - 1]
    return round(((prev['t1'] + w['t0'])/2)*FPS)/FPS
P = {p['id']: p for p in edl['pieces']}; ps = lambda i: P[i]['n0']/FPS; pe = lambda i: (P[i]['n0'] + P[i]['frames'])/FPS
segs = edl['clip']['segs']; C1E = edl['clip'].get('layout_cut_film') or segs[1]['n0']/FPS; CE = edl['clip']['frames']/FPS; END = edl['total_frames']/FPS
def talk(id, size, piece, a, b): return dict(id=id, kind='talk', size=size, piece=piece, a=a, b=b)
def card(id, a, b): return dict(id=id, kind='card', a=a, b=b)           # a full-screen HyperFrames card on the moving field (graphics.py)
def broll(id, clip, ai, a, b, src_t0=0.0): return dict(id=id, kind='broll', clip=clip, ai=ai, a=a, b=b, src_t0=src_t0)
SH = [dict(id='S0', kind='clip', a=0.0, b=C1E), dict(id='PW', kind='panelwatch', a=C1E, b=CE), dict(id='PR', kind='panelresp', piece='P1', a=CE, b=pe('P1'))]
if VERSION == 'scripted':
    c_so = cut_before('so you did', piece='P2'); c_andif = cut_before('and if you', piece='P3'); c_this = cut_before('this is the', piece='P3')
    c_where = cut_before('where you just', piece='P4')
    SH += [card('K1', ps('P2'), c_so),                                                                  # the cheat day math (script: FULL SCREEN GRAPHIC, each line lands as he says it)
           talk('S1', 'T', 'P2', c_so, pe('P2')),                                                       # "So you did six days of hard work and you're right back where you started."
           talk('S2', 'W', 'P3', ps('P3'), c_andif),                                                    # "The math behind cheat days simply doesn't work."
           broll('B1', 'A0197', True, c_andif, c_this),                                                 # "And if you haven't lost any weight while doing cheat days,"
           talk('S3', 'T', 'P3', c_this, pe('P3')),                                                     # "this is the reason why."
           talk('S4', 'W', 'P4', ps('P4'), c_where),                                                    # G01 the rule
           broll('B2', 'A0242', True, c_where, pe('P4')),   # review 1: A0202 (a man pouting, never eating) read as mocking and did not show the line; A0242 a man taking a drive-thru bag
                                                         # "where you just eat any high calorie food you want without tracking."
           talk('S5', 'T', 'P5', ps('P5'), pe('P5')),                                                   # G02 ripped guys / fat guys
           talk('S6', 'W', 'P6', ps('P6'), END)]                                                        # subscribe card
else:
    c_then = cut_before("then you're not", piece='P6'); c_and = cut_before('and whether', piece='P7'); c_eat = cut_before("you're eating", piece='P8'); c_while = cut_before("while you're", piece='P8')
    SH += [card('K1', ps('P2'), pe('P4')),                                                              # the cheat day math, in this take's words; covers the 'easily' repeat cut (P3|P4)
           talk('S1', 'T', 'P5', ps('P5'), pe('P5')),                                                   # "So guys, this concept of a cheat day does not work mathematically."
           talk('S2', 'W', 'P6', ps('P6'), c_then),                                                     # "If you have a cheat day, even if you're dieting hard all the other six days,"
           broll('B1', 'A0197', True, c_then, pe('P6')),                                                # "then you're not going to lose any weight most likely."
           talk('S3', 'T', 'P7', ps('P7'), c_and),                                                      # G01 one cheat meal, not a cheat day
           talk('S4', 'W', 'P7', c_and, pe('P7')),                                                      # "And whether ... track your calories,"
           talk('S4b', 'T', 'P8', ps('P8'), c_while),                                                    # "You'll find if you're actually tracking your calories" (review 1: the cutaway now covers only the line it shows)
           broll('B2', 'A0242x', True, c_while, c_eat),                                                 # "while you're going hog wild for an entire day,"
                                                           # "you'll find if you're actually tracking your calories while you're going hog wild for an entire day,"
           talk('S5', 'T', 'P8', c_eat, pe('P8')),                                                      # G02 6,000 to 8,000 calories
           talk('S6', 'W', 'P9', ps('P9'), pe('P9')),                                                   # G03 the bottom line
           talk('S7', 'T', 'P10', ps('P10'), END)]                                                      # subscribe card
for s in SH: s['n0'], s['n1'] = fr(s['a']), fr(s['b'])
for x, y in zip(SH, SH[1:]): assert x['n1'] == y['n0'], (x['id'], y['id'], x['n1'], y['n0'])
assert SH[-1]['n1'] == edl['total_frames']
for s in SH: assert s['n1'] - s['n0'] >= 28, (s['id'], s['n1'] - s['n0'])
for s in SH:
    if s['kind'] == 'talk': assert P[s['piece']]['n0'] <= s['n0'] and s['n1'] <= P[s['piece']]['n0'] + P[s['piece']]['frames'], s['id']
if os.environ.get('SHOTS_ONLY'):
    (O/'shots-times.json').write_text(json.dumps(SH, indent=1)); print([(x['id'], round(x['a'], 2), round(x['b'], 2)) for x in SH]); sys.exit()

def window(m, size, head=HEAD):
    hmin = float(np.nanmin(m[:, 0])); w = SIZE[size]
    w = int(min(w, (KH - hmin)/((1 - head)*16/9)))//2*2
    if size == 'T': w = min(w, int(SIZE['W']/1.17)//2*2)
    h = round(w*16/9); y0 = hmin - head*h; y0 = max(0.0, min(y0, KH - h))
    return w, h, y0, hmin
frames = {}; report = []
for s in SH:
    if s['kind'] != 'talk': continue
    pc = P[s['piece']]; off = s['n0'] - pc['n0']; n = s['n1'] - s['n0']
    m = measure(KP, pc['start'] + off/FPS, n)
    w, h, y0, hmin = window(m, s['size'])
    y0 = min(y0 + {('offcuff', 'S4'): 8.0}.get((VERSION, s['id']), 0.0), KH - h)   # DS-41 gate (framing:headroom): this hold read 72 px of headroom (30-70 allowed)
    clear_out = (hmin - y0)*1920/h
    dn, cx, heads, info = landing.vertical_dense(np.arange(n), m[:, 1], [dict(n0=0, n1=n)], w)
    cx = cx + {('scripted', 'S1'): 14.0}.get((VERSION, s['id']), 0.0)   # DS-41 gate (framing:centering): head sat 6.4 % right of the window centre at this shot's first frames
    xs = np.clip(cx - w/2, 0, max(0, KW - w))
    st = landing.motion_stats(np.arange(n), m[:, 1], xs + w/2, [dict(n0=0, n1=n)], w)
    s.update(crop_w=w, crop_h=h, y0=round(y0, 1), hair_top_min=round(hmin, 1), hair_clear_px_1080=round(clear_out, 1), motion=st)
    frames[s['id']] = [[round(float(x), 1), round(y0, 1), w, h] for x in xs]
    report.append(dict(id=s['id'], size=s['size'], w=w, hair_min=round(hmin), clear_px=round(clear_out, 1), headroom_pct=round(100*(hmin - y0)/h, 2), **st))

# --- opening placements (R5): corner, the large watching layer, the response layer
RMC = edl['clip']['roll_minus_clip']
mw = [measure('watchA', segs[0]['clip_in'] + RMC, segs[0]['frames']), measure('watchB', segs[1]['clip_in'] + RMC, segs[1]['frames'])]   # S0 (clip piece 1), PW (clip piece 2)
corner = dict(scale=CORNER_SCALE, x0=0, y0=1920 - round(KHF*CORNER_SCALE))
lowest_w = float(np.nanmax(mw[1][:, 0]))                      # PW part
watch = dict(scale=WATCH_SCALE, x0=0, y0=round(PANEL_BOTTOM - OVERLAP - lowest_w*WATCH_SCALE))
p1 = P['P1']; nPR = SH[2]['n1'] - SH[2]['n0']; mr = measure(KP, p1['start'], nPR)
lowest_r = float(np.nanmax(mr[:, 0])); cxr = float(np.nanmedian(mr[:, 1]))
resp = dict(scale=RESP_SCALE, x0=round(540 - cxr*RESP_SCALE), y0=round(PANEL_BOTTOM - OVERLAP - lowest_r*RESP_SCALE))
assert resp['x0'] <= 0 and resp['x0'] + KW*RESP_SCALE >= 1080 and resp['y0'] + KH*RESP_SCALE >= 1920, resp
assert watch['y0'] + KHF*WATCH_SCALE >= 1920, watch
SH[0].update(corner=corner); SH[1].update(place=watch, panel=PANEL); SH[2].update(place=resp, panel=PANEL)
extra = []
for nm, m, pl in [('PW', mw[1], watch), ('PR', mr, resp)] + extra:
    tops = pl['y0'] + m[:, 0]*pl['scale']
    report.append(dict(id=nm, scale=round(pl['scale'], 4), x0=pl['x0'], y0=pl['y0'], hair_y_min=round(float(np.nanmin(tops)), 1),
                       hair_y_max=round(float(np.nanmax(tops)), 1), overlap_min_px=round(PANEL_BOTTOM - float(np.nanmax(tops)), 1),
                       overlap_max_px=round(PANEL_BOTTOM - float(np.nanmin(tops)), 1)))
report.append(dict(id='S0', corner=corner, corner_hair_y=round(corner['y0'] + float(np.nanmin(mw[0][:, 0]))*CORNER_SCALE, 1)))

# --- the clip's portrait window in S0: one camera on Kevin James for the whole of piece 1; face centre x measured on the clip
# (prep_media.py writes src/clip_face_x.json: median of skin pixels over 41.4-47.8 s), no burned text in the clip
FACE_X = 924.0; wc = 1080*9/16   # window x 620-1228: the skin median (src/clip_face_x.json, 860) leans to his beard and hand; checked on a frame a second
# through piece 1 that both headphones stay inside the window (at 860 the right one is cut on his last words)
SH[0]['cams'] = [dict(a=0.0, b=C1E, kind='kevin', face_x=FACE_X, crop=[round(float(np.clip(FACE_X - wc/2, 0, 1920 - wc)), 1), 0, round(wc, 1), 1080])]
(O/'shots.json').write_text(json.dumps(SH, indent=1)); (O/'framing-frames.json').write_text(json.dumps(frames))
(O/'framing-report.json').write_text(json.dumps(report, indent=1))
for r in report: print(r)
