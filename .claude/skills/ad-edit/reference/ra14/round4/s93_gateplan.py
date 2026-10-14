#!/usr/bin/env python3
"""RA-14 round 4: the delivery-gate plan for the 9:16 master.  python3 round4/s93_gateplan.py  (from /Volumes/Extreme/_edit_work/ra14)

Built only from the locked round 3 parts and measurements on the delivered file (nothing typed in):
  beats_r3.json (timeline, punch, cards, overlays), cut.json (audio splices, take seams), round3/gfx/manifest.json
  (graphic boxes), round3/cap_9x16/caption_states.json (the PNG states the compositor laid), round3/cards/cards.json
  (phone box, which P1 frames carry which chip), round4/chips/chips.json (s92_chips.py), round4/speech_9x16.json
  (CTC on the delivered audio), round4/transcript_9x16.json (Whisper on the delivered file), round4/logs/negative_scan_9x16.json.
"""
import hashlib, json, os, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L

FPS = L.FPS
R4 = os.path.abspath("round4")
MASTER = f"{R4}/the cheat code for six pack abs | claude | 9x16 | RA-14.mp4"
PL = json.load(open("beats_r3.json")); CUT = json.load(open("cut.json"))
MAN = {m["id"]: m for m in json.load(open("round3/gfx/manifest.json"))}
CAP = json.load(open("round3/cap_9x16/caption_states.json"))["states"]
CARDS = json.load(open("round3/cards/cards.json"))
CH = json.load(open(f"{R4}/chips/chips.json"))
CARD = {c["name"]: c for c in PL["cards"]}
# round 4 ends the film on the held smile (s95_trim.py): every span that ran to the old end stops at the new one
TRIM = json.load(open(f"{R4}/trim.json")) if os.path.exists(f"{R4}/trim.json") else None
END_F = TRIM["end_frames"] if TRIM else PL["total_frames"]
END_T = round(END_F / FPS, 6)
clamp = lambda t: min(t, END_T)
for m in MAN.values(): m["b"] = clamp(m["b"])


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


SHA = sha256(MASTER)
rect = lambda b: [int(b[0]), int(b[1]), int(b[2] - b[0]), int(b[3] - b[1])]

# audio splices on the delivered timeline (the opener plays over the first line, so cut time == film time) + the take seams
acc, audio_joins = 0.0, []
for a, b in CUT["keeps"][:-1]:
    acc += b - a; audio_joins.append(round(acc, 3))
joins = sorted(set(audio_joins) | {round(s["t"], 3) for s in CUT["seams"]})

card_beats = [list(c["beat"]) for c in PL["cards"]]
# `punch` lists every span in film order, the full-screen cards included as COVERED segments: the gate's cut:jump_cut
# compares neighbours in this list, and a NEAR shot either side of a full-screen card (A1, T1) is a cutaway, not a
# jump (gate docstring: "a segment hidden under a full-frame insert or card carries the previous level on purpose").
spans = [(p["beat"][0], clamp(p["beat"][1]), p["level"], False) for p in PL["punch"]] + [(a, b, "CARD", True) for a, b in card_beats]
spans.sort()
punch = [[a, b, lv] for a, b, lv, _ in spans]
punch_covered = [cv for *_, cv in spans]
# one full-frame talking-head window per hold of Dan (beats_r3 timeline kind "dan"): the framing rows otherwise drop
# every beat a lower third, R1 or the button sits over him, and measured 11 samples in 50 s
windows = [dict(name=it["name"], beat=[round(it["f0"] / FPS, 6), clamp(round(it["f1"] / FPS, 6))], rect=[0, 0, 1080, 1920], motion="tracking")
           for it in PL["timeline"] if it["kind"] == "dan"]
PH = json.load(open(f"{R4}/phone_rects.json"))

# P1 is two pictures: his REAL photo on the phone (demo frame 78 on, card frames 18..47), then the AI result card (48..100)
p1a = CARD["P1"]["beat"][0]
log = CARDS["P1"]["log"]
real_f = [e["f"] for e in log if e.get("chip") == "Real picture of me. Not AI-generated."]
ai_f = [e["f"] for e in log if e.get("chip") == "AI-GENERATED"]
assert real_f == list(range(real_f[0], real_f[-1] + 1)) and ai_f == list(range(ai_f[0], ai_f[-1] + 1))
p1_real = [round(p1a + real_f[0] / FPS, 6), round(p1a + (real_f[-1] + 1) / FPS, 6)]
p1_ai = [round(p1a + ai_f[0] / FPS, 6), CARD["P1"]["beat"][1]]

chip = lambda k: dict(chip=CH[k]["png"], pos=CH[k]["pos"])
ai_inserts = [dict(name="O2", beat=CARD["O0"]["beat"], **chip("O2")),
              dict(name="P1_result", beat=p1_ai, **chip("P1_ai")),
              dict(name="A1", beat=CARD["A1"]["beat"], **chip("A1"))]
real_photos = [dict(name="P1_real_photo", beat=p1_real, **chip("P1_real"))]

graphics = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], mov=MAN[k]["mov"]) for k in ("L1", "L2", "L3", "R1", "C1")] +
            [dict(name="O2", beat=CARD["O0"]["beat"], mov=os.path.abspath("round3/opener/O2.mp4")),
             dict(name="P1", beat=CARD["P1"]["beat"], mov=os.path.abspath("round3/cards/P1.mp4")),
             dict(name="A1", beat=CARD["A1"]["beat"], mov=MAN["A1"]["mov"]),
             dict(name="T1", beat=CARD["T1"]["beat"], mov=os.path.abspath("round3/cards/T1.mp4"))])

phone = CARDS["P1"]["phone_box"]
p1_phone_end = round(p1a + CARDS["P1"]["phone_frames"] / FPS, 6)
graphic_regions = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], rect=rect(MAN[k]["box"])) for k in ("L1", "L2", "L3", "R1", "C1")] +
                   [dict(name="O2_chip", beat=CARD["O0"]["beat"], rect=rect(CH["O2"]["box"])),
                    dict(name="P1_phone", beat=[p1a, p1_phone_end], rect=rect(PH["P1"]["rect"])),
                    dict(name="P1_real_chip", beat=p1_real, rect=rect(CH["P1_real"]["box"])),
                    dict(name="P1_ai_chip", beat=p1_ai, rect=rect(CH["P1_ai"]["box"])),
                    dict(name="A1_card", beat=CARD["A1"]["beat"], rect=rect(MAN["A1"]["card"])),
                    dict(name="A1_chip", beat=CARD["A1"]["beat"], rect=rect(MAN["A1"]["chip"])),
                    dict(name="T1_phone", beat=CARD["T1"]["beat"], rect=rect(PH["T1"]["rect"]))])

states = [dict(name=s["name"], beat=s["beat"], image=s["image"], image_sha256=sha256(s["image"]), rect=s["rect"], word=s["word"])
          for s in CAP]
SPEECH = json.load(open(f"{R4}/speech_9x16.json"))["words"]
TX = json.load(open(f"{R4}/transcript_9x16.json"))["words"]
WORDS = json.load(open("words_aligned.json"))["words"]

plan = {
    "target_seconds": END_T, "target_frames": END_F,
    "joins": joins, "audio_joins": audio_joins,
    "covered": card_beats,
    "punch": punch, "punch_covered": punch_covered, "talking_head_windows": windows,
    "graphics": graphics, "ai_inserts": ai_inserts, "real_photos": real_photos,
    "cards": [],
    "_cards_why": ("`cards` is the gate's list of FULL-SCREEN beats a caption may not sit on. None here: every card stops above "
                   "the caption line (P1/T1 phones end at y 1348, measured on every card frame by s94_phonebox.py; the shell image's box reaches 1386 with transparent padding, A1 at 1376; captions start at 1400) and two picture beats carry captions over the picture by design: the opener O2 and P1's AI result card (15.78-17.55 s, the caption runs over the bottom of the goal photo; RA-01 rule 5, 'captions run from the first word to the last, over photo cards too'). Both are in the first 30 s Dan approved finished on 2026-10-14. The opener carries "
                   "its captions by Dan's approval of round 3 (MadMuscles captions run first word to last). The phones, A1's card and every "
                   "chip are in `graphic_regions` with their measured rectangles, so captions:graphic_clearance grades those gaps "
                   "in delivered pixels; P1's result photo is left out of it because the caption runs over it by design."),
    "_labels_why": ("T1 (app tour) is not in ai_inserts: its only AI picture is the app's own Push-Up demo of a clothed "
                    "trainer (beats_r3 physique false), which carries the app's own AI-GENERATED chip inside the screen "
                    "recording at phone-screen size. The independent reviewer checks it by eye."),
    "label_chips": {"ai": CH["O2"]["png"], "real": CH["P1_real"]["png"]},
    "label_pos": {"ai": CH["O2"]["pos"], "real": CH["P1_real"]["pos"]},
    "srt": os.path.abspath("round3/cap_9x16/captions.srt"),
    "evidence_contract": {"version": 2, "video_sha256": SHA},
    "caption_states": states, "graphic_regions": graphic_regions,
    "speech_words": SPEECH, "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
    "words": [dict(w=w["w"], t=w["t"], e=w["e"]) for w in WORDS],
    "transcript_words": [dict(w=w) for w in TX],
    "source_audio": os.path.abspath("cut_audio.wav"),
    "banned_source": ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                      "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4"),
    "banned_times": [26.5, 27.5, 29.5, 31.0],
    "watch_log": f"{R4}/watch/logs/watch_pass.json",
    "negative_events_scan": json.load(open(f"{R4}/logs/negative_scan_9x16.json")),
    "junk_report": os.path.abspath("junk_report.json"),
}
assert plan["negative_events_scan"]["sha256"] == SHA, "negative scan was made on another file"
json.dump(plan, open(f"{R4}/plan.json", "w"), indent=1)
print(f"plan.json  sha {SHA[:12]}  joins {len(joins)}  punch {len(punch)}  ai {len(ai_inserts)} real {len(real_photos)}  "
      f"graphics {len(graphics)}  states {len(states)}  speech {len(SPEECH)}  tx {len(TX)}")
print("P1 real", p1_real, "P1 ai", p1_ai)
