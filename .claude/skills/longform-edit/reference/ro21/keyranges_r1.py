"""RO-21: source frame ranges to key = every presenter-visible shot (shots.json, not covered by a full-screen item) mapped
through the EDL, plus 6 frames of handle each side (stage 1.5 neighbours), merged when closer than 45 frames.
Writes round1/key_ranges.json [{name, f0, n, film: [t0, t1] list}]. Key once: names are stable by f0."""
import json
B = '/Volumes/Expansion/_edit_work/RO-21/round1'; FPS = 30000 / 1001; H = 6
E = json.load(open(f'{B}/edl_r1.json')); S = json.load(open(f'{B}/shots.json'))
segs = []
for s in S:
    if s['covered']: continue
    for e in E:
        a, b = max(s['t0'], e['film_in']), min(s['t1'], e['film_out'])
        if b - a < 0.02: continue
        f0 = e['f_in'] + int((a - e['film_in']) * FPS) - H; f1 = e['f_in'] + int((b - e['film_in']) * FPS + 0.999) + H
        segs.append([max(e['f_in'] - H, f0), min(e['f_out'] + H, f1), round(a, 2), round(b, 2)])
segs.sort(); M = []
for s in segs:
    if M and s[0] - M[-1][1] < 45: M[-1][1] = max(M[-1][1], s[1]); M[-1][2].append([s[2], s[3]])
    else: M.append([s[0], s[1], [[s[2], s[3]]]])
out = [dict(name=f'K{m[0]:05d}', f0=m[0], n=m[1] - m[0], film=m[2]) for m in M]
json.dump(out, open(f'{B}/key_ranges.json', 'w'), indent=1)
tot = sum(o['n'] for o in out)
for o in out: print(o['name'], o['f0'], o['n'], 'film', o['film'][0][0], '..', o['film'][-1][1])
print(len(out), 'ranges', tot, 'frames,', round(tot * 6.5 / 3600, 1), 'CPU-h at 6.5 CPU-s a frame')
