"""RO-21 round 1 presenter shots: a picture cut at every EDL join, every full-screen insert edge and every side-card edge
(Dan moves right under a 3A card), plus framing changes at sentence ends so no shot runs past about 12 s. Framing alternates
W/T at every cut (house rule: a cut always changes the framing). Writes round1/shots.json [{t0, t1, framing}]."""
import json
B = '/Volumes/Expansion/_edit_work/RO-21/round1'
E = json.load(open(f'{B}/edl_r1.json')); P = json.load(open(f'{B}/plan_r1.json')); W = json.load(open(f'{B}/film_words.json'))
END = P[-1]['b'] if P[-1]['kind'] == 'ladder' else E[-1]['film_out']
hard = {round(e['film_in'], 3) for e in E[1:]}
full = [p for p in P if p['kind'] in ('ladder', 'fact', 'broll', 'photo', 'photo_ai')]
for p in full + [p for p in P if p['kind'] == 'l3' and not p.get('overlay_on')]: hard |= {round(p['a'], 3), round(p['b'], 3)}
hard = sorted(t for t in hard if 0 < t < END)
sent = [w['t1'] + 0.12 for i, w in enumerate(W[:-1]) if w['w'].endswith(('.', '?', '!')) and W[i + 1]['t0'] - w['t1'] > 0.2]
cuts, last = [], 0.0
pts = sorted(set(hard) | {round(s, 3) for s in sent})
for t in pts:
    if t in hard or t - last >= 7.0:
        nxt_hard = min([h for h in hard if h > t] + [END])
        if t not in hard and nxt_hard - t < 3.0: continue      # no short sliver before a hard cut
        if t - last > 0.3: cuts.append(t); last = t
bounds = [0.0] + cuts + [END]
shots = []; f = 'W'
for a, b in zip(bounds, bounds[1:]):
    covered = any(p['a'] <= a + 0.01 and p['b'] >= b - 0.01 for p in full)
    shots.append(dict(t0=round(a, 3), t1=round(b, 3), framing=f, covered=covered))
    if not covered: f = 'T' if f == 'W' else 'W'
json.dump(shots, open(f'{B}/shots.json', 'w'), indent=1)
vis = [s for s in shots if not s['covered']]
print(len(shots), 'shots,', len(vis), 'with Dan on screen; longest', max(s['t1'] - s['t0'] for s in vis))
print('Dan on screen', round(sum(s['t1'] - s['t0'] for s in vis), 1), 's of', round(END, 1))
