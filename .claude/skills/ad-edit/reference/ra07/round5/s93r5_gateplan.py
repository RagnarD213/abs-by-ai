#!/usr/bin/env python3
"""RA-07 round 5 (from round 3's s93r3): the delivery-gate plan for the 9:16 master (RA-14 round 4 s93_gateplan.py, adapted).

Built only from locked parts and measurements on the delivered file:
  PLAN (beats_r3_cam.json: the film as delivered), cut.json, round2/gfx/manifest.json (L1-L3, C1), cap_9x16/caption_states.json,
  round2/cards/cards.json (P1 real-photo / AI-result frames), round3/phone_rects.json (measured phone bottoms), round3/chips/chips.json,
  round3/delivered_words.json (Whisper large-v3 on the delivered audio), round3/logs/negative_scan_9x16.json.
  python3 round3/s93r3_gateplan.py     (from /Volumes/Extreme/_edit_work/ra07)  -> round3/plan.json
"""
import hashlib, json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L

FPS = L.FPS
R3 = os.path.abspath("round5"); R3OLD = os.path.abspath("round3")
MASTER = f"{R3}/deliver/fire your trainer | claude | 9x16 | RA-07.mp4"
PL = json.load(open(os.environ.get("PLAN", "beats_r5.json"))); CUT = json.load(open("cut.json"))
MAN = {m["id"]: m for m in json.load(open("round2/gfx/manifest.json"))}
CAP = json.load(open("cap_9x16/caption_states.json"))["states"]
CARDS = json.load(open("round2/cards/cards.json"))
CH = json.load(open(f"{R3}/chips/chips.json")); PH = json.load(open(f"{R3OLD}/phone_rects.json"))
CARD = {c["name"]: c for c in PL["cards"]}
END_F = PL["total_frames"]; END_T = round(END_F / FPS, 6)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


SHA = sha256(MASTER)
rect = lambda b: [int(b[0]), int(b[1]), int(b[2] - b[0]), int(b[3] - b[1])]
acc, audio_joins = 0.0, []
for a, b in CUT["keeps"][:-1]:
    acc += b - a; audio_joins.append(round(acc, 3))
joins = sorted(set(audio_joins) | {round(s["t"], 3) for s in CUT["seams"]})
card_beats = [list(c["beat"]) for c in PL["cards"]]
spans = [(p["beat"][0], p["beat"][1], p["level"], False) for p in PL["punch"]] + [(a, b, "CARD", True) for a, b in card_beats]
spans.sort()
punch = [[a, b, lv] for a, b, lv, _ in spans]; punch_covered = [cv for *_, cv in spans]
windows = [dict(name=it["name"], beat=[round(it["f0"] / FPS, 6), round(it["f1"] / FPS, 6)], rect=[0, 0, 1080, 1920], motion="tracking")
           for it in PL["timeline"] if it["kind"] == "dan"]

# P1: his REAL photo on the phone (card frames with the real chip), then the AI result card
p1a = CARD["P1"]["beat"][0]; log = CARDS["P1"]["log"]
real_f = [e["f"] for e in log if e.get("chip") == "Real picture of me. Not AI-generated."]
ai_f = [e["f"] for e in log if e.get("chip") == "AI-GENERATED"]
assert real_f == list(range(real_f[0], real_f[-1] + 1)) and ai_f == list(range(ai_f[0], ai_f[-1] + 1))
p1_real = [round(p1a + real_f[0] / FPS, 6), round(p1a + (real_f[-1] + 1) / FPS, 6)]
p1_ai = [round(p1a + ai_f[0] / FPS, 6), CARD["P1"]["beat"][1]]
p1_phone_end = round(p1a + CARDS["P1"]["phone_frames"] / FPS, 6)

chip = lambda k: dict(chip=CH[k]["png"], pos=CH[k]["pos"])
CLIPS = [c for c in ("H1", "A1", "G1", "M1", "O1", "H2", "I5") if c in CARD]
A1B = CARD["A1"]["beat"]; A1_SPLIT = round(A1B[0] + 34 * L.FD, 6)       # piece 0 is 34 film frames (s75r5 SRC A1), piece 1 the rest
a1_parts = [dict(name="A1_p0", beat=[A1B[0], A1_SPLIT], **chip("A1_p0")), dict(name="A1_p1", beat=[A1_SPLIT, A1B[1]], **chip("A1_p1"))]
ai_inserts = ([dict(name=c, beat=CARD[c]["beat"], **chip(c)) for c in CLIPS if c != "A1"] + a1_parts +
              [dict(name="P1_result", beat=p1_ai, **chip("P1_ai"))] +
              # K1 pushes in 2.5 % over the card, chip included: one reference per 9-frame window, scaled and placed by that push
              [{k: v for k, v in s.items() if k != "box"} for s in json.load(open(f"{R3}/chips/K1_push.json"))])
real_photos = [dict(name="P1_real_photo", beat=p1_real, **chip("P1_real"))]
clipfile = lambda c: os.path.abspath(f"round2/clips/{c}.mp4" if c == "H1" else f"round5/clips/{c}.mp4")
graphics = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], mov=MAN[k]["mov"]) for k in ("L1", "L2", "L3", "C1")] +
            [dict(name=k, beat=CARD[k]["beat"], mov=os.path.abspath(f"round2/cards/{k}.mp4")) for k in ("P1", "K1", "W1")] +
            [dict(name=c, beat=CARD[c]["beat"], mov=clipfile(c)) for c in CLIPS])
graphic_regions = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], rect=rect(MAN[k]["box"])) for k in ("L1", "L2", "L3", "C1")] +
                   [dict(name="P1_phone", beat=[p1a, p1_phone_end], rect=rect(PH["P1"]["rect"])),
                    dict(name="P1_real_chip", beat=p1_real, rect=rect(CH["P1_real"]["box"])),
                    dict(name="P1_ai_chip", beat=p1_ai, rect=rect(CH["P1_ai"]["box"])),
                    dict(name="K1_phone", beat=CARD["K1"]["beat"], rect=rect(PH["K1"]["rect"])),
                    dict(name="K1_chip", beat=CARD["K1"]["beat"], rect=rect(CH["K1"]["box"])),
                    dict(name="W1_phone", beat=CARD["W1"]["beat"], rect=rect(PH["W1"]["rect"]))] +
                   [dict(name=f"{c}_chip", beat=CARD[c]["beat"], rect=rect(CH[c]["box"])) for c in CLIPS if c != "A1"] +
                   [dict(name=f"{p['name']}_chip", beat=p["beat"], rect=rect(CH[p["name"]]["box"])) for p in a1_parts])
states = [dict(name=s["name"], beat=s["beat"], image=s["image"], image_sha256=sha256(s["image"]), rect=s["rect"], word=s["word"]) for s in CAP]
DW = json.load(open(f"{R3OLD}/delivered_words.json"))["segments"][0]["words"]
# Whisper supplies the words; CTC forced alignment on the delivered audio supplies the times (s96_ctc1.py: one window over the whole 53 s file, so no window edge hands a word the previous word's audio, which misplaced "a", "lose" and "abs" in windowed runs; "20" spelled TWENTY; Whisper word times run ~180 ms late here)
SPEECH = [dict(w=w["w"], t=w["t"], e=w["e"], src="ctc on the delivered audio") for w in json.load(open(f"{R3OLD}/delivered_words_ctc1.json"))["words"]]
WORDS = json.load(open("words_aligned.json"))["words"]
NEG = json.load(open(f"{R3}/logs/negative_scan_9x16.json"))
assert NEG["sha256"] == SHA, "negative scan was made on another file"
plan = {
    "target_seconds": END_T, "target_frames": END_F,
    "joins": joins, "audio_joins": audio_joins, "covered": card_beats,
    "punch": punch, "punch_covered": punch_covered, "talking_head_windows": windows,
    "graphics": graphics, "ai_inserts": ai_inserts, "real_photos": real_photos, "cards": [],
    "_cards_why": ("`cards` is the gate's list of FULL-SCREEN beats a caption may not sit on. None: the phone cards stop above the caption line "
                   "(phones end at y 1348-1358, measured on every frame, round3/phone_rects.json) and every full-screen AI clip carries its captions "
                   "over the picture by design (RA-01 rule 5, Dan approved round 2's first 30 s finished this way). Every phone, chip and lower "
                   "third is in `graphic_regions` with its measured rectangle."),
    "_labels_why": ("W1 (the real AI Trainer screens) is not in ai_inserts: it is a real screen recording; its exercise demo is the app's own "
                    "AI-Dan video at phone-screen size, clothed (beats physique false), and carries no chip in the approved round 2 first 30 s."),
    "label_chips": {"ai": CH["H1"]["png"], "real": CH["P1_real"]["png"]},
    "label_pos": {"ai": CH["H1"]["pos"], "real": CH["P1_real"]["pos"]},
    "srt": os.path.abspath("cap_9x16/captions.srt"),
    "evidence_contract": {"version": 2, "video_sha256": SHA},
    "caption_states": states, "graphic_regions": graphic_regions,
    "speech_words": SPEECH, "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
    "words": [dict(w=w["w"], t=w["t"], e=w["e"]) for w in WORDS],
    "transcript_words": [dict(w=w["word"].strip()) for w in DW],
    "source_audio": os.path.abspath("cut_audio.wav"),
    "banned_source": ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                      "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4"),
    "banned_times": [26.5, 27.5, 29.5, 31.0],
    "watch_log": f"{R3}/deliver/logs/watch_pass.json",
    "negative_events_scan": NEG,
    "junk_report": os.path.abspath("round2/junk_report.json"),
}
json.dump(plan, open(f"{R3}/plan.json", "w"), indent=1)
print(f"plan.json  sha {SHA[:12]}  joins {len(joins)}  punch {len(punch)}  ai {len(ai_inserts)} real {len(real_photos)}  "
      f"graphics {len(graphics)}  states {len(states)}  speech {len(SPEECH)}  windows {len(windows)}")
