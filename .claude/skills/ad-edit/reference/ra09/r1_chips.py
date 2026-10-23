#!/usr/bin/env python3
"""RA-09 round 1 (from RA-12): the label-chip references for the delivery gate's compliance:labels row -> r1/gate/chips/<id>.png + chips.json.

Each chip is redrawn by the SAME call that drew it into its card, or cut from the approved component where no PIL call exists:
  K1      s83b_clips.py   SB.disclosure(im, "AI-GENERATED", (60, 236))           (anchor "lt")
  P1_real s63_stills.py   B.disclosure(im, "Real picture of me. Not AI-generated.", xy=(540, 1580), anchor="mt")
  P1_ai / G1  softblue.scene_photo(..., GOAL, "AI-GENERATED"): disclosure at (w/2, py + ph + 22u), anchor "mt"
  A1      the HyperFrames analysis card: cut from A1.mov at the manifest's chip box
  W1 D1 Q1  the HyperFrames media-card plates: cut from each plate .mov (alpha) around the chip the scene declares
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

W, H = 1080, 1920
OUT = "r1/gate/chips"; os.makedirs(OUT, exist_ok=True)
res = {}


def redraw(cid, text, xy, anchor):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0, x1, y1 = B.disclosure(im, text, xy=xy, anchor=anchor)
    box = (int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x1)), int(np.ceil(y1)))
    im.crop(box).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[box[0], box[1]], box=list(box), text=text, how="redrawn")


def cut_rgba(cid, mov, t, box, text, how):
    x0, y0, x1, y1 = box
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", mov, "-frames:v", "1",
                          "-vf", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0},format=rgba", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    Image.frombytes("RGBA", (x1 - x0, y1 - y0), raw).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[x0, y0], box=[x0, y0, x1, y1], text=text, how=how)


CL = json.load(open("r1/cards/clips.json"))
redraw("H1", "AI-GENERATED", tuple(CL["H1"]["chip_xy"]), "lt")          # r1_cards.py: SB.disclosure(im, "AI-GENERATED", xy=(cx, cy)), anchor lt
redraw("P1_phone", "AI-GENERATED", (W // 2, 1580), "mt")
redraw("P1_real", "Real Photo Of Me, Not AI-Generated", (W // 2, 1580), "mt")   # reference for the gate's label_chips["real"] only: no real photo is in this ad                 # s63_stills.phone_card chip under the phone (RA-12 R2)
u = B.unit(W, H)
pw, ph = B.photo_size("/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg", W - 80 * u, H - 160 * u)
py = (H - ph) / 2 - 10 * u
redraw("P1_ai", "AI-GENERATED", (W / 2, py + ph + 22 * u), "mt")
res["G1"] = dict(res["P1_ai"], how="same call as P1_ai (softblue.scene_photo of the goal picture)")
MAN = {m["id"]: m for m in json.load(open("r1/gfx/manifest.json"))}
a1 = MAN["A1"]
cut_rgba("A1", a1["mov"], (a1["b"] - a1["a"]) * 0.6, a1["chip"], "AI-GENERATED", "cut from A1.mov at 60 % of the card")
# RA-07 R6's approved cards are reused pixel for pixel: their chip references are RA-07's own (the PNG laid on each clip)
R7 = json.load(open("/Volumes/Extreme/_edit_work/ra07/round6/chips/chips.json"))
import shutil
for mine, theirs in (("I1_p0", "A1_p0"), ("I1_p1", "A1_p1"), ("G2", "G1"), ("M1", "M1")):
    shutil.copy(R7[theirs]["png"], f"{OUT}/{mine}.png")
    res[mine] = dict(png=os.path.abspath(f"{OUT}/{mine}.png"), pos=R7[theirs]["pos"], box=R7[theirs]["box"], text="AI-GENERATED",
                     how=f"RA-07 R6 chip {theirs} (the card is RA-07's approved file, unchanged)")
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"], v["how"])
