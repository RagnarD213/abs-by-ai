"""DS-107 R1 graphics (python3 graphics.py): Soft Blue Light HyperFrames, moving for their whole screen time; eyebrows in capitals,
main points in title case (VIDEO-RULES 2026-10-16/20).
  K1  full-screen study card on the line-graph template (script: "STUDY ON SCREEN: SCIENCE, 2021. 6,421 PEOPLE, 29 COUNTRIES.
      CALORIES BURNED SHOWN AS A FLAT LINE FROM AGE 20 TO 60"), laid out on the full 1080 x 1920 canvas with the plot inside the
      picture area (the title band is laid over rows 0-310 by the assembly). The flat 20-60 line draws on "calories burned stayed
      flat from 20 to 60"; the red decline after 60 draws on "After 60, it drops less than 1% a year". Pontzer et al., Science 2021
      (373:808): adjusted daily energy expenditure stable from 20 to 60, falling about 0.7 % a year after 60.
  G00 T3 "Four things, and they were all hit after 40."   WHAT CHANGED AFTER 40 / Stress, Food, / Movement, Sleep
  G01 T5 "Food first. Decide what you eat before you're hungry and then eat the protein first."  FIX 1: FOOD FIRST / Plan Your Meals Ahead, / Eat Protein First
  G02 T6 "It gets you moving again and it takes the edge off the stress for the rest of the day."  FIX 2: 15 MINUTES EVERY MORNING / Gets You Moving, / Takes The Edge Off Stress
  G03 T7 subscribe                                         MORE LIKE THIS / Subscribe To My Channel
Writes main/hf renders + graphics-manifest.json (Compositor format)."""
from pathlib import Path
import sys, json
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); import vertical as V, hfbuild as H
FPS = 30000/1001; O = W/'main'
words = json.load(open(O/'words_out.json')); edl = json.load(open(O/'edl.json'))
shots = {s['id']: s for s in json.load(open(O/('shots.json' if (O/'shots.json').exists() else 'shots-times.json')))}
def at(phrase, after=0, end=False):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and [x['w'].lower().strip('.,!?…') for x in words[i:i+len(toks)]] == toks:
            return words[i + len(toks) - 1]['t1'] if end else words[i]['t0']
    raise ValueError(phrase)
END = edl['total_frames']/FPS
def on(sid, topic, parts, a=None): return ((a if a is not None else shots[sid]['a'] + 0.15), shots[sid]['b'] - 0.09, topic, parts)
LT = [('G00',) + on('T3', 'What Changed After 40', [('Stress, Food,', 'four things'), ('Movement, Sleep', 'they were all')], a=at('four things') - 0.35),
      ('G01',) + on('T5', 'Fix 1: Food First', [('Plan Your Meals Ahead,', 'decide what'), ('Eat Protein First', 'and then eat')]),   # R1 review: the second line had 0.3 s fully on; it lands on 'and then eat' now
      ('G02',) + on('T6', 'Fix 2: 15 Minutes Every Morning', [('Gets You Moving,', 'it gets'), ('Takes The Edge Off Stress', 'it takes')]),
      ('G03', at('subscribe') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])]

def study_card(gid, a, b):
    DY = 310                                                     # everything sits in the picture area under the title band
    x0, x1, ytop, yaxis = 116, 1000, 330 + DY + 40, 1040 + DY    # plot: y axis 680..1350 (captions start at 1412)
    age = lambda v: x0 + (v - 20)*(x1 - x0)/70                    # x axis: age 20 .. 90
    H100 = 560; y100 = yaxis - H100; ydrop = round(yaxis - 0.80*H100)   # honest scale: the x axis is zero calories; 100 % at y 790, about 80 % at 90 (0.7 %/yr over 30 yrs) at y 902
    pts = [[round(age(20), 1), y100 + 2], [round(age(60), 1), y100], [round(age(90), 1), ydrop]]   # the flat part rises 2 px so the template draws it cyan
    t_flat0, t_flat1 = at('calories burned'), at('to 60', end=True)
    t_drop0, t_drop1 = at('after 60'), at('a year', end=True)
    labels = [dict(s='Calories Burned A Day', x=x0 - 6, y=ytop - 96, px=32, c='white', bold=True),
              dict(s='Adjusted For Body Size', x=x0 - 6, y=ytop - 54, px=26, c='cyan', bold=False),
              dict(s='Same As At 20', x=x0 + 14, y=y100 - 46, px=26, c='cyan', bold=False)] + \
             [dict(s=str(v), x=round(age(v) - H.text_w(str(v), 30)/2), y=yaxis + 14, px=30, c='white', bold=True) for v in (20, 40, 60, 80)] + \
             [dict(s='Age', x=x1 - H.text_w('Age', 30) + 6, y=yaxis + 14, px=30, c='white', bold=True)]
    segs = [dict(a=H.rel(t_flat0, a), b=H.rel(t_flat1, a)), dict(a=H.rel(t_drop0, a), b=H.rel(min(t_drop1, b - 0.3), a))]
    cfg = dict(id=gid, dur=round(b - a, 3), drift=-10, canvas=[1080, 1920], accent=[64, 46 + DY, 78],
               eyebrow=dict(x=64, y=64 + DY, px=32, s='SCIENCE, 2021'), title=dict(x=64, y=112 + DY, px=60, s='Metabolism Stays Flat'),
               foot=dict(x=64, y=196 + DY, px=26, s='6,421 People In 29 Countries  ·  Pontzer Et Al.'),
               plot=dict(x0=x0, x1=x1, ytop=ytop, yaxis=yaxis, ybase=y100, axis_w=4, base_w=3, line_w=9, dot_r=11),
               labels=labels, points=pts, segments=segs, transparent=True)
    assert H.text_w(cfg['title']['s'], 60) <= 1080 - 128
    return [(Path(__file__).resolve().parent/'hf-templates'/'line-graph'/'line-graph.template.htm', cfg, ())]   # local copy: glow filter in user space (see the template)

if __name__ == '__main__':
    out = O/'hf'; man = []
    for gid, a, b, topic, parts in LT:
        ps = [[s, max(a, at(p, a - 1)) if p else a] for s, p in parts]
        a = max(a, ps[0][1] - 0.27)            # DS-41: never an empty frosted card
        c = {'id': gid, 'a': a, 'b': b, 'topic': topic, 'parts': ps}
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, out, render=True, snap=1)
        man.append(dict(id=gid, a=a, b=b, template='lower-third', kind='glass', mov=str(out/'renders'/f'{gid}.mov'), mask=str(out/'renders'/f'{gid}_mask.mov'),
                        band=meta['band'], box=meta['box'], lines=meta['lines'], words=topic.upper() + ': ' + ' '.join(s for s, _ in parts),
                        lands=[[s, t] for s, t in ps]))
    ka, kb = shots['K1']['a'], shots['K1']['b']
    sc = study_card('K1', ka, kb)
    V.build(sc, out, render=True, snap=min(kb - ka - 0.2, sc[0][1]['segments'][-1]['b'] + 0.5))
    man.append(dict(id='K1', a=ka, b=kb, template='line-graph', kind='overlay', mov=str(out/'renders'/'K1.mov'),
                    words='SCIENCE, 2021: Metabolism Stays Flat / 6,421 People In 29 Countries / Calories Burned A Day, Adjusted For Body Size / Same As At 20 / Age 20 40 60 80',
                    lands=[['flat line 20-60', round(ka + sc[0][1]['segments'][0]['a'], 3)], ['decline after 60', round(ka + sc[0][1]['segments'][1]['a'], 3)]]))
    man = sorted(man, key=lambda x: x['a']); man[0]['_edl_frames'] = edl['total_frames']   # build.sh re-renders when the edit list changes (R1: a stale manifest kept old timings)
    (O/'graphics-manifest.json').write_text(json.dumps(man, indent=1))
    print('GRAPHICS COMPLETE', [(m['id'], round(m['a'], 2), round(m['b'], 2), m.get('box')) for m in man], flush=True)
