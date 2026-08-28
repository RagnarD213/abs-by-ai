#!/usr/bin/env python3
"""Word-level transcription of the clean supplements master.

⚠ whisper.transcribe(path) shells out to a bare `ffmpeg` on PATH, which does not exist on
this Mac (the project ships its own static binary at Media/video_edit/bin/ffmpeg). Load the
already-extracted 16 kHz mono WAV into a float32 array and hand Whisper the ARRAY instead.

Two passes: /ad-edit found that Whisper's default pass can silently DROP a whole run of
speech and emit one word in its place, invisibly. The source here is an already-cut edit so
the risk is lower than on a raw roll, but the orphan scan is cheap insurance.
"""
import json, time, wave
import numpy as np, whisper

w = wave.open('work/audio16k.wav')
assert w.getframerate() == 16000 and w.getnchannels() == 1
audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
w.close()
print(f'{len(audio)/16000:.1f}s of audio loaded', flush=True)

t0 = time.time()
m = whisper.load_model('medium.en')
print(f'model loaded in {time.time()-t0:.0f}s', flush=True)

for tag, cond in (('a', True), ('b', False)):
    t = time.time()
    r = m.transcribe(audio, language='en', word_timestamps=True,
                     condition_on_previous_text=cond, verbose=False)
    json.dump(r, open(f'work/whisper-{tag}.json', 'w'))
    nw = sum(len(s.get('words', [])) for s in r['segments'])
    print(f'pass {tag} (cond={cond}): {len(r["segments"])} segments, {nw} words, '
          f'{time.time()-t:.0f}s', flush=True)
print('DONE', flush=True)
