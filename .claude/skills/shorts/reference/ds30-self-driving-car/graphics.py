"""DS-30 R1 graphics (python3 graphics.py): Soft Blue Light HyperFrames, moving for their whole screen time; eyebrows in capitals,
main points in title case (VIDEO-RULES 2026-10-16/20). Lower thirds at the 9:16 layout (strip x 68..1012, bottom at 68 %),
the cost comparison on the shared compare-card template at the full 1080 x 1920 canvas (opaque; captions burn on top).
  K1  compare card under "Kelley Blue Book puts the five-year cost on a base Model 3 at about $47,000 all in. A base Camry is
      about $48,000." (Dan's final take; his numbers.) Covers the P3/P4 join.
  G01 on the wide hold "That's seven hours a week when you can't do anything but stare at the road."
        THE COST OF DRIVING / 7 Hours A Week / You Could Spend Training
  G02 on the wide hold "You'll be shocked at how much focus and energy you have left for working once you stop wasting it on driving."
        THE PAYOFF / Hours Back Every Week, / More Energy Left For You
Writes hf/ renders + graphics-manifest.json (Compositor format)."""
from pathlib import Path
import sys, json
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); sys.path.insert(0, str(HF/'compare-card'))
import vertical as V, hfbuild as H
import importlib.util
spec = importlib.util.spec_from_file_location('cc', HF/'compare-card'/'build.py'); CC = importlib.util.module_from_spec(spec); spec.loader.exec_module(CC)
FPS = 30000/1001
words = json.load(open(W/'words_out.json')); edl = json.load(open(W/'edl.json'))
shots = json.load(open(W/'shots.json'))
def at(phrase, after=0, end=False):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and [x['w'].lower().strip('.,!?…') for x in words[i:i+len(toks)]] == toks:
            return words[i + len(toks) - 1]['t1'] if end else words[i]['t0']
    raise ValueError(phrase)
def shot(kind, near):
    return min((s for s in shots if s.get('size', s.get('k')) == kind), key=lambda s: abs(s['a'] - near))
S1 = shot('wide', 10.3); S2 = shot('wide', 52.6); K = [s for s in shots if s['kind'] == 'card'][0]
LT = [('G01', S1['a'] + 0.15, S1['b'] - 0.09, 'The Cost Of Driving', [('7 Hours A Week', "that's seven"), ('You Could Spend Training', 'but stare')]),
      ('G02', S2['a'] + 0.15, S2['b'] - 0.09, 'The Payoff', [('Hours Back Every Week,', "you'll be shocked"), ('More Energy Left For You', 'energy you have')])]

def kbb_card():
    a, b = K['a'], K['b']
    s = dict(id='K1', a=a, b=b, canvas=[1080, 1920], eyebrow='5-YEAR COST TO OWN  ·  KELLEY BLUE BOOK',
             panels=[dict(head='Tesla Model 3 (Base)', t=at('kelley blue book') + 0.15, rows=[['About $47,000 All In', at('$47,000')]]),
                     dict(head='Toyota Camry (Base)', t=at('a base camry') - 0.05, rows=[['About $48,000', at('$48,000')]])])
    cfg = CC.scene_cfg(s, head_px=68, row_px=62, rh=112, top=560, gap=70)
    # larger type than the template's 1080 x 1610 default: push the divider and rows down to clear the 68 px header
    y = 560
    for p in cfg['panels']:
        p['div_y'] = 128
        for r in p['rows']: r['y'] += 30
        p['h'] += 30; p['y'] = y; y += p['h'] + 70
    cfg['eyebrow']['y'] = 448; cfg['eyebrow']['px'] = 36
    cfg['accent'] = [64, 424, 96]
    for p in cfg['panels']: assert p['y'] + p['h'] < 1330, ('card clears the captions', p['y'] + p['h'])
    return [(HF/'compare-card'/'compare-card.template.htm', cfg, ())], s

if __name__ == '__main__':
    out = W/'hf'; man = []
    for gid, a, b, topic, parts in LT:
        ps = [[s, max(a, at(p, a - 1))] for s, p in parts]
        a = max(a, ps[0][1] - 0.27)
        # watch judge (final pass): the default 9:16 position (bottom at 68 %) sat across his torso in the original-frame wide
        # shot; VIDEO-RULES keeps compact graphics in measured clear space, off face and abs. The backdrop above his head is
        # empty: the strip goes at y 150-398, >= 40 px above his highest hair top (438 px, source-measurements.json).
        c = {'id': gid, 'a': a, 'b': b, 'topic': topic, 'parts': ps, 'top_y': 150}
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, out, render=True, snap=1)
        man.append(dict(id=gid, a=a, b=b, template='lower-third', kind='glass', mov=str(out/'renders'/f'{gid}.mov'), mask=str(out/'renders'/f'{gid}_mask.mov'),
                        band=meta['band'], box=meta['box'], lines=meta['lines'], words=topic.upper() + ': ' + ' '.join(s for s, _ in parts),
                        lands=[[s, t] for s, t in ps]))
    sc, s = kbb_card()
    V.build(sc, out, render=True, snap=round(at('$48,000') - K['a'] + 0.8, 2))
    man.append(dict(id='K1', a=K['a'], b=K['b'], template='compare-card', kind='opaque', mov=str(out/'renders'/'K1.mov'),
                    words='5-YEAR COST TO OWN · KELLEY BLUE BOOK / Tesla Model 3 (Base): About $47,000 All In / Toyota Camry (Base): About $48,000',
                    lands=[[p['head'], round(p['t'], 3)] for p in s['panels']] + [[r[0], round(r[1], 3)] for p in s['panels'] for r in p['rows']]))
    # Evidence twin for the delivery gate: the same card, same timing, field left out (transparent), so the gate's
    # caption-clearance row measures the card's content, not a full-frame alpha (DS-107 lesson). Not composited.
    ev = dict(sc[0][1], id='K1e', transparent=True)
    V.build([(W/'recipe'/'hf-templates'/'compare-card'/'compare-card.template.htm', ev, ())], out, render=True, snap=None)
    man[-1]['evidence_mov'] = str(out/'renders'/'K1e.mov')
    man = sorted(man, key=lambda x: x['a']); man[0]['_edl_frames'] = edl['total_frames']
    (W/'graphics-manifest.json').write_text(json.dumps(man, indent=1))
    print('GRAPHICS COMPLETE', [(m['id'], round(m['a'], 2), round(m['b'], 2), m.get('box')) for m in man], flush=True)
