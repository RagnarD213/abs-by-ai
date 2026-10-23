"""DS-44 R1 graphics: Soft Blue Light HyperFrames lower thirds (shared vertical.py template, moving for their whole time on
screen), times from the words on the film timeline. Eyebrow in CAPITALS, main text in title case (GRAPHICS-STANDARDS, 2026-10-20).
  G01 source tag over the clip:            ALEX HORMOZI / The Iced Coffee Hour
  G02 key point (distils, never echoes):    THE REAL PROBLEM / Not Your Willpower, Your Stopping Point
  G03 the rule (the script's own on-screen text cue "2 POUNDS OVER = CUT BACK THAT DAY", on Dan's shot after the scale clip):  THE RULE / 2 Pounds Over = Cut Back That Day
  G04 subscribe tag:                        MORE LIKE THIS / Subscribe To My Channel
The source tag sits on Hormozi's own shot only (8.6-12.0 s), in the top band (y 140-316) over his cap, clear of every face.
Writes hf/ renders + graphics-manifest.json (Compositor format)."""
from pathlib import Path
import sys, json
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); HF = R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0, str(HF)); import vertical as V
sys.path.insert(0, str(HF.parent)); import buildcap
FPS = 30000/1001
words = json.load(open(W/'words_out.json')); edl = json.load(open(W/'edl.json')); shots = {s['id']: s for s in json.load(open(W/'shots.json'))}
def at(phrase, after=0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and [x['w'].lower().strip('.,!?') for x in words[i:i+len(toks)]] == toks: return words[i]['t0']
    raise ValueError(phrase)
def end_of(phrase, after=0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and [x['w'].lower().strip('.,!?') for x in words[i:i+len(toks)]] == toks: return words[i + len(toks) - 1]['t1']
    raise ValueError(phrase)
END = edl['total_frames']/FPS
LT = [
    # id, a, b, topic, parts [(text, spoken phrase it lands on)], top_y (None = template default band, bottom at 68 %)
    # build 3 (independent review 1): only on Hormozi's own shot (clip 43.42-51.0 = film 8.38-15.95), in the top band over the crown
    # of his cap (his face runs y ~560-1200), so it never names the caller and never covers a mouth
    ('G01', 8.60, 12.00, 'Alex Hormozi', [('The Iced Coffee Hour', None)], 140),
    # R2: Dan now sits lower (hair at y 540 under the interview frame), so the default band (1058-1306) covered his chin and
    # mouth; placed by its top edge at 1225: under his chin (~1185 on the tight shot); captions moved down to MarginV 340
    ('G02', at('your stopping point is just') - 0.1, shots['S3']['b'] - 0.05, 'The Real Problem',
     [('Not Your Willpower,', 'your stopping point is'), ('Your Stopping Point', 'set too high')], 1225),
    # on Dan's shot after the scale B-roll (over the B-roll its glass hid the scale itself): "Not next week, not on Monday, that day."
    ('G03', shots['S5']['a'] + 0.15, shots['S5']['b'] - 0.09, 'The Rule',      # -0.09: build 2's G03 rendered 1 frame short of a -0.05 slot
     [('2 Pounds Over =', 'not next week'), ('Cut Back That Day', 'that day')], None),
    ('G04', at('subscribe') - 0.1, END - 0.05, 'More Like This', [('Subscribe To My Channel', 'subscribe')], None),
]
if __name__ == '__main__':
    pass   # each graphic is under 10 s: hfbuild.render takes a quick-lane slot itself (renderq README)
    out = W/'hf'; man = []
    for gid, a, b, topic, parts, top_y in LT:
        ps = [[s, max(a, at(p, a - 1)) if p else a] for s, p in parts]
        c = {'id': gid, 'a': a, 'b': b, 'topic': topic, 'parts': ps}
        if top_y is not None: c['top_y'] = top_y
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, out, render=True, snap=1)
        man.append(dict(id=gid, a=a, b=b, template='lower-third', kind='glass', mov=str(out/'renders'/f'{gid}.mov'), mask=str(out/'renders'/f'{gid}_mask.mov'),
                        band=meta['band'], box=meta['box'], lines=meta['lines'], words=topic + ': ' + ' '.join(s for s, _ in parts),
                        lands=[[s, t] for s, t in ps]))
    (W/'graphics-manifest.json').write_text(json.dumps(sorted(man, key=lambda x: x['a']), indent=1))
    print('GRAPHICS COMPLETE', [(m['id'], round(m['a'], 2), round(m['b'], 2), m['box']) for m in man], flush=True)
