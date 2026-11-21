"""RO-21 round 2 review media, all in the approved B Rich grade and voice A, on the round 2 plan files:
  the first minute (0-62 s, with the new B01) -> round2/fm/DRAFT - RO-21 round 2 - first minute.mp4
  B01 context cut from it; P12 and G10 context windows rendered on their own (G10 starts on the cut after B10, so the
  rejected stock sleep shot is not shown again). 540p context clips + posters in round2/review/context/.
  python3 ctx_r2.py [fm|p12|g10 ...]"""
import os, subprocess, sys
B = '/Volumes/Expansion/_edit_work/RO-21'; R2 = f'{B}/round2'
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001
VOICE = f'{B}/audio/film/film_voice_B.wav'; OUT = f'{R2}/review/context'
JOBS = {'fm': (0.0, 62.0, f'{R2}/fm/DRAFT - RO-21 round 2 - first minute.mp4', [('B01', 15.859, 19.659)]),
        'p12': (298.437, 308.737, f'{R2}/review/_ctx_p12.mp4', [('P12', 302.437, 304.737)]),
        'g10': (323.993, 338.334, f'{R2}/review/_ctx_g10.mp4', [('G10', 323.993, 334.334)])}
def run(key):
    w0, w1, full, its = JOBS[key]; g0, g1 = int(round(w0 * FPS)), int(round(w1 * FPS)); pic = full.replace('.mp4', '_pic.mp4')
    subprocess.run(['python3', f'{B}/recipe/assemble_r1.py', pic, '--g0', str(g0), '--g1', str(g1), '--grade', 'rich',
                    '--plan', f'{R2}/bg_plan.json', '--manifest', f'{R2}/film_manifest.json'], check=True)
    subprocess.run([FF, '-v', 'error', '-y', '-i', pic, '-ss', f'{g0 / FPS:.4f}', '-t', f'{(g1 - g0) / FPS:.4f}', '-i', VOICE, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', full], check=True)
    for iid, a, b in its:
        s0, s1 = max(w0, a - 4.0), min(w1, b + 4.0)
        subprocess.run([FF, '-v', 'error', '-y', '-ss', f'{s0 - g0 / FPS:.3f}', '-t', f'{s1 - s0:.3f}', '-i', full, '-vf', 'scale=960:540:flags=lanczos',
                        '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart',
                        f'{OUT}/{iid}-context - REVIEW 540p.mp4'], check=True)
        subprocess.run([FF + '.real', '-v', 'error', '-y', '-ss', f'{(a + b) / 2 - g0 / FPS:.3f}', '-i', full, '-frames:v', '1', '-vf', 'scale=640:360',
                        f'{OUT}/{iid}.jpg'], check=True)
        print('ctx', iid, flush=True)
for k in (sys.argv[1:] or ['p12', 'g10', 'fm']): run(k)
print('CTX R2 DONE')
