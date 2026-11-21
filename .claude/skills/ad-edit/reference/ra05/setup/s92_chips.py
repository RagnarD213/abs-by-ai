#!/usr/bin/env python3
"""RA-05 setup: the label-chip references for the delivery gate's compliance:labels row (RA-14 round 4 s92_chips.py method).
   python3 s92_chips.py          (any cwd; reads round3/, writes setup/chips/)

Each chip comes from the SAME place that put it in the approved film, never typed in:
  couch  s06_couch3.py   SB.disclosure(im, "AI-GENERATED", (40, 96), size=20)   xy and box from cards_9x16/meta.json couch.chip_box
  scan   s06_scan3.py    SB.disclosure(im, "AI-GENERATED", (20, 160), size=20)  xy and box from cards_9x16/meta.json scan.chip_box
  lock   s06_inserts05.py fill_card: SB.disclosure(im, "AI-GENERATED", (60, 236)) at the default size (meta keeps no lock entry,
         so the redraw is checked against the delivered master below)
  open   the HyperFrames media-card plate P_open.mov draws its own chip (hf9/configs/P_open.json chip, shown from the AI result
         on): cut from the plate on a settled frame, its box MEASURED as the chip-coloured pixels around the config's x/y
  A1     the HyperFrames analysis card: cut from the locked A1.mov at the manifest's chip box, 60 % into the card
  real   reference only (compliance:labels looks for both chips; this film shows no real photo of Dan): redrawn at (60, 236)
Every chip is then correlated against the DELIVERED master at the middle of its beat, and the score is recorded.
Writes setup/chips/<id>.png (RGBA) and setup/chips/chips.json {id: {png, pos, box, how, corr_master}}.
"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image
WD = "/Volumes/Extreme/_edit_work/ra05"; R3 = f"{WD}/round3"; OUT = f"{WD}/setup/chips"
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes"); sys.path.insert(0, R3)
import softblue as SB
import composite as CP
import ra01lib as L
MASTER = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/how ai can get you real six pack abs - RA-05/"
          "how ai can get you real six pack abs | claude | 9x16 | RA-05.mp4")
SHA = "c0a57092fc85b01575d507ec3dcedf28cd1d60b35c1e56ef96f9a298acbcaceb"
W, H = 1080, 1920; FPS = L.FPS
os.makedirs(OUT, exist_ok=True)
h = hashlib.sha256()
with open(MASTER, "rb") as f:
    for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
assert h.hexdigest() == SHA, "the master is not the approved file"
B = json.load(open(f"{R3}/beats.json")); CARD = {c["name"]: c for c in B["cards"]}
META = json.load(open(f"{R3}/cards_9x16/meta.json"))
MAN = {m["id"]: m for m in json.load(open(f"{R3}/hf9/manifest.json"))}
PL = json.load(open(f"{R3}/hf9/plates.json"))
res = {}


def redraw(cid, text, xy, size=23, expect=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, y0, x1, y1 = SB.disclosure(im, text, xy, size=size)
    box = (int(np.floor(x0)), int(np.floor(y0)), int(np.ceil(x1)), int(np.ceil(y1)))
    if expect is not None:
        assert [round(v) for v in (x0, y0, x1, y1)] == list(expect), (cid, (x0, y0, x1, y1), expect)
    im.crop(box).save(f"{OUT}/{cid}.png")
    res[cid] = dict(png=f"{OUT}/{cid}.png", pos=[box[0], box[1]], box=list(box), text=text,
                    how=f"redrawn: SB.disclosure({text!r}, {tuple(xy)}, size={size})")


def master_frame(t):
    k = int(round(t * FPS))
    return next(CP.reader(MASTER, k, 1, False, (W, H))), k


# couch: both shots carry the same chip (meta chip_box "0" and "1")
cb = META["couch"]["chip_box"]; assert cb["0"] == cb["1"], cb
redraw("couch", "AI-GENERATED", tuple(cb["0"][:2]), 20, cb["0"])
redraw("scan", "AI-GENERATED", tuple(META["scan"]["chip_box"][:2]), 20, META["scan"]["chip_box"])
redraw("lock", "AI-GENERATED", (60, 236))
redraw("real", "Real picture of me. Not AI-generated.", (60, 236))

# open: the plate's own chip, measured on a settled frame after the AI result comes up
cfg = json.load(open(f"{R3}/hf9/configs/P_open.json"))[0]["chip"]
f_res = META["open"]["result_frame"]
assert abs(cfg["spans"][0][0] - f_res / FPS) < 1 / FPS, ("chip span start vs result frame", cfg["spans"][0][0], f_res / FPS)
g = f_res + (PL["open"]["frames"] - f_res) // 2
fr = None
for fr in CP.reader(PL["open"]["mov"], g, 1, True, (W, H)): pass
x0, y0 = cfg["x"] - 40, cfg["y"] - 40
sub = fr[y0:cfg["y"] + 140, x0:cfg["x"] + cfg["w"] + 40].astype(int)
chip_px = (np.abs(sub[..., :3] - np.array(SB.CHIP)).sum(2) < 24) & (sub[..., 3] > 200)
ys, xs = np.nonzero(chip_px)
box = [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()) + 1, y0 + int(ys.max()) + 1]
Image.fromarray(fr[box[1]:box[3], box[0]:box[2]].astype(np.uint8)).save(f"{OUT}/open.png")
res["open"] = dict(png=f"{OUT}/open.png", pos=box[:2], box=box, text=cfg["s"],
                   how=f"cut from P_open.mov frame {g}; box = chip-coloured pixels around config x/y {cfg['x']},{cfg['y']}")

# A1: the analysis card's chip, cut from the locked component at the manifest box
a1 = MAN["A1"]; cx0, cy0, cx1, cy1 = a1["chip"]
g = int(round((a1["b"] - a1["a"]) * 0.6 * FPS))
for fr in CP.reader(a1["mov"], g, 1, True, (W, H)): pass
Image.fromarray(fr[cy0:cy1, cx0:cx1]).save(f"{OUT}/A1.png")
res["A1"] = dict(png=f"{OUT}/A1.png", pos=[cx0, cy0], box=[cx0, cy0, cx1, cy1], text="AI-GENERATED",
                 how=f"cut from locked A1.mov frame {g} at the manifest chip box")

# check every chip against the delivered master, mid-beat (open: mid AI-result span)
beat = {"couch": CARD["couch"]["beat"], "scan": CARD["scan"]["beat"], "lock": CARD["lock"]["beat"], "A1": CARD["A1"]["beat"],
        "open": [CARD["open"]["beat"][0] + f_res / FPS, CARD["open"]["beat"][1]]}
for cid, (a, b) in beat.items():
    m, k = master_frame((a + b) / 2)
    x0, y0, x1, y1 = res[cid]["box"]
    ref = np.asarray(Image.open(res[cid]["png"]).convert("RGBA")).astype(np.float32)
    got = m[y0:y1, x0:x1].astype(np.float32)
    msk = ref[..., 3] > 128
    rg, gg = ref[..., :3].mean(2)[msk], got.mean(2)[msk]
    corr = float(np.corrcoef(rg, gg)[0, 1])
    res[cid].update(corr_master=round(corr, 4), checked_frame=k)
    print(f"{cid:6s} box {res[cid]['box']}  corr vs master frame {k}: {corr:.4f}")
    assert corr > 0.9, (cid, corr, "the chip is not where the plan would say it is")
json.dump(res, open(f"{OUT}/chips.json", "w"), indent=1)
print("chips.json written")
