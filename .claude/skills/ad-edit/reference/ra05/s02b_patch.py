#!/usr/bin/env python3
"""RA-05: correct four Whisper word times from the 5 ms envelope (ad-edit RA-07 lesson 3: Whisper stretches the first
word of a phrase back across the silence before it). Idempotent: keeps the untouched pass in tx/c1664.whisper.orig.json."""
import json, os, shutil
P = "tx/c1664.whisper.json"; O = "tx/c1664.whisper.orig.json"
if not os.path.exists(O): shutil.copy(P, O)
d = json.load(open(O))
FIX = [  # (word, whisper start within, new start, new end or None)   onset read from env.json in 40 ms steps
 ("Seriously,", (216.5, 216.7), 217.22, None),     # pause 216.58-217.22 after "life."
 ("it'll",      (245.7, 245.9), 247.22, None),     # the restart; the first attempt ends "lose and" at 245.80
 ("So",         (283.3, 283.5), 283.34, 283.46),   # zero-length in Whisper
 ("Tap",        (292.8, 293.0), 293.17, None),     # breath 292.7-293.0, the word starts 293.18
]
n = 0
for s in d["segments"]:
    for w in s["words"]:
        for word, (lo, hi), ns, ne in FIX:
            if w["word"].strip() == word and lo <= w["start"] <= hi:
                print(f"  {word!r} {w['start']:.2f}-{w['end']:.2f} -> {ns:.2f}-{(ne or w['end']):.2f}")
                w["start"] = ns
                if ne: w["end"] = ne
                n += 1
assert n == len(FIX), n
# word TEXT fixes (captions print these): Whisper heard "Abs by AI" as "Addis by AI"; the restart word opens a sentence
TXT = {("Addis", 266.0, 270.0): " Abs", ("it'll", 247.0, 247.4): " It'll"}
m = 0
for s in d["segments"]:
    for w in s["words"]:
        for (word, lo, hi), new in TXT.items():
            if w["word"].strip() == word and lo <= w["start"] <= hi:
                print(f"  text {w['word']!r} -> {new!r} at {w['start']:.2f}"); w["word"] = new; m += 1
assert m == len(TXT), m
json.dump(d, open(P, "w"), indent=1)
