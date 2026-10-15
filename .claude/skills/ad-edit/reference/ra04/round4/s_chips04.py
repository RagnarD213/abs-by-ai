#!/usr/bin/env python3
"""RA-04 round 4: the label-chip references for the delivery gate's compliance:labels row (RA-15 round 3 s_chips15.py method).
A PIL chip is redrawn by the SAME call that drew it (softblue.disclosure, same text and xy); a media-card plate chip is cut from its
rendered MOV on a settled frame; the adkit analysis card writes its own chip PNG (cards_<key>/analysis_chip_ai.png).
-> round4/chips/<key>_<name>.png + chips.json"""
import json, os, shutil, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes")
import softblue as SB
import composite as CP
OUT = "round4/chips"; os.makedirs(OUT, exist_ok=True)
res = json.load(open(f"{OUT}/chips.json")) if os.path.exists(f"{OUT}/chips.json") else {}
KEYS = (sys.argv[1:] or ["9x16", "16x9"])

def redraw(cid, wh, text, xy):
    im = Image.new("RGBA", wh, (0, 0, 0, 0)); x0, y0, x1, y1 = SB.disclosure(im, text, xy)
    box = (int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x1)), int(np.ceil(y1)))
    im.crop(box).save(f"{OUT}/{cid}.png"); res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[box[0], box[1]], box=list(box), how="redrawn")

def cut(cid, mov, wh, box, n_settled):
    f = None
    for i, fr in enumerate(CP.reader(mov, 0, n_settled + 1, True, wh)): f = fr
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    Image.fromarray(f[y0:y1, x0:x1]).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[x0, y0], box=[x0, y0, x1, y1], how=f"cut from {os.path.basename(mov)} frame {n_settled}")

def analysis(cid, key):
    m = json.load(open(f"cards_{key}/meta.json"))["analysis"]; src = f"cards_{key}/analysis_chip_ai.png"
    im = Image.open(src); x, y = m["chip_pos"]
    shutil.copy(src, f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[int(x), int(y)], box=[int(x), int(y), int(x) + im.width, int(y) + im.height],
                    how=f"adkit analysis_card chip ({src})")

for key, wh, plates in (("9x16", (1080, 1920), "hf9/plates.json"), ("16x9", (1920, 1080), "hf16/plates.json")):
    if key not in KEYS: continue
    P = json.load(open(plates))
    if key == "9x16":
        redraw("9x16_lock", wh, "AI-GENERATED", (60, 236)); redraw("9x16_brokenarm", wh, "AI-GENERATED", (60, 236))
        names = ("flow_b",)
    else:
        names = ("lock", "flow_b", "brokenarm")
    for nm in names:
        c = P[nm]["chip"]; cut(f"{key}_{nm}", P[nm]["mov"], wh, (c["x"], c["y"], c["x"] + c["w"], c["y"] + 80), 20)
    analysis(f"{key}_analysis", key)
# the REAL-photo chip as a reference only (compliance:labels looks for both chips; this ad shows no real photo of Dan)
redraw("9x16_real", (1080, 1920), "Real picture of me. Not AI-generated.", (60, 236))
redraw("16x9_real", (1920, 1080), "Real picture of me. Not AI-generated.", (54, 54))
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"], v["how"])
