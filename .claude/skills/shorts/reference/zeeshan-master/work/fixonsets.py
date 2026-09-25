#!/usr/bin/env python3
"""Correct Whisper word boundaries against MEASURED silence.

Whisper routinely stretches a word across a real pause, so its claimed span can contain, or
begin inside, measured silence. The skill already records the phenomenon ("V6 'the' =
148.28-149.00 hides a measured 148.44-148.63 gap"); on this batch it caused three faults:

  * snapIn walked back past a whole sentence, so short E opened on "...from there."
  * a word straddling a piece boundary failed the caption builder's >50%-overlap test and
    would have been SPOKEN BUT NOT CAPTIONED - the mirror of the zero-duration bug.
  * short B's "you're" was timed 1046.94-1048.82, swallowing the 0.70s hesitation Dan called
    "junk footage in the beginning at 0:01", which hid it from the pause scan.

Three corrections, all bounded so a word can never invert or vanish:
  1. onset inside a gap            -> the word begins at that gap's END
  2. offset inside a gap           -> the word ended at that gap's START
  3. a gap of >=0.25s wholly INSIDE the word -> a word cannot contain a quarter-second of
     silence; its real onset is the end of the gap it swallowed
"""
import json
words = json.load(open('work/words.json'))['chunks']
gaps = json.load(open('work/gaps.json'))

def gap_at(t):
    for g0, g1 in gaps:
        if g0 < t < g1: return (g0, g1)
        if g0 > t: break
    return None

n1 = n2 = n3 = nzero = 0
for w in words:
    s, e = w['timestamp']
    # Zero-duration words carry no span to correct; captions.js gives them a nominal
    # duration, and running them through the logic below would invert them.
    if e - s <= 0.0001:
        nzero += 1
        continue
    g = gap_at(s)
    if g and g[1] < e:
        w['timestamp'][0] = round(g[1], 3); n1 += 1
    else:
        s2, e2 = w['timestamp']
        for g0, g1 in gaps:
            if g0 > e2: break
            if g0 > s2 + 0.02 and g1 < e2 - 0.02 and g1 - g0 >= 0.25:
                w['timestamp'][0] = round(g1, 3); n3 += 1
                break
    s, e = w['timestamp']
    g = gap_at(e)
    if g and g[0] > s:
        w['timestamp'][1] = round(g[0], 3); n2 += 1
    assert w['timestamp'][1] > w['timestamp'][0], w

json.dump({'chunks': words}, open('work/words.json', 'w'))
print(f"onsets moved out of silence {n1}, offsets {n2}, words that had SWALLOWED a pause {n3} "
      f"({len(words)} words, {nzero} zero-duration untouched)")
