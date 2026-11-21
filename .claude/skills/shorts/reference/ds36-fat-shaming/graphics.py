"""DS-36 R1 graphics for ONE version (python3 graphics.py scripted|offcuff; from DS-43 R2): Soft Blue Light HyperFrames lower thirds
(shared vertical.py template, moving for their whole time on screen), each on the shot whose words it distils, eyebrow in CAPITALS,
main text in title case; plus the R5 titled panel plate (media card, hole [0, 92, 1080, 608], radius 0, kicker x 36 y 24 at 32 px,
"Bill Maher | Real Time (HBO)" as the approved DS-40 R5 film) from the panel's first frame to its last, composited UNDER Dan.
Scripted (key points from the scripted words):
  G01 S2 "Shame works, but fat shaming other people is a pointless waste of energy."
                                              THE TRUTH / Shame Works / On Yourself, Not Others
  G02 S4 "...if you get more than three pounds over your goal weight, force yourself to feel a deep sense of shame..."
                                              STEP 1 / Weigh In Every Morning / 3 Pounds Over? Feel It
  G03 S6 "This will force you to look at yourself shirtless for a few minutes every day..."  (after "standing vacuums in the mirror")
                                              STEP 2 / Vacuums In The Mirror / Every Morning
  G04 S8 subscribe                            MORE LIKE THIS / Subscribe To My Channel
Off the cuff (key points distil THIS take's own words, never the script's):
  G01 S1 "That's just cruel and there's no point to doing it. Because those people aren't going to change anyway."
                                              THE TRUTH / Shaming Others / Changes Nothing
  G02 S3 "If you get more than three pounds above your goal weight, make yourself feel a deep sense of healthy shame."
                                              THE RULE / 3 Pounds Over? / Feel The Shame
  G03 S4 "Feel that shame when you're only a little bit over your goal weight rather than 20 or 30 pounds"
                                              CATCH IT EARLY / At 3 Pounds, / Not 20 Or 30
  G04 S7 "Shame can be healthy, shame can be good, and shame can literally save your life if it's shame about belly fat."
                                              THE POINT / Shame Can Be Healthy / It Can Save Your Life
  G05 S9 "Use that shame as motivation, as a fuel you'll need to get back on track"
                                              USE IT / Shame Is Fuel / To Get Back On Track
  G06 S10 subscribe                           MORE LIKE THIS / Subscribe To My Channel
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
        ('G01',) + on('S2', 'The Truth', [('Shame Works', 'shame works'), ('On Yourself, Not Others', 'other people')]),   # R1 review: the old card repeated the line and was full for only 0.8 s
        ('G02',) + on('S4', 'Step 1', [('Weigh In Every Morning', 'and if you get'), ('3 Pounds Over? Feel It', 'force yourself')]),
        ('G03',) + on('S6', 'Step 2', [('Vacuums In The Mirror', 'this will force'), ('Every Morning', 'look at yourself')]),
        ('G04', at('subscribe') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],
    'offcuff': lambda: [
        ('G01',) + on('S1', 'The Truth', [('Shaming Others', "that's just cruel"), ('Changes Nothing', "aren't going")]),
        ('G02',) + on('S3', 'The Rule', [('3 Pounds Over?', 'three pounds'), ('Feel The Shame', 'deep sense')]),
        ('G03',) + on('S4', 'Catch It Early', [('At 3 Pounds,', 'little bit over'), ('Not 20 Or 30', '20 or 30')]),
        ('G04',) + on('S7', 'The Point', [('Shame Can Be Healthy', 'shame can be healthy'), ('It Can Save Your Life', 'literally save')]),
        ('G05',) + on('S9', 'Use It', [('Shame Is Fuel', 'as a fuel'), ('To Get Back On Track', 'back on track')]),
        ('G06', at('subscribe') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', None)])],
}[VERSION]())()
KICKER = 'Bill Maher | Real Time (HBO)'
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
    # one plate for the whole panel stretch (the clip keeps playing in it, spoken then silent behind Dan's reply)
    for pid, pa, pb, kick in (('P01', shots['PW']['a'], shots['PR']['b'], KICKER),):
        scene, _ = V.media_card_scene(pid, pb - pa, 16/9, kicker=kick, caps=False)
        tpl, cfg, assets = scene; cfg['hole'] = [0, 92, 1080, 608]; cfg['radius'] = 0
        cfg['kicker'] = {'x': 36, 'y': 24, 'px': 32, 's': kick}
        V.build([(tpl, cfg, assets)], out, render=True, snap=1)
        plates.append(dict(id=pid, a=pa, b=pb, kind='overlay', mov=str(out/'renders'/f'{pid}.mov'), hole=[0, 92, 1080, 608], words=kick))
    (O/'plate-manifest.json').write_text(json.dumps(plates, indent=1))
    print('GRAPHICS COMPLETE', VERSION, [(m['id'], round(m['a'], 2), round(m['b'], 2), m['box']) for m in man], flush=True)
