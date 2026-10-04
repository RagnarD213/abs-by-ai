#!/usr/bin/env python3
"""THE 1:1 TALKING-HEAD CROP = the vertical's crop with the width opened to the height (skill A14.3): the same hold
schedule, the same NEAR/FAR heights (832 / 1024 of the 1080 source: a 1.30x / 1.05x picture, sharper than the 9:16), the
same hair-anchored y0 and the same zoom ramps. Horizontal centre: the shared landing standard at the square's own width
(dead band 3.3 % of the crop width), which at these widths is steady per shot. Writes crop_sq.json."""
import json, sys, numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import landing
FPS = 30000/1001
C = json.load(open('crop.json')); E = json.load(open('edl_picture.json'))
M = [m for m in json.load(open('measure.json')) if m.get('ok')]
_FACE = json.load(open('measure_face.json'))          # his face centre (zcrop.py explains), not the mask's head column
mn = np.array([m['n'] for m in M]); mhead = np.array([_FACE.get(str(m['n']), m['head'] + 9.9) for m in M])
frames = {}
for k, (x0, y0, w, h) in C['frames'].items():
    h2 = min(h, 1080.0 - y0); cx = x0 + w/2
    frames[int(k)] = [round(float(np.clip(cx - h2/2, 0, 1920 - h2)), 2), y0, round(h2, 2), round(h2, 2)]
sys.path.insert(0, '.'); import beats as _B
cuts = ({s['n0'] for s in E} & {j['n'] for j in C['joins'] if j['visible']}) | ({h['n0'] for h in C['holds']} & {b['n0'] for b in _B.timeline()[0]}); segs = []      # re-land only at VISIBLE joins (zcrop.py)
for h in C['holds']:
    if segs and h['n0'] == segs[-1]['n1'] and h['n0'] not in cuts: segs[-1]['n1'] = h['n1']
    else: segs.append(dict(n0=h['n0'], n1=h['n1']))
edges = {b['n0'] for b in _B.timeline()[0]}; _mn = [int(v) for v in mn]; _mh = [float(v) for v in mhead]; _sp = []
for sg in segs:                               # land where a window opens or closes inside a hold too (zcrop.py, round 3)
    a_ = sg['n0']
    for e in sorted(e for e in edges if sg['n0'] < e < sg['n1']) + [sg['n1']]:
        _sp.append(dict(n0=a_, n1=e)); a_ = e
        if e < sg['n1'] and e not in _mn: _mn.append(e); _mh.append(float(np.interp(e, mn, mhead)))
_o = np.argsort(_mn); segs = _sp
rep = landing.vertical_crop_frames(frames, segs, np.array(_mn)[_o], np.array(_mh)[_o], FPS)
json.dump(dict(C, frames={str(k): v for k, v in frames.items()}), open('crop_sq.json', 'w'))
json.dump(rep, open('square-centering-stats.json', 'w'), indent=1)
tr = sum(r['stats']['travel_px'] for r in rep); fx = sum(1 for r in rep if r['stats']['travel_px'] == 0)
print(f"{len(frames)} frames, {len(segs)} segments, {fx} with one fixed centre; total crop travel {tr:.0f} source px; "
      f"max off-centre {max(r['stats']['off_centre_px']['max'] for r in rep):.0f} px")
