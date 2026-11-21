"""Word-timed transcripts of the downloaded interview clips (small.en, word timestamps) -> clips/src/<name>.words.json + printout."""
import sys, json, whisper
D = '/Volumes/Expansion/_edit_work/RO-24/round3/clips/src'
m = whisper.load_model('small.en')
for n in sys.argv[1:]:
    r = m.transcribe(f'{D}/{n}.mp4', word_timestamps=True, language='en', condition_on_previous_text=False)
    W = [dict(w=w['word'].strip(), t0=round(w['start'], 2), t1=round(w['end'], 2)) for s in r['segments'] for w in s['words']]
    json.dump(W, open(f'{D}/{n}.words.json', 'w'))
    print('##', n)
    for s in r['segments']: print(f"  {s['start']:6.2f}-{s['end']:6.2f} {s['text'].strip()}")
