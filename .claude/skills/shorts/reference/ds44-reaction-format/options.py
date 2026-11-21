"""DS-44 R1 options for the round 1 page.
Colour: one matching frame of the final key (cache c2_A, 'Your stopping point is just set too high', T window), the three
looks of the approved DS-40 grade module: B Warm Vivid = Dan's pick for Bill Maher on this set (recommended, in the film),
A Natural, C Bold.
Voice: one continuous spoken passage in the film (from "You already stopped somewhere" 8.6 s, speech in the first 0.5 s, no
pause over 1.5 s: measured below), both chains level matched by the chain (-14.1 LUFS), plus the untreated lav for reference.
Alternative take: the off-the-cuff reaction (C1730 2325.0-2391.0), raw camera (not keyed), with its own lav, for comparison."""
import sys, subprocess, json, numpy as np, cv2, re
from pathlib import Path
W = Path(__file__).resolve().parents[1]; RC = Path(__file__).resolve().parent; sys.path.insert(0, str(RC))
import assemble as AS
from grade import LOOKS
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
edl = json.load(open(W/'edl.json')); words = json.load(open(W/'words_out.json')); shots = json.load(open(W/'shots.json'))
O = W/'options'; O.mkdir(exist_ok=True)
w0 = next(w for w in words if w['w'].lower() == 'your' and w['piece'] == 'A' and words[words.index(w)+1]['w'] == 'stopping')
g = AS.fr(w0['t0'] + 0.6); s = next(x for x in shots if x['n0'] <= g < x['n1']); assert s['kind'] == 'talk', s['id']
for look in ('B_warmvivid', 'A_natural', 'C_bold'):
    AS.LOOK = look; f = AS.render(g)
    cv2.imwrite(str(O/f'colour-{look}.jpg'), cv2.cvtColor(AS.u8(f[200:1500, 90:990]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
# voice window, measured on the lav track (voice file time = film time - transition start)
a = next(w for w in words if w['w'].lower() == 'you' and w['piece'] == 'A' and words[words.index(w)+1]['w'] == 'already')['t0']
t0 = a - edl['tr']['film0'] - 0.05; D = 8.6
raw = subprocess.check_output([F, '-v', 'error', '-ss', f'{t0:.3f}', '-i', str(W/'lav.wav'), '-t', str(D), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'])
x = np.frombuffer(raw, np.int16).astype(np.float32)/32768; k = 160; e = 20*np.log10(np.sqrt((x[:len(x)//k*k].reshape(-1, k)**2).mean(1)) + 1e-9)
sp = e > (np.median(e) - 6); first = np.argmax(sp)*0.01; gaps = []; run = 0
for v in sp:
    run = 0 if v else run + 1; gaps.append(run)
print('voice window speech starts', round(first, 2), 's; longest pause', round(max(gaps)*0.01, 2), 's')
assert first < 0.5 and max(gaps)*0.01 < 1.5
for name in ('house_bass15', 'balanced'):
    subprocess.run([F, '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-i', str(W/f'voice-{name}.wav'), '-t', str(D), '-c:a', 'aac', '-b:a', '192k', str(O/f'voice-{name}.m4a')], check=True)
subprocess.run([F, '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-i', str(W/'lav.wav'), '-t', str(D), '-af', 'loudnorm=I=-14', '-c:a', 'aac', '-b:a', '192k', str(O/'voice-untreated.m4a')], check=True)
# the off-the-cuff take, raw camera, centre vertical window above the laptop, its own lav level-normalised
SRC = edl['pieces'][0]['source']
subprocess.run([F, '-v', 'error', '-y', '-ss', '2325.0', '-i', SRC, '-t', '66.0', '-map', '0:v', '-map', '0:a:0',
                '-vf', 'scale=in_color_matrix=bt709:in_range=tv:out_range=tv,crop=1960:3484:100:0,scale=540:960', '-af', 'pan=mono|c0=c0,loudnorm=I=-14',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '22', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(O/'alt-off-the-cuff-take.mp4')], check=True)
print('OPTIONS DONE')
