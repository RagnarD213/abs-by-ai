#!/usr/bin/env python3
# ⚠ SUPERSEDED BY `.claude/skills/_shared/deliver/gate.py` (2026-09-11, Phase 1 of
#   Handoffs/handoff-20260911-video-quality-engine.md). Its rows are folded into the shared gate,
#   with every bound moved to `_shared/deliver/formats.py` beside the file and the date it was
#   measured on. DO NOT add a check here -- add it there, or it lands in one of six pipelines and
#   the other five keep the bug.
#   ⚠ STILL ON DISK ON PURPOSE: three sessions were mid-build against these scripts when the shared
#   gate landed (ad1-sq, ad2-sq, ad3-vert, ad4-vert, ad5-vert). It is deleted once those deliver,
#   and it still carries rows the shared gate has not absorbed yet -- framing is Phase 2, the watch
#   pass Phase 3. RUN BOTH until those land.
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
