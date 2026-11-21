"""RO-24 round 2 B-roll inserts as full-screen clips for the compositor (kind opaque), 1920x1080 at 30000/1001, exact frame counts.
B1 167.80: real Dan ab-wheel rollout (B0030 0.8-3.2 s, real moving footage: no label) then AI-Dan salmon dinner (A0200, 'AI-GENERATED').
B2 255.55 (Dan's choice A): AI-Dan dumbbell bench press, one full rep (A0111 0.5-3.6 s, 'AI-GENERATED'). Writes broll_manifest.json."""
import subprocess, json, sys, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import softblue as B
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001
L = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'; O = '/Volumes/Expansion/_edit_work/RO-24/round2/broll'
SRC = {'B0030': f'{L}/03 B-Roll - Real Footage/dan-filmed/B0030_dan-ab-wheel-rollout-rep-poolside_16x9_8s.mp4',
       'A0200': f'{L}/04 AI-Generated Clips/concepts-and-gags/A0200_ai-dan-salmon-dinner-cutting_16x9_3s.mp4',
       'A0111': f'{L}/04 AI-Generated Clips/exercise-demos/A0111_ai-dan-db-bench-press-demo_16x9_24s.mp4'}
chip = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); B.disclosure(chip, 'AI-GENERATED', xy=(56, 48)); chip.save(f'{O}/ai_chip.png')
def part(clip, t0, t1, out, ai):
    n = int(round((t1 - t0) * FPS))
    vf = f"[0:v]fps=30000/1001,scale=1920:1080:flags=lanczos,setsar=1[v]" + (";[v][1:v]overlay=0:0[o]" if ai else "")
    cmd = [FF, '-y', '-v', 'error', '-ss', f'{t0}', '-i', SRC[clip]] + (['-i', f'{O}/ai_chip.png'] if ai else []) + \
          ['-filter_complex', vf, '-map', '[o]' if ai else '[v]', '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow',
           '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out]
    subprocess.run(cmd, check=True); return n
n1 = part('B0030', 0.8, 3.2, f'{O}/b1_rollout.mp4', False); n2 = part('A0200', 0.0, 2.875, f'{O}/b1_salmon.mp4', True)
subprocess.run([FF, '-y', '-v', 'error', '-i', f'{O}/b1_rollout.mp4', '-i', f'{O}/b1_salmon.mp4', '-filter_complex', '[0:v][1:v]concat=n=2:v=1[v]',
                '-map', '[v]', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p', f'{O}/B1.mp4'], check=True)
n3 = part('A0111', 0.5, 3.6, f'{O}/B2.mp4', True)
a1 = 167.80; a2 = 255.55
M = [dict(id='B1', kind='opaque', template='broll', a=a1, b=a1 + (n1 + n2) / FPS, mov=f'{O}/B1.mp4', note='B0030 rollout (real) then A0200 salmon (AI, labelled)'),
     dict(id='B2', kind='opaque', template='broll', a=a2, b=a2 + n3 / FPS, mov=f'{O}/B2.mp4', note='A0111 dumbbell bench press (AI, labelled); Dan picks A (use) or B (stay on camera)')]
json.dump(M, open(f'{O}/broll_manifest.json', 'w'), indent=1); print('BROLL DONE', [(m['id'], round(m['a'], 2), round(m['b'], 2)) for m in M])
