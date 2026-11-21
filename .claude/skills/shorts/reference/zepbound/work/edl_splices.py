#!/usr/bin/env python3
"""Exact picture-splice positions in the clean master, from the source EDL.

Far better than a 320x180 scene detector: the edit's own range list says precisely where
every cut is. Two cumulative models are computed because render.py rounds each segment to
whole FRAMES, and the skill records that this rounding accumulated +0.65s over 44 ranges on
the spray-tan build. The frame model is the one to trust; the float model is printed beside
it so the drift is visible rather than assumed.
"""
import json
from fractions import Fraction
EDL = json.load(open("/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/edl.json"))
fps = float(Fraction(EDL['fps']))
tf = tx = 0.0
rows = []
for i, r in enumerate(EDL['ranges']):
    d = r['end'] - r['start']
    nf = round(d * fps)
    rows.append({'i': i, 'beat': r['beat'], 'srcStart': r['start'], 'srcEnd': r['end'],
                 'outFloat': round(tx, 3), 'outFrame': round(tf, 3), 'dur': round(d, 3)})
    tx += d
    tf += nf / fps
print(f"{len(rows)} ranges; total float {tx:.3f}s  frame-quantised {tf:.3f}s  "
      f"(master is 1827.751s)  drift {tf-tx:+.3f}s")
json.dump(rows, open('work/edl_splices.json', 'w'), indent=1)
for r in rows:
    print(f"  {r['i']:2d} out {r['outFrame']:8.3f}  ({r['outFrame']/60:5.2f}m)  "
          f"{r['dur']:6.2f}s  {r['beat']}")
