"""RO-21 round 4 (Dan 2026-10-30): round 3's manifest + background plan with
  - a third set: a Hispanic man in his 30s (round4/hm/H*.png). Dan's own pictures stay the intro and the first example at every
    level (ladders, level cards, Next Stop panels); the backgrounds rotate the other two men: W 0:06, W 0:28, H 0:53, H 1:21, W 1:57,
    H 2:29, W 3:12, H 3:59, W 5:05, H 6:28. The two remaining side-by-side TV pairs of Dan become single pictures (same before/after note).
  - the gym clips (B07, B11) and the two blurred gym stills regraded (broll_r4.py);
  - the AI label never on a face or abs: on the Next Stop panels it sits above the pair, which moves down 42 px; on the floating cards it
    moves up and the top-left card moves down.
-> round4/film_manifest.json, round4/bg_plan.json"""
import json, os
B = '/Volumes/Expansion/_edit_work/RO-21'; R3 = f'{B}/round3'; R4 = f'{B}/round4'
M = json.load(open(f'{R3}/film_manifest.json'))
for m in M:
    if m['id'] in ('B07', 'B11'): m['mov'] = f'{R4}/broll/{m["id"]}.mp4'
    for k in ('mov',):
        if not os.path.isabs(m[k]): raise SystemExit(m)
json.dump(M, open(f'{R4}/film_manifest.json', 'w'), indent=1)
P = json.load(open(f'{R3}/bg_plan.json')); seg = {g['id']: g for g in P['segments']}
H = lambda l: f'{R4}/hm/H{l:02d}.png'
SLOTS = [[300, 375, 380, -7], [330, 835, 400, 5], [1625, 320, 380, 6], [1590, 790, 400, -5], [650, 175, 300, 4], [1270, 185, 300, -4]]
for k in ('BG01', 'BG04'): seg[k].update(slots=SLOTS, ai_label=False, chip_xy=[56, 20])
seg['BG04'].update(photos=[H(l) for l in (30, 20, 12, 25, 15, 8)]); seg['BG04']['why'] += ' | R4 (Dan 10-30): third set, a Hispanic man in his 30s'
for k, l in (('BG06', 35), ('BG11', 30), ('BG16', 20), ('BG27', 8)):
    g = seg[k]; g.pop('photos', None); g.pop('clip', None)
    g['clip'] = dict(src=f'{R4}/bgclips/H{l:02d}_tv.mp4', windows=[[0.0, round(min(18.9, g['t1'] - g['t0'] + 0.3), 2)]])
    g['why'] += ' | R4: rotate the other two men in the background, one picture'
for k in ('BG14', 'BG18', 'BG26'): seg[k].update(panel_y=126, chip_xy=[84, 26], ai_label=False)
for k, s in (('BG03', 'gym'), ('BG15', 'gym'), ('BG25', 'cable')): seg[k]['photos'] = [f'{R4}/bgstills/{s}.jpg']
json.dump(P, open(f'{R4}/bg_plan.json', 'w'), indent=1)
print('round 4 manifest + bg plan written')
