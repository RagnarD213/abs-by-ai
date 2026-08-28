#!/usr/bin/env python3
"""Sample frames from the SOURCE master for every talking-head shot in a Shorts build,
so the crop window actually used can be checked against where the presenter really is."""
import json, os, subprocess, sys, shutil

ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/YouTube Long Form Video Content"
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SP = "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/39032698-3f11-4a8d-9382-8b0b6599b994/scratchpad"

BUILDS = {
    'v2': ('six-ways-ai-abs', 'V2 - How To Get Real Six Pack Abs With AI(2) - READY FOR UPLOAD.mp4'),
    'v3': ('v3-top10-tips', 'V3 - My Top 10 Tips For Getting Six Pack Abs(3).mp4 - READY FOR UPLOAD.mp4'),
    'v6': ('v6-3min-home-workout', 'V6 - 3 Minute Total Body Home Workout(2).mp4 - READY FOR UPLOAD.mp4'),
}
FPS = 2.0
TREAT = set(os.environ.get('TREAT','talk').split(','))
SCALE = 960  # analysis resolution; coordinates are fractions so this is lossless for our purpose

def load(bid):
    d, srcname = BUILDS[bid]
    bd = os.path.join(ROOT, d)
    man = json.load(open(os.path.join(bd, 'shots', 'manifest.json')))
    crops = json.load(open(os.path.join(bd, 'shots', 'crops.json')))
    plan = json.loads(subprocess.check_output(
        ['node', '-e', "const p=require('./plan.js');const {SEGMENTS}=require('./segments.js');"
         "console.log(JSON.stringify({SHOTS:p.SHOTS,TALK_X:p.TALK_X,"
         "SEG:SEGMENTS.map(s=>({id:s.id,slug:s.slug}))}))"], cwd=bd).decode())
    return bd, os.path.join(ROOT, srcname), man, crops, plan

def main(bid):
    bd, src, man, crops, plan = load(bid)
    out = os.path.join(SP, 'fr', bid)
    os.makedirs(out, exist_ok=True)
    meta = []
    for m in man:
        spec = plan['SHOTS'][m['name']]
        if spec['t'] not in TREAT:
            continue
        n, t0, dur = m['name'], m['absStart'], m['dur']
        od = os.path.join(out, n)
        if not os.path.isdir(od) or not os.listdir(od):
            os.makedirs(od, exist_ok=True)
            subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}',
                            '-i', src, '-vf', f'fps={FPS},scale={SCALE}:-2',
                            os.path.join(od, '%03d.png')], check=True)
        meta.append({'shot': n, 'seg': m['seg'], 'start': t0, 'dur': dur,
                     'x': crops.get(n, plan['TALK_X']), 'n': len(os.listdir(od))})
    json.dump({'build': bid, 'segs': plan['SEG'], 'talk_x': plan['TALK_X'], 'shots': meta},
              open(os.path.join(SP, f'fr/{bid}.json'), 'w'), indent=1)
    print(bid, len(meta), 'talk shots,', sum(s['n'] for s in meta), 'frames')

for b in sys.argv[1:] or ['v2', 'v3', 'v6']:
    main(b)
