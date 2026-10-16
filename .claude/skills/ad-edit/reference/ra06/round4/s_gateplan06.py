#!/usr/bin/env python3
"""RA-06 round 4: the delivery-gate plan for one master.   python3 round4/s_gateplan06.py 9x16|16x9 <master>
(RA-15 round 3 s_gateplan15.py method.) Built only from the locked parts and measurements on the delivered file:
beats.json, cut.json, hf9|hf16 manifest + plates, cards_<key>/meta.json + split.json, cap_<key>/caption_states.json, round4/chips/chips.json,
round4/speech_<key>.json (CTC on the delivered audio), round4/transcript_<key>.json (Whisper on the delivered file),
logs/negative_scan_<key>.json, round4/junk_<key>.json."""
import hashlib, json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
import ra01lib as L
KEY, MASTER = sys.argv[1], os.path.abspath(sys.argv[2]); FPS = L.FPS
W, H = (1080, 1920) if KEY == "9x16" else (1920, 1080)
PL = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
MAN = {m["id"]: m for m in json.load(open("hf9/manifest.json" if KEY == "9x16" else "hf16/manifest.json"))}
PLATES = json.load(open("hf9/plates.json" if KEY == "9x16" else "hf16/plates.json"))
SPLIT = json.load(open(f"cards_{KEY}/split.json"))
CAP = json.load(open(f"cap_{KEY}/caption_states.json"))["states"]
CH = json.load(open("round4/chips/chips.json"))
CARD = {c["name"]: c for c in PL["cards"]}
if KEY == "16x9" and os.path.exists("round4/r4_16x9_overrides.json"):   # the split holds k frames longer in 16:9 (see that file)
    _k = json.load(open("round4/r4_16x9_overrides.json"))["split_hold_frames"]; _t = round((PL["timeline"][0]["f1"] + _k) / FPS, 6)
    CARD["split"] = dict(CARD["split"], beat=[0.0, _t]); PL["cards"] = [CARD[c["name"]] for c in PL["cards"]]
    PL["punch"] = [dict(p, beat=[_t, p["beat"][1]]) if abs(p["beat"][0] - PL["timeline"][1]["a"]) < 1e-3 else p for p in PL["punch"]]
    PL["timeline"] = [dict(PL["timeline"][0], f1=PL["timeline"][0]["f1"] + _k), dict(PL["timeline"][1], f0=PL["timeline"][1]["f0"] + _k)] + PL["timeline"][2:]
    for _nm, _lv in json.load(open("round4/r4_16x9_overrides.json")).get("level16", {}).items():   # 16:9-only shot sizes
        _t = next(t for t in PL["timeline"] if t["name"] == _nm)
        PL["punch"] = [dict(p, level=_lv) if abs(p["beat"][0] - _t["a"]) < 1e-3 else p for p in PL["punch"]]
END_T = round(PL["total_frames"] / FPS, 6)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SHA = sha256(MASTER)
rect = lambda b: [int(b[0]), int(b[1]), int(b[2] - b[0]), int(b[3] - b[1])]
audio_joins = [round(p["t_out"], 3) for p in CUT["pieces"][:-1]]
joins = sorted(set(audio_joins) | {round(s["t"], 3) for s in CUT.get("seams", [])})
card_beats = [list(c["beat"]) for c in PL["cards"]]
spans = sorted([(p["beat"][0], min(p["beat"][1], END_T), p["level"], False) for p in PL["punch"]] + [(a, b, "CARD", True) for a, b in card_beats])
windows = [dict(name=it["name"], beat=[round(it["f0"] / FPS, 6), min(END_T, round(it["f1"] / FPS, 6))], rect=[0, 0, W, H],
                motion="tracking" if KEY == "9x16" else "fixed-wide") for it in PL["timeline"] if it["kind"] == "dan"]
AI = ["I3", "I1", "fired", "flow_b", "I4"]
chip = lambda nm: dict(chip=CH[f"{KEY}_{nm}"]["png"], pos=CH[f"{KEY}_{nm}"]["pos"])
ai_inserts = [dict(name=nm, beat=CARD[nm]["beat"], **chip(nm)) for nm in AI]
LTS = [k for k in MAN if k != "CTA"]
graphics = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], mov=MAN[k]["mov"]) for k in LTS + ["CTA"]] +
            [dict(name=nm, beat=CARD[nm]["beat"], mov=os.path.abspath(f"cards_{KEY}/{nm}.mp4")) for nm in CARD])
regions = [dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], rect=rect(MAN[k]["box"])) for k in LTS + ["CTA"]]
for nm in AI:
    regions.append(dict(name=nm + "_chip", beat=CARD[nm]["beat"], rect=rect(CH[f"{KEY}_{nm}"]["box"])))
for nm, pl in PLATES.items():
    regions.append(dict(name=nm + "_hole", beat=CARD[nm]["beat"], rect=rect(pl["hole"])))
for i, b in enumerate(SPLIT["label_boxes"]):
    regions.append(dict(name=f"split_label{i}", beat=CARD["split"]["beat"], rect=rect(b)))
if KEY == "16x9":
    for p in SPLIT["panels"]:
        x, y, w, h = p["box"]; regions.append(dict(name="split_" + p["roll"], beat=CARD["split"]["beat"], rect=[x, y, w, h]))
states = [dict(name=s["name"], beat=s["beat"], image=s["image"], image_sha256=sha256(s["image"]), rect=s["rect"], word=s["word"]) for s in CAP]
SPEECH = json.load(open(f"round4/speech_{KEY}.json"))["words"]
TX = json.load(open(f"round4/transcript_{KEY}.json"))["words"]
WORDS = json.load(open("words_aligned.json"))["words"]
NEG = json.load(open(f"logs/negative_scan_{KEY}.json")); assert NEG["sha256"] == SHA, "negative scan was made on another file"
full = ("the AI clips (I3, I1, fired, I4) fill the frame and carry captions over the picture by design, and the split screen's bottom (vacuum) "
        "panel carries the caption band under his chin (round 1 lesson 8); every phone plate ends above the 1376 caption line") if KEY == "9x16" \
       else "no card fills the frame in 16:9: every plate and the split screen end at y 892/900, above the 930 caption line"
plan = {
    "target_seconds": END_T, "target_frames": PL["total_frames"],
    "joins": joins, "audio_joins": audio_joins, "covered": card_beats,
    "punch": [[a, b, lv] for a, b, lv, _ in spans], "punch_covered": [cv for *_, cv in spans], "talking_head_windows": windows,
    "graphics": graphics, "ai_inserts": ai_inserts, "real_photos": [], "cards": [],
    "_cards_why": ("`cards` lists FULL-SCREEN beats a caption may not sit on. None: " + full + " (RA-01 rule 5: captions run from the first "
                   "word to the last; the 9:16 approved by Dan 2026-10-15). Every hole, chip, label, the lower third and the CTA are in "
                   "graphic_regions with their measured rectangles, so captions:graphic_clearance grades them in delivered pixels."),
    "_labels_why": ("tour/tour2 (B0034, B0544) and flow_a (B0049's generating screen with the man's own real upload) are real app "
                    "recordings with no AI imagery; the split screen is Dan's real exercise B-roll, not a result picture."),
    "label_chips": {"ai": CH[f"{KEY}_I3"]["png"], "real": CH[f"{KEY}_real"]["png"]},
    "label_pos": {"ai": CH[f"{KEY}_I3"]["pos"], "real": CH[f"{KEY}_real"]["pos"]},
    "srt": os.path.abspath(f"cap_{KEY}/captions.srt"),
    "evidence_contract": {"version": 2, "video_sha256": SHA},
    "caption_states": states, "graphic_regions": regions,
    "speech_words": SPEECH, "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
    "words": [dict(w=w["w"], t=w["t"], e=w["e"]) for w in WORDS],
    "transcript_words": [dict(w=w) for w in TX],
    "source_audio": os.path.abspath("cut_audio.wav"),
    "banned_source": json.load(open("clip_paths.json"))["B0049"], "banned_times": [26.5, 27.5, 29.5, 31.0],
    "watch_log": os.path.abspath(f"round4/watch_{KEY}/logs/watch_pass.json"),
    "source_picture": os.path.abspath(f"seg_{KEY}/base.mp4"),
    "negative_events_scan": NEG,
    "junk_report": os.path.abspath(f"round4/junk_{KEY}.json"),
}
json.dump(plan, open(f"round4/plan_{KEY}.json", "w"), indent=1)
print(f"round4/plan_{KEY}.json  sha {SHA[:12]}  joins {len(joins)}  punch {len(plan['punch'])}  ai {len(ai_inserts)}  graphics {len(graphics)}  "
      f"regions {len(regions)}  states {len(states)}  speech {len(SPEECH)}  tx {len(TX)}")
