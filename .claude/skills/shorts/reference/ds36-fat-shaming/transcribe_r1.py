"""DS-36 R1: medium.en word timestamps on the Bill Maher clip and on C1730's watch, scripted and off-the-cuff ranges (lav, left channel)."""
import whisper, json, subprocess
from pathlib import Path
W = Path(__file__).resolve().parents[1]
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
P = 'Bill Maher, fat shaming, obesity, shame, seatbelts, littering.'
JOBS = [('clip', str(W/'src/maher_full.mkv'), 330.0, 55.0, 'pan=mono|c0=0.5*c0+0.5*c1', P),
        ('watch', SRC, 518.0, 46.0, 'pan=mono|c0=c0', P),
        ('scripted', SRC, 560.0, 72.0, 'pan=mono|c0=c0', 'Um, uh, so, Bill Maher is right here. Fat shaming is good. Being over fat, vacuums, sixpackabs.com.'),
        ('offcuff', SRC, 630.0, 90.0, 'pan=mono|c0=c0', 'Um, uh, so, Bill Maher is right. Fat shaming, sh- shame, weigh in, sixpackabs.com.')]
m = whisper.load_model('medium.en')
for name, src, t0, d, pan, prompt in JOBS:
    wav = W/f'audio/{name}16.wav'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', str(t0), '-i', src, '-t', str(d), '-map', '0:a:0', '-af', pan, '-ar', '16000', str(wav)], check=True)
    r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0, condition_on_previous_text=False, initial_prompt=prompt)
    ws = [dict(w=x['word'].strip(), t=round(x['start'] + t0, 3), e=round(x['end'] + t0, 3), p=round(x.get('probability', 0), 2)) for s in r['segments'] for x in s['words']]
    (W/f'audio/{name}_words.json').write_text(json.dumps(ws, indent=1))
    print('==', name, r['text'], flush=True)
