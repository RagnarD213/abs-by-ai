"""RO-24 round 3 context clips from the exact preview export: every background segment with 3 s either side (the "10-15 s
sample of every type in context"), every photo scene and both clips that play in the preview, at 540p; a still at the middle
of each; the six interview clips on their own (540p); pair stills for the rest of the film. -> review/context/, index.json"""
import json, subprocess, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3'); FPS = 30000 / 1001
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
PV = R3 / 'review/preview/DRAFT - RO-24 round 3 - first 2m50s.mp4'; END = 5111 / FPS
O = R3 / 'review/context'; O.mkdir(parents=True, exist_ok=True)
plan = json.load(open(R3 / 'bg_plan.json'))['segments']; man = {m['id']: m for m in json.load(open(R3 / 'film_manifest_r3.json'))}
items = [(s['id'], s['t0'], s['t1'], 'bg') for s in plan if s['t1'] <= END + 0.05]
items += [(i, man[i]['a'], man[i]['b'], 'photo') for i in ('P0', 'P1', 'P2', 'P3')]
items += [(i, man[i]['a'], man[i]['b'], 'clip') for i in ('C_sharon', 'C_fatjoe')]
out = []
for i, a, b, kind in items:
    a0, b0 = max(0.0, a - 3.0), min(END, b + 3.0)
    mp4 = O / f'{i}-context - REVIEW 540p.mp4'; jpg = O / f'{i}.jpg'
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{a0:.3f}', '-i', str(PV), '-t', f'{b0 - a0:.3f}', '-vf', 'scale=960:540', '-c:v', 'libx264',
                    '-crf', '22', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(mp4)], check=True)
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{(a + b) / 2:.3f}', '-i', str(PV), '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '3', str(jpg)], check=True)
    out.append(dict(id=i, kind=kind, a=round(a, 2), b=round(b, 2), ctx_a=round(a0, 2), ctx_b=round(b0, 2), mp4=f'context/{mp4.name}', jpg=f'context/{jpg.name}'))
    print(i, round(a0, 1), round(b0, 1), flush=True)
ins = json.load(open(R3 / 'clips/inserts.json'))
for n, I in ins.items():
    mp4 = O / f'clip-{n} - REVIEW 540p.mp4'; jpg = O / f'clip-{n}.jpg'
    subprocess.run([FF, '-y', '-v', 'error', '-i', str(R3 / I['file']), '-i', str(R3 / I['wav']), '-map', '0:v', '-map', '1:a', '-vf', 'scale=960:540',
                    '-c:v', 'libx264', '-crf', '22', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(mp4)], check=True)
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{I["dur"] / 2:.2f}', '-i', str(R3 / I['file']), '-frames:v', '1', '-vf', 'scale=960:540', '-q:v', '3', str(jpg)], check=True)
    out.append(dict(id=f'clip-{n}', kind='clip-alone', mp4=f'context/{mp4.name}', jpg=f'context/{jpg.name}', dur=I['dur']))
# planned before / after pairs for the rest of the film (round 4), as plain side-by-side stills
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/worktrees/agitated-pike-89e952/.claude/skills/_shared/greenscreen-bg'); import gsbg as G
facts = json.load(open(R3 / 'facts.json'))
for person, P in facts['people'].items():
    for k, pr in enumerate(P.get('pairs', [])):
        ims = [G.person_crop(G.Context(R3).path(p), 3 / 4, k=pr.get('crop_k', 6.0), top=pr.get('top', 0.55)).resize((420, 560)) for p in pr['photos']]
        W = Image.new('RGB', (900, 640), (8, 18, 34)); W.paste(ims[0], (20, 20)); W.paste(ims[1], (460, 20))
        d = ImageDraw.Draw(W); f = ImageFont.truetype('/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/assets/fonts/Poppins-Bold.ttf', 26)
        d.text((20, 592), f"{person}  {pr['years'][0]} / {pr['years'][1]}   {P['stat']}", font=f, fill=(150, 210, 255))
        name = f"pair-{person.split()[0].lower()}-{k}.jpg"; W.save(O / name, quality=90)
        out.append(dict(id=name[:-4], kind='pair', person=person, years=pr['years'], credits=pr.get('credits'), jpg=f'context/{name}'))
json.dump(out, open(O / 'index.json', 'w'), indent=1); print('CONTEXT DONE', len(out))
