#!/usr/bin/env python3
"""RA-06 round 4: the 16:9 Soft Blue graphics from the same plan (beats.json) through the shared HyperFrames templates at 1920x1080
(from RA-15 round 3's gfx16.py).
  LT2     the Motivation lower third on the approved 16:9 box (x 86..1828, bottom 1016); captions lift above it (s07_captions16.py)
  CTA     the glass button with the 9:16's copy, compact and UPPER LEFT beside his shoulder: measured on the end hold (dan07, NEAR,
          person mask on 12 frames) his arms fill x 383..1619 from y 500 down, so RA-01's bottom-left spot is inside his arms; the box
          x 60..650, y 296..416 has 0 person pixels. During I4 (41.47 s on) it sits on the field left of the phone plate.
  plates  a media-card plate per 9:16 card: a full-height hole (y 40..892; the caption line is 930) in the clip's own shape, centred,
          the AI-GENERATED chip on the field right of the hole's top corner (never on the picture)
Writes hf16/manifest.json and hf16/plates.json."""
import json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
from hv16 import V
H = V.H
B = json.load(open("beats.json")); OUT = os.path.abspath("hf16"); FPS = 30000/1001
CTA_COPY = ("Tap The Button Below To", "Start Training With AI")
W, Hh = 1920, 1080
man = []
if not os.environ.get("PLATES_ONLY"):
    # ROUND 4 (watch judge, 16:9): the full-width strip (x 86..1828) covered his abs for all 4.3 s of LT2 in the FAR shot. Measured on the
    # 16:9 picture (person mask, 16 frames 15.7-19.9 s) nothing of him is left of x ~500 below y 800, so LT2 is the same template and copy
    # in a narrow strip in the bottom-left corner (x 86..560, three lines: "Copy-Paste" is 346 px), clear of his torso (it reaches his elbow at most).
    _orig_box = V.B.lower_third_default_box
    LT_X1 = {"LT2": 560}
    for c in B["lt"]:
        if c["id"] in LT_X1:
            V.B.lower_third_default_box = lambda w, h, lines=1, _x1=LT_X1[c["id"]]: (lambda b: (b[0], b[1], _x1, b[3]))(_orig_box(w, h, lines))
        scenes, meta = V.lt_scenes(c)
        V.B.lower_third_default_box = _orig_box
        V.build(scenes, OUT, render=True, snap=max(0.5, c["b"] - c["a"] - 0.6))
        man.append(dict(id=c["id"], template="lower-third", a=c["a"], b=c["b"], canvas=[W, Hh], topic=c["topic"], parts=c["parts"],
                        mov=f"{OUT}/renders/{c['id']}.mov", mask=f"{OUT}/renders/{c['id']}_mask.mov", **meta))
        print(c["id"], meta, flush=True)
    a, b = B["cta"][0]; top, big = CTA_COPY
    big_px, top_px = 40, 22
    bw = round(max(H.text_w(big, big_px) + 56 + 22 + 60, H.text_w(top, top_px) + 60)); bh = 120
    x0, by = 60, 296
    assert x0 + bw <= 700, ("CTA reaches the phone plate / his shoulder", bw)
    bx_ = x0 + (bw - H.text_w(big, big_px) - 56) / 2
    Lc = dict(btn=[x0, by, bw, bh], radius=22, top=dict(x=round(x0 + (bw - H.text_w(top, top_px)) / 2), y=round(by + 22), px=top_px, s=top),
              big=dict(x=round(bx_), y=round(by + 22 + top_px * 1.4 + 6), px=big_px, s=big),
              arrow=dict(x=round(bx_ + H.text_w(big, big_px) + 22), y=round(by + 22 + top_px * 1.4 + 6), px=big_px))
    scenes = [(V.HERE / "cta" / "cta.template.htm", dict(id="CTA16" + ("_mask" if m == "mask" else ""), mode=m, dur=round(b - a, 3), canvas=[W, Hh],
                                                       hold_out=True, full=False, **Lc), ()) for m in ("content", "mask")]
    meta = dict(kind="glass", band=[int(by - 12), int(by + bh + 40)], box=[x0, by, x0 + bw, by + bh])
    V.build(scenes, OUT, render=True, snap=max(0.5, b - a - 0.6))
    man.append(dict(id="CTA", template="cta", a=a, b=b, canvas=[W, Hh], copy=CTA_COPY, mov=f"{OUT}/renders/CTA16.mov",
                    mask=f"{OUT}/renders/CTA16_mask.mov", **meta))
    print("CTA", meta, flush=True)
    json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)

# plates: name -> (media aspect, label)
PL = {"I3": (9/16, "AI-GENERATED"), "I1": (9/16, "AI-GENERATED"), "I4": (9/16, "AI-GENERATED"), "fired": (9/16, "AI-GENERATED"),
      "tour": (780/1476, None), "tour2": (432/920, None), "flow_a": (1320/1600, None), "flow_b": (1320/1600, "AI-GENERATED")}
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
