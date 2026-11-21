#!/usr/bin/env python3
"""RA-12: the label-chip references for the delivery gate's compliance:labels row -> round1/gate/chips/<id>.png + chips.json.

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
sys.path.insert(0, "/Volumes/Expansion/_edit_work/ra12")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

W, H = 1080, 1920
OUT = "round1/gate/chips"; os.makedirs(OUT, exist_ok=True)
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


redraw("K1", "AI-GENERATED", (W // 2, 1580), "mt")   # RA-12 re-review N3: K1 is the code-built phone card
redraw("P1_real", "Real picture of me. Not AI-generated.", (W // 2, 1580), "mt")
u = B.unit(W, H)
pw, ph = B.photo_size(S63.GOAL, W - 80 * u, H - 160 * u)
py = (H - ph) / 2 - 10 * u
redraw("P1_ai", "AI-GENERATED", (W / 2, py + ph + 22 * u), "mt")
res["G1"] = dict(res["P1_ai"], how="same call as P1_ai (softblue.scene_photo of the goal picture)")

MAN = {m["id"]: m for m in json.load(open("round1/gfx/manifest.json"))}
a1 = MAN["A1"]
cut_rgba("A1", a1["mov"], (a1["b"] - a1["a"]) * 0.6, a1["chip"], "AI-GENERATED", "cut from A1.mov at 60 % of the card")

CL = json.load(open("round1/cards/clips.json"))
for cid in ("W1", "D1", "Q1"):
    ch = CL[cid]["chip"]; mov = os.path.abspath(f"round1/plates/renders/P_{cid}.mov")
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", "1.0", "-i", mov, "-frames:v", "1", "-vf", "format=rgba", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(H, W, 4)
    ya, yb = ch["y"] - 6, ch["y"] + 130; xa, xb = ch["x"] - 6, ch["x"] + ch["w"] + 6
    region = a[ya:yb, xa:xb]
    # the chip is the darker pill on the plate: rows/cols whose pixels differ from the plate field just outside it
    ref = a[ya:yb, xa - 20:xa - 10].astype(int).mean(1, keepdims=True)
    diff = np.abs(region[..., :3].astype(int) - ref[..., :3]).sum(2) > 30
    ys, xs = np.nonzero(diff)
    box = [xa + int(xs.min()), ya + int(ys.min()), xa + int(xs.max()) + 1, ya + int(ys.max()) + 1]
    cut_rgba(cid, mov, 1.0, box, "AI-GENERATED", f"cut from the plate P_{cid}.mov at 1.0 s, measured box")
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
for k, v in res.items(): print(k, v["box"], v["how"])
