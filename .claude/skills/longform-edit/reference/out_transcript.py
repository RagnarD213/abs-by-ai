#!/usr/bin/env python3
"""Sentence-level transcript on the OUTPUT timeline - used to time inserts to the word."""
import json
from pathlib import Path
B = Path("/Volumes/Seagate 4TB/_edit_work/spraytan")
edl = json.load(open(B/"edl.json")); R = edl["ranges"]
W = [w for s in json.load(open(B/"C1512.whisper.json"))["segments"] for w in s.get("words",[])]
offs, acc = [], 0.0
for r in R: offs.append(acc); acc += round(r["end"]-r["start"], 3)
mapped=[]
for r,o in zip(R,offs):
    for w in W:
        mid=(w["start"]+w["end"])/2
        if r["start"] <= mid < r["end"]:
            mapped.append((round(o+(w["start"]-r["start"]),2), w["word"].strip()))
mapped.sort()
def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"
cur=[]; start=None
for t,txt in mapped:
    if start is None: start=t
    cur.append(txt)
    if txt.endswith(('.','!','?')):
        print(f"{mmss(start):>9s}  {' '.join(cur)}")
        cur=[]; start=None
if cur: print(f"{mmss(start):>9s}  {' '.join(cur)}")
