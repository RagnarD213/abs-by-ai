"""RO-21 round 3 (Dan 2026-10-29: "too many pictures of me ... occasionally break that up throughout the video with pictures
of another guy at a similar body fat percentage"): round 2's manifest + background plan with
  BG01 (6 s) and BG04 (57 s) floating cards -> the other man (a white man in his 40s, round3/om/O*.png) at the same levels;
  BG02 (28 s, "the average man at 28%") -> no side-by-side pair (it read as a before/after): the set's TV plays one picture of
     the other man at 30% (slow push-in clip);
  three later set-TV level pairs -> the other man's pair at the same two levels: BG09 (35/30), BG13 (25/20), BG20 (12/10).
  B10 -> the new AI clip (round3/broll/B10.mp4, chip burned in) once built.
Everything else is round 2 as approved. -> round3/film_manifest.json, round3/bg_plan.json"""
import json, os
B = '/Volumes/Expansion/_edit_work/RO-21'; R2 = f'{B}/round2'; R3 = f'{B}/round3'
O = lambda l: f'{R3}/om/O{l:02d}.png'
M = json.load(open(f'{R2}/film_manifest.json'))
if os.path.exists(f'{R3}/broll/B10.mp4'):
    for m in M:
        if m['id'] == 'B10': m['mov'] = f'{R3}/broll/B10.mp4'
json.dump(M, open(f'{R3}/film_manifest.json', 'w'), indent=1)
P = json.load(open(f'{R2}/bg_plan.json')); seg = {g['id']: g for g in P['segments']}
WHY = ' | R3 (Dan 10-29): other man, to break up the pictures of Dan'
seg['BG01'].update(photos=[O(l) for l in (35, 30, 25, 20, 15, 12)]); seg['BG01']['why'] += WHY
seg['BG04'].update(photos=[O(l) for l in (30, 20, 12, 25, 15, 8)]); seg['BG04']['why'] += WHY
seg['BG02'].pop('photos', None)
seg['BG02'].update(clip=dict(src=f'{R3}/bgclips/O30_tv.mp4', windows=[[0.0, 13.9]]),
                   why='R3 (Dan 10-29): the 30%/25% pair read as a before/after; the TV shows one picture of the other man at 30% (the average man)')
# R3 independent review: a pair of neighbouring levels side by side reads as a before/after, the layout Dan rejected at 0:28.
# The other man's spots are single pictures (slow push-in on the TV), and BG11 (the exact Dan 30%/25% pair he rejected at
# 0:28) becomes one picture of Dan at 30%. The three other Dan pairs approved in round 1 (BG06, BG16, BG27) stay; Dan's call.
for k, src in (('BG09', 'O35'), ('BG11', 'L30'), ('BG13', 'O25'), ('BG20', 'O12')):
    seg[k].pop('photos', None); g = seg[k]
    g['clip'] = dict(src=f'{R3}/bgclips/{src}_tv.mp4', windows=[[0.0, round(min(18.9, g['t1'] - g['t0'] + 0.3), 2)]])
    g['why'] += ' | R3: one picture, no side-by-side pair (reads as a before/after)'
# R3 watch judge: the A35 and M12 left-third cards cover the set's top-left AI chip (81.4-84.8 s, 304.7-314.0 s); on those two
# set segments the chip moves to the bottom left (no lower third runs there) and the set's own chip is turned off
for k in ('BG06', 'BG20'): seg[k].update(ai_label=False, chip_xy=[56, 952])
json.dump(P, open(f'{R3}/bg_plan.json', 'w'), indent=1)
missing = [p for g in P['segments'] for p in g.get('photos', []) + [((g.get('clip') or {}).get('src') or '')] if p and not os.path.exists(p)]
print('round 3 manifest + bg plan written; missing:', missing or 'none')
