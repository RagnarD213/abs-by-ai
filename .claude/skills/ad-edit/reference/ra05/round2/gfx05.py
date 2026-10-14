#!/usr/bin/env python3
"""RA-04 Soft Blue Light graphics at 9:16 through the shared HyperFrames templates (vertical.py):
three TIP lower thirds, the CTA glass button, and the media-card plates for the phone inserts.
Writes hf9/manifest.json (overlays for the compositor) and hf9/plates.json (hole + mov per insert)."""
import json, os, sys
HF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes"
sys.path.insert(0, HF)
import vertical as V
B = json.load(open("beats.json")); OUT = os.path.abspath("hf9"); FPS = 30000/1001
CTA_COPY = ("Tap The Button Below To", "See Yourself With Abs")
man = []
for c in B["lt"]:
    scenes, meta = V.lt_scenes(c)
    V.build(scenes, OUT, render=True, snap=max(0.5, c["b"] - c["a"] - 0.6))
    man.append(dict(id=c["id"], template="lower-third", a=c["a"], b=c["b"], canvas=V.CANVAS, topic=c["topic"], parts=c["parts"],
                    mov=f"{OUT}/renders/{c['id']}.mov", mask=f"{OUT}/renders/{c['id']}_mask.mov", **meta))
    print(c["id"], meta, flush=True)
a, b = B["cta"][0]
scenes, meta = V.cta_scenes("CTA", b - a, *CTA_COPY, hold_out=True)
V.build(scenes, OUT, render=True, snap=max(0.5, b - a - 0.6))
man.append(dict(id="CTA", template="cta", a=a, b=b, canvas=V.CANVAS, copy=CTA_COPY,
                mov=f"{OUT}/renders/CTA.mov", mask=f"{OUT}/renders/CTA_mask.mov", **meta))
print("CTA", meta, flush=True)
# ROUND 2: the Soft Blue analysis card from the shared HyperFrames template (Dan's RA-14 instruction, the standard now).
by = {c["name"]: c for c in B["cards"]}
a1 = by["A1"]
c = dict(id="A1", a=a1["beat"][0], b=a1["beat"][1], photo=os.path.abspath("media/after_man.png"), label="AI-GENERATED",
         reveal=a1["config"]["reveal"], band=a1["config"]["band"])
scenes, meta = V.analysis_scenes(c)
V.build(scenes, OUT, render=True, snap=max(0.5, c["b"] - c["a"] - 0.6))
man.append(dict(id="A1", template="analysis-card", a=c["a"], b=c["b"], canvas=V.CANVAS, mov=f"{OUT}/renders/A1.mov", **meta))
print("A1", meta, flush=True)
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)
# plates: name -> (media aspect, label, max_w, label spans in card seconds or None)
# Round 1 self-check: a phone that ran down behind the captions put white words on the app's white screens and a caption
# across the result picture's abs. Every card now ENDS ABOVE the caption line (y 1376), so the words sit on the field.
# ROUND 2: "open" carries the AI-GENERATED chip only while the AI result is on screen (OPEN_RESULT_F, from s06's
# segment table), never over the real before photo; "scan" is the start VSL body scan (AI), its sides trimmed to the callouts.
import s06_open as O
PL = {"open": (1320/1600, "AI-GENERATED", 888, [[O.RESULT_F / FPS, 99.0]]), "tour": (432/920, None, 574, None),
      "scan": (O.SCAN_W / 1080, "AI-GENERATED", None, None)}
plates = {}
for name, (ar, label, mh, spans) in PL.items():
    n = by[name]["frames"]
    scene, hole = V.media_card_scene("P_" + name, n / FPS + 0.2, ar, label=label, max_w=mh, spans=spans)
    assert hole[3] + (148 if label else 0) <= 1376, (name, hole)
    V.build([scene], OUT, render=True, snap=(O.RESULT_F / FPS + 0.5) if name == "open" else 1.0)
    plates[name] = dict(frames=n, hole=hole, mov=f"{OUT}/renders/P_{name}.mov", chip=scene[1].get("chip"))
    print(name, hole, scene[1].get("chip"), flush=True)
json.dump(plates, open(f"{OUT}/plates.json", "w"), indent=1)
print("GFX_COMPLETE")
