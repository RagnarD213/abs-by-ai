#!/usr/bin/env python3
"""Map SOURCE time (the 538 s graded cut) to TIGHT time (the 433 s re-cut), and back.

Every later pass -- inserts, graphics, captions, chapters -- is authored against the
tight timeline, but the transcript and the beat boundaries are known in source time.
"""
import json
from pathlib import Path
R2 = Path(__file__).parent
P = json.load(open(R2/"plan.json"))
KEEPS = P["keeps"]
DUR = P["dur"]

_OFF = []
acc = 0.0
for a, b in KEEPS:
    _OFF.append(acc); acc += b - a

def s2t(t):
    """source -> tight. Returns None if that moment was cut."""
    for (a, b), o in zip(KEEPS, _OFF):
        if a <= t < b: return round(o + (t - a), 3)
    return None

def s2t_near(t):
    """source -> tight, snapping to the nearest kept moment (never None)."""
    best = None
    for (a, b), o in zip(KEEPS, _OFF):
        if a <= t < b: return round(o + (t - a), 3)
        d = a - t if t < a else t - b
        if best is None or d < best[0]:
            best = (d, round(o + (0 if t < a else b - a), 3))
    return best[1]

def t2s(t):
    for (a, b), o in zip(KEEPS, _OFF):
        if o <= t < o + (b - a): return round(a + (t - o), 3)
    return KEEPS[-1][1]

def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"

if __name__ == "__main__":
    import timeline as T
    words = [{"t": s2t(w["t"]), "e": s2t_near(w["e"]), "w": w["w"], "beat": w["beat"]}
             for w in T.WORDS]
    words = [w for w in words if w["t"] is not None]
    json.dump(words, open(R2/"words_tight.json","w"))
    beats = []
    for b in T.BEATS:
        a2, b2 = s2t_near(b["a"]), s2t_near(b["b"])
        beats.append({"beat": b["beat"], "a": a2, "b": b2, "source": b["source"]})
    json.dump(beats, open(R2/"beats_tight.json","w"), indent=1)
    print(f"tight duration {mmss(DUR)}  ({DUR:.2f}s)   {len(words)} words on the tight timeline\n")
    for b in beats:
        ws=[w for w in words if b["a"]<=w["t"]<b["b"]]
        d=b["b"]-b["a"]
        print(f"{b['beat']:26s} {mmss(b['a']):>7s}-{mmss(b['b']):>7s} {d:6.2f}s  {len(ws):4d} words")
