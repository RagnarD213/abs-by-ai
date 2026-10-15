#!/usr/bin/env python3
"""RA-04 round 4: the 16:9 Soft Blue graphics from the same plan (beats.json), through the shared HyperFrames templates at 1920x1080
(RA-15 round 3's gfx16.py, the latest delivered 16:9 of these ads).
  LT1-3   the Motivation lower third on the approved 16:9 box (x 86..1828, bottom 1016); captions lift above it (s07_captions.py)
  CTA     the glass button, compact, upper LEFT beside Dan's shoulder (RA-15 round 3 b): bottom left is the caption line and his
          hands; same copy as the 9:16. Placement checked by person mask on the rendered hold (round4/cta16_check.py).
  plates  one media-card plate per 9:16 card: a full-height hole (y 40..892, the caption line is 930) in the clip's own shape, centred,
          the AI-GENERATED chip on the field right of the hole's top corner, never on the picture. A native-vertical clip in a 16:9
          frame goes in a plate, never cropped (ad-edit lesson 61; clip_fit.decide() is for horizontal clips in vertical frames).
Writes hf16/manifest.json and hf16/plates.json."""
import json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
from hv16 import V
H = V.H
B = json.load(open("beats.json")); OUT = os.path.abspath("hf16"); FPS = 30000/1001
CTA_COPY = ("Tap The Button Below To", "See Yourself With Abs")
W, Hh = 1920, 1080
man = []
if not os.environ.get("PLATES_ONLY"):
    for c in B["lt"]:
        scenes, meta = V.lt_scenes(c)
        V.build(scenes, OUT, render=True, snap=max(0.5, c["b"] - c["a"] - 0.6))
        man.append(dict(id=c["id"], template="lower-third", a=c["a"], b=c["b"], canvas=[W, Hh], topic=c["topic"], parts=c["parts"],
                        mov=f"{OUT}/renders/{c['id']}.mov", mask=f"{OUT}/renders/{c['id']}_mask.mov", **meta))
        print(c["id"], meta, flush=True)
    a, b = B["cta"][0]; top, big = CTA_COPY
    big_px, top_px = 40, 22
    bw = round(max(H.text_w(big, big_px) + 56 + 22 + 60, H.text_w(top, top_px) + 60)); bh = 120
    x0, by = 60, int(os.environ.get("CTA_Y", "296"))
    assert x0 + bw <= 650, ("CTA reaches his shoulder", bw)
    bx_ = x0 + (bw - H.text_w(big, big_px) - 56) / 2
    L = dict(btn=[x0, by, bw, bh], radius=22, top=dict(x=round(x0 + (bw - H.text_w(top, top_px)) / 2), y=round(by + 22), px=top_px, s=top),
             big=dict(x=round(bx_), y=round(by + 22 + top_px * 1.4 + 6), px=big_px, s=big),
             arrow=dict(x=round(bx_ + H.text_w(big, big_px) + 22), y=round(by + 22 + top_px * 1.4 + 6), px=big_px))
    scenes = [(V.HERE / "cta" / "cta.template.htm", dict(id="CTA16" + ("_mask" if m == "mask" else ""), mode=m, dur=round(b - a, 3), canvas=[W, Hh],
                                                       hold_out=True, full=False, **L), ()) for m in ("content", "mask")]
    meta = dict(kind="glass", band=[int(by - 12), int(by + bh + 40)], box=[x0, by, x0 + bw, by + bh])
    V.build(scenes, OUT, render=True, snap=max(0.5, b - a - 0.6))
    man.append(dict(id="CTA", template="cta", a=a, b=b, canvas=[W, Hh], copy=CTA_COPY, mov=f"{OUT}/renders/CTA16.mov",
                    mask=f"{OUT}/renders/CTA16_mask.mov", **meta))
    print("CTA", meta, flush=True)
    json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)

# plates: name -> (media aspect, label); the same crops as the 9:16 (s06_inserts04.py)
PL = {"lock": (9/16, "AI-GENERATED"), "flow_a": (1320/2420, None), "flow_b": (1320/1520, "AI-GENERATED"), "tour": (432/920, None),
      "brokenarm": (9/16, "AI-GENERATED")}
by = {c["name"]: c for c in B["cards"]}; plates = {}
for name, (ar, label) in PL.items():
    n = by[name]["frames"]
    hh = 852; hw = int(hh * ar) // 2 * 2; hx = (W - hw) // 2 // 2 * 2; hy = 40
    cfg = dict(id="P16_" + name, dur=round(n / FPS + 0.2, 3), canvas=[W, Hh], hole=[hx, hy, hw, hh], radius=26 if ar > 0.7 else 44)
    if label:
        cw_ = round(H.text_w(label, 23 * 2, False) + 40 * 2)
        cfg["chip"] = dict(x=hx + hw + 36, y=hy + 8, s=label, w=cw_)
    V.build([(V.HERE / "media-card" / "media-card.template.htm", cfg, ())], OUT, render=True, snap=1.0)
    plates[name] = dict(frames=n, hole=[hx, hy, hx + hw, hy + hh], mov=f"{OUT}/renders/P16_{name}.mov", chip=cfg.get("chip"))
    print(name, plates[name]["hole"], cfg.get("chip"), flush=True)
json.dump(plates, open(f"{OUT}/plates.json", "w"), indent=1)
print("GFX16_COMPLETE")
