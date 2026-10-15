#!/usr/bin/env python3
"""RA-04 round 3: rebuild ONLY the TIP 3 lower third for its new end (39.139, where the AI clip now starts) and patch its manifest
entry. gfx04.py would re-render every graphic; the others did not change. Same calls as gfx04.py."""
import json, os, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import vertical as V
B = json.load(open("beats.json")); OUT = os.path.abspath("hf9")
c = next(x for x in B["lt"] if x["id"] == "LT3")
scenes, meta = V.lt_scenes(c)
V.build(scenes, OUT, render=True, snap=max(0.5, c["b"] - c["a"] - 0.6))
M = json.load(open(f"{OUT}/manifest.json")); i = next(k for k, x in enumerate(M) if x["id"] == "LT3")
M[i] = dict(id="LT3", template="lower-third", a=c["a"], b=c["b"], canvas=V.CANVAS, topic=c["topic"], parts=c["parts"],
            mov=f"{OUT}/renders/LT3.mov", mask=f"{OUT}/renders/LT3_mask.mov", **meta)
json.dump(M, open(f"{OUT}/manifest.json", "w"), indent=1); print("LT3", c["a"], c["b"], meta); print("LT3_DONE")
