#!/usr/bin/env python3
"""What the DELIVERED file actually says (Whisper small on the delivered audio) -> <dir>/transcript_words.json, for the
gate's words rows. The 9:16 and the 1:1 of one length carry the same audio, so one transcript serves both."""
import json, os, sys, whisper
vid = sys.argv[1]; out = sys.argv[2]
r = whisper.load_model('small').transcribe(vid, word_timestamps=False, language='en')
tw = [dict(w=w) for seg in r['segments'] for w in seg['text'].split()]
json.dump(tw, open(out, 'w')); print(out, len(tw), 'words')
