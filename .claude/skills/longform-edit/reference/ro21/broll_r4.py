#!/usr/bin/env python3
"""RO-21 round 4 (Dan 2026-10-30 at 3:43: "Color correct this footage and make the color correction better ... color correct all the
gym B"): the six Oct 23 gym pieces (B07, B11) get a film grade on top of the Color C masters: warm white balance, a real midtone lift
with blacks held down, more colour. Dark clips take the stronger curve, the two bright floor clips the gentler one, so they land
together. Everything else in broll_r1.py is unchanged.  python3 broll_r4.py [--measure] -> round4/broll/B07.mp4, B11.mp4"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import broll_r1 as B
B.OUT = f"{B.W}/round4/broll"
WB = dict(hi=(0.90, 0.93, 1.0))
A_ = "0/0 0.06/0.05 0.2/0.27 0.5/0.64 0.8/0.88 1/1"; B_ = "0/0 0.06/0.055 0.2/0.31 0.5/0.70 0.8/0.91 1/1"; C_ = "0/0 0.05/0.05 0.15/0.27 0.4/0.66 0.8/0.93 1/1"
B.GRADES.update(GYM_A=B.grade(curve=A_, sat=0.12, **WB), GYM_B=B.grade(curve=B_, sat=0.14, **WB), GYM_C=B.grade(curve=C_, sat=0.16, **WB))
PICK = {"cardio bike": "GYM_B", "leg press": "GYM_B", "incline DB press": "GYM_A", "decline med-ball sit-up": "GYM_A", "cable crunch": "GYM_C", "leg raise": "GYM_A"}
for iid in ("B07", "B11"):
    B.ITEMS[iid] = [tuple(list(p[:6]) + [PICK[p[0]]]) for p in B.ITEMS[iid]]
if __name__ == "__main__":
    if "--measure" in sys.argv: B.measure(["B07", "B11"])
    elif "--grades" in sys.argv: print(B.GRADES["GYM_A"]); print(B.GRADES["GYM_B"])
    else:
        for i in ("B07", "B11"): print(B.build(i))
