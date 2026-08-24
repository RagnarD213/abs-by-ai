#!/usr/bin/env python3
"""Assert Dan's rev1 rule: no window longer than 30s with no clip and no graphic.
Also asserts no full-frame insert covers a J2 chip."""
import json, importlib.util
from pathlib import Path
B = Path("/Volumes/Extreme/_edit_work/spraytan")
s = importlib.util.spec_from_file_location("i", B/"inserts.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
chips = json.load(open(B/"chip_timings.json"))
edl = json.load(open(B/"edl.json"))
TOTAL = round(sum(round(r["end"]-r["start"],3) for r in edl["ranges"]), 3)
ins = [(a, a+d, k, key) for a, d, k, key, _ in m.INSERTS]
def mm(t): return f"{int(t//60)}:{t%60:05.2f}"
bad = [(c["key"], key) for c in chips for (a,b,k,key) in ins if k in ("clip","photo") and a < c["end"] and b > c["start"]]
print("inserts hiding a chip:", bad or "none")
evts = sorted([(c["start"], c["end"]) for c in chips] + [(a,b) for a,b,_,_ in ins])
cur, gaps = 0.0, []
for a, b in evts:
    if a - cur > 0: gaps.append((cur, a))
    cur = max(cur, b)
if TOTAL - cur > 0: gaps.append((cur, TOTAL))
over = [(a,b) for a,b in gaps if b-a > 30]
print(f"total {mm(TOTAL)}  events {len(evts)}  covered {sum(b-a for a,b in evts):.0f}s "
      f"({100*sum(b-a for a,b in evts)/TOTAL:.0f}%)")
print("longest uncovered gaps:")
for a,b in sorted(gaps, key=lambda g:-(g[1]-g[0]))[:6]: print(f"   {mm(a)} - {mm(b)}  {b-a:.1f}s")
print("GAPS OVER 30s:", [(mm(a),mm(b),round(b-a,1)) for a,b in over] or "NONE  ** rule satisfied **")
