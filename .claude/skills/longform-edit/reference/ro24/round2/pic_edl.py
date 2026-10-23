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
# framing next to a side card (independent review R2, 6:11.6): S and W are the same size, so a cut between them reads as a sideways
# jump on continuous speech. The shot either side of an S shot is T; shots between two S shots re-alternate from T to T, and if their
# count cannot do that, one reframe-only cut (never a take join) is removed: the pair with the shortest combined length merges.
flat = []; g = 0
for pi, p in enumerate(out):
    for si, sh in enumerate(p['shots']):
        end = p['shots'][si + 1]['f0'] if si + 1 < len(p['shots']) else p['f1']
        flat.append(dict(pi=pi, si=si, join=si == 0, n=end - sh['f0'], t=(g + sh['f0'] - p['f0']) / FPS, sh=sh))
    g += p['f1'] - p['f0']
S = [i for i, x in enumerate(flat) if x['sh']['framing'] == 'S']
drop = set()
for k, i in enumerate(S):
    a = i + 1; b = S[k + 1] if k + 1 < len(S) else len(flat)
    run = [j for j in range(a, b)]
    if k + 1 < len(S) and len(run) % 2 == 0:            # T ... T needs an odd count: merge one reframe-only pair
        cand = [j for j in run[1:] if not flat[j]['join']]
        j = min(cand, key=lambda j: flat[j]['n'] + flat[j - 1]['n']); drop.add(j); run.remove(j)
        print('merged the reframe cut at', round(flat[j]['t'], 2), 'to keep T next to both side cards')
    for m, j in enumerate(run): flat[j]['sh']['framing'] = 'T' if m % 2 == 0 else 'W'
first = S[0] if S else len(flat)
assert first == 0 or flat[first - 1]['sh']['framing'] == 'T', 'shot before the first side card must be tight'
for pi, p in enumerate(out):
    p['shots'] = [x['sh'] for x in flat if x['pi'] == pi and flat.index(x) not in drop]
print('side-card spans', [(round(a, 2), round(b, 2), i) for a, b, i in spans])
json.dump(dict(note=E['note'] + '; take 4 split at 18614 for its two key ranges; S framing under side cards', pieces=out), open(f'{W}/edl_film_pic.json', 'w'), indent=1)
print('pieces', len(out))
