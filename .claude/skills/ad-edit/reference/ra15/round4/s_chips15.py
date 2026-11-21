#!/usr/bin/env python3
"""RA-15 round 3: the label-chip references for the delivery gate's compliance:labels row, both shapes (RA-14 round 4 s92 method).
A PIL chip is redrawn by the SAME call that drew it (softblue.disclosure, same text and xy); an HTML chip (media-card plates, the
analysis card) is cut from its rendered MOV at the chip box on a settled frame. -> round4/chips/<key>_<name>.png + chips.json"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes")
import softblue as SB
import composite as CP
OUT = "round4/chips"; os.makedirs(OUT, exist_ok=True); res = {}

def redraw(cid, wh, text, xy):
    im = Image.new("RGBA", wh, (0, 0, 0, 0)); x0, y0, x1, y1 = SB.disclosure(im, text, xy)
    box = (int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x1)), int(np.ceil(y1)))
    im.crop(box).save(f"{OUT}/{cid}.png"); res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[box[0], box[1]], box=list(box), how="redrawn")

def cut(cid, mov, wh, box, n_settled):
    f = None
    for i, fr in enumerate(CP.reader(mov, 0, n_settled + 1, True, wh)):
        f = fr
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    Image.fromarray(f[y0:y1, x0:x1]).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[x0, y0], box=[x0, y0, x1, y1], how=f"cut from {os.path.basename(mov)} frame {n_settled}")

M9 = json.load(open("cards_9x16/meta.json")); P9 = json.load(open("hf9/plates.json")); CH = json.load(open("round2/chip_place.json"))
AN = json.load(open("round4/analysis_hf.json"))
# 9:16 (s06_inserts15.py calls)
redraw("9x16_opener", (1080, 1920), "AI-GENERATED", (60, 236))
redraw("9x16_lock", (1080, 1920), "AI-GENERATED", (60, 236))
for k, nm in (("I2", "fridge"), ("I4", "restaurant")):
    redraw(f"9x16_{nm}", (1080, 1920), "AI-GENERATED", tuple(CH[k]["chip_xy"][:2]))
for nm in ("flow", "enjoy"):
    c = P9[nm]["chip"]; cut(f"9x16_{nm}", P9[nm]["mov"], (1080, 1920), (c["x"], c["y"], c["x"] + c["w"], c["y"] + 80), 20)
cut("9x16_analysis", AN["9x16"]["mov"], (1080, 1920), AN["9x16"]["meta"]["chip"], 60)
# 16:9
if os.path.exists("cards_16x9/meta.json"):
    M16 = json.load(open("cards_16x9/meta.json")); P16 = json.load(open("hf16/plates.json"))
    for nm in ("opener", "enjoy"):
        b = M16[nm]["chip_box"]; redraw(f"16x9_{nm}", (1920, 1080), "AI-GENERATED", (b[0], b[1]))
    for nm in ("flow", "fridge", "restaurant", "lock"):
        c = P16[nm]["chip"]; cut(f"16x9_{nm}", P16[nm]["mov"], (1920, 1080), (c["x"], c["y"], c["x"] + c["w"], c["y"] + 80), 20)
    cut("16x9_analysis", AN["16x9"]["mov"], (1920, 1080), AN["16x9"]["meta"]["chip"], 60)
# the REAL-photo chip as a reference only (compliance:labels looks for both chips; this ad shows no real photo of Dan)
redraw("9x16_real", (1080, 1920), "Real picture of me. Not AI-generated.", (60, 236))
redraw("16x9_real", (1920, 1080), "Real picture of me. Not AI-generated.", (54, 54))
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"], v["how"])
