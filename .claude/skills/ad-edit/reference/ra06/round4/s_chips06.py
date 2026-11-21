#!/usr/bin/env python3
"""RA-06 round 4: the label-chip references for the delivery gate's compliance:labels row, both shapes (RA-15 round 3 s_chips15.py method).
A PIL chip is redrawn by the SAME call that drew it (softblue.disclosure, same text and xy); an HTML chip (media-card plates) is cut from
its rendered MOV at the chip box on a settled frame. -> round4/chips/<key>_<name>.png + chips.json"""
import json, os, sys
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
    for fr in CP.reader(mov, 0, n_settled + 1, True, wh): f = fr
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    Image.fromarray(f[y0:y1, x0:x1]).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[x0, y0], box=[x0, y0, x1, y1], how=f"cut from {os.path.basename(mov)} frame {n_settled}")

# 9:16 (s06_inserts06.py: I3/I1/I4/fired drawn by softblue.disclosure; flow_b's chip is the HyperFrames plate's)
M9 = json.load(open("cards_9x16/meta.json")); P9 = json.load(open("hf9/plates.json"))
for nm in ("I3", "I1", "I4", "fired"):
    b = M9[nm]["chip_box"]; redraw(f"9x16_{nm}", (1080, 1920), "AI-GENERATED", (b[0], b[1]))
c = P9["flow_b"]["chip"]; cut("9x16_flow_b", P9["flow_b"]["mov"], (1080, 1920), (c["x"], c["y"], c["x"] + c["w"], c["y"] + 80), 20)
# 16:9: every AI chip is a plate chip
P16 = json.load(open("hf16/plates.json"))
M16 = json.load(open("cards_16x9/meta.json"))
for nm in ("I3", "I1", "I4", "fired", "flow_b"):
    if P16[nm].get("layout") == "beside-dan":     # round 4: drawn by softblue.disclosure in s06_beside16.py
        b = M16[nm]["chip_box"]; redraw(f"16x9_{nm}", (1920, 1080), "AI-GENERATED", (b[0], b[1])); continue
    c = P16[nm]["chip"]; cut(f"16x9_{nm}", P16[nm]["mov"], (1920, 1080), (c["x"], c["y"], c["x"] + c["w"], c["y"] + 80), 20)
# the REAL-photo chip as a reference only (compliance:labels looks for both chips; this ad shows no real result photo of Dan)
redraw("9x16_real", (1080, 1920), "Real picture of me. Not AI-generated.", (60, 236))
redraw("16x9_real", (1920, 1080), "Real picture of me. Not AI-generated.", (54, 54))
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"], v["how"])
