"""DS-78 R1 take analysis on C1882 243-334 s: lav ch0 level profile (0.05 s) and disfluency-prompted Whisper per window."""
from pathlib import Path
import subprocess, json, os, sys, numpy as np
from scipy.io import wavfile
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = R/'Media/video_edit/bin/ffmpeg'
S = '/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/C1882.MP4'; E = W/'evidence/takes'; E.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
renderq.hold_until_exit('DS-78 R1 take analysis', pool='light', group='DS-78')
os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
T0 = 243.0; wav = E/'range-48k.wav'; ff(['-ss', T0, '-i', S, '-t', 92, '-vn', '-af', 'pan=mono|c0=c0', '-ar', 48000, '-c:a', 'pcm_s16le', wav])
sr, x = wavfile.read(wav); x = x/32768.; st = int(0.05*sr)
lv = [round(float(20*np.log10(np.sqrt(np.mean(x[i:i+st]**2))+1e-9)), 1) for i in range(0, len(x)-st, st)]
json.dump(dict(t0=T0, step=0.05, rms_db=lv), open(E/'levels.json', 'w'))
# quiet runs (< -44 dBFS) of 0.15 s or more
runs = []; s = None
for i, v in enumerate(lv + [0]):
    if v < -44 and s is None: s = i
    if v >= -44 and s is not None:
        if (i-s)*0.05 >= 0.15: runs.append([round(T0+s*0.05, 2), round(T0+i*0.05, 2)])
        s = None
json.dump(runs, open(E/'quiet-runs.json', 'w')); print('QUIET', runs)
import whisper
m = whisper.load_model('small')
wins = {'hook': (268.2, 277.95), 'seat': (277.9, 286.6), 'stretch1': (286.6, 296.95), 'risk2': (297.2, 302.6), 'far2': (303.7, 306.65),
        'next': (306.6, 314.5), 'four': (314.6, 315.9), 'sets': (317.3, 329.2), 'cta': (329.0, 333.3)}
out = {}
for k, (a, b) in wins.items():
    p = E/f'{k}.wav'; ff(['-ss', a, '-i', S, '-t', round(b-a, 2), '-vn', '-af', 'pan=mono|c0=c0', '-ar', 16000, p])
    r = m.transcribe(str(p), word_timestamps=True, language='en', condition_on_previous_text=False, initial_prompt='Um, uh, so, I- I set the, the seat, chest flies, tearing a pec.')
    ws = [dict(w=w['word'].strip(), s=round(w['start']+a, 2), e=round(w['end']+a, 2)) for sg in r['segments'] for w in sg['words']]
    out[k] = dict(window=[a, b], text=' '.join(w['w'] for w in ws), words=ws); print(k, out[k]['text'], flush=True)
    ff(['-i', p, '-c:a', 'libmp3lame', '-b:a', '128k', E/f'{k}.mp3'])
json.dump(out, open(E/'disfluency-asr.json', 'w'), indent=1); print('TAKES_DONE')
