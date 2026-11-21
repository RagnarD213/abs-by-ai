#!/usr/bin/env python3
"""Word-level inspector over C1511.whisper.json.
  python3 w.py find "phrase to find"      -> matches with word index + times
  python3 w.py span 1234 1290             -> every word in that source span, with times
  python3 w.py cut 1234.5 1250.0          -> proposed cut boundaries for deleting that span
"""
import json, sys
from pathlib import Path
BASE = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/invest-health")
W = []
for s in json.load(open(BASE/"C1511.whisper.json"))["segments"]:
    for w in s.get("words", []):
        t = w["word"].strip()
        if t: W.append({"t": t, "s": w["start"], "e": w["end"]})
SIL = json.load(open(BASE/"silences.json"))

def norm(x): return x.lower().strip(".,!?\"'")

cmd = sys.argv[1]
if cmd == "find":
    q = [norm(x) for x in sys.argv[2].split()]
    lo = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    hi = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
    for i in range(len(W)-len(q)+1):
        if all(norm(W[i+k]["t"]) == q[k] for k in range(len(q))) and lo <= W[i]["s"] <= hi:
            print(f"idx {i}  {W[i]['s']:.2f}-{W[i+len(q)-1]['e']:.2f}  "
                  f"| ...{' '.join(x['t'] for x in W[max(0,i-6):i])} [["
                  f"{' '.join(x['t'] for x in W[i:i+len(q)])}]] "
                  f"{' '.join(x['t'] for x in W[i+len(q):i+len(q)+6])}...")
elif cmd == "span":
    a, b = float(sys.argv[2]), float(sys.argv[3])
    for i, w in enumerate(W):
        if a <= w["s"] <= b:
            d = w["e"] - w["s"]
            mark = "  <<STRETCHED" if d > 0.8 else ("  <<ZEROLEN" if d <= 0.001 else "")
            print(f"{i:5d} {w['s']:9.3f}-{w['e']:8.3f} ({d:5.3f}) {w['t']!r}{mark}")
elif cmd == "sil":
    a, b = float(sys.argv[2]), float(sys.argv[3])
    for s, e in SIL:
        if e >= a and s <= b:
            print(f"  silence {s:9.3f}-{e:8.3f}  ({e-s:.3f}s)")
