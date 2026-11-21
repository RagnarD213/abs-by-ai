#!/usr/bin/env python3
"""RA-04 round 3: the edit sheet for the 16:9 master (_shared/edit-sheet README).  python3 round5/s_sheet15.py <master 16x9> [--approved "..."]
The shared writer's adkit path is RA-01's (every card is Dan with physique, graphics are adkit:*), which is wrong for this film, so
this writes the same schema from RA-04's own build files with its helpers (video_block, sha) and the shared validator:
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
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
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
                        measured="framing.json (5 fps on the raw roll) + framing_holdstart.json; 16:9 crops fixed, one centre for the film (horizontal stays static)"))
grade = dict(filter=L.grade(gr["exposure"], gr["saturation"]), lut=None, decode="bt709", order="at_source_size",
             note="RA-01 approved grade (8/28 S-Log3 LUT, exposure %s, saturation %s), s32_grade.py" % (gr["exposure"], gr["saturation"]))
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
an = json.load(open("cards_16x9/analysis.json")); a0, a1 = cards["analysis"]["beat"]
graphics.append(dict(id="A1", template="adkit:analysis_card", config=dict(aspect="16x9", image=an["image"], rows=an["rows"], footer=an["footer"],
                     label=an["label"], chip_text="AI-GENERATED", chip_pos=an["chip_pos"], photo_box=an["photo_box"], card_rect=an["card_rect"], dur=an["dur"],
                     palette="Soft Blue (s06_inserts04.py patches AC.LIME/OLIVE/PLAN_GREEN, cardlib.field; Dan 2026-10-14 D2: the blue graphic)"),
                     text=["AI-GENERATED"] + an["rows"] + [an["footer"]], t0=a0, t1=a1, layer="full", driven_by=[]))
# who is in each picture (people / physique / label) -- the facts, by eye on the used frames and the clip library
FACTS = {"gen": ("round5/gen_white_man_rec.mp4", "other", True, "ai", "round 5: a heavier white man (NOT Dan; AI-generated before photo, Codex) in the app's real generation on absbyai.com: loader, then his AI result alone (the app's before/after pair hidden in the page, never rendered)"),
         "lock": ("round5/lock_src.mp4", "other", True, "ai", "round 5: A0074's phone on marble with the white man's AI result as the lock screen (r5_lock.py); not Dan"),
         "flow_a": ("B0049", "other", True, "none", "the app's generate screen with the demo man's real before photo; he is NOT Dan (VIDEO-RULES 2026-09-12)"),
         "flow_b": ("B0049", "other", True, "ai", "the same man's AI result screen alone (B0049 from 28.0 s, after the banned before/after screen)"),
         "analysis": ("media/after_man.png", "other", True, "ai", "the same man's AI result (B0049 at 29.6 s)"),
         "tour": ("B0544", "dan", False, "none", "the app's real screens; its AI-Dan push-up demo carries the app's own burned AI-GENERATED badge"),
         "brokenarm": ("media/ai1.mp4", "other", False, "ai", "round 3 AI clip (Veo 3.1 Fast): a man with a broken arm at the squat rack, then the leg press"),
         "home": ("B0464", "dan", False, "none", "Dan's real bodyweight squats on the lawn: moving workout footage illustrating 'a home workout', not a physique result; no label (VIDEO-RULES 2026-09-16: the real-picture label is for still physique photos)")}
SRC_IN = {"gen": 3.40, "lock": 0.0, "flow_a": 6.3, "flow_b": 28.0, "analysis": 0.0, "tour": 6.05, "brokenarm": 0.0, "home": 0.2}
pictures = []
for nm, (asset, ppl, phys, lk, why) in FACTS.items():
    c = cards[nm]; path = CP.get(asset) or os.path.abspath(asset)
    pictures.append(dict(id=nm, t0=c["beat"][0], t1=c["beat"][1], kind="photo" if path.endswith(".png") else "clip",
                         sources=[dict(path=path, src_in=SRC_IN[nm])], label_kind=lk, label="AI-GENERATED" if lk == "ai" else None,
                         label_source="round5/chips/chips.json (the chip drawn on this card)", people=ppl, physique=phys, people_source=why,
                         approved_crop=None, card_kind=c["kind"]))
audio = dict(mix=master, untreated=os.path.abspath("cut_audio.wav"), gate_stamp=master + ".audio_gate.json",
             chain=os.path.abspath("mix_r5.wav.voice_chain.json"), music=os.path.abspath("music/Realizer.mp3"))
dec = json.load(open("round3-plan/decisions.json")); dec5 = json.load(open("round5-plan/decisions.json"))
approvals = dict(status="approved" if approved else "pending", round=5, source=os.path.abspath("round5-plan/decisions.json"), full_film=approved,
                 decisions=[dict(id=i["id"], verdict=i["verdict"], words=i.get("words")) for i in json.load(open("round2-plan/decisions.json"))["items"] + dec["items"]]
                 + [dict(id="round3_motion", verdict=dec["round3_motion"]["verdict"], words=dec["round3_motion"].get("dan_words_verdict"))]
                 + [dict(id=i["id"], verdict=i["verdict"], words=i.get("words")) for i in dec5["items"]])
S = dict(schema=validate.SCHEMA, job="RA-04", title="Top 3 Tips For Getting Abs", type="AD", editor="claude", video=V, grade=grade, edl=edl,
         framing=fr_rows, words=words, graphics=graphics, pictures=pictures, audio=audio, approvals=approvals,
         provenance=dict(written=time.strftime("%Y-%m-%dT%H:%M:%S"), by="ra04 round5/s_sheet15.py (RA-04 build, shared schema and validator)",
                         build_dir=B, inputs={f: SFC.sha(f) for f in ("cut.json", "beats.json", "timeline_16x9.json", "framing.json", "grade.json")}))
E = validate.check(S, do_hash=False)
out = master[:-4] + ".edit-sheet.json"
if E:
    json.dump(S, open(out + ".INCOMPLETE.json", "w"), indent=1); print("INCOMPLETE"); [print(" -", e) for e in E]; sys.exit(1)
json.dump(S, open(out, "w"), indent=1)
print(out, len(edl), "segments", len(graphics), "graphics", len(pictures), "pictures")
