#!/usr/bin/env python3
"""Sample frames from the SOURCE for every shot that contains a human subject, so the
framing actually used can be checked against where the subject really is."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.dirname(HERE)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"], cwd=BD).decode())['SRC']
FPS, SCALE = 2.0, 960
man = json.load(open(os.path.join(BD, 'shots', 'manifest.json')))
plan = json.loads(subprocess.check_output(
    ['node', '-e', "const p=require('./plan.js');console.log(JSON.stringify({SHOTS:p.SHOTS,TALK_X:p.TALK_X}))"],
    cwd=BD, stderr=subprocess.DEVNULL).decode())
# Shots whose subject is NOT a single human, so a person mask cannot judge the framing.
SKIP = set(os.environ.get('SKIP', 'A-p0-s03,A-p0-s04,A-p0-s05,A-p0-s06,A-p0-s07').split(','))
out = os.path.join(HERE, 'fr'); os.makedirs(out, exist_ok=True)
meta = []
for m in man:
    n = m['name']
    spec = plan['SHOTS'][n]
    if n in SKIP or spec['t'] == 'extern':
        continue
    od = os.path.join(out, n)
    if not os.path.isdir(od) or not [f for f in os.listdir(od) if not f.startswith('._')]:
        os.makedirs(od, exist_ok=True)
        subprocess.run([FF, '-nostdin', '-y', '-v', 'error', '-ss', f"{m['absStart']:.3f}",
                        '-t', f"{m['dur']:.3f}", '-i', SRC,
                        '-vf', f'fps={FPS},scale={SCALE}:-2', os.path.join(od, '%03d.png')], check=True)
    meta.append({'shot': n, 'seg': m['seg'], 'start': m['absStart'], 'dur': m['dur'],
                 't': spec['t'], 'zoom': bool(spec.get('zoom')),
                 'cardCrop': spec.get('cardCrop'), 'minX0': spec.get('minX0'),
                 'n': len([f for f in os.listdir(od) if not f.startswith('._')])})
json.dump({'shots': meta, 'talk_x': plan['TALK_X']}, open(os.path.join(HERE, 'fr.json'), 'w'), indent=1)
print(len(meta), 'shots,', sum(s['n'] for s in meta), 'frames  (skipped', len(SKIP), 'non-person shots)')
