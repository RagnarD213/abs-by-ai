"""RO-24 round 2 context clips: every graphic, photo scene and B-roll insert played in the finished picture with Dan's narration and
about 3.5 s either side (PRE-RENDER-APPROVAL: each item in its moving context), rendered window by window (no full-film render).
    python3 ctx_r2.py [--only G03,P3,...]
Merges hf/manifest.json + broll/broll_manifest.json into film_manifest.json (what the film build uses too). Items that sit inside
the first minute are covered by the first-minute player and skipped. Writes review/context/<id>.mp4 (960x540) + <id>.jpg (fullest
moment) and review/context/index.json."""
import json, subprocess, sys, os
W = '/Volumes/Expansion/_edit_work/RO-24/round2'; R = f'{W}/recipe'; OUT = f'{W}/review/context'; os.makedirs(OUT, exist_ok=True)
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001; FM_END = 1889 / FPS
M = json.load(open(f'{W}/hf/manifest.json')) + json.load(open(f'{W}/broll/broll_manifest.json'))
for m in M: assert os.path.exists(m['mov']), ('missing render', m['id'], m['mov'])
json.dump(M, open(f'{W}/film_manifest.json', 'w'), indent=1)
only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
N = sum(p['f1'] - p['f0'] for p in json.load(open(f'{W}/edl_film_pic.json'))['pieces'])
idx = []
for m in sorted(M, key=lambda m: m['a']):
    if m['b'] <= FM_END + 0.01 or (only and m['id'] not in only): continue
    a, b = max(0.0, m['a'] - 3.5), min(N / FPS, m['b'] + 3.5); g0, g1 = int(a * FPS), int(b * FPS)
    pic = f'{OUT}/_{m["id"]}_pic.mp4'; out = f'{OUT}/{m["id"]}.mp4'
    subprocess.run(['python3', f'{R}/assemble16.py', f'{W}/edl_film_pic.json', pic, '--bg', 'depth', '--grade', 'warm', '--hf', f'{W}/film_manifest.json',
                    '--g0', str(g0), '--g1', str(g1)], check=True)
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{g0 / FPS:.4f}', '-i', f'{W}/audio/film_voice_A.wav', '-i', pic, '-map', '1:v:0', '-map', '0:a:0',
                    '-t', f'{(g1 - g0) / FPS:.4f}', '-vf', 'scale=960:540', '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k',
                    '-movflags', '+faststart', out], check=True)
    mid = (min(m['b'], m['a'] + 4.0) - a) if m['id'].startswith('G') else (m['a'] + m['b']) / 2 - a
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{mid:.3f}', '-i', pic, '-frames:v', '1', '-q:v', '3', '-vf', 'scale=960:540', f'{OUT}/{m["id"]}.jpg'], check=True)
    os.remove(pic); [os.remove(f'{pic}.build.json')] if os.path.exists(f'{pic}.build.json') else None
    idx.append(dict(id=m['id'], kind=m['kind'], template=m.get('template'), a=round(m['a'], 2), b=round(m['b'], 2), clip_t0=round(a, 2), mp4=f'context/{m["id"]}.mp4', jpg=f'context/{m["id"]}.jpg'))
    print('CTX', m['id'], round(a, 1), round(b, 1), flush=True)
old = json.load(open(f'{OUT}/index.json')) if os.path.exists(f'{OUT}/index.json') and only else []
keep = {x['id']: x for x in old}; keep.update({x['id']: x for x in idx})
json.dump(sorted(keep.values(), key=lambda x: x['a']), open(f'{OUT}/index.json', 'w'), indent=1); print('CTX DONE', len(idx))
