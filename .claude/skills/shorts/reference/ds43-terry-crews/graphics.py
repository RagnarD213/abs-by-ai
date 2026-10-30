"""DS-43 R1 graphics for ONE version (python3 graphics.py scripted|offcuff): Soft Blue Light HyperFrames lower thirds (shared
vertical.py template, moving for their whole time on screen), each on the shot whose words it distils, eyebrow in CAPITALS,
main text in title case; plus the R5 titled panel plate (media card, hole [0, 92, 1080, 608], radius 0, kicker x 36 y 24 at
32 px) from the panel's first frame to its last, composited UNDER Dan.
Scripted (key points from the scripted words):
  G02 S2 "your digestive system adapts. After a few weeks ... you won't even get hungry until about 2."
                                              WHY IT GETS EASY / Your Hunger Adapts / In A Few Weeks
  G03 S4 "If you're not fasting, you'll probably have to eat a small, low calorie dinner to hit your calories."
                                              THE TRADE-OFF / Skip Breakfast, / Eat A Bigger Dinner
  G04 S6 subscribe                            MORE LIKE THIS / Subscribe To My Channel
Off the cuff (key points distil THIS take's own words, never the script's):
  G02 S6 "Fasting does not make you lose muscle. Get that out of your head."
                                              THE TRUTH / Fasting Does Not / Cost You Muscle  (R1 review: "The Myth" over this line read backwards)
  G03 S7 "your body adapts to it over time, and over time it actually becomes easy."
                                              WHY IT GETS EASY / Your Body Adapts / Over Time
  G04 S8 "If you're not fasting, you're gonna have to have a much smaller dinner, which for me is much harder."
                                              THE TRADE-OFF / Skip Breakfast, / Eat A Bigger Dinner
  G05 S10 subscribe                           MORE LIKE THIS / Subscribe To My Channel
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
        ('G02',) + on('S2', 'Why It Gets Easy', [('Your Hunger Adapts', 'digestive system'), ('In A Few Weeks', 'a few weeks')]),
        ('G03',) + on('S4', 'The Trade-Off', [('Skip Breakfast,', "if you're not"), ('Eat A Bigger Dinner', 'low calorie dinner')]),
        ('G04', at('learn how') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],
    'offcuff': lambda: [
        ('G02',) + on('S6', 'The Truth', [('Fasting Does Not', 'fasting does not'), ('Cost You Muscle', 'lose muscle')]),
        ('G03',) + on('S7', 'Why It Gets Easy', [('Your Body Adapts', 'body adapts'), ('Over Time', 'over time')]),
        ('G04',) + on('S8', 'The Trade-Off', [('Skip Breakfast,', "if you're not"), ('Eat A Bigger Dinner', 'smaller dinner')]),
        ('G05', at('learn how') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],
}[VERSION]())()
KICKER = 'Terry Crews | Business Insider'
if __name__ == '__main__':
    out = O/'hf'; man = []
    for gid, a, b, topic, parts in LT:
        ps = [[s, max(a, at(p, a - 1)) if p else a] for s, p in parts]
        a = max(a, ps[0][1] - 0.35)   # R1 watch judge: never an empty frosted card -- enter 0.35 s before the first line lands
        c = {'id': gid, 'a': a, 'b': b, 'topic': topic, 'parts': ps}
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, out, render=True, snap=1)
        man.append(dict(id=gid, a=a, b=b, template='lower-third', kind='glass', mov=str(out/'renders'/f'{gid}.mov'), mask=str(out/'renders'/f'{gid}_mask.mov'),
                        band=meta['band'], box=meta['box'], lines=meta['lines'], words=topic + ': ' + ' '.join(s for s, _ in parts),
                        lands=[[s, t] for s, t in ps]))
    (O/'graphics-manifest.json').write_text(json.dumps(sorted(man, key=lambda x: x['a']), indent=1))
    plates = []
    # R2: the Business Insider title stays on his interview; the jacked-Terry reel behind the reply and the physique lines gets a plain title
    for pid, pa, pb, kick in (('P01', shots['PW']['a'], shots['PW']['b'], KICKER), ('P02', shots['PR']['a'], shots['S2']['b'], 'Terry Crews')):
        scene, _ = V.media_card_scene(pid, pb - pa, 16/9, kicker=kick, caps=False)
        tpl, cfg, assets = scene; cfg['hole'] = [0, 92, 1080, 608]; cfg['radius'] = 0
        cfg['kicker'] = {'x': 36, 'y': 24, 'px': 32, 's': kick}
        V.build([(tpl, cfg, assets)], out, render=True, snap=1)
        plates.append(dict(id=pid, a=pa, b=pb, kind='overlay', mov=str(out/'renders'/f'{pid}.mov'), hole=[0, 92, 1080, 608], words=kick))
    (O/'plate-manifest.json').write_text(json.dumps(plates, indent=1))
    print('GRAPHICS COMPLETE', VERSION, [(m['id'], round(m['a'], 2), round(m['b'], 2), m['box']) for m in man], flush=True)
