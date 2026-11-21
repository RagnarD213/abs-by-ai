#!/usr/bin/env python3
"""RA-15 round 3: the edit sheet for the 16:9 master (_shared/edit-sheet README).  python3 round4/s_sheet15.py <master 16x9> [--approved "..."]
The shared writer's adkit path is RA-01's (every card is Dan with physique, graphics are adkit:*), which is wrong for this film, so
this writes the same schema from RA-15's own build files with its helpers (video_block, sha) and the shared validator:
  edl / framing   cut.json pieces on the frame grid; crops from timeline_16x9.json (the delivered crops); head from framing.json
  words           words_aligned.json (CTC)
  graphics        the HyperFrames configs actually rendered (hf16/configs, hf_analysis_16x9/configs): LT1-3 lower-third, CTA, the
                  media-card plates, the analysis-card
  pictures        every card, with people / physique / label from the facts table below (handoff 2026-10-14: the three new AI clips
                  are other, false, AI-GENERATED)"""
import json, os, sys, time
import numpy as np
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/edit-sheet"
sys.path.insert(0, SH)
import sheet_from_claude_build as SFC
import validate
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
import ra01lib as L
B = os.path.abspath("."); FPS = SFC.FPS
master = os.path.abspath(sys.argv[1]); approved = sys.argv[sys.argv.index("--approved") + 1] if "--approved" in sys.argv else None
roll = os.path.splitext(os.path.basename(L.ROLL))[0]
V = SFC.video_block(master, {roll: L.ROLL})
cut = json.load(open("cut.json")); bt = json.load(open("beats.json")); tl = json.load(open("timeline_16x9.json"))["items"]
fm = json.load(open("framing.json")); gr = json.load(open("grade.json")); CP = json.load(open("clip_paths.json"))
edl, prev = [], 0
P = cut["pieces"]
for i, p in enumerate(P):
    f1 = int(round(p["t_out"] * FPS)) if i < len(P) - 1 else V["frames"]
    n = f1 - prev
    edl.append(dict(roll=roll, src_f0=int(round(p["src_in"] * FPS)), src_in=p["src_in"], src_out=round(p["src_in"] + n / FPS, 5),
                    out_f0=prev, out_f1=f1, out_in=round(prev / FPS, 5), out_out=round(f1 / FPS, 5), shot=f"{p['range']}.{i}",
                    audio="sync", join="first" if not i else "cut"))
    prev = f1
dan = [x for x in tl if x["kind"] == "dan"]
fr_rows = []
for s in edl:
    d = min(dan, key=lambda x: abs((x["a"] + x["b"]) / 2 - (s["out_in"] + s["out_out"]) / 2))
    sm = [x for x in fm["samples"] if s["src_in"] - 0.3 <= x["src"] <= s["src_out"] + 0.3] or sorted(fm["samples"], key=lambda x: abs(x["src"] - s["src_in"]))[:3]
    lvl = next((p["level"] for p in bt["punch"] if p["beat"][0] <= d["a"] + 1e-3 < p["beat"][1]), "NEAR")
    fr_rows.append(dict(name=lvl, crop=list(d["crop"]), head=dict(hair_top=min(x["hair"] for x in sm), cx=float(np.median([x["cx"] for x in sm])),
                        chin=float(np.median([x["chin"] for x in sm])), samples=len(sm)),
                        measured="framing.json (5 fps on the raw roll) + framing_holdstart.json; 16:9 crops fixed per hold (horizontal stays static)"))
grade = dict(filter=gr["filter"], lut=gr.get("lut"), decode="bt709", order="at_source_size", note=gr.get("_rule", ""))
wa = json.load(open("words_aligned.json"))["words"]
words = dict(list=[dict(w=w["w"], t0=w["t"], t1=w["e"]) for w in wa], timing="ctc", fixes=[])
strs = lambda c: [s for s in validate.strings(c)]
graphics = []
for m in json.load(open("hf16/manifest.json")):
    if m["template"] == "lower-third":
        c = next(x for x in bt["lt"] if x["id"] == m["id"])
        graphics.append(dict(id=m["id"], template="lower-third", config=c, text=[c["topic"]] + [p[0] for p in c["parts"]], t0=m["a"], t1=m["b"],
                             layer="overlay", driven_by=[dict(text=p[0], t=p[1]) for p in c["parts"]]))
    else:
        c = dict(top=m["copy"][0], big=m["copy"][1], hold_out=True, box=m["box"])
        graphics.append(dict(id="CTA", template="cta", config=c, text=list(m["copy"]), t0=m["a"], t1=m["b"], layer="overlay", driven_by=[]))
cards = {c["name"]: c for c in bt["cards"]}
plates = json.load(open("hf16/plates.json"))
for nm, pl in plates.items():
    cfg = json.load(open(f"hf16/configs/P16_{nm}.json"))[0]
    graphics.append(dict(id="plate-" + nm, template="media-card", config=dict(cfg, media=cards[nm]["asset"]), text=[cfg["chip"]["s"]] if cfg.get("chip") else [],
                         t0=cards[nm]["beat"][0], t1=cards[nm]["beat"][1], layer="full", driven_by=[]))
an = json.load(open("round4/analysis_hf.json"))["16x9"]; a0 = cards["analysis"]["beat"][0]
acfg = dict(an["cfg"], a=a0, b=cards["analysis"]["beat"][1], reveal=[round(a0 + r, 3) for r in an["cfg"]["reveal"]], band=[an["cfg"]["band"][0], round(a0 + an["cfg"]["band"][1], 3)])
graphics.append(dict(id="A1", template="analysis-card", config=acfg, text=["AI-GENERATED", acfg["band"][0]], t0=acfg["a"], t1=acfg["b"], layer="full",
                     driven_by=[dict(text=r, t=t) for r, t in zip(["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"], acfg["reveal"])]))
# who is in each picture (people / physique / label) -- the facts, by eye on the used frames and the clip library
FACTS = {"opener": ("A0016", "other", False, "ai", "a man in a white coat in a museum display case (clip library: other-man)"),
         "flow": ("B0049", "other", True, "ai", "the app's own generation of a man who is NOT Dan (VIDEO-RULES 2026-09-12; the library's 'ai-dan' tag is wrong)"),
         "analysis": ("media/after_man.png", "other", True, "ai", "the same man's AI result (B0049 at 29.6 s)"),
         "fridge": ("I2", "other", False, "ai", "round 2 AI clip, a man at an open fridge (handoff: other, false, AI-GENERATED)"),
         "enjoy": ("A0086", "other", False, "ai", "a man eating steak (clip library: other-man); shirtless but the shot is the meal, not a physique"),
         "macro": ("B0038", "none", False, "none", "app recording of a salmon plate photo"),
         "restaurant": ("I4", "other", False, "ai", "round 2 AI clip, a man ordering from a waiter (handoff: other, false, AI-GENERATED)"),
         "lock": ("A0074", "dan", True, "ai", "a phone lock screen showing Dan's AI goal picture (clip library: ai-dan)")}
SRC_IN = {"opener": 0.0, "flow": 13.0, "analysis": 0.0, "fridge": 33/24, "enjoy": 0.0, "macro": 0.0, "restaurant": 32/24, "lock": 0.5}
pictures = []
for nm, (asset, ppl, phys, lk, why) in FACTS.items():
    c = cards[nm]; path = CP.get(asset) or os.path.abspath(asset)
    pictures.append(dict(id=nm, t0=c["beat"][0], t1=c["beat"][1], kind="photo" if path.endswith(".png") else "clip",
                         sources=[dict(path=path, src_in=SRC_IN[nm])], label_kind=lk, label="AI-GENERATED" if lk == "ai" else None,
                         label_source="round4/chips/chips.json (the chip drawn on this card)", people=ppl, physique=phys, people_source=why,
                         approved_crop=None, card_kind=c["kind"]))
audio = dict(mix=master, untreated=os.path.abspath("cut_audio.wav"), gate_stamp=master + ".audio_gate.json",
             chain=os.path.abspath("mix_bass.wav.voice_chain.json"), music=os.path.abspath("music/Realizer.mp3"))
dec = json.load(open("round4-plan/decisions.json"))
approvals = dict(status="approved" if approved else "pending", round=4, source=os.path.abspath("round4-plan/decisions.json"), full_film=approved,
                 decisions=[dict(id=i["id"], verdict=i["verdict"], words=i.get("words")) for i in dec["items"]])
S = dict(schema=validate.SCHEMA, job="RA-15", title="Never Pay A Nutritionist Again", type="AD", editor="claude", video=V, grade=grade, edl=edl,
         framing=fr_rows, words=words, graphics=graphics, pictures=pictures, audio=audio, approvals=approvals,
         provenance=dict(written=time.strftime("%Y-%m-%dT%H:%M:%S"), by="ra15 round4/s_sheet15.py (RA-15 build, shared schema and validator)",
                         build_dir=B, inputs={f: SFC.sha(f) for f in ("cut.json", "beats.json", "timeline_16x9.json", "framing.json", "grade.json")}))
E = validate.check(S, do_hash=False)
out = master[:-4] + ".edit-sheet.json"
if E:
    json.dump(S, open(out + ".INCOMPLETE.json", "w"), indent=1); print("INCOMPLETE"); [print(" -", e) for e in E]; sys.exit(1)
json.dump(S, open(out, "w"), indent=1)
print(out, len(edl), "segments", len(graphics), "graphics", len(pictures), "pictures")
