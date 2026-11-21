"""RO-24 round 3 film manifest for the compositor: round 2's graphics on the new timeline (manifest_r2_mapped.json), the
round 3 photo scenes in place of P0-P3, and the six clip inserts as opaque items. -> film_manifest_r3.json"""
import json, pathlib
R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3'); FPS = 30000 / 1001
M = {m['id']: m for m in json.load(open(R3 / 'manifest_r2_mapped.json'))}
for m in json.load(open(R3 / 'hf/photos_manifest.json')):
    old = M.get(m['id']); assert old is None or abs(old['a'] - m['a']) < 0.02 and abs(old['b'] - m['b']) < 0.02, (m['id'], old, m)
    M[m['id']] = dict(m, round=3)
E = json.load(open(R3 / 'edl_r3.json'))['items']
for it in E:
    if it['kind'] == 'insert':
        M['C_' + it['clip']] = dict(id='C_' + it['clip'], kind='opaque', template='clip', a=round(it['o0'] / FPS + 0.0005, 4),
                                    b=round(it['o1'] / FPS + 0.0005, 4), mov=it['mov'], note='interview clip, plays with its own sound')
out = sorted(M.values(), key=lambda m: m['a'])
for a, b in zip([m for m in out if m['kind'] == 'opaque'], [m for m in out if m['kind'] == 'opaque'][1:]):
    assert round(a['b'] * FPS) <= round(b['a'] * FPS), ('opaque overlap', a['id'], b['id'])
json.dump(out, open(R3 / 'film_manifest_r3.json', 'w'), indent=1)
print(len(out), 'items'); [print(f"{m['id']:9s} {m['kind']:7s} {m['a']:8.2f}-{m['b']:8.2f}") for m in out if m['a'] < 175]
