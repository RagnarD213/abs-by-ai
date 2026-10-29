"""Scale a round 4 frame spec (START pixels, 1672x941) to a Flow take (1920x1080) for clipcheck, and declare the camera locked
(every motion prompt asked for a locked camera). Optional --at A: boxes moved to frame A of the take are not attempted here;
clipcheck reads boxes in frame A's pixels, so windows that start late use a spec with no rigid/contacts (still and props only).
  takespec_r5.py SPEC OUT [--w 1920 --h 1080]"""
import json, sys
src, out = sys.argv[1], sys.argv[2]; W, H = 1920, 1080; SW, SH = 1672, 941
sx, sy = W / SW, H / SH
def box(b): return [round(b[0] * sx), round(b[1] * sy), round(b[2] * sx), round(b[3] * sy)]
S = json.load(open(src)); S['take_scale'] = f'{SW}x{SH} -> {W}x{H} (takespec_r5.py)'; S['camera'] = 'locked'
for k in ('may_change', 'still'):
    if k in S: S[k] = {n: box(b) for n, b in S[k].items()}
for p in S.get('props', []): p['box'] = box(p['box'])
for c in S.get('contacts', []): c['box'] = box(c['box'])
for r in S.get('rigid', []):
    r['parts'] = {n: box(b) for n, b in r['parts'].items()} if isinstance(r.get('parts'), dict) else [box(b) for b in r.get('parts', [])]
    if 'extent' in r: r['extent'] = box(r['extent'])
    if 'guide' in r: r['guide'] = box(r['guide'])
    if 'move_px' in r: r['move_px'] = [round(v * sx) for v in r['move_px']]
pe = S.get('person') or {}
if 'guide' in pe: pe['guide'] = box(pe['guide'])
if 'legs_hidden' in pe: pe['legs_hidden']['below_y'] = round(pe['legs_hidden']['below_y'] * sy)
json.dump(S, open(out, 'w'), indent=1); print(out, sorted(S))
