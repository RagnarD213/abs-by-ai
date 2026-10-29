"""RO-21 round 1 context clips: every graphic, picture card and clip with about 4 s of narration either side.
Windows that overlap are rendered once (assemble_r1.py, warm grade), the voice is muxed, and each item's clip is cut out at 540p:
round1/review/context/<ID>-context - REVIEW 540p.mp4 + a poster still (<ID>.jpg, the item's middle frame).
  python3 ctx_r1.py [--only IDS] [--from-fm]   (--from-fm: cut items inside 0-62 s from the first-minute draft, no render)"""
import json, os, subprocess, sys
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'; OUT = f'{R1}/review/context'; os.makedirs(OUT, exist_ok=True)
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001; PAD = 4.0
VOICE = f'{B}/audio/film/film_voice_B.wav'; FM = f'{R1}/fm/DRAFT - RO-21 round 1 - first minute.mp4'; FM_END = 62.0
P = json.load(open(f'{R1}/plan_r1.json')); END = max(p['b'] for p in P)
only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
items = [p for p in P if not only or p['id'] in only]
def cut(src, src_t0, it, w0, w1):
    o = f"{OUT}/{it['id']}-context - REVIEW 540p.mp4"
    subprocess.run([FF, '-v', 'error', '-y', '-ss', f'{w0 - src_t0:.3f}', '-t', f'{w1 - w0:.3f}', '-i', src, '-vf', 'scale=960:540:flags=lanczos',
                    '-c:v', 'libx264', '-crf', '22', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', o], check=True)
    mid = (it['a'] + it['b']) / 2 - src_t0
    subprocess.run([FF.replace('ffmpeg', 'ffmpeg.real'), '-v', 'error', '-y', '-ss', f'{mid:.3f}', '-i', src, '-frames:v', '1', '-vf', 'scale=640:360', f"{OUT}/{it['id']}.jpg"], check=True)
fmi = [p for p in items if p['b'] + 0.5 <= FM_END]
if '--from-fm' in sys.argv:
    for it in fmi: cut(FM, 0.0, it, max(0, it['a'] - PAD), min(FM_END, it['b'] + PAD)); print('ctx', it['id'], 'from first minute')
    sys.exit(0)
rest = sorted([p for p in items if p not in fmi], key=lambda p: p['a'])
wins = []
for it in rest:
    w0, w1 = max(0, it['a'] - PAD), min(END, it['b'] + PAD)
    if wins and w0 <= wins[-1][1] + 1.0 and w1 - wins[-1][0] < 45: wins[-1][1] = max(wins[-1][1], w1); wins[-1][2].append(it)
    else: wins.append([w0, w1, [it]])
for k, (w0, w1, its) in enumerate(wins):
    g0, g1 = int(round(w0 * FPS)), int(round(w1 * FPS)); pic = f'{R1}/review/_ctx_{g0}.mp4'; full = pic.replace('.mp4', '_av.mp4')
    if not os.path.exists(full):
        subprocess.run(['python3', f'{B}/recipe/assemble_r1.py', pic, '--g0', str(g0), '--g1', str(g1)], check=True)
        subprocess.run([FF, '-v', 'error', '-y', '-i', pic, '-ss', f'{g0 / FPS:.4f}', '-t', f'{(g1 - g0) / FPS:.4f}', '-i', VOICE, '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', full], check=True)
    for it in its:
        cut(full, g0 / FPS, it, max(g0 / FPS, it['a'] - PAD), min(g1 / FPS, it['b'] + PAD)); print('ctx', it['id'], flush=True)
print('CTX DONE', len(wins), 'windows')
