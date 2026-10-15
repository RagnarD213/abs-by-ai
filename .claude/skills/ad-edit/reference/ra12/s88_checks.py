#!/usr/bin/env python3
"""RA-14 round 3 checks on the working composite (round1/work/picture_9x16.mp4), written to round1/checks.json for the page.

  * every glass graphic over Dan (L1 L2 L3 the lower thirds, C1 the button) and the recap card R1: the Vision face box
    (hyperframes/facebox.swift) must end at least 40 px above the graphic's top edge, every 5th frame it is up;
  * captions never touch a graphic: each caption state's ink box (from its PNG) against every graphic box up at that time,
    >= 20 px apart vertically wherever they overlap horizontally (the lower thirds and button end above the caption line;
    R1 lifts the captions above it);
  * a contact strip of the 5 consecutive frames around every picture cut in the first 30 seconds, for the eye
    (round1/checks/cuts_*.jpg).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Expansion/_edit_work/ra12")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/hyperframes")
import checks as HC

FPS = L.FPS; W, H = 1080, 1920
PIC = "round1/work/picture_9x16.mp4"
OUT = "round1/checks"; os.makedirs(f"{OUT}/frames", exist_ok=True)
PL = json.load(open("beats.json")); MAN = json.load(open("round1/gfx/manifest.json"))
CAP = json.load(open("round1/cap_9x16/caption_states.json"))["states"]
res = {}


def grab(g, out):
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{(g + 0.2) / FPS:.4f}", "-i", PIC, "-frames:v", "1",
                    "-vf", "scale=in_color_matrix=bt709:in_range=tv", out], check=True)


# ---- faces vs graphics
for m in MAN:
    if m["id"] == "A1": continue
    box = m.get("box"); g0, g1 = int(round(m["a"] * FPS)), int(round(m["b"] * FPS))
    paths = []
    for g in range(g0 + 2, g1 - 1, 5):
        p = f"{OUT}/frames/{g:05d}.png"
        if not os.path.exists(p): grab(g, p)
        paths.append(p)
    r = subprocess.run([HC.facebox_bin()] + paths, capture_output=True, text=True, check=True).stdout
    gaps, none = [], 0
    for line in r.strip().splitlines():
        pth, fb = line.split("\t")
        if fb in ("none", "error"): none += 1; continue
        gaps.append(box[1] - int(fb.split()[3]))
    worst = min(gaps) if gaps else None
    ok = worst is not None and worst >= 40
    res[m["id"]] = dict(frames=len(paths), no_face=none, face_to_graphic_min_px=worst, ok=ok)
    print(m["id"], res[m["id"]])

# ---- captions vs graphics (ink boxes from the state PNGs)
coll = []
for s in CAP:
    a = np.asarray(Image.open(s["image"]))[..., 3] > 8
    ys, xs = np.nonzero(a)
    if not len(ys): continue
    ink = (xs.min(), ys.min(), xs.max(), ys.max())
    for m in MAN:
        if m["id"] == "A1" or not m.get("box"): continue
        if min(s["beat"][1], m["b"]) - max(s["beat"][0], m["a"]) <= 0.02: continue
        bx = m["box"]
        if ink[2] < bx[0] or ink[0] > bx[2]: continue
        gap = max(bx[1] - ink[3], ink[1] - bx[3])
        if gap < 20: coll.append(dict(state=s["name"], line=s["line"], graphic=m["id"], gap=int(gap)))
res["captions"] = dict(states=len(CAP), collisions=coll, ok=not coll)
print("captions", len(coll), "collisions")

# ---- A1: captions keep running under the card; the card ends above the caption line
a1 = next(m for m in MAN if m["id"] == "A1")
res["A1"] = dict(card_bottom=a1["card"][3], caption_top=min(int(np.nonzero(np.asarray(Image.open(s["image"]))[..., 3] > 8)[0].min())
                 for s in CAP if s["beat"][0] < a1["b"] and s["beat"][1] > a1["a"]), chip=a1["chip"], photo=a1["photo"])
res["A1"]["ok"] = res["A1"]["card_bottom"] + 20 <= res["A1"]["caption_top"] and a1["chip"][1] >= a1["photo"][3]

# ---- 5-frame strips at every picture cut in the first 30 s
cuts = [it["f0"] for it in PL["timeline"] if 0 < it["f0"] < PL["total_frames"]]   # RA-12: every cut of the whole ad
for k in range(0, len(cuts), 4):
    rows = []
    for c in cuts[k:k + 4]:
        ims = []
        for g in range(c - 2, c + 3):
            p = f"{OUT}/frames/c{g:05d}.png"
            if not os.path.exists(p): grab(g, p)
            ims.append(Image.open(p).convert("RGB").resize((216, 384)))
        rows.append((c, ims))
    sh = Image.new("RGB", (5 * 216, len(rows) * 404), (0, 0, 0)); d = ImageDraw.Draw(sh)
    for i, (c, ims) in enumerate(rows):
        for j, im in enumerate(ims): sh.paste(im, (j * 216, i * 404))
        d.text((4, i * 404 + 386), f"cut at frame {c} ({c / FPS:.2f} s): frames {c-2}..{c+2}", fill=(255, 255, 0))
    sh.save(f"{OUT}/cuts_{k // 4}.jpg", quality=86)
res["cuts"] = cuts
json.dump(res, open("round1/checks_raw.json", "w"), indent=1, default=int)
print(json.dumps({k: v.get("ok") for k, v in res.items() if isinstance(v, dict)}))

# page notes, one line per item (round1/checks.json)
CK = {}
for k, v in res.items():
    if not isinstance(v, dict) or k == "captions": continue
    if "face_to_graphic_min_px" in v: CK[k] = f"your face stays at least {v['face_to_graphic_min_px']} px above it on every 5th frame it is up ({'pass' if v['ok'] else 'FAIL'})"
    elif k == "A1": CK[k] = f"card ends at y {v['card_bottom']}, captions start at y {v['caption_top']} ({'pass' if v['ok'] else 'FAIL'})"
CK["captions"] = f"{res['captions']['states']} caption states, {len(res['captions']['collisions'])} touching a graphic"
json.dump(CK, open("round1/checks.json", "w"), indent=1)
