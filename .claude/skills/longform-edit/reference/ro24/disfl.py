"""Disfluency check of chosen windows (VIDEO-RULES 2026-10-20: stumbles inside a kept take get fixed): medium.en with a
disfluency prompt, condition_on_previous_text False, word timestamps; prints words with long durations and gaps."""
import sys, json, subprocess, whisper, os
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
os.environ['PATH'] = os.path.dirname(FF) + ':' + os.environ['PATH']
m = whisper.load_model('medium.en')
out = {}
for spec in sys.argv[1:]:
    a, b = map(float, spec.split(':'))
    tmp = f'/tmp/_disfl_{os.getpid()}.wav'
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-t', str(b - a), '-i', '/Volumes/Expansion/_edit_work/RO-24/round1/audio/lav_full.wav', '-ar', '16000', '-ac', '1', tmp], check=True)
    r = m.transcribe(tmp, word_timestamps=True, language='en', condition_on_previous_text=False, initial_prompt='Um, uh, so, I- I mean, pri- priority, the- the')
    ws = [(x['word'].strip(), round(x['start'] + a, 2), round(x['end'] + a, 2)) for s in r['segments'] for x in s['words']]
    out[spec] = ws
    line = []
    prev = None
    for w, t0, t1 in ws:
        g = t0 - prev if prev is not None else 0
        line.append((f'<{g:.2f}> ' if g > .35 else '') + w + (f'{{{t1-t0:.2f}}}' if t1 - t0 > .5 else ''))
        prev = t1
    print(f'== {spec}\n' + ' '.join(line))
json.dump(out, open('/Volumes/Expansion/_edit_work/RO-24/round1/audio/disfl.json', 'w'), indent=0)
