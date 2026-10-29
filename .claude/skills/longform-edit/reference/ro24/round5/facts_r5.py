"""RO-24 round 5 plan and manifest: round 4's, moved through the pause retime (retime_r5.py, r5_t), plus Dan's round 4 notes:
G06 rebuilt (round5/hf/gfx), P8 Amy Schumer's abs post (round5/hf), and the AI motion inserts in ai_inserts.json (written by
ai_r5.py once each take has passed clipcheck and a fresh frame-reviewer). Nothing else changes; the planner is not re-run
(Dan approved every round 4 background).

  python3 facts_r5.py   ->  round5/film_manifest_r5.json, round5/bg_plan.json
BG20 (7 DAYS A WEEK big type) loses its last 19 frames at the new cut; its round 4 render is used as is (the type has landed
by then; the segment's frames end at the cut)."""
import json, pathlib, sys
R4 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round4'); R5 = R4.parent / 'round5'
sys.path.insert(0, str(R5 / 'recipe')); from retime_r5 import r5_t, AT, CUT, FPS

MAN = json.load(open(R4 / 'film_manifest_r4.json'))
for m in MAN:
    assert m['b'] <= AT / FPS + 1e-6 or m['a'] >= (AT + CUT) / FPS - 1e-6, ('item spans the removed frames', m)
    m['a'], m['b'] = round(r5_t(m['a']), 4), round(r5_t(m['b']), 4)
    if m['id'] == 'G06':
        m.update(mov=str(R5 / 'hf/gfx/renders/G06.mov'), round=5,
                 note="Dan R4: 'Zepbound beats Ozempic in studies', Zepbound / Ozempic labels, quit bars 2.7 % / 5.6 %")
P8 = next(m for m in json.load(open(R5 / 'hf/photos_manifest.json')) if m['id'] == 'P8')
MAN.append(dict(P8, round=5, note="Dan R4: Amy Schumer's abs picture on 'and she posted pictures of her abs'"))
AI = R5 / 'ai_inserts.json'
if AI.exists():
    for x in json.load(open(AI)):
        MAN = [m for m in MAN if m['id'] not in x.get('replaces', [])]
        MAN.append(dict(id=x['id'], template='broll', kind='opaque', a=x['a'], b=x['b'], mov=x['mov'], round=5, note=x['note']))
MAN.sort(key=lambda m: m['a'])
op = [m for m in MAN if m['kind'] == 'opaque']
for p, q in zip(op, op[1:]): assert q['a'] >= p['b'] - 1e-3, ('opaque items overlap', p['id'], q['id'])
json.dump(MAN, open(R5 / 'film_manifest_r5.json', 'w'), indent=1)

P = json.load(open(R4 / 'bg_plan.json'))
for s in P['segments']:
    s['t0'], s['t1'] = round(r5_t(s['t0']), 4), round(r5_t(s['t1']), 4)
    if s.get('line_times'): s['line_times'] = [round(r5_t(t), 3) for t in s['line_times']]
    if s['id'] == 'BG20': s['why'] += ' | round 5: ends 19 frames earlier, at the tightened cut (pause removed)'
json.dump(P, open(R5 / 'bg_plan.json', 'w'), indent=1)
print(len(MAN), 'manifest items,', len(P['segments']), 'segments; film', round(json.load(open(R5 / 'edl_r5.json'))['items'][-1]['o1'] / FPS, 3), 's')
