#!/usr/bin/env python3
"""Build plan.json for _shared/deliver/gate.py from THIS build's own files (never by hand).

Everything here is read out of the build: the beat sheet, the picture EDL, crop.json, the caption
states, words_ctc.json and qc.json. `--transcribe` re-transcribes the DELIVERED file (the gate wants
what the render actually says, not what the script meant to say).
  python3 plan_build.py [--cut] [--transcribe]
"""
import json, os, subprocess, sys, hashlib, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CUT = '--cut' in sys.argv
D = 'cut' if CUT else '.'
sys.path.insert(0, D)
import importlib
B = importlib.import_module('cut.beats' if CUT else 'beats') if False else None
if CUT:
    sys.path.insert(0, os.path.abspath('cut')); import beats as B          # noqa
else:
    import beats as B                                                      # noqa
FPS = B.FPS; NTOT = B.NTOT
VID = f'{D}/ad5_vertical_9x16_59s.mp4' if CUT else 'ad5_vertical_9x16.mp4'
tl, ov = B.timeline()
Q = json.load(open(f'{D}/qc.json'))

# --- joins: every picture cut on the DELIVERED timeline (his J/L cuts, not the audio splices)
E = json.load(open(f'{D}/edl_picture.json'))
joins = sorted({round(s['n0']/FPS, 3) for s in E[1:]})

# --- covered: the beats that hide a join; cards: the full-screen beats a caption may not sit on
covered = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl if b['kind'] != 'talk']
muted = set(B.NO_CAPS_KINDS); mbodies = set(B.NO_CAPS_BODIES)
cards = [[round(b['t0'], 3), round(b['t1'], 3)] for b in tl
         if b['kind'] in muted or (b['kind'] == 'window' and b.get('body') in mbodies)]

# --- punch: the hair-anchored NEAR/FAR FRAMING SEGMENTS.
# ⚠ crop.json's `holds` are NOT framing segments one-for-one: zcrop splits a hold at a beat edge or a
# y0 change while KEEPING the level, so the file carries contiguous same-level pairs that are one
# segment on screen (20 of 68 here). Fed raw they read to the gate as "adjacent visible segments at
# one framing" -- a jump cut that does not exist. MERGE contiguous same-level holds first.
# And a segment is COVERED when an insert sits immediately before it: the level change then happens
# across the insert, which is the whole point of cutting away (gate's own words).
C = json.load(open(f'{D}/crop.json'))
kind_of = {}
for b in tl:
    for n in range(b['n0'], b['n1']): kind_of[n] = b['kind']
merged = []
for h in C['holds']:
    if merged and merged[-1]['level'] == h['level'] and merged[-1]['n1'] == h['n0']:
        merged[-1] = dict(merged[-1], n1=h['n1'])
    else:
        merged.append(dict(n0=h['n0'], n1=h['n1'], level=h['level']))
punch = [[round(h['n0']/FPS, 3), round(h['n1']/FPS, 3), h['level']] for h in merged]
punch_covered = [kind_of.get(h['n0'] - 1, 'talk') != 'talk' for h in merged]

# --- the two labels: the chip images the compositor draws, and where it draws them
import g5 as G
os.makedirs(f'{D}/plan_assets', exist_ok=True)
lay = G.blank(); G.real_chip(lay)
bb = lay.getchannel('A').getbbox(); lay.crop(bb).save(f'{D}/plan_assets/chip_real.png')
real_pos = [bb[0], bb[1]]
lay2 = G.blank(); G.ai_chip(lay2, 960 - 18, 1330 - 12)          # the lock/app card's hole, the AI chip's commonest home
bb2 = lay2.getchannel('A').getbbox(); lay2.crop(bb2).save(f'{D}/plan_assets/chip_ai.png')
ai_pos = [bb2[0], bb2[1]]

def beat_of(n0, n1): return [round(n0/FPS, 3), round(n1/FPS, 3)]
real_photos = [dict(name=os.path.basename(str(b.get('media', ''))), beat=beat_of(b['n0'], b['n1']))
               for b in tl if b['kind'] == 'bleed']
# AI imagery OF DAN. ⚠ The app beat carries its AI chip only from `result_n` (the goal image alone on
# the result screen); the 6.3 s of recording before it is the product UI and carries no label, so the
# insert's beat is the LABELLED span, not the whole beat.
AI_OF_DAN = {'lock', 'app'}
ai_inserts = []
for b in tl:
    if b['kind'] in AI_OF_DAN or (b['kind'] == 'card' and b.get('label')):
        a = b.get('result_n', b['n0'])
        ai_inserts.append(dict(name=os.path.basename(str(b.get('media', ''))), beat=beat_of(a, b['n1'])))

# --- captions as an SRT, regenerated from the SAME states the compositor burned
import captions as CP
words = CP.load_words(); gs = CP.groups(words, CP.suppressed())
def ts(t):
    h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')
srt = []
for i, g in enumerate(gs, 1):
    srt.append(f"{i}\n{ts(g[0][1])} --> {ts(g[-1][2])}\n{' '.join(x[0] for x in g)}\n")
open(f'{D}/plan_assets/captions.srt', 'w').write('\n'.join(srt))

plan = dict(
    target_seconds=round(NTOT/FPS, 6), target_frames=NTOT,
    reference_cut=os.path.abspath('ref/ad5_v3_hd.mp4') if not CUT else None,
    joins=joins, covered=covered, cards=cards, punch=punch, punch_covered=punch_covered,
    real_photos=real_photos, ai_inserts=ai_inserts,
    label_chips=dict(real=os.path.abspath(f'{D}/plan_assets/chip_real.png'),
                     ai=os.path.abspath(f'{D}/plan_assets/chip_ai.png')),
    label_pos=dict(real=real_pos, ai=ai_pos),
    srt=os.path.abspath(f'{D}/plan_assets/captions.srt'),
    words=[dict(w=w['word'], t=round(float(w['start']), 3), e=round(float(w['end']), 3)) for w in json.load(open(f'{D}/words_ctc.json'))],
    source_audio=os.path.abspath(f'{D}/his_mix.wav'),
    banned_source=Q.get('banned_source'), banned_times=Q.get('banned_times'),
    watch_log=os.path.abspath(f'{D}/logs/watch_pass.json'),
)
if plan['reference_cut'] is None: del plan['reference_cut']

old = json.load(open(f'{D}/plan.json')) if os.path.exists(f'{D}/plan.json') else {}
for k in ('transcript_words', 'negative_events_scan'):
    if k in old: plan[k] = old[k]

if '--transcribe' in sys.argv:
    import whisper
    r = whisper.load_model('small').transcribe(VID, word_timestamps=False, language='en')
    plan['transcript_words'] = [dict(w=w) for seg in r['segments'] for w in seg['text'].split()]

json.dump(plan, open(f'{D}/plan.json', 'w'), indent=1)
print(f"{D}/plan.json: {len(joins)} joins, {len(punch)} holds, {len(real_photos)} real photos, "
      f"{len(ai_inserts)} AI-of-Dan inserts, {len(gs)} caption cues, {len(plan['words'])} words, "
      f"transcript {len(plan.get('transcript_words') or [])}")
