#!/usr/bin/env python3
"""RA-14 round 4: the label-chip references for the delivery gate's compliance:labels row.

Each chip is redrawn by the SAME call that drew it into its locked component (never cropped from the candidate):
  O2  opener      s81_opener.py   SB.disclosure(im, "AI-GENERATED", xy=(60, 1296), anchor="lt")
  P1r phone card  s63_stills.py   B.disclosure(im, "Real picture of me. Not AI-generated.", xy=(540, 1580), anchor="mt")
  P1a result card softblue.scene_photo(..., S63.GOAL, "AI-GENERATED"): disclosure at (w/2, py + ph + 22u), anchor "mt"
  A1  analysis card (HyperFrames, HTML): no PIL call to repeat, so its chip is cut from the locked A1.mov at the
      manifest's chip box on a settled frame (A1.mov is the approved component, hash-checked in round4/HASHES.json).
Writes round4/chips/<id>.png (RGBA, transparent outside the chip) and round4/chips/chips.json {id: {png, pos}}.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

W, H = 1080, 1920
OUT = "round4/chips"; os.makedirs(OUT, exist_ok=True)
res = {}


def redraw(cid, text, xy, anchor):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0, x1, y1 = B.disclosure(im, text, xy=xy, anchor=anchor)
    box = (int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x1)), int(np.ceil(y1)))
    im.crop(box).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=os.path.abspath(f"{OUT}/{cid}.png"), pos=[box[0], box[1]], box=list(box), text=text, how="redrawn")


redraw("O2", "AI-GENERATED", (60, 1296), "lt")
redraw("P1_real", "Real picture of me. Not AI-generated.", (W // 2, 1580), "mt")
u = B.unit(W, H)
pw, ph = B.photo_size(S63.GOAL, W - 80 * u, H - 160 * u)
py = (H - ph) / 2 - 10 * u
redraw("P1_ai", "AI-GENERATED", (W / 2, py + ph + 22 * u), "mt")

# A1: cut from the approved component at the manifest's chip box, mid-card
MAN = {m["id"]: m for m in json.load(open("round3/gfx/manifest.json"))}
a1 = MAN["A1"]; x0, y0, x1, y1 = a1["chip"]
t = (a1["b"] - a1["a"]) * 0.6
raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", a1["mov"], "-frames:v", "1",
                      "-vf", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0},format=rgba", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
Image.frombytes("RGBA", (x1 - x0, y1 - y0), raw).save(f"{OUT}/A1.png")
res["A1"] = dict(png=os.path.abspath(f"{OUT}/A1.png"), pos=[x0, y0], box=[x0, y0, x1, y1], text="AI-GENERATED",
                 how=f"cut from locked A1.mov at {t:.2f} s into the card")
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
print(json.dumps(res, indent=1))
