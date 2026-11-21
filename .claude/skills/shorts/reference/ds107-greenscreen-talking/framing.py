"""DS-107 R1 framing (from DS-41 R1).   python3 framing.py  (SHOTS_ONLY=1 writes shot times only)
Dedicated green-screen Short, Soft Blue shorts standard: title band y 0-310 for the whole short, the picture area 1080 x 1610 under
it. Dan is keyed (house key, 0.75 cache 1620 x 2880 = the full 2160 x 3840 portrait frame; no laptop on this roll) onto the moving
Soft Blue field. Talk windows have the picture area's shape (1080:1610); the window's top = the shot's highest hair minus 3.5 % of
the window height (VIDEO-RULES 2026-10-20: >= 20 px at 1080), so his hair sits about 56 px under the title band.
W = hair to upper thigh (1240 cache px wide), T = hair to about the belly (860). Horizontal: shared landing.vertical_dense (lands, then holds).
"""
from pathlib import Path
import json, sys, os
import numpy as np
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0, str(R/'.claude/skills/_shared/cut')); import landing
FPS = 30000/1001; KW, KH = 1620, 2880
O = W/'main'
edl = json.load(open(O/'edl.json')); words = json.load(open(O/'words_out.json'))
DROP, PH = 310, 1610; AR = 1080/PH
def fr(t): return int(round(t*FPS))
SIZE = dict(W=1060, T=860)          # Dan stands close on C1908 (head ~300 cache px wide, hair-to-chin ~440 rows): W = 1060: the widest window that keeps his head >= 27 % on every hold (gate framing:no_wide_level; 1080 read 26.7 % on T5b, 1240 read 24 %); his elbows-out stance spans 1045-1093 at p90, centred on his body midline, T = hair to belly
HEAD = 0.035

def measure(start, frames):
    """per frame: hair top row and head centre x (cache px) from the stage-1 key matte (alpha > 0.5); a raised hand is not hair
    (DS-36): hair is read within +-330 px of a 31-frame running median of the head column."""
    from scipy.ndimage import median_filter
    ck = W/'framing-cache'/f'c_{start:.4f}_{frames}.npy'
    if ck.exists(): ct = np.load(ck)
    else:
        ck.parent.mkdir(exist_ok=True)
        name, t0, d_ = next(x for x in edl['key']['T'] if x[1] - 1e-6 <= start and start + frames/FPS <= x[1] + x[2] - 3/FPS)
        i0 = int(round((start - t0)*FPS)); ct = np.full((frames, KW), KH, np.int16)
        for j, i in enumerate(range(i0, i0 + frames)):
            m_ = np.asarray(np.load(W/'key'/f'c1_{name}'/f'f{i:04d}.npy', mmap_mode='r')[..., 3]) > 0.5
            m_[:40] = False                                    # the lens's dark top edge is never hair
            has = m_.any(0); ct[j, has] = m_[:, has].argmax(0)
        np.save(ck, ct)
    ct = ct.astype(np.float32); ct[:, :40] = KH; ct[:, KW-40:] = KH
    raw = []
    for r in ct:
        s7 = np.sort(r)[6]; cols = np.where(r <= s7 + 120)[0]
        raw.append(float(np.median(cols)) if len(cols) else np.nan)
    raw = np.array(raw); ok = ~np.isnan(raw)
    cxm = median_filter(np.where(ok, raw, np.nanmedian(raw)), size=min(31, len(raw) | 1), mode='nearest')
    out = []
    for r, c in zip(ct, cxm):
        lo, hi = int(max(0, c - 330)), int(min(KW, c + 330)); win = r[lo:hi]
        top = float(np.sort(win)[6]) if (win < KH).sum() > 6 else -1.0
        cols = lo + np.where(win <= top + 120)[0]
        out.append((top, float(np.mean(cols)) if len(cols) else np.nan))
    return np.array(out)

def at(phrase, piece=None, after=0.0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and (piece is None or words[i]['piece'] == piece) and \
           [x['w'].lower().strip('.,!?…') for x in words[i:i+len(toks)]] == toks:
            return words[i]
    raise ValueError(phrase)
def cut_before(phrase, **k):
    w = at(phrase, **k); i = words.index(w); prev = words[i - 1]
    return round(((prev['t1'] + w['t0'])/2)*FPS)/FPS
P = {p['id']: p for p in edl['pieces']}; ps = lambda i: P[i]['n0']/FPS; pe = lambda i: (P[i]['n0'] + P[i]['frames'])/FPS
END = edl['total_frames']/FPS
def talk(id, size, piece, a, b): return dict(id=id, kind='talk', size=size, piece=piece, a=a, b=b)
def card(id, a, b): return dict(id=id, kind='card', a=a, b=b)
def broll(id, clip, ai, a, b, src_t0=0.0): return dict(id=id, kind='broll', clip=clip, ai=ai, a=a, b=b, src_t0=src_t0)
def still(id, photo, a, b): return dict(id=id, kind='still', photo=photo, a=a, b=b)
c = cut_before
SH = [dict(broll('B0', 'B0448', False, 0.0, c("i'll prove"), 1.6), speed=float(__import__('os').environ.get('B0_SPEED', '1.25'))),   # R2 (Dan): "accelerate that initial jump rope clip by 25 %"; picture only, his voice unchanged. From clip 1.6 s (the both-feet hop ends 1.53 s) so the 5.5 s it now uses ends at roll ~102.1, before B7's first frame   # R1 review: from 2.0 s (0.5-1.6 s holds a both-feet hop; RO-28 used it from 1.5 s)           # "Your metabolism at 45 is the same as it was at 25." First 5 s (VIDEO-RULES 2026-10-08): Dan's real jump rope, shirtless at 41, as the opener
      talk('T2', 'W', 'P1', c("i'll prove"), c('a study')),             # "I'll prove it to you and show you the real reason why people gain weight as they age."
      card('K1', c('a study'), pe('P3')),                               # the study (script: STUDY ON SCREEN, flat line 20 to 60); hides the P1|P3 take join
      talk('T3', 'T', 'P4', ps('P4'), pe('P4')),                        # "So, what changed since you were 25? Four things, and they were all hit after 40."
      broll('B1', 'A0063', True, ps('P5'), c('a career'), 0.0),         # "You have more stress," (R1 review: the clip's 1.75-2.75 s whirl, jacket off and a briefcase appearing, is cut around)
      broll('B1b', 'A0063', True, c('a career'), c("you're eating"), 2.85),  # "a career, a mortgage, and kids." (kids holding his jacket, he slumps)
      talk('T4', 'W', 'P5', c("you're eating"), c('because')),          # "You're eating worse food without realizing it"
      broll('B2', 'A0242', True, c('because'), c('or eating'), 0.30),   # "because you're grabbing fast food between meetings"
      broll('B3', 'A0072', True, c('or eating'), c('you move'), 0.40),  # "or eating whatever your wife cooks."
      broll('B4', 'A0182', True, c('you move'), c('and you sleep'), 1.8),   # "You move less"
      broll('B5', 'B0559', False, c('and you sleep'), c('food first'), 0.5),   # cache starts at clip 39.0 s (prep_media)  # "and you sleep worse."
      talk('T5', 'T', 'P5', c('food first'), c("if it's")),             # G01 "Food first. Decide what you eat before you're hungry and then eat the protein first."
      talk('T5b', 'W', 'P5', c("if it's"), c('then do')),               # "If it's fast food, order for protein." (R1 review: the chicken bowl B0042 showed protein, not fast food; no library clip shows a fast-food protein order, so Dan stays on camera with a zoom cut)
      broll('B7', 'B0542', False, c('then do'), c('it gets'), 0.33),     # "Then do 15 minutes of exercise first thing every morning." (real Dan, the correct boxer skip, second cut: no overlap with B0's roll time)
      talk('T6', 'W', 'P5', c('it gets'), pe('P5')),            # G02 "It gets you moving again and it takes the edge off the stress for the rest of the day."
      still('S1', 'before', ps('P5b'), pe('P5b')),                # "Bottom line, it's not your age," (script: REAL PHOTO OF ME AT 200 POUNDS, FULL SCREEN)
      still('S2', 'today', ps('P6'), c('subscribe')),                   # "which means you can fix it." (script: REAL PHOTO OF ME TODAY, FULL SCREEN)
      talk('T7', 'T', 'P6', c('subscribe'), END)]                       # G03 subscribe
for s in SH: s['n0'], s['n1'] = fr(s['a']), fr(s['b'])
for x, y in zip(SH, SH[1:]): assert x['n1'] == y['n0'], (x['id'], y['id'], x['n1'], y['n0'])
assert SH[-1]['n1'] == edl['total_frames']
for s in SH: assert s['n1'] - s['n0'] >= 28, (s['id'], s['n1'] - s['n0'])
for s in SH:
    if s['kind'] == 'talk': assert P[s['piece']]['n0'] <= s['n0'] and s['n1'] <= P[s['piece']]['n0'] + P[s['piece']]['frames'], s['id']
if os.environ.get('SHOTS_ONLY'):
    (O/'shots-times.json').write_text(json.dumps(SH, indent=1))
    for x in SH: print(x['id'], x['kind'], x.get('clip', x.get('size', '')), round(x['a'], 2), round(x['b'], 2), round(x['b'] - x['a'], 2))
    # the roll stretches Dan is on screen (key only these, plus 6 frames of handles each side)
    st = []
    for x in SH:
        if x['kind'] != 'talk': continue
        p = P[x['piece']]; r0 = p['start'] + (x['n0'] - p['n0'])/FPS; r1 = p['start'] + (x['n1'] - p['n1'] + p['frames'])/FPS if False else p['start'] + (x['n1'] - p['n0'])/FPS
        st.append([x['id'], round(r0, 3), round(r1, 3)])
    print('ONSCREEN', st, 'total', round(sum(b - a for _, a, b in st), 2), 's'); sys.exit()

def window(m, size):
    hmin = float(np.nanmin(m[:, 0])); w = SIZE[size]
    h = round(w/AR); y0 = hmin - HEAD*h; y0 = max(0.0, min(y0, KH - h))
    return w, h, y0, hmin
frames = {}; report = []
for s in SH:
    if s['kind'] != 'talk': continue
    pc = P[s['piece']]; off = s['n0'] - pc['n0']; n = s['n1'] - s['n0']
    m = measure(pc['start'] + off/FPS, n)
    w, h, y0, hmin = window(m, s['size'])
    clear_out = (hmin - y0)*PH/h
    dn, cx, heads, info = landing.vertical_dense(np.arange(n), m[:, 1], [dict(n0=0, n1=n)], w)
    if s['size'] == 'W': cx = cx + {'T2': 17.0, 'T4': 3.0, 'T5b': 23.0, 'T6': 27.0}.get(s['id'], 17.0)   # R1 review: an elbow sat past the right edge with free field on the left; each wide window is centred on his measured body midline at elbow height (stage-1 matte, rows 1300-2100), not his head
    xs = np.clip(cx - w/2, 0, max(0, KW - w))
    st = landing.motion_stats(np.arange(n), m[:, 1], xs + w/2, [dict(n0=0, n1=n)], w)
    s.update(crop_w=w, crop_h=h, y0=round(y0, 1), hair_top_min=round(hmin, 1), hair_clear_px_out=round(clear_out, 1), motion=st)
    frames[s['id']] = [[round(float(x), 1), round(y0, 1), w, h] for x in xs]
    report.append(dict(id=s['id'], size=s['size'], w=w, hair_min=round(hmin), clear_px=round(clear_out, 1), headroom_pct=round(100*(hmin - y0)/h, 2), **st))
(O/'shots.json').write_text(json.dumps(SH, indent=1)); (O/'framing-frames.json').write_text(json.dumps(frames))
(O/'framing-report.json').write_text(json.dumps(report, indent=1))
for r in report: print(r)
