"""DS-43 R1 framing for ONE version (python3 framing.py scripted|offcuff; SHOTS_ONLY=1 writes shot times only).
The Bill Maher Codex R5 sequence, adapted to the 0.75 key cache (1620 wide; talk pieces 2618 rows = source rows 0-3490, above
the laptop; the watching piece 2880 rows, laptop kept):
  S0  clip full screen (fixed portrait window on Terry), Dan lower left at 0.40 of full size (432 x 768, flush left/bottom)
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
    """per frame: hair top row and head centre x in the cache space, from the stage 1 key matte (alpha > 0.5), every frame"""
    ck = W/'framing-cache'/f'm_{piece}_{start:.4f}_{frames}.npy'
    if ck.exists(): return np.load(ck)
    ck.parent.mkdir(exist_ok=True)
    t0 = edl['key']['watchF'] if piece == 'watchF' else edl['key']['T']
    i0 = int(round((start - t0)*FPS)); out = []
    for i in range(i0, i0 + frames):
        a = np.load(W/'key'/f'c1_{piece}'/f'f{i:04d}.npy', mmap_mode='r')[..., 3]
        rows = np.where((np.asarray(a[:, 100:1520]) > 0.5).sum(1) > 6)[0]; top = int(rows[0]) if len(rows) else -1
        band = np.asarray(a[top:top + 120]) > 0.5
        out.append((float(top), float(np.mean(np.where(band)[1])) if band.any() else np.nan))
    m = np.array(out); np.save(ck, m); return m

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
segs = edl['clip']['segs']; C1E = segs[1]['n0']/FPS; CE = edl['clip']['frames']/FPS; END = edl['total_frames']/FPS
def talk(id, size, piece, a, b): return dict(id=id, kind='talk', size=size, piece=piece, a=a, b=b)
SH = [dict(id='S0', kind='clip', a=0.0, b=C1E), dict(id='PW', kind='panelwatch', a=C1E, b=CE), dict(id='PR', kind='panelresp', piece='P1', a=CE, b=pe('P1'))]
if VERSION == 'scripted':
    c_but = cut_before('but what most', piece='P3'); c_you = cut_before('you can have', piece='P4')
    c_watch = cut_before('watch that', piece='P5'); c_and = cut_before('and shut', piece='P5')
    SH += [dict(id='B1', kind='broll', clip='A0210', ai=True, a=ps('P2'), b=pe('P2'), src_t0=0.0),       # "I've been doing fasting ... first meal at 2."
           talk('S1', 'W', 'P3', ps('P3'), c_but),
           talk('S2', 'T', 'P3', c_but, pe('P3')),                                                       # G02 hunger adapts
           talk('S3', 'W', 'P4', ps('P4'), c_you),
           dict(id='B2', kind='broll', clip='B0317', ai=False, a=c_you, b=pe('P4'), src_t0=1.5),          # "...a huge dinner with all your favorite foods..."
           talk('S4', 'T', 'P5', ps('P5'), c_watch),                                                     # G03 the trade-off
           dict(id='K1', kind='still', clip='NYSE', a=c_watch, b=c_and),                                 # "watch that Terry Crews video again"
           talk('S5', 'W', 'P5', c_and, pe('P5')),                                                       # "and shut the fuck up."
           talk('S6', 'T', 'P6', ps('P6'), END)]                                                         # subscribe card from 'learn how'
else:
    c_but = cut_before("but he's got", piece='P2'); c_look = cut_before('look at how', piece='P4'); c_many = cut_before("and there's many", piece='P4')
    c_fast = cut_before('fasting does not', piece='P4'); c_ifnot = cut_before("if you're not", piece='P6')
    SH += [talk('S1', 'W', 'P2', ps('P2'), c_but),
           talk('S2', 'T', 'P2', c_but, pe('P2')),
           talk('S3', 'W', 'P3', ps('P3'), pe('P3')),
           talk('S4', 'T', 'P4', ps('P4'), c_look),
           dict(id='K1', kind='still', clip='NYSE', a=c_look, b=c_many),                                 # "Look at how muscular Terry Crews is..."
           talk('S5', 'W', 'P4', c_many, c_fast),
           talk('S6', 'T', 'P4', c_fast, pe('P4')),                                                      # G02 the myth
           talk('S7', 'W', 'P5', ps('P5'), pe('P5')),                                                    # G03 body adapts
           dict(id='B2', kind='broll', clip='B0317', ai=False, a=ps('P6'), b=c_ifnot, src_t0=1.5),        # "...a big dinner with all your favorite foods..."
           talk('S8', 'T', 'P6', c_ifnot, pe('P6')),                                                     # G04 the trade-off
           talk('S9', 'W', 'P7', ps('P7'), pe('P7')),
           talk('S10', 'T', 'P8', ps('P8'), END)]                                                        # subscribe card from 'learn how'
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
    clear_out = (hmin - y0)*1920/h
    dn, cx, heads, info = landing.vertical_dense(np.arange(n), m[:, 1], [dict(n0=0, n1=n)], w)
    xs = np.clip(cx - w/2, 0, max(0, KW - w))
    st = landing.motion_stats(np.arange(n), m[:, 1], xs + w/2, [dict(n0=0, n1=n)], w)
    s.update(crop_w=w, crop_h=h, y0=round(y0, 1), hair_top_min=round(hmin, 1), hair_clear_px_1080=round(clear_out, 1), motion=st)
    frames[s['id']] = [[round(float(x), 1), round(y0, 1), w, h] for x in xs]
    report.append(dict(id=s['id'], size=s['size'], w=w, hair_min=round(hmin), clear_px=round(clear_out, 1), headroom_pct=round(100*(hmin - y0)/h, 2), **st))

# --- opening placements (R5): corner, the large watching layer, the response layer
RMC = edl['clip']['roll_minus_clip']
mw = [measure('watchF', s['clip_in'] + RMC, s['frames']) for s in segs]
corner = dict(scale=CORNER_SCALE, x0=0, y0=1920 - round(KHF*CORNER_SCALE))
lowest_w = float(np.nanmax(mw[1][:, 0]))                      # PW only shows segment C2
watch = dict(scale=WATCH_SCALE, x0=0, y0=round(PANEL_BOTTOM - OVERLAP - lowest_w*WATCH_SCALE))
p1 = P['P1']; mr = measure(KP, p1['start'], p1['frames'])
lowest_r = float(np.nanmax(mr[:, 0])); cxr = float(np.nanmedian(mr[:, 1]))
resp = dict(scale=RESP_SCALE, x0=round(540 - cxr*RESP_SCALE), y0=round(PANEL_BOTTOM - OVERLAP - lowest_r*RESP_SCALE))
assert resp['x0'] <= 0 and resp['x0'] + KW*RESP_SCALE >= 1080 and resp['y0'] + KH*RESP_SCALE >= 1920, resp
assert watch['y0'] + KHF*WATCH_SCALE >= 1920, watch
SH[0].update(corner=corner); SH[1].update(place=watch, panel=PANEL); SH[2].update(place=resp, panel=PANEL)
for nm, m, pl in (('PW', mw[1], watch), ('PR', mr, resp)):
    tops = pl['y0'] + m[:, 0]*pl['scale']
    report.append(dict(id=nm, scale=round(pl['scale'], 4), x0=pl['x0'], y0=pl['y0'], hair_y_min=round(float(np.nanmin(tops)), 1),
                       hair_y_max=round(float(np.nanmax(tops)), 1), overlap_min_px=round(PANEL_BOTTOM - float(np.nanmax(tops)), 1),
                       overlap_max_px=round(PANEL_BOTTOM - float(np.nanmin(tops)), 1)))
report.append(dict(id='S0', corner=corner, corner_hair_y=round(corner['y0'] + float(np.nanmin(mw[0][:, 0]))*CORNER_SCALE, 1)))

# --- the clip's portrait window in S0: the hook shot (one camera shot 0-4.32 s), Terry's face centre x = 1280 of 1920
# (measured on stills; his burned caption text sits at x 120-760, outside the window)
FACE_X = 1280.0; wc = 1080*9/16
SH[0]['cams'] = [dict(a=0.0, b=4.32, kind='terry', face_x=FACE_X, crop=[round(float(np.clip(FACE_X - wc/2, 0, 1920 - wc)), 1), 0, round(wc, 1), 1080])]
(O/'shots.json').write_text(json.dumps(SH, indent=1)); (O/'framing-frames.json').write_text(json.dumps(frames))
(O/'framing-report.json').write_text(json.dumps(report, indent=1))
for r in report: print(r)
