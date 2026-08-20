#!/usr/bin/env python3
"""YouTube chapter markers from chip_timings.json. First chapter MUST be 0:00,
minimum 3 chapters, each at least 10s. usage: make_chapters.py <slug> <out.txt>"""
import json, sys
from pathlib import Path
slug, out = sys.argv[1], sys.argv[2]
BASE = Path(f"/Volumes/Seagate 4TB/_edit_work/{slug}")
chips = json.load(open(BASE / "chip_timings.json"))
titles = {c["key"]: c for c in chips}
import importlib.util
spec = importlib.util.spec_from_file_location("c", BASE / "chips.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
label = {k: t for k, _, _, t in mod.CHIPS}
ACR = {"Ai":"AI","Absbyai.Com":"AbsByAI.com","Mg":"mg","Lbs":"LBS","Dim":"DIM",
       "B6":"B6","Diy":"DIY","G":"g","Vs":"vs"}
def titlecase(t):
    return " ".join(ACR.get(w.title(), w.title()) if not w.isupper() or len(w) > 4 else w
                    for w in t.title().split())
def ts(s):
    s = int(s); h, r = divmod(s, 3600); m, sec = divmod(r, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
lines, prev = [], -99.0
for i, c in enumerate(chips):
    t = 0.0 if i == 0 else c["start"]
    if t - prev < 10: continue
    lines.append(f"{ts(t)} {titlecase(label[c['key']])}")
    prev = t
open(BASE / "roughcuts" / out, "w").write("\n".join(lines) + "\n")
print(f"{len(lines)} chapters -> {out}"); print("\n".join(lines[:4]), "...")
