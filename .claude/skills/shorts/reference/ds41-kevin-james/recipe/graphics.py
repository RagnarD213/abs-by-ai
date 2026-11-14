"""DS-41 R1 graphics for ONE version (python3 graphics.py scripted|offcuff; from DS-36 R1): Soft Blue Light HyperFrames, moving for
their whole time on screen, eyebrow and text in title case; plus the R5 titled panel plate (media card, hole [0, 92, 1080, 608],
radius 0, kicker x 36 y 24 at 32 px, "Kevin James | The Joe Rogan Experience") from the panel's first frame to its last,
composited UNDER Dan.
Scripted (the shoot doc's cues, key points from the scripted words):
  K1  full-screen card (script: "FULL SCREEN GRAPHIC, EACH LINE LANDS AS I SAY IT: 6 DAYS X 500 CALORIES = DOWN 3,000. 1 CHEAT DAY =
      3,000 BACK")                              The Math / Why Cheat Days Fail / - 6 Days x 500 = 3,000 Down / + 1 Cheat Day = 3,000 Back
  G01 S4 "If you want a treat, that's fine. Just fit it inside that day's calories."  (script: NO CHEAT DAYS. FIT THE TREAT INSIDE
      THAT DAY'S CALORIES)                      The Rule / No Cheat Days. / Fit The Treat In Your Calories
  G02 S5 "ripped guys occasionally have a cheat meal. Fat guys diet all week and then have a cheat day"  (script: RIPPED GUYS: A
      CHEAT MEAL. FAT GUYS: A CHEAT DAY)        Remember / Ripped Guys: A Cheat Meal. / Fat Guys: A Cheat Day
  G03 S6 subscribe                              More Like This / Subscribe To My Channel
Off the cuff (key points distil THIS take's own words, never the script's):
  K1  full-screen card over "you have a 500 calorie deficit in each day, 3,000 calorie total deficit. On that one cheat day, you
      can easily have a 3,000 calorie or more surplus"
                                                The Math / Why Cheat Days Fail / - 6 Days x 500 = 3,000 Deficit / + 1 Cheat Day = 3,000+ Surplus
  G01 S3 "So I would say just make it one cheat meal and not a cheat day."
                                                My Advice / One Cheat Meal, / Not A Cheat Day
  G02 S5 "you're eating 6,000, 7,000, 8,000 calories in one day"
                                                Track It Once / A Cheat Day Can Hit / 8,000 Calories
  G03 S6 "So no cheat days, make it a cheat meal only, and still track when you cheat."
                                                Bottom Line / A Cheat Meal Only. / And Still Track It
  G04 S7 subscribe                              More Like This / Subscribe To My Channel
Writes <version>/hf renders + graphics-manifest.json + plate-manifest.json (Compositor format)."""
from pathlib import Path
import sys, json
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); import vertical as V
FPS = 30000/1001
VERSION = sys.argv[1]; O = W/VERSION
words = json.load(open(O/'words_out.json')); edl = json.load(open(O/'edl.json'))
shots = {s['id']: s for s in json.load(open(O/('shots.json' if (O/'shots.json').exists() else 'shots-times.json')))}
def at(phrase, after=0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and words[i]['speaker'] == 'dan' and [x['w'].lower().strip('.,!?…') for x in words[i:i+len(toks)]] == toks:
            return words[i]['t0']
    raise ValueError(phrase)
END = edl['total_frames']/FPS
def on(sid, topic, parts): return (shots[sid]['a'] + 0.15, shots[sid]['b'] - 0.09, topic, parts)
LT = (lambda: {
    'scripted': lambda: [
        ('G01',) + on('S4', 'The Rule', [('No Cheat Days.', 'if you want'), ('Fit The Treat In Your Calories', 'just fit')]),
        ('G02',) + on('S5', 'Remember', [('Ripped Guys: A Cheat Meal.', 'ripped guys'), ('Fat Guys: A Cheat Day', 'fat guys')]),
        ('G03', at('subscribe') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],
    'offcuff': lambda: [
        ('G01',) + on('S3', 'My Advice', [('Keep The Cheat', 'just make'), ('To One Meal', 'one cheat meal')]),          # off-cuff review 1: the old lines repeated his words under the captions
        ('G02',) + on('S5', 'Track It Once', [('A Cheat Day Can', "you're eating"), ('Hit 8,000 Calories', '8,000')]),   # review 1: 'Hit' wrapped alone and built before the rest
        ('G03',) + on('S6', 'Bottom Line', [('No Cheat Days.', 'so no'), ('Count The Cheat Meal Too', 'and still')]),
        ('G04', shots['S7']['a'] + 0.15, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],   # review 1: it entered empty across the S6/S7 cut
}[VERSION]())()
# the full-screen math card: (id, shot, eyebrow, headline, rows [(marker, marker colour, text, phrase it lands on)])
CARD = {'scripted': ('K1', 'K1', 'The Math', 'Why Cheat Days Fail',
                     [('\u2212', '#7FE3A1', '6 Days x 500 Calories', 'cut 500', 0), ('=', '#7FE3A1', '3,000 Down', 'down about', 0),
                      ('+', '#FF8A8A', '1 Big Cheat Day', 'one big', 0), ('=', '#FF8A8A', '3,000 Back', '3,000 calorie surplus', 0)]),
        'offcuff': ('K1', 'K1', 'The Math', 'Why Cheat Days Fail',
                    [('\u2022', '#7FE3A1', '6 Days x 500 Calories', 'six days', 0), ('=', '#7FE3A1', '3,000 Deficit', '3,000 calorie total', 0),
                     ('\u2022', '#FF8A8A', '1 Cheat Day', 'one cheat', 0), ('=', '#FF8A8A', '3,000+ Surplus', '3,000 calorie or', 0)])}[VERSION]   # off-cuff review 1: - = + = read as one sum that did not add up; two separate equations now
def math_card(gid, t0, t1, eyebrow, headline, items, k=1.3):
    """review 1: the shared title card's sizes left 74 % of the frame empty for 11 s. Same template and family, laid out 1.3x
    larger (headline 94, rows 60 px), one row per step of the sum so something new lands on each number he says."""
    x, maxw = 40*V.U, V.W - 80*V.U
    size = round(72*k)
    while size > 60 and V.H.text_w(headline, size) > maxw: size -= 2
    rpx = round(46*k)
    while max(V.H.text_w(s_, rpx) for s_ in items) > maxw - 100 - 34: rpx -= 2
    lh = size*1.22; rh, rg = round(116*k), round(18*k)
    blockh = 98*k + lh + 40*k + len(items)*(rh + rg)
    y = (V.Hh - blockh)/2
    c = dict(id=gid, dur=round(t1 - t0, 3), drift=-10, canvas=V.CANVAS, line_px=size, accent=[x, round(y + 8), round(78*k)],
             eyebrow=dict(x=x, y=round(y + 30*k), px=round(34*k), s=eyebrow))
    ly = y + 98*k
    c['lines'] = [dict(x=x - 4, y=round(ly), s=headline, at=0.02)]      # review 1: the title starts rising on the card's first frame
    ry = ly + lh + 40*k
    c.update(rows=[dict(x=x, y=round(ry + i*(rh + rg)), w=maxw, h=rh, s=s_, t=0.35) for i, s_ in enumerate(items)], row_px=rpx, row_ty=round((rh - rpx*1.4)/2))
    return [(V.HERE/'title-card'/'title-card.template.htm', c, ())], dict(kind='opaque')
KICKER = 'Kevin James | The Joe Rogan Experience'
if __name__ == '__main__':
    out = O/'hf'; man = []
    for gid, a, b, topic, parts in LT:
        ps = [[s, max(a, at(p, a - 1)) if p else a] for s, p in parts]
        a = max(a, ps[0][1] - 0.27)   # R1 watch judge: never an empty frosted card -- enter 0.35 s before the first line lands
        c = {'id': gid, 'a': a, 'b': b, 'topic': topic, 'parts': ps}
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, out, render=True, snap=1)
        man.append(dict(id=gid, a=a, b=b, template='lower-third', kind='glass', mov=str(out/'renders'/f'{gid}.mov'), mask=str(out/'renders'/f'{gid}_mask.mov'),
                        band=meta['band'], box=meta['box'], lines=meta['lines'], words=topic + ': ' + ' '.join(s for s, _ in parts),
                        lands=[[s, t] for s, t in ps]))
    gid, sid, eyebrow, headline, rows = CARD; ka, kb = shots[sid]['a'], shots[sid]['b']
    scenes, meta = math_card(gid, ka, kb, eyebrow, headline, [r[2] for r in rows])
    cfg = scenes[0][1]
    for row, (mk, col, txt, ph, _af) in zip(cfg['rows'], rows):
        row['marker'] = mk; row['markerColor'] = col; row['t'] = round(max(0.35, at(ph, ka - 0.5) - ka - 0.10), 3)
    V.build(scenes, out, render=True, snap=max(r['t'] for r in cfg['rows']) + 1.0)
    man.append(dict(id=gid, a=ka, b=kb, template='title-card', kind='opaque', mov=str(out/'renders'/f'{gid}.mov'),
                    words=eyebrow + ': ' + headline + ' / ' + ' / '.join(r[2] for r in rows), lands=[[r['s'], round(ka + r['t'], 3)] for r in cfg['rows']]))
    (O/'graphics-manifest.json').write_text(json.dumps(sorted(man, key=lambda x: x['a']), indent=1))
    plates = []
    # one plate for the whole panel stretch (the clip keeps playing in it, spoken then silent behind Dan's reply)
    for pid, pa, pb, kick in (('P01', shots['PW']['a'], shots['PR']['b'], KICKER),):
        scene, _ = V.media_card_scene(pid, pb - pa, 16/9, kicker=kick, caps=False)
        tpl, cfg, assets = scene; cfg['hole'] = [0, 92, 1080, 608]; cfg['radius'] = 0
        cfg['kicker'] = {'x': 36, 'y': 24, 'px': 32, 's': kick}
        V.build([(tpl, cfg, assets)], out, render=True, snap=1)
        plates.append(dict(id=pid, a=pa, b=pb, kind='overlay', mov=str(out/'renders'/f'{pid}.mov'), hole=[0, 92, 1080, 608], words=kick))
    (O/'plate-manifest.json').write_text(json.dumps(plates, indent=1))
    print('GRAPHICS COMPLETE', VERSION, [(m['id'], round(m['a'], 2), round(m['b'], 2), m.get('box')) for m in man], flush=True)
