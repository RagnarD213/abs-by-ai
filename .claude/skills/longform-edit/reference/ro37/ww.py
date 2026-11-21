"""ww.py ROLL T0 T1 : words with start times in a window (medium.en if present, else the base.en index)."""
import json, sys, os
r, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; p = f"{W}/words_{r}.json"
if os.path.exists(p):
    d = json.load(open(p)); d = d[0] if isinstance(d[0], list) else d; ws = [(x["t"], x["e"], x["w"]) for x in d]
else:
    d = json.load(open(f"/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/footage-index/shoot-20261023/{r}.transcript.json"))["words"]; ws = [(x["start"], x["end"], x["word"]) for x in d]
print(" ".join(f"{t:.2f}{w.strip()}" for t, e, w in ws if a <= t <= b))
