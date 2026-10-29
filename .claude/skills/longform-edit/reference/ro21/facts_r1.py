"""RO-21 round 1: the facts the green-screen background planner reads (greenscreen-bg/planner.py), on the round 1 film
timeline, then the planner -> round1/bg_plan.json. Each body fat level is a "person": its AI picture, a pair (this level and
the next one down) for the panel, big type for its number. Behind-Dan AI pictures get the AI-GENERATED chip from the film's
assembler (ai_label), since only the shared set type draws one itself.
  python3 facts_r1.py"""
import json, subprocess
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'
GS = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'
P = json.load(open(f'{R1}/plan_r1.json')); S = json.load(open(f'{R1}/shots.json')); W = json.load(open(f'{R1}/film_words.json'))
import importlib.util; spec = importlib.util.spec_from_file_location('plan', f'{B}/recipe/plan_r1.py')
def at(phrase, lo=0.0):
    import re
    n = lambda s: re.sub(r"[^a-z0-9%']", '', s.lower().replace('-', ''))
    toks = [n(t) for t in phrase.split()]
    for i, w in enumerate(W):
        if w['t0'] < lo - 0.05: continue
        if all(i + k < len(W) and n(W[i + k]['w']).startswith(t) for k, t in enumerate(toks)): return round(w['t0'], 3)
    raise SystemExit(f'not found {phrase}')
IMG = lambda l: f'{B}/ai_images/L{l:02d}.png'
LV = [35, 30, 25, 20, 15, 12, 10, 8]
name = lambda l: f'{l}% Body Fat'
people = {}
for k, l in enumerate(LV):
    nxt = LV[k + 1] if k + 1 < len(LV) else None
    pr = [IMG(l), IMG(nxt)] if nxt else [IMG(LV[k - 1]), IMG(l)]
    yrs = [f'{l}%', f'{nxt}%'] if nxt else [f'{LV[k - 1]}%', f'{l}%']
    people[name(l)] = dict(photos=[IMG(l)], pairs=[dict(photos=pr, years=yrs, crop_k=7.0)],
                           stat=(f'Next Stop: {nxt}%' if nxt else 'The Full Six Pack'), big=[f'{l}%', 'BODY FAT'])
facts = {p['level']: p['a'] for p in P if p['kind'] == 'fact' and p['id'].startswith('F')}
sections = [dict(t0=facts[l], t1=(facts[LV[k + 1]] if k + 1 < len(LV) else P[-1]['a']), person=name(l)) for k, l in enumerate(LV)]
kind = {'ladder': 'card', 'fact': 'photo', 'broll': 'broll', 'photo': 'photo', 'photo_ai': 'photo'}
inserts = []
for p in P:
    if p['kind'] in kind:
        it = dict(t0=p['a'], t1=p['b'], kind='intro' if p['id'] == 'G01' else kind[p['kind']])
        if p['kind'] == 'fact': it['person'] = name(p['level'])
        inserts.append(it)
numbers = [dict(t=at('first 20 pounds'), lines=['20 LB', 'THE FIRST']), dict(t=at('five minutes for a workout') if False else at('Now, 5 minutes'), lines=['5 MIN', 'EVERY MORNING']),
           dict(t=at("let's say you're 180"), lines=['180 LB', 'AT 12%'])]
transformations = [dict(t0=at('And this is the reason why'), t1=at('Your action step is to cut every'), person=name(30)),
                   dict(t0=at('It will also protect'), t1=at("Now, let's talk about 20"), person=name(25)),
                   dict(t0=at('Now, this is the level'), t1=at("Let's talk about 12"), person=name(15)),
                   dict(t0=at("Ab exercises don't burn"), t1=at("That's why I train abs every day now"), person=name(8))]
side = [dict(t0=p['a'], t1=p['b']) for p in P if p['kind'] in ('l3', 'phone') and not p.get('overlay_on')]
lts = [dict(t0=p['a'], t1=p['b']) for p in P if p['kind'] == 'lt']
F = dict(shots=[dict(t0=s['t0'], t1=s['t1'], framing=s['framing']) for s in S if not s['covered']], inserts=inserts, people=people,
         sections=sections, numbers=numbers, transformations=transformations, side_cards=side, lower_thirds=lts,
         everyone=[IMG(l) for l in LV])
json.dump(F, open(f'{R1}/facts.json', 'w'), indent=1)
ovr = {'BG02': dict(photos=[IMG(30), IMG(25)], why='he talks about the average man at 28%: the TV shows 30% and 25%, not the lean end'),
       'BG04': dict(type='cards', photos=[IMG(l) for l in [30, 20, 12, 25, 15, 8]], why='variety: the eight pictures float again while he explains how to use them (the planner chose the set)')}
json.dump(ovr, open(f'{R1}/bg_overrides.json', 'w'), indent=1)
subprocess.run(['python3', f'{GS}/planner.py', f'{R1}/facts.json', f'{R1}/bg_plan.json', '--overrides', f'{R1}/bg_overrides.json'], check=True)
# The calm "soft" background blurred an AI picture of Dan behind Dan: it read as a ghost of him (first-minute check,
# 2026-10-29). Soft segments get a blurred still of the film's own graded B-roll for that section instead (real footage).
ST = lambda n: f'{R1}/bgstills/{n}.jpg'
SOFT = {None: 'gym', name(35): ['squat', 'kb'], name(30): 'soda', name(25): 'kb', name(20): 'gym', name(15): 'mealprep',
        name(12): ['salmon', 'sleep'], name(10): 'steak', name(8): 'cable'}
plan = json.load(open(f'{R1}/bg_plan.json')); used = {}
import os
for g in plan['segments']:                       # the HyperFrames text backgrounds (hfbg.py --render writes bg/<id>.mov)
    if g['type'] in ('panel', 'bigtype') and os.path.exists(f"{R1}/bg/{g['id']}.mov"): g['mov'] = f"bg/{g['id']}.mov"
for g in plan['segments']:
    if g['type'] != 'soft': continue
    c = SOFT.get(g.get('person'), 'gym'); c = c if isinstance(c, str) else c[min(used.get(g.get('person'), 0), len(c) - 1)]
    used[g.get('person')] = used.get(g.get('person'), 0) + 1
    g.update(photos=[ST(c)], ai_label=False, why=g['why'] + f' (blurred still of the film B-roll: {c})')
# PH1 (the app phone on the left third) follows the A10 card: one calm segment behind both, so the phone never covers the set's
# TV and its AI chip (round 1 context sheet, 2026-10-29)
segs = plan['segments']; ph = [p for p in P if p['id'] == 'PH1'][0]
for k, g in enumerate(segs):
    if g['type'] == 'soft' and g['t0'] <= ph['a'] < g['t1'] and k + 1 < len(segs) and segs[k + 1]['t0'] < ph['b']:
        g['t1'] = segs[k + 1]['t1']; g['why'] += ' (editor: runs on under the app phone, merged with the next segment)'; del segs[k + 1]; break
json.dump(plan, open(f'{R1}/bg_plan.json', 'w'), indent=1)
for g in plan['segments']:
    if g['type'] == 'soft': print(g['id'], g.get('person'), g['photos'][0].rsplit('/', 1)[-1])
