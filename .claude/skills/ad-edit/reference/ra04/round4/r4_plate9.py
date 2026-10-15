#!/usr/bin/env python3
"""RA-04 round 4: rebuild ONLY the 9:16 flow_b media-card plate for the new B0049 crop (1320x1520 from y 250, below the app header),
with gfx04.py's own call (same label, same max_w), and update hf9/plates.json. The lower thirds and CTA are untouched."""
import json, os, sys
HF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes"
sys.path.insert(0, HF)
import vertical as V
B = json.load(open("beats.json")); OUT = os.path.abspath("hf9"); FPS = 30000/1001
PL = json.load(open("hf9/plates.json")); by = {c["name"]: c for c in B["cards"]}
name, ar, label, mh = "flow_b", 1320/1520, "AI-GENERATED", 888
n = by[name]["frames"]
scene, hole = V.media_card_scene("P_" + name, n / FPS + 0.2, ar, label=label, max_w=mh)
assert hole[3] + 148 <= 1376, (name, hole)
V.build([scene], OUT, render=True, snap=1.0)
PL[name] = dict(frames=n, hole=hole, mov=f"{OUT}/renders/P_{name}.mov", chip=scene[1].get("chip"))
json.dump(PL, open("hf9/plates.json", "w"), indent=1)
print(name, hole, scene[1].get("chip"), "PLATE9_COMPLETE")
