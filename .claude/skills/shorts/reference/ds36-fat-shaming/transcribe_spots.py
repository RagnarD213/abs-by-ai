"""DS-36 R1 spot pass: every kept word over ~0.5 s and every join, re-transcribed with a disfluency prompt (VIDEO-RULES 2026-10-20)."""
import whisper, json, subprocess
from pathlib import Path
W = Path(__file__).resolve().parents[1]
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
SPOTS = [574.6, 580.6, 604.4, 607.4, 614.4, 625.2, 628.9, 646.4, 657.6, 658.4, 664.6, 669.2, 673.2, 682.2, 691.4, 705.0, 714.6]
m = whisper.load_model('medium.en'); out = {}
for t in SPOTS:
    a = t - 1.2; wav = W/'audio'/f'spot_{t:.1f}.wav'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-i', SRC, '-t', '3.0', '-map', '0:a:0', '-af', 'pan=mono|c0=c0', '-ar', '16000', str(wav)], check=True)
    r = m.transcribe(str(wav), language='en', fp16=False, word_timestamps=True, temperature=0, condition_on_previous_text=False, initial_prompt='Um, uh, I- I mean, sh- shame, pri- priority, the the.')
    out[f'{t:.1f}'] = [(x['word'].strip(), round(x['start'] + a, 2), round(x['end'] + a, 2)) for s in r['segments'] for x in s['words']]
    print(t, r['text'], flush=True)
(W/'audio/spots.json').write_text(json.dumps(out, indent=1))
