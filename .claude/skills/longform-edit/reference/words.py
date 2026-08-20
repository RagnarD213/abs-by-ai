#!/usr/bin/env python3
"""Print word-level timestamps in a window.  usage: words.py <whisper.json> <t0> <t1>"""
import json,sys
d=json.load(open(sys.argv[1])); t0,t1=float(sys.argv[2]),float(sys.argv[3])
ws=[]
for s in d["segments"]:
    for w in s.get("words",[]):
        if w["end"]>=t0 and w["start"]<=t1: ws.append(w)
line=[]
for w in ws:
    dur=w["end"]-w["start"]
    mark="*" if dur<0.001 else ("~" if dur>0.8 else "")
    line.append(f"{w['word'].strip()}[{w['start']:.2f}{mark}]")
print(" ".join(line))
