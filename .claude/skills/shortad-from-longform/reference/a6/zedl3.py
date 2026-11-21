#!/usr/bin/env python3
"""Clean the bridged EDL: trim frames that are INSERT frames (per-frame r < 0.5 at the segment's offset -- a talk
range that ran one frame past his hard cut into the next clip), and drop segments that do not match at all
(rmed < 0.8: the fit's false positive inside the beach clip). Rewrites edl_picture.json."""
import json
E = json.load(open('edl_picture.json')); P = json.load(open('pic.json'))
SPIKE = [89,156,216,327,340,353,364,372,373,749,750,1180,1284,1400,1509,1510,1678,1808,1826,1999,2000,2430,2610,2748,
         2792,2832,2970,2971,3225,3226,3478,3618,3791,4048,4049,4291,4530,4568,4919,5132,5294,5295,5477,5675,5758,5759,5893]
INSERT_STARTS = {156,216,327,1180,1284,1509,1808,2430,2748,2792,2832,3478,3618,4291,4530,4919,5477,5893}   # talk -> insert cuts
out = []
for s in E:
    if s['rmed'] < 0.8: print('drop', s['t0'], s['t1'], s['rmed']); continue
    n0, n1 = s['n0'], s['n1']
    for c in INSERT_STARTS:
        if n0 < c < n1: n1 = c                           # never run past his cut into an insert
    fr = s['framing'][:n1-s['n0']]
    s.update(n1=n1, t1=round(n1/24,4), framing=fr)
    out.append(s)
json.dump(out, open('edl_picture.json','w'))
for s in out: print(f"{s['t0']:8.3f}-{s['t1']:8.3f}  n{s['n0']}-{s['n1']}  off {s['off']:+.3f}")
