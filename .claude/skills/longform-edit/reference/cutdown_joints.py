#!/usr/bin/env python3
"""Every NEW joint this variant introduces, in FINISHED-RENDER time.
Derived from the EDLs themselves, not from the cut list: a boundary is NEW when
its (source-out, source-in) pair does not exist in the approved v3 edit. That
catches merged and coincident deletions that a cut-list walk would miss.
Usage: python3 joints.py cons|sub30"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/"
           "Media/longform-raw/absbyai-0803-shoot/invest-health")
V = sys.argv[1]

v3 = json.load(open(SRC / "edit" / "edl.json"))["ranges"]
old = {(round(a["end"], 2), round(b["start"], 2)) for a, b in zip(v3, v3[1:])}

edl = json.load(open(HERE / V / "edl.json"))
ranges = edl["ranges"]
offs, acc = [], 0.0
for r in ranges:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)

words = []
for s in json.load(open(SRC / "C1511.whisper.json"))["segments"]:
    for w in s.get("words", []):
        t = w["word"].strip()
        if t: words.append({"t": t, "s": w["start"], "e": w["end"]})
def before(t, n=8):
    return " ".join(w["t"] for w in words if w["e"] <= t + 0.02)[-90:]
def after(t, n=8):
    return " ".join(w["t"] for w in words if w["s"] >= t - 0.02)[:90]

joints = []
for i, (a, b) in enumerate(zip(ranges, ranges[1:])):
    key = (round(a["end"], 2), round(b["start"], 2))
    if key in old:
        continue
    joints.append({"i": i + 1, "out_t": round(offs[i + 1], 2),
                   "src_out": a["end"], "src_in": b["start"],
                   "beats": f'{a["beat"]} -> {b["beat"]}',
                   "join": f"{before(a['end'])}  ]|[  {after(b['start'])}"})
json.dump({"total": acc, "joints": joints}, open(HERE / V / "new_joints.json", "w"), indent=1)
print(f"{V}: {len(joints)} NEW joints of {len(ranges)-1} total boundaries "
      f"-> {V}/new_joints.json  (render total {acc:.1f}s)")
