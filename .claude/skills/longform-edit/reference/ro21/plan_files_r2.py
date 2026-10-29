"""RO-21 round 2: the round 1 manifest and background plan with Dan's 2026-10-29 changes (round 1 files untouched).
  B01 -> round2/broll/B01.mp4 (A0207 + chip), P12 -> round2/hf/tpl/renders/P12.mov ("Upper Four Abs"),
  BG22 (G10 span) -> the set's TV plays round2/bgclips/G10_man.mp4 (sleep-deprived overweight man, set's own AI chip).
  B10 stays the round 1 stock until Dan approves the new frames and the motion is made.
-> round2/film_manifest.json, round2/bg_plan.json"""
import json
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'; R2 = f'{B}/round2'
M = json.load(open(f'{R1}/film_manifest.json'))
for m in M:
    if m['id'] == 'B01': m['mov'] = f'{R2}/broll/B01.mp4'
    if m['id'] == 'P12': m['mov'] = f'{R2}/hf/tpl/renders/P12.mov'
json.dump(M, open(f'{R2}/film_manifest.json', 'w'), indent=1)
P = json.load(open(f'{R1}/bg_plan.json'))
for g in P['segments']:
    if g['id'] == 'BG22':
        g.pop('photos', None)
        g.update(clip=dict(src=f'{R2}/bgclips/G10_man.mp4', windows=[[0.0, 10.9]]),
                 why='R2 (Dan 10-29): the TV shows a sleep-deprived overweight man during the sleep study lower third')
json.dump(P, open(f'{R2}/bg_plan.json', 'w'), indent=1)
print('round 2 manifest + bg plan written')
