#!/usr/bin/env python3
"""RA-04 round 4: rebuild ONLY the named 9:16 media-card plates for the round 4 B0049 crops (flow_b 1320x1520 from y 250, flow_a 1320x2300 from y 170),
with gfx04.py's own call (same label, same max_w), and update hf9/plates.json. The lower thirds and CTA are untouched."""
import json, os, sys
HF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes"
sys.path.insert(0, HF)
import vertical as V
B = json.load(open("beats.json")); OUT = os.path.abspath("hf9"); FPS = 30000/1001
PL = json.load(open("hf9/plates.json")); by = {c["name"]: c for c in B["cards"]}
SPEC = {"flow_a": (1320/2300, None, 668), "flow_b": (1320/1520, "AI-GENERATED", 888)}     # gfx04.py's PL entries (round 4 crops)
for name in (sys.argv[1:] or ["flow_b"]):
    ar, label, mh = SPEC[name]; n = by[name]["frames"]
    scene, hole = V.media_card_scene("P_" + name, n / FPS + 0.2, ar, label=label, max_w=mh)
    assert hole[3] + (148 if label else 0) <= 1376, (name, hole)
    V.build([scene], OUT, render=True, snap=1.0)
    PL[name] = dict(frames=n, hole=hole, mov=f"{OUT}/renders/P_{name}.mov", chip=scene[1].get("chip"))
    print(name, hole, scene[1].get("chip"))
json.dump(PL, open("hf9/plates.json", "w"), indent=1)
print("PLATE9_COMPLETE")
