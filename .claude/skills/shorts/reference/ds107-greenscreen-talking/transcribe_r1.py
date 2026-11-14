"""DS-107 R1: medium.en word timestamps on C1908 B08 range (lav a:0 c0) + 10 ms level map (audio/takes_db10ms.npy)."""
import whisper, json, subprocess, numpy as np, time
from pathlib import Path
W = Path(__file__).resolve().parents[1]
F = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = '/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4'
P = ("Your metabolism at 45 is the same as it was at 25. A study published in Science in 2021 looked at 6,421 people in 29 countries. "
     "Um, uh, so, a career, a mortgage, kids. SixPackAbs.com.")
T0, D = 80.0, 179.0
t = time.time()
raw = subprocess.run([F, '-nostdin', '-v', 'error', '-ss', str(T0), '-i', SRC, '-t', str(D), '-map', '0:a:0', '-af', 'pan=mono|c0=c0', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32); n = len(x)//480; db = 10*np.log10((x[:n*480].reshape(n, 480)**2).mean(1) + 1e-12)
np.save(W/'audio/takes_db10ms.npy', db.astype(np.float32)); open(W/'audio/takes_db10ms.t0', 'w').write(str(T0))
np.save(W/'audio/takes_48k.npy', x); print('level map', n, 'bins', round(time.time()-t, 1), flush=True)
m = whisper.load_model('medium.en')
wav = W/'audio/talk16.wav'
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', str(T0), '-i', SRC, '-t', str(D), '-map', '0:a:0', '-af', 'pan=mono|c0=c0', '-ar', '16000', str(wav)], check=True)
r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0, condition_on_previous_text=False, initial_prompt=P)
ws = [dict(w=x['word'].strip(), t=round(x['start'] + T0, 3), e=round(x['end'] + T0, 3), p=round(x.get('probability', 0), 2)) for s in r['segments'] for x in s['words']]
(W/'audio/talk_words.json').write_text(json.dumps(ws, indent=1))
print('== TEXT', r['text'], flush=True); print('WALL', round(time.time()-t, 1), flush=True)
