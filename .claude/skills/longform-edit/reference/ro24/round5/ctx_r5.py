"""RO-24 round 4 context clips from the exact full-film export: every background segment after 2:50 and every changed or
newly placed item (P4-P7, G12, G14, the four later clips, B2) with 4 s either side, 540p, plus a still at its middle.
-> review/context/, index.json (page_r4.py reads it)"""
import json, subprocess, pathlib
R4 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round5')
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
F = R4 / 'final/RO24_R5_MASTER.mp4'; O = R4 / 'review/context'; O.mkdir(parents=True, exist_ok=True)
plan = json.load(open(R4 / 'bg_plan.json'))['segments']; man = {m['id']: m for m in json.load(open(R4 / 'film_manifest_r5.json'))}
END = max(m['b'] for m in man.values())
items = [(s['id'], s['t0'], s['t1'], 'bg') for s in plan if s['id'] in ('BG20', 'BG21')]   # round 5: the tightened cut
items += [(i, man[i]['a'], man[i]['b'], 'item') for i in ('G06', 'P8', 'A3', 'A4') if i in man]   # round 5 changes
out = []
for i, a, b, kind in items:
    a0, b0 = max(0.0, a - 4.0), min(END, b + 4.0)
    mp4 = O / f'{i}-context - REVIEW 540p.mp4'; jpg = O / f'{i}.jpg'
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{a0:.3f}', '-i', str(F), '-t', f'{b0 - a0:.3f}', '-vf', 'scale=960:540', '-c:v', 'libx264',
                    '-crf', '22', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(mp4)], check=True)
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{(a + b) / 2:.3f}', '-i', str(F), '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '3', str(jpg)], check=True)
    out.append(dict(id=i, kind=kind, a=round(a, 2), b=round(b, 2), ctx_a=round(a0, 2), ctx_b=round(b0, 2), mp4=f'context/{mp4.name}', jpg=f'context/{jpg.name}'))
json.dump(out, open(O / 'index.json', 'w'), indent=1); print('CONTEXT DONE', len(out))
