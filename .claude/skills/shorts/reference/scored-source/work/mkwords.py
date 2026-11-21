#!/usr/bin/env python3
"""Convert an openai-whisper JSON (either the plain result or the chunked-script output)
into the {chunks:[{text,timestamp:[s,e]}]} shape the shorts pipeline expects."""
import json, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
segs = d['segments'] if isinstance(d, dict) else d
ch = []
for s in segs:
    for w in s.get('words', []):
        ch.append({'text': w['word'], 'timestamp': [round(w['start'], 3), round(w['end'], 3)]})
ch.sort(key=lambda c: c['timestamp'][0])
json.dump({'chunks': ch}, open(out, 'w'))
print(f'{len(ch)} words  {ch[0]["timestamp"][0]:.2f} -> {ch[-1]["timestamp"][1]:.2f}')
