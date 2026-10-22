"""Picture EDL for round 2: edl_film.json with take 4 split at its shot change 18614 into the two key ranges it was keyed in
(R04a 17942-18618, R04b 18610-19987; same box and plate, so frames at least 3 from either range end are identical). The audio keeps
edl_film.json (one continuous piece there: crossfading a piece with itself would add 3 dB)."""
import json
W = '/Volumes/Expansion/_edit_work/RO-24/round2'; K = f'{W}/key'
E = json.load(open(f'{W}/edl_film.json')); out = []
for p in E['pieces']:
    if p['key'].endswith('/R04.mkv'):
        SPLIT = 18614; assert any(s['f0'] == SPLIT for s in p['shots'])
        a = dict(p, id=p['id'] + 'a', f1=SPLIT, key=f'{K}/R04a.mkv', shots=[s for s in p['shots'] if s['f0'] < SPLIT])
        b = dict(p, id=p['id'] + 'b', f0=SPLIT, key=f'{K}/R04b.mkv', shots=[s for s in p['shots'] if s['f0'] >= SPLIT])
        out += [a, b]
    else: out.append(p)
# left-third side cards (hf manifest, kind overlay): every shot inside a card span becomes ONE shot in framing S (wide, Dan shifted
# right); the span must start on a shot boundary. The card enters on a cut and leaves on a cut.
import os
FPS = 30000 / 1001; spans = []
if os.path.exists(f'{W}/hf/manifest.json'):
    spans = [(m['a'], m['b'], m['id']) for m in json.load(open(f'{W}/hf/manifest.json')) if m['kind'] == 'overlay']
g = 0
for p in out:
    keep = []
    for s in p['shots']:
        t = (g + s['f0'] - p['f0']) / FPS
        inside = [sp for sp in spans if sp[0] - 0.05 <= t < sp[1] - 0.05]
        if inside:
            if keep and keep[-1].get('card') == inside[0][2]: continue          # merged into the span's first shot
            if abs(t - inside[0][0]) > 0.05 and not (keep and keep[-1].get('card')): print('WARN card', inside[0][2], 'does not start on this cut', round(t, 2))
            keep.append(dict(s, framing='S', card=inside[0][2]))
        else: keep.append(s)
    p['shots'] = keep; g += p['f1'] - p['f0']
print('side-card spans', [(round(a, 2), round(b, 2), i) for a, b, i in spans])
json.dump(dict(note=E['note'] + '; take 4 split at 18614 for its two key ranges; S framing under side cards', pieces=out), open(f'{W}/edl_film_pic.json', 'w'), indent=1)
print('pieces', len(out))
