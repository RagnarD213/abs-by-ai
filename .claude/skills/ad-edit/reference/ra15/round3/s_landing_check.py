#!/usr/bin/env python3
"""RA-15 round 3: land-then-hold check (VIDEO-RULES 2026-10-03). Crops are fixed per hold; this measures how far his head
drifts from each hold's fixed centre, against the 3.3 % of crop width at which the standard method would start to follow."""
import json, sys
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import landing
B = json.load(open("beats.json")); T = json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"]
lv = json.load(open("framing_choice.json")); FPS = 30000/1001
rows, ns, hs, cs, segs = [], [], [], [], []
for p in B["punch"]:
    a, b = p["beat"]; cw = lv[p["level"]][0]
    s = sorted([x for x in T if a <= x["t"] <= b], key=lambda x: x["t"])
    off = [abs(x["cx"] - p["cx"]) for x in s]
    rows.append(dict(beat=[a, b], level=p["level"], crop_w=cw, n=len(s), max_off_px=round(max(off), 1),
                     max_off_pct=round(100*max(off)/cw, 2), over_3_3=max(off)/cw > 0.033))
    for x in s: ns.append(int(round(x["t"]*FPS))); hs.append(x["cx"]); cs.append(p["cx"])
    segs.append(dict(cut_in=a, cut_out=b))
o = np.argsort(ns); ns, hs, cs = np.array(ns)[o], np.array(hs)[o], np.array(cs)[o]
st = landing.motion_stats(ns, hs, cs, segs, lv["NEAR"][0])
json.dump(dict(holds=rows, motion_stats=st), open("round3/landing_check.json", "w"), indent=1)
for r in rows: print(r)
print(st)
