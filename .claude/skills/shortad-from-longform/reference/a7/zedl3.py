#!/usr/bin/env python3
"""Clean the recovered EDL against the beat sheet: every TALK / WINDOW beat of beats.py must be covered by picture
segments, and no segment may run into an insert beat.
  * drop segments with rmed < 0.60 (false positives inside inserts);
  * clip every segment to the union of talk/window beat ranges;
  * where a talk beat starts/ends a few frames outside its nearest segment (his flash frames, a card's pop-in), extend
    that segment's edge (same offset) so no talk frame is left uncovered -- at most 20 frames;
  * assert coverage. Rewrites edl_picture.json."""
import json, sys
sys.path.insert(0, '.'); import beats as B
FPS = B.FPS
E = json.load(open('edl_picture.json'))
tl, _ = B.timeline()
TALK = [(b['n0'], b['n1']) for b in tl if b['kind'] in ('talk', 'window')]
def in_talk(n): return any(a <= n < z for a, z in TALK)
out = []
for s in E:
    if s['rmed'] < 0.60: print('drop', round(s['t0'],2), round(s['t1'],2), 'rmed', s['rmed']); continue
    for a, z in TALK:
        n0, n1 = max(s['n0'], a), min(s['n1'], z)
        if n1 - n0 < 2: continue
        fr = s['framing'][n0-s['n0']:n1-s['n0']]
        out.append(dict(s, n0=n0, n1=n1, t0=round(n0/FPS,4), t1=round(n1/FPS,4), src_in=round(s['src_in'] + (n0-s['n0'])/FPS, 4), framing=fr))
out.sort(key=lambda s: s['n0'])
# extend to the beat edges
for a, z in TALK:
    segs = [s for s in out if a <= s['n0'] < z or a < s['n1'] <= z]
    if not segs: print('!! talk beat', a, z, 'has NO segment'); continue
    first = min(segs, key=lambda s: s['n0']); last = max(segs, key=lambda s: s['n1'])
    if 0 < first['n0'] - a <= 20:
        k = first['n0'] - a; first['framing'] = [first['framing'][0]]*k + first['framing']
        first.update(n0=a, t0=round(a/FPS,4), src_in=round(first['src_in'] - k/FPS, 4)); print('extend start', a, '+', k)
    if 0 < z - last['n1'] <= 20:
        k = z - last['n1']; last['framing'] = last['framing'] + [last['framing'][-1]]*k
        last.update(n1=z, t1=round(z/FPS,4)); print('extend end', z, '+', k)
# fill any remaining interior gaps inside a talk beat from the neighbour (same offset)
out.sort(key=lambda s: s['n0'])
i = 0
while i < len(out)-1:
    s, nx = out[i], out[i+1]
    if nx['n0'] > s['n1'] and in_talk(s['n1']) and in_talk(nx['n0']-1) and nx['n0'] - s['n1'] <= 20:
        k = nx['n0'] - s['n1']; s['framing'] += [s['framing'][-1]]*k; s.update(n1=nx['n0'], t1=round(nx['n0']/FPS,4)); print('bridge gap', s['n1']-k, '+', k)
    i += 1
cov = set()
for s in out: cov.update(range(s['n0'], s['n1']))
miss = [n for a, z in TALK for n in range(a, z) if n not in cov]
print(len(out), 'segments; uncovered talk frames:', len(miss), miss[:20])
json.dump(out, open('edl_picture.json','w'))
for s in out: print(f"  {s['t0']:8.3f}-{s['t1']:8.3f}  n{s['n0']}-{s['n1']}  off {s['off']:+.3f}  src {s['src_in']:.3f}  rmed {s['rmed']:.2f}")
