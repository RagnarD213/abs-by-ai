#!/usr/bin/env python3
"""RA-07 round 3: the label-chip references for the delivery gate's compliance:labels row (RA-14 round 4 s92_chips.py).

Each chip comes from the component that drew it, never from the candidate:
  P1_real, K1    SB.disclosure at (540, 1580) "mt"  (s63_stills.phone_card / s63_cards07.lock_screen)
  P1_ai          softblue.scene_photo(..., S63.GOAL, "AI-GENERATED"): disclosure under the photo, "mt"
  H1, I2         the fixed chip spots in round 2's s75_clips.py, redrawn
  clips          every other clip's chip is the RGBA PNG s75 / s75r3 overlaid on it (<clip>_chip.png), cropped to its ink
  python3 round3/s92r3_chips.py      -> round3/chips/<id>.png + round3/chips/chips.json {id: {png, pos, box}}
"""
import glob, json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

W, H = 1080, 1920
OUT = "round3/chips"; os.makedirs(OUT, exist_ok=True)
res = {}


def keep(cid, im, how, text="AI-GENERATED"):
    a = np.asarray(im.split()[-1]); ys, xs = np.nonzero(a > 0)
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    im.crop(box).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[box[0], box[1]], box=list(box), text=text, how=how)


def redraw(cid, text, xy, anchor):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); B.disclosure(im, text, xy=xy, anchor=anchor)
    keep(cid, im, f"redrawn: disclosure {xy} {anchor}", text)


redraw("P1_real", "Real picture of me. Not AI-generated.", (W // 2, 1580), "mt")
redraw("K1", "AI-GENERATED", (W // 2, 1580), "mt")
u = B.unit(W, H)
pw, ph = B.photo_size(S63.GOAL, W - 80 * u, H - 160 * u)
py = (H - ph) / 2 - 10 * u
redraw("P1_ai", "AI-GENERATED", (W / 2, py + ph + 22 * u), "mt")
redraw("H1", "AI-GENERATED", (W // 2, 1262), "mt")
redraw("I2", "AI-GENERATED", (940, 214), "rt")
for p in sorted(glob.glob("round3/clips/*_chip.png")):
    cid = os.path.basename(p)[:-9]
    keep(cid, Image.open(p).convert("RGBA"), f"the chip PNG s75r3 laid on the clip ({p})")
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"])
