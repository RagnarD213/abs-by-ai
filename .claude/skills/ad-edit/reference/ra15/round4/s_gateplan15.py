#!/usr/bin/env python3
"""RA-15 round 3: the delivery-gate plan for one master.   python3 round4/s_gateplan15.py 9x16|16x9 <master>
(RA-14 round 4 s93_gateplan.py method.) Built only from the locked parts and measurements on the delivered file:
beats.json, cut.json, hf9|hf16 manifest + plates, cards_<key>/meta.json, cap_<key>/caption_states.json, round4/chips/chips.json,
round4/speech_<key>.json (CTC on the delivered audio), round4/transcript_<key>.json (Whisper on the delivered file),
logs/negative_scan_<key>.json, round4/junk_<key>.json."""
import hashlib, json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
import ra01lib as L
KEY, MASTER = sys.argv[1], os.path.abspath(sys.argv[2]); FPS = L.FPS
W, H = (1080, 1920) if KEY == "9x16" else (1920, 1080)
PL = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
MAN = {m["id"]: m for m in json.load(open("hf9/manifest.json" if KEY == "9x16" else "hf16/manifest.json"))}
PLATES = json.load(open("hf9/plates.json" if KEY == "9x16" else "hf16/plates.json"))
META = json.load(open(f"cards_{KEY}/meta.json")); AN = json.load(open("round4/analysis_hf.json"))[KEY]
CAP = json.load(open(f"cap_{KEY}/caption_states.json"))["states"]
CH = json.load(open("round4/chips/chips.json"))
CARD = {c["name"]: c for c in PL["cards"]}
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
AI = ["opener", "flow", "analysis", "fridge", "enjoy", "restaurant", "lock"]
chip = lambda nm: dict(chip=CH[f"{KEY}_{nm}"]["png"], pos=CH[f"{KEY}_{nm}"]["pos"])
ai_inserts = [dict(name=nm, beat=CARD[nm]["beat"], **chip(nm)) for nm in AI]
graphics = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], mov=MAN[k]["mov"]) for k in ("LT1", "LT2", "LT3", "CTA")] +
            [dict(name=nm, beat=CARD[nm]["beat"], mov=os.path.abspath(f"cards_{KEY}/{nm}.mp4")) for nm in CARD])
regions = [dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], rect=rect(MAN[k]["box"])) for k in ("LT1", "LT2", "LT3", "CTA")]
for nm in AI:
    regions.append(dict(name=nm + "_chip", beat=CARD[nm]["beat"], rect=rect(CH[f"{KEY}_{nm}"]["box"])))
for nm, pl in PLATES.items():
    if nm not in CARD: continue
    regions.append(dict(name=nm + "_hole", beat=CARD[nm]["beat"], rect=rect(pl["hole"])))
regions.append(dict(name="analysis_card", beat=CARD["analysis"]["beat"], rect=rect(AN["meta"]["card"])))
regions.append(dict(name="analysis_photo", beat=CARD["analysis"]["beat"], rect=rect(AN["meta"]["photo"])))
states = [dict(name=s["name"], beat=s["beat"], image=s["image"], image_sha256=sha256(s["image"]), rect=s["rect"], word=s["word"]) for s in CAP]
SPEECH = json.load(open(f"round4/speech_{KEY}.json"))["words"]
TX = json.load(open(f"round4/transcript_{KEY}.json"))["words"]
WORDS = json.load(open("words_aligned.json"))["words"]
NEG = json.load(open(f"logs/negative_scan_{KEY}.json")); assert NEG["sha256"] == SHA, "negative scan was made on another file"
full = "the opener (A0016), the three AI clips (fridge, restaurant, lock) and the steak clip fill the frame and carry captions over the picture by design" if KEY == "9x16" \
       else "the opener (A0016) and the steak clip (A0086) fill the frame and carry captions over the picture by design; every other card ends at y 892 above the 930 caption line"
plan = {
    "target_seconds": END_T, "target_frames": PL["total_frames"],
    "joins": joins, "audio_joins": audio_joins, "covered": card_beats,
    "punch": [[a, b, lv] for a, b, lv, _ in spans], "punch_covered": [cv for *_, cv in spans], "talking_head_windows": windows,
    "graphics": graphics, "ai_inserts": ai_inserts, "real_photos": [], "cards": [],
    "_cards_why": ("`cards` lists FULL-SCREEN beats a caption may not sit on. None: " + full + " (RA-01 rule 5: captions run from the first "
                   "word to the last, approved by Dan in round 2 on this film). Every hole, chip, lower third, the CTA and the analysis card "
                   "are in graphic_regions with their measured rectangles, so captions:graphic_clearance grades them in delivered pixels."),
    "_labels_why": "macro (B0038) is not in ai_inserts: a real app recording of a real salmon plate photo, no AI imagery and no person.",
    "label_chips": {"ai": CH[f"{KEY}_opener"]["png"], "real": CH[f"{KEY}_real"]["png"]},
    "label_pos": {"ai": CH[f"{KEY}_opener"]["pos"], "real": CH[f"{KEY}_real"]["pos"]},
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
