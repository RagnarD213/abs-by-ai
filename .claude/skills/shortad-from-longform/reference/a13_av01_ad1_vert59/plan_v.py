#!/usr/bin/env python3
"""Build cut/plan.json for _shared/deliver/gate.py from THIS cutdown's own files.

Adapted from the square's plan_sq.py. The differences are the ones AV-01 has by construction:
this cut is a SELECTION out of the approved 9:16 master, so there is no render to read graphics
and chips out of -- the master's chips are located on the delivered pixels (chiplocate.py) and the
three chips this cutdown adds come from label_place.json, measured by vlabelplace.py.

  python3 plan_v.py [--transcribe]
"""
import glob, json, os, subprocess, sys
import importlib.util

BUILD = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(BUILD, 'cut')
os.chdir(CUT)
sys.path.insert(0, CUT)
FPS = 30000/1001
VID = os.path.join(BUILD, 'ad1_vertical_59s.mp4')

spec = importlib.util.spec_from_file_location('cutbeats', os.path.join(CUT, 'beats.py'))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
sys.modules['beats'] = B

tl, ov = B.timeline()
NTOT = json.load(open(os.path.join(BUILD, 'cut_plan.json')))['frames']

# --- joins: every picture cut on the DELIVERED timeline (cut_edl.py mapped the master's own
# cuts through the range map and added every range boundary).
E = json.load(open('edl_frames.json'))
joins, n = [], 0
for s in E:
    if n: joins.append(round(n/FPS, 3))
    n += s['frames']

covered = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl if b['kind'] != 'talk']
muted = set(B.NO_CAPS_KINDS)
cards = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl + ov
         if b['kind'] in muted or b['kind'] in ('lt', 'cta') or b.get('caps') is False]

# --- punch: Muhammad's push ramps, sampled off the cut beat sheet's own push_at
lev, prev, a0 = [], None, 0.0
for k in range(NTOT):
    t = k/FPS
    L = 'NEAR' if B.push_at(t) > 1.0 + (B.PUSH_Z - 1.0)*0.5 else 'FAR'
    if L != prev:
        if prev is not None: lev.append([round(a0, 3), round(t, 3), prev])
        prev, a0 = L, t
lev.append([round(a0, 3), round(NTOT/FPS, 3), prev])
kind_at = {}
for b in tl:
    for k in range(int(round(b['t0']*FPS)), min(NTOT, int(round(b['t1']*FPS)))): kind_at[k] = b['kind']
punch, punch_covered = [], []
for a, bb, L in lev:
    punch.append([a, bb, L])
    k0 = int(round(a*FPS))
    punch_covered.append(kind_at.get(k0 - 1, 'talk') != 'talk' or kind_at.get(k0, 'talk') != 'talk')

# --- the labels -------------------------------------------------------------
# three this cutdown ADDS (measured placements), four the approved master already burns in.
from PIL import Image
sys.path.insert(0, BUILD)
import chips as CH
os.makedirs('plan_assets', exist_ok=True)
place = json.load(open('label_place.json'))
burned = json.load(open('burned_chips.json'))
CUTBEAT = {b.get('media'): [round(b['t0'], 3), round(b['t1'], 3)] for b in tl if b.get('media')}

def added(media):
    c = place[media]
    label = CH.REAL_LABEL if c['kind'] == 'real' else CH.AI_LABEL
    lay = CH.chip_at(label, c['x'], c['y'], c['lines'], c['size'])
    bb = lay.getchannel('A').getbbox()
    p = os.path.abspath(f"plan_assets/chip_{c['kind']}_{media}.png")
    lay.crop(bb).save(p)
    return dict(name=media, beat=CUTBEAT[media], chip=p, pos=[bb[0], bb[1]])

real_photos = [added('today_towel'), added('today_trees')]
ai_inserts = [added('after_reveal')] + [
    dict(name=k, beat=CUTBEAT[k], chip=v['chip'], pos=v['pos'])
    for k, v in burned.items()]
ai_inserts.sort(key=lambda x: x['beat'][0])
label_chips = {'real': real_photos[0]['chip'], 'ai': ai_inserts[0]['chip']}
label_pos = {'real': real_photos[0]['pos'], 'ai': ai_inserts[0]['pos']}

# --- graphics: the master's overlay MOVs for the two CTA pills that survive
graphics = []
for o in ov:
    for f in sorted(glob.glob(os.path.join(BUILD, 'gfx', f"ov_{o['kind']}_*.mov"))):
        graphics.append(dict(name=f"{o['kind']}@{o['t0']:.2f}",
                             beat=[round(o['t0'], 3), round(o['t1'], 3)],
                             mov=os.path.abspath(f))); break

# --- captions as an SRT, from the SAME groups the compositor burned
import captions as CP
words = CP.load_words(); gs = CP.groups(words, CP.suppressed())
def ts(t):
    h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')
open('plan_assets/captions.srt', 'w').write(
    '\n'.join(f"{i}\n{ts(g[0][1])} --> {ts(g[-1][2])}\n{' '.join(x[0] for x in g)}\n"
              for i, g in enumerate(gs, 1)))

plan = dict(
    target_seconds=round(NTOT/FPS, 6), target_frames=NTOT,
    joins=joins, covered=covered, cards=cards, punch=punch, punch_covered=punch_covered,
    real_photos=real_photos, ai_inserts=ai_inserts, graphics=graphics,
    label_chips=label_chips, label_pos=label_pos,
    srt=os.path.abspath('plan_assets/captions.srt'),
    words=[dict(w=w['word'], t=round(float(w['start']), 3), e=round(float(w['end']), 3))
           for w in json.load(open('words_ctc.json'))],
    source_audio=os.path.abspath('his_mix.wav'),
    banned_source='/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets/clip_109_replacement.mp4',
    banned_times=[26.4, 27.5, 29.6, 31.0],
    watch_log=os.path.abspath('logs/watch_pass.json'),
)
old = json.load(open('plan.json')) if os.path.exists('plan.json') else {}
for k in ('transcript_words', 'negative_events_scan', 'declare'):
    if k in old: plan[k] = old[k]
if '--transcribe' in sys.argv:
    import whisper
    r = whisper.load_model('small').transcribe(VID, word_timestamps=False, language='en')
    plan['transcript_words'] = [dict(w=w) for seg in r['segments'] for w in seg['text'].split()]
json.dump(plan, open('plan.json', 'w'), indent=1)
print(f"cut/plan.json: {len(joins)} joins, {len(punch)} framing segments, {len(real_photos)} real "
      f"photos, {len(ai_inserts)} AI inserts, {len(graphics)} graphics, {len(gs)} caption cues, "
      f"{len(plan['words'])} words, transcript {len(plan.get('transcript_words') or [])}")
