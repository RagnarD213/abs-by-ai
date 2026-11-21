"""RO-21 round 1 graphics: plan_r1.json -> from_plan.py items (lt, l3, fact) and the three ladder configs (custom template,
recipe/hf/ladder). python3 gfx_r1.py [--render] [--only IDS]"""
import json, sys, subprocess, pathlib
B = pathlib.Path('/Volumes/Expansion/_edit_work/RO-21'); R1 = B / 'round1'; HF = B / 'round1/hf'
FP = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py'
P = json.load(open(R1 / 'plan_r1.json'))
items = []
for p in P:
    base = dict(id=p['id'], t0=p['a'], t1=p['b'])
    if p['kind'] == 'lt':
        items.append(dict(base, kind='lt', topic=p['topic'], point=' '.join(x for x, _ in p['parts']), parts=p['parts']))
    elif p['kind'] == 'l3':
        items.append(dict(base, kind='l3', heading=p['heading'], points=p['points'], reveal=p['reveal']))
    elif p['kind'] == 'fact':
        items.append(dict(base, kind='scene', scene='fact', photo=p['photo'], label=p['label'], eyebrow=p['eyebrow'],
                          headline=p['headline'], **({'detail': p['detail']} if p.get('detail') else {})))
HF.mkdir(parents=True, exist_ok=True)
json.dump(items, open(HF / 'plan_resolved.json', 'w'), indent=1)
args = ['python3', FP, '--plan', str(HF / 'plan_resolved.json'), '--words', str(R1 / 'film_words.json'), '--out', str(HF / 'tpl')]
if '--only' in sys.argv: args += ['--only', sys.argv[sys.argv.index('--only') + 1]]
if '--render' in sys.argv: args.append('--render')
r = subprocess.run(args); assert r.returncode == 0
# ladders
LD = HF / 'ladder'; LD.mkdir(exist_ok=True)
img = lambda l: str(B / f'ai_images/L{l:02d}.png')
for p in P:
    if p['kind'] != 'ladder': continue
    if '--only' in sys.argv and p['id'] not in sys.argv[sys.argv.index('--only') + 1].split(','): continue
    a = p['a']; ix = {t['level']: k for k, t in enumerate(p['tiles'])}
    cfg = dict(id=p['id'], dur=round(p['b'] - a, 3), title=p.get('title'),
               tiles=[dict(media=img(t['level']), pct=f"{t['level']}%", at=round(t['at'] - a, 3), pos='50% 12%') for t in p['tiles']])
    if p.get('highlight'): cfg['highlight'] = [dict(tile=ix[h['level']], at=round(h['at'] - a, 3)) for h in p['highlight']]
    if p.get('band'): cfg['band'] = dict(lines=[dict(s=b['s'], lead=b.get('lead'), at=round(b['at'] - a, 3), px=40) for b in p['band']])
    body = json.dumps(cfg, indent=1); cj = LD / f"{p['id']}.json"; mov = LD / f"{p['id']}.mov"
    if '--render' in sys.argv and cj.exists() and cj.read_text() == body and mov.exists() and (LD / f"{p['id']}.ok").exists():
        print(p['id'], 'unchanged, render kept'); continue
    cj.write_text(body); (LD / f"{p['id']}.ok").unlink(missing_ok=True)
    cmd = ['python3', str(B / 'recipe/hf/ladder/build.py'), str(LD / f"{p['id']}.json"), str(LD), '--snap', f"{min(cfg['dur'] - 0.1, 4.0)},{cfg['dur'] - 0.2}"]
    if '--render' in sys.argv: cmd.append('--render')
    assert subprocess.run(cmd).returncode == 0, p['id']
    if '--render' in sys.argv: (LD / f"{p['id']}.ok").write_text(body)
print('GFX DONE')
