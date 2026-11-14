"""DS-41 R1: medium.en word timestamps on the Kevin James clip (JRE Clips tX5ZQ8rfHzY) and on C1730's watch, scripted and
off-the-cuff ranges (lav, left channel); plus the 10 ms level map of the lav over the whole section (audio/takes_db10ms.npy)."""
import whisper, json, subprocess, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
P = 'Kevin James, Joe Rogan, cheat day, trainer, you can\'t outwork a bad diet.'
JOBS = [('clip', str(W/'src/kevin_full.mkv'), 25.0, 60.0, 'pan=mono|c0=0.5*c0+0.5*c1', P),
        ('watch', SRC, 1590.0, 78.0, 'pan=mono|c0=c0', P),
        ('scripted', SRC, 1664.0, 64.0, 'pan=mono|c0=c0', "Um, uh, so, Kevin James's trainer is right. And here's why. 500 calories a day, 3,000 calories, cheat day, cheat meal."),
        ('offcuff', SRC, 1724.0, 82.0, 'pan=mono|c0=c0', 'Um, uh, so, Kevin James and his trainer are absolutely right about this. Cheat day, ch- cheat meal, 3,000 calorie deficit.')]
T0, D = 1590.0, 216.0
raw = subprocess.run([F, '-nostdin', '-v', 'error', '-ss', str(T0), '-i', SRC, '-t', str(D), '-map', '0:a:0', '-af', 'pan=mono|c0=c0', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32); n = len(x)//480; db = 10*np.log10((x[:n*480].reshape(n, 480)**2).mean(1) + 1e-12)
np.save(W/'audio/takes_db10ms.npy', db.astype(np.float32)); open(W/'audio/takes_db10ms.t0', 'w').write(str(T0))
np.save(W/'audio/takes_48k.npy', x); print('level map', n, 'bins', flush=True)
m = whisper.load_model('medium.en')
for name, src, t0, d, pan, prompt in JOBS:
    wav = W/f'audio/{name}16.wav'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', str(t0), '-i', src, '-t', str(d), '-map', '0:a:0', '-af', pan, '-ar', '16000', str(wav)], check=True)
    r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0, condition_on_previous_text=False, initial_prompt=prompt)
    ws = [dict(w=x['word'].strip(), t=round(x['start'] + t0, 3), e=round(x['end'] + t0, 3), p=round(x.get('probability', 0), 2)) for s in r['segments'] for x in s['words']]
    (W/f'audio/{name}_words.json').write_text(json.dumps(ws, indent=1))
    print('==', name, r['text'], flush=True)
