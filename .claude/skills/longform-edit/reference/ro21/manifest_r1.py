"""RO-21 round 1 compositor manifest: from_plan's HyperFrames items (lower thirds, side cards, level/photo cards) + the three
ladder scenes + the B-roll inserts (opaque) + the app phone overlay. -> round1/film_manifest.json. Missing media are
listed (round 1 builds the first minute before everything exists)."""
import json, os, pathlib
R1 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-21/round1'); B = R1.parent
P = {p['id']: p for p in json.load(open(R1 / 'plan_r1.json'))}
M = [m for m in json.load(open(R1 / 'hf/tpl/manifest.json')) if m['id'] in P]
for m in M: m.update(a=P[m['id']]['a'], b=P[m['id']]['b'])
for p in P.values():
    if p['kind'] == 'ladder': M.append(dict(id=p['id'], template='local:ladder', a=p['a'], b=p['b'], mov=str(R1 / f"hf/ladder/{p['id']}.mov"), kind='opaque'))
    if p['kind'] == 'broll': M.append(dict(id=p['id'], template='local:broll', a=p['a'], b=p['b'], mov=str(B / f"broll/{p['id']}.mp4"), kind='opaque'))
    if p['kind'] == 'phone': M.append(dict(id=p['id'], template='local:phone', a=p['a'], b=p['b'], mov=str(R1 / f"hf/phone/{p['id']}.mov"), kind='overlay',
                                           card_right=752, card=[36, 42, 752, 1038]))
M.sort(key=lambda m: m['a'])
for x, y in zip(M, M[1:]):
    if x['kind'] == 'opaque' and y['kind'] == 'opaque': assert x['b'] <= y['a'] + 1e-3, (x['id'], y['id'])
missing = [m['id'] for m in M if not os.path.exists(m['mov'])]
json.dump(M, open(R1 / 'film_manifest.json', 'w'), indent=1)
print(len(M), 'items; missing media:', ', '.join(missing) or 'none')
