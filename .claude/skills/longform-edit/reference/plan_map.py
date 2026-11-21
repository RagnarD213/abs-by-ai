#!/usr/bin/env python3
"""REV1 planning map: output timeline, chip coverage, and every gap > 30s.
Prints what Dan is SAYING in each gap so inserts can be chosen editorially."""
import json, importlib.util, sys
from pathlib import Path
B = Path("/Volumes/Extreme/_edit_work/spraytan")
edl = json.load(open(B/"edl.json")); R = edl["ranges"]
spec = importlib.util.spec_from_file_location("c", B/"chips.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
W = [w for s in json.load(open(B/"C1512.whisper.json"))["segments"] for w in s.get("words",[])]

offs, acc = [], 0.0
for r in R: offs.append(acc); acc += round(r["end"]-r["start"], 3)
TOTAL = acc
def s2o(t):
    for r, o in zip(R, offs):
        if r["start"] <= t < r["end"]: return round(o + (t - r["start"]), 2)
    return None
def o2s(t):
    for r, o in zip(R, offs):
        d = round(r["end"]-r["start"],3)
        if o <= t < o+d: return round(r["start"] + (t-o), 2)
    return None
def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"
def text_at(o0, o1):
    s0, s1 = o2s(o0), o2s(max(o0, o1-0.01))
    out=[]
    for r,o in zip(R,offs):
        d=round(r["end"]-r["start"],3)
        a=max(o,o0); b=min(o+d,o1)
        if b<=a: continue
        sa, sb = r["start"]+(a-o), r["start"]+(b-o)
        out += [w["word"].strip() for w in W if sa <= w["start"] < sb]
    return " ".join(out)

print(f"TOTAL {mmss(TOTAL)} ({TOTAL:.2f}s)  {len(R)} ranges\n")
print("=== OUTPUT TIMELINE (beats) ===")
for r,o in zip(R,offs):
    d=round(r["end"]-r["start"],3)
    print(f"{mmss(o):>8s} - {mmss(o+d):>8s} ({d:6.2f}s) {r['beat']:24s} src {r['start']:7.2f}")
DUR=6.4
chips=[]
for key, st, eye, ttl in m.CHIPS:
    o=s2o(st)
    if o is None: print(f"WARN chip {key} src {st} dropped"); continue
    chips.append({"key":key,"start":o,"end":round(o+DUR,2),"title":ttl})
chips.sort(key=lambda c:c["start"])
print("\n=== EXISTING CHIP COVERAGE (26) ===")
for c in chips: print(f"{mmss(c['start']):>8s} - {mmss(c['end']):>8s}  {c['key']:10s} {c['title']}")
print("\n=== GAPS with no chip (>20s listed; >30s = MUST FILL) ===")
evts=[(c["start"],c["end"]) for c in chips]
cur=0.0; gaps=[]
for a,b in evts:
    if a-cur > 20: gaps.append((cur,a))
    cur=max(cur,b)
if TOTAL-cur > 20: gaps.append((cur,TOTAL))
for a,b in gaps:
    flag = "  *** >30s" if b-a>30 else ""
    print(f"\n--- GAP {mmss(a)} - {mmss(b)}  ({b-a:.1f}s){flag}")
    txt=text_at(a,b)
    print("   ", txt[:900])
