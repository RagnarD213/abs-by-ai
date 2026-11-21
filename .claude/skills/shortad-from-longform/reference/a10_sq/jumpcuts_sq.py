#!/usr/bin/env python3
"""STEP 7c, structurally: which of his picture splices does OUR beat map leave bare?

The skill's method: list every splice in the recovered picture EDL, mark which are covered in
HIS map and which in OURS, and the difference is exactly what our deviations broke. Here the
comparison that matters is against the APPROVED VERTICAL, because the square is a re-layout of
it -- if the square covers every splice the vertical covered, the square cannot have created a
naked jump cut that Dan has not already seen and approved.

Cover = a flash window, an insert/graphic beat, or a beat boundary within +-0.20 s.
"""
import importlib.util, json, sys

FPS = 30000/1001

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

sys.path.insert(0, '.')
sq = load('beats', 'beats.py')
vt = load('beats_v', 'beats_9x16_orig.py')

def covered(B, t):
    for a, b in B.FLASHES:
        if a - 0.02 <= t <= b + 0.02: return 'flash'
    tl, _ = B.timeline()
    for b in tl:
        if b['kind'] != 'talk' and b['t0'] - 0.02 <= t <= b['t1'] + 0.02: return b['kind']
        if abs(b['t0'] - t) <= 0.20 or abs(b['t1'] - t) <= 0.20: return 'boundary'
    return None

P = json.load(open('edl_picture.json'))
cuts = [s['cut_in'] for s in P[1:]]
rows = [(t, covered(vt, t), covered(sq, t)) for t in cuts]
bare_v = [t for t, v, s in rows if v is None]
bare_s = [t for t, v, s in rows if s is None]
new = [t for t, v, s in rows if v is not None and s is None]
print(f'{len(cuts)} picture splices in the recovered EDL')
print(f'  bare in the APPROVED VERTICAL : {len(bare_v)}  {[round(t,2) for t in bare_v]}')
print(f'  bare in the SQUARE            : {len(bare_s)}  {[round(t,2) for t in bare_s]}')
print(f'  NEWLY bare (the square broke) : {len(new)}  {[round(t,2) for t in new]}')
chg = [(round(t,2), v, s) for t, v, s in rows if v != s]
print(f'  splices whose cover CHANGED   : {len(chg)}  {chg}')
json.dump(dict(cuts=len(cuts), bare_vertical=bare_v, bare_square=bare_s, newly_bare=new,
               changed=[(t, v, s) for t, v, s in rows if v != s]),
          open('logs/jumpcuts_sq.json', 'w'), indent=1)
sys.exit(1 if new else 0)
