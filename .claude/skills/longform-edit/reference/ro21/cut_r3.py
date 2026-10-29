"""RO-21 round 3, third fix (independent re-review, 2026-10-29): a false start in the recap. At 7:12.5 Dan says "12%, eat at least
.8 grams of...", stops, pauses 2.5 s and says the whole line from 7:17.2. Both are in edit piece 13 under the full-screen recap
picture row (G11), so:
  sound   -> cut film 432.050-436.888 s (145 frames' worth, both ends in the pause; 10 ms crossfade)
  picture -> cut the same 145 frames from the G11 hold on 12% (film frames 13007-13152), a 10-frame dissolve inside the still
             graphic, so the 12% highlight (432.296) lands on the clean "12%" (old 437.16 -> new 432.32) and the 10%/8% highlights
             stay on their words. Only frames from the keyframe at 12801 on are re-encoded (same x264 settings).
  data    -> round3 copies of the plan, words, edit list and build map shifted by -145 frames after the cut; G11 MOV cut the same
             way for the watch pass's graphic-presence check; the bed rebuilt to the new length.
  python3 cut_r3.py"""
import json, subprocess, numpy as np, shutil, os
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'; R3 = f'{B}/round3'; O = f'{R3}/final'
P_ = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin'; FF = f'{P_}/ffmpeg'; FFR = f'{P_}/ffmpeg.real'
FPS = 30000 / 1001; NCUT = 145; DT = NCUT / FPS; A0 = 432.050; A1 = A0 + DT; X = 13007; K = 12801; XF = 10; N = 13556
sr = 48000; S = lambda t: int(round(t * sr))
# ---- sound
rd = lambda p: np.frombuffer(subprocess.run([FFR, '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout, np.float32).astype(np.float64)
v = rd(f'{B}/audio/film/film_voice_raw_r3.wav'); f = S(0.010); r = np.sin(np.linspace(0, np.pi / 2, f)) ** 2
head, tail = v[:S(A0) + f].copy(), v[S(A1):].copy(); head[-f:] = head[-f:] * r[::-1] + tail[:f] * r; out = np.concatenate([head, tail[f:]])
subprocess.run([FFR, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le', f'{B}/audio/film/film_voice_raw_r3b.wav'], input=out.astype(np.float32).tobytes(), check=True)
print('voice', round(len(out) / sr, 3), 's')
# ---- picture: head [0,K) stream copy; tail re-encoded with the dissolve
if not os.path.exists(f'{O}/picture_v3.mp4'): shutil.copy2(f'{O}/picture.mp4', f'{O}/picture_v3.mp4'); shutil.copy2(f'{O}/picture.build.json', f'{O}/picture_v3.build.json')
src = f'{O}/picture_v3.mp4'; t = lambda fr: f'{fr / FPS:.6f}'
subprocess.run([FFR, '-v', 'error', '-y', '-i', src, '-frames:v', str(K), '-c', 'copy', f'{R3}/film/cut_head.mp4'], check=True)
la, lb0 = (X + XF // 2) - K, X + NCUT - XF // 2
fc = (f"[0:v]trim=start_frame={K}:end_frame={X + XF // 2},setpts=PTS-STARTPTS[a];[0:v]trim=start_frame={lb0}:end_frame={N},setpts=PTS-STARTPTS[b];"
      f"[a][b]xfade=transition=fade:duration={XF / FPS:.6f}:offset={(la - XF) / FPS:.6f},format=yuv420p[v]")
subprocess.run([FF, '-v', 'error', '-y', '-i', src, '-filter_complex', fc, '-map', '[v]', '-r', '30000/1001', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', f'{R3}/film/cut_tail.mp4'], check=True)
open(f'{R3}/film/list_cut.txt', 'w').write(f"file 'cut_head.mp4'\nfile 'cut_tail.mp4'\n")
subprocess.run([FFR, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{R3}/film/list_cut.txt', '-c', 'copy', f'{O}/picture.mp4'], check=True)
# ---- G11 MOV cut the same way (graphic presence check)
g0 = round(402.093 * FPS); gx = X - g0
fc = (f"[0:v]trim=end_frame={gx + XF // 2},setpts=PTS-STARTPTS[a];[0:v]trim=start_frame={gx + NCUT - XF // 2},setpts=PTS-STARTPTS[b];"
      f"[a][b]xfade=transition=fade:duration={XF / FPS:.6f}:offset={(gx + XF // 2 - XF) / FPS:.6f}[v]")
subprocess.run([FF, '-v', 'error', '-y', '-i', f'{R1}/hf/ladder/G11.mov', '-filter_complex', fc, '-map', '[v]', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', f'{R3}/G11_cut.mov'], check=True)
# ---- data shifted after the cut
sh = lambda x: x - DT if x > A0 + 0.01 else x
P = json.load(open(f'{B}/round2/plan_r2.json'))
for p in P:
    if p['b'] > A0: p['b'] = round(sh(p['b']), 3)
    if p['a'] > A0: p['a'] = round(sh(p['a']), 3)
    for key in ('highlight', 'band'):
        for h in p.get(key) or []:
            if h['at'] > A0 + 1: h['at'] = round(sh(h['at']), 3)
json.dump(P, open(f'{R3}/plan_r3.json', 'w'), indent=1)
W = json.load(open(f'{R1}/film_words.json')); W3 = []
for w in W:
    if A0 - 0.02 <= w['t0'] < A1 - 0.3: continue                        # the false start (its medium.en words, incl. the stretched "protein")
    W3.append(dict(w, t0=round(sh(w['t0']), 3), t1=round(sh(w['t1']), 3)))
# medium.en had merged the false start and the clean line ("protein" 434.54-439.70): put the clean words back from the delivered whisper
json.dump(W3, open(f'{R3}/film_words_r3.json', 'w'), indent=1)
E = json.load(open(f'{R1}/edl_r1.json'))
for e in E:
    for k in ('film_in', 'film_out'):
        if e[k] > A0: e[k] = round(sh(e[k]), 4)
json.dump(E, open(f'{R3}/edl_r3.json', 'w'), indent=1)
M = json.load(open(f'{R3}/film_manifest.json'))
for m in M:
    if m['b'] > A0: m['b'] = round(sh(m['b']), 3)
    if m['id'] == 'G11': m['mov'] = f'{R3}/G11_cut.mov'
json.dump(M, open(f'{R3}/film_manifest_cut.json', 'w'), indent=1)
bj = json.load(open(f'{O}/picture_v3.build.json')); runs = []
for rr in bj['runs']:
    a, z = rr['o0'], rr['o1']
    a = a if a < X else max(X, a - NCUT); z = z if z <= X else max(X, z - NCUT)
    if a < z: runs.append(dict(rr, o0=a, o1=z))
json.dump(dict(bj, frames=N - NCUT, g1=N - NCUT, runs=runs, hair=[h for h in bj['hair'] if h[0] < X]), open(f'{O}/picture.build.json', 'w'))
json.dump(dict(audio_cut=[A0, round(A1, 4)], picture_cut_frames=[X, X + NCUT], dissolve_frames=XF, new_frames=N - NCUT, new_seconds=round((N - NCUT) / FPS, 4)), open(f'{R3}/cut_r3.json', 'w'), indent=1)
print('picture', N - NCUT, 'frames =', round((N - NCUT) / FPS, 4), 's; audio cut', A0, round(A1, 3))
