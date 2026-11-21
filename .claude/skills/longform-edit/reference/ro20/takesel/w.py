"""print medium words with times in windows. usage: w.py t0:t1 ..."""
import json, sys
W = json.load(open("/Volumes/Extreme/_edit_work/ro20/words.json"))["words"]
for spec in sys.argv[1:]:
    a, b = map(float, spec.split(":"))
    print(spec, " ".join(f"{w['word'].strip()}[{w['start']:.2f}-{w['end']:.2f}]" for w in W if w["end"] > a and w["start"] < b))
