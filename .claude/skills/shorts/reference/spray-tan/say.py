#!/usr/bin/env python3
"""Print the exact Whisper word text in a time window - the search space for phrase anchors."""
import json,sys
w=json.load(open('work/words.json'))['chunks']
a,b=float(sys.argv[1]),float(sys.argv[2])
out=[x['text'] for x in w if x['timestamp'][1]>a and x['timestamp'][0]<b]
print(f"[{a:.0f}-{b:.0f}] "+''.join(out).strip())
