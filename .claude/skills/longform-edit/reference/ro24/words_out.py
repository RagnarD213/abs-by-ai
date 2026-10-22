"""Map source words (audio/words_src.json, medium.en, source seconds) through an EDL to film time: a word is kept only when
its midpoint lies strictly inside a kept piece (longform lesson 9). Writes words_out.json [{w, t0, t1}] and out_sentences.txt."""
import sys, json, re
FPS = 30000 / 1001
edl, out = sys.argv[1], sys.argv[2]
E = json.load(open(edl)); W = json.load(open('/Volumes/Expansion/_edit_work/RO-24/round1/audio/words_src.json'))
res = []; g = 0
for p in E['pieces']:
    s0, s1 = p['f0'] / FPS, p['f1'] / FPS; o = g / FPS
    for w in W:
        mid = (w['t0'] + w['t1']) / 2
        if s0 < mid < s1:
            res.append(dict(w=w['w'], t0=round(o + max(w['t0'], s0) - s0, 3), t1=round(o + min(w['t1'], s1) - s0, 3), src=w['t0']))
    g += p['f1'] - p['f0']
json.dump(res, open(out, 'w'), indent=0)
sent = []; cur = []
for w in res:
    cur.append(w)
    if re.search(r'[.?!]$', w['w']): sent.append(f"{cur[0]['t0']:6.2f} {' '.join(x['w'] for x in cur)}"); cur = []
if cur: sent.append(f"{cur[0]['t0']:6.2f} {' '.join(x['w'] for x in cur)}")
open(out.replace('.json', '_sentences.txt'), 'w').write('\n'.join(sent)); print('\n'.join(sent)); print('film', g / FPS)
