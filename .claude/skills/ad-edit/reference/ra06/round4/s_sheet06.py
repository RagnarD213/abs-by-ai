#!/usr/bin/env python3
"""RA-06 round 4 (from RA-15 round 3 s_sheet15.py): the edit sheet for the 16:9 master (_shared/edit-sheet README).  python3 round4/s_sheet06.py <master 16x9> [--approved "..."]
The shared writer's adkit path is RA-01's (every card is Dan with physique, graphics are adkit:*), which is wrong for this film, so
this writes the same schema from RA-06's own build files with its helpers (video_block, sha) and the shared validator:
  edl / framing   cut.json pieces on the frame grid; crops from timeline_16x9.json (the delivered crops); head from framing.json
  words           words_aligned.json (CTC)
  graphics        the HyperFrames configs actually rendered (hf16/configs): LT2 lower-third, CTA, the
                  media-card plates
  pictures        every card, with people / physique / label from the facts table below (handoff 2026-10-14: the three new AI clips
                  are other, false, AI-GENERATED)"""
import json, os, sys, time
import numpy as np
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/edit-sheet"
sys.path.insert(0, SH)
import sheet_from_claude_build as SFC
import validate
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
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
for _it in tl:      # round 4: a Dan hold shown beside the phone in 16:9 (r4_16x9_overrides.json dan_as_card) is a card here
    if _it["kind"] == "card" and _it["name"] not in cards:
        cards[_it["name"]] = dict(name=_it["name"], kind="beside", beat=[_it["a"], _it["b"]], asset="B0049")
plates = json.load(open("hf16/plates.json"))
for nm, pl in plates.items():
    if pl.get("layout") == "beside-dan": continue     # round 4: Dan on camera beside a PIL phone panel (s06_beside16.py), listed under pictures
    cfg = json.load(open(f"hf16/configs/P16_{nm}.json"))[0]
    graphics.append(dict(id="plate-" + nm, template="media-card", config=dict(cfg, media=cards[nm]["asset"]), text=[cfg["chip"]["s"]] if cfg.get("chip") else [],
                         t0=cards[nm]["beat"][0], t1=cards[nm]["beat"][1], layer="full", driven_by=[]))
# who is in each picture (people / physique / label) -- the facts, by eye on the used frames and the clip library
FACTS = {"split": ("C1683", "dan", False, "none", "Dan's own 8/28 pool B-roll of three ab exercises (C1683 plank, C1682 toe touches, C1677 vacuum), filmed live the same day as the talking roll: exercise demonstration footage like the talking-head shots, not a still result picture of his physique, so no real/AI chip (as in the 9:16 Dan approved 2026-10-15)"),
         "I3": ("I3", "other", False, "ai", "round 3 Kling clip from approved frames: an ordinary man in a T-shirt under a body-scan line"),
         "I1": ("I1", "other", False, "ai", "round 3 Kling clip: a trainer handing out copies of one plan to waiting men"),
         "fired": ("A0147", "other", False, "ai", "AI clip: the fired trainer carries his box out while a robot spots a lifter (clip library: concepts-and-gags)"),
         "tour": ("B0034", "none", False, "none", "real app recording: Monday's workout list; in the 16:9 a phone panel beside Dan on camera (s06_beside16.py)"),
         "flow_a": ("B0049", "other", True, "none", "the app's generating screen with the sample man's own upload (a man who is NOT Dan, VIDEO-RULES 2026-09-12)"),
         "flow_b": ("B0049", "other", True, "ai", "the app's AI result for the same man (from 28.0 s, after the banned before/after screen)"),
         "tour2": ("B0544", "none", False, "none", "real app recording: meal photo analysed to 775 cal; in the 16:9 a phone panel beside Dan on camera"),
         "I4": ("I4", "other", False, "ai", "round 3 Kling clip: the trainer leaves through the door while the robot waves")}
SRC_IN = {"split": 135.5, "I3": 0.0, "I1": 0.0, "fired": 0.0, "tour": 0.0, "flow_a": 13.0, "flow_b": 28.0, "tour2": 6.05, "I4": 0.25}
R3M = "/Volumes/Extreme/_edit_work/ra06/round3/motion"
CP.update({"I3": f"{R3M}/I3_v1.mp4", "I1": f"{R3M}/I1_v1.mp4", "I4": f"{R3M}/I4_v2.mp4",
           "C1683": "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1683.MP4"})
pictures = []
for nm, (asset, ppl, phys, lk, why) in FACTS.items():
    c = cards[nm]; path = CP.get(asset) or os.path.abspath(asset)
    pictures.append(dict(id=nm, t0=c["beat"][0], t1=c["beat"][1], kind="photo" if path.endswith(".png") else "clip",
                         sources=[dict(path=path, src_in=SRC_IN[nm])], label_kind=lk, label="AI-GENERATED" if lk == "ai" else None,
                         label_source="round4/chips/chips.json (the chip drawn on this card)", people=ppl, physique=phys, people_source=why,
                         approved_crop=None, card_kind=c["kind"]))
audio = dict(mix=master, untreated=os.path.abspath("cut_audio.wav"), gate_stamp=master + ".audio_gate.json",
             chain=os.path.abspath("mix.wav.voice_chain.json"), music=os.path.abspath("music/Realizer.mp3"))
dec = json.load(open("round3-plan/decisions.json")); d4 = json.load(open("round4-plan/decisions.json"))
approvals = dict(status="approved" if approved else "pending", round=4, source=os.path.abspath("round4-plan/decisions.json"), full_film=approved,   # round 4 review N8: Dan's 2026-10-15 words approve the 9:16; the 16:9 is pending until he rules on it
                 note="9:16 approved 2026-10-15: " + d4["dan_words_verbatim"] + " The 16:9 has not been seen by Dan.",
                 decisions=[dict(id=i["id"], verdict=i["verdict"], words=i.get("words")) for i in dec["items"]])
S = dict(schema=validate.SCHEMA, job="RA-06", title="What's The Best Ab Exercise?", type="AD", editor="claude", video=V, grade=grade, edl=edl,
         framing=fr_rows, words=words, graphics=graphics, pictures=pictures, audio=audio, approvals=approvals,
         provenance=dict(written=time.strftime("%Y-%m-%dT%H:%M:%S"), by="ra06 round4/s_sheet06.py (RA-06 build, shared schema and validator)",
                         build_dir=B, inputs={f: SFC.sha(f) for f in ("cut.json", "beats.json", "timeline_16x9.json", "framing.json", "grade.json")}))
E = validate.check(S, do_hash=False)
out = master[:-4] + ".edit-sheet.json"
if E:
    json.dump(S, open(out + ".INCOMPLETE.json", "w"), indent=1); print("INCOMPLETE"); [print(" -", e) for e in E]; sys.exit(1)
json.dump(S, open(out, "w"), indent=1)
print(out, len(edl), "segments", len(graphics), "graphics", len(pictures), "pictures")
