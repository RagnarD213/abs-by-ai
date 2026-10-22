#!/usr/bin/env python3
"""RA-14 round 4: the delivery-gate plan for the 9:16 master.  python3 round4/s93_gateplan.py  (from /Volumes/Expansion/_edit_work/RA-09)

Built only from the locked round 3 parts and measurements on the delivered file (nothing typed in):
  beats.json (timeline, punch, cards, overlays), cut.json (audio splices, take seams), r1/gfx/manifest.json
  (graphic boxes), r1/cap_9x16/caption_states.json (the PNG states the compositor laid), r1/cards/cards.json
  (phone box, which P1 frames carry which chip), round4/chips/chips.json (s92_chips.py), round4/speech_9x16.json
  (CTC on the delivered audio), round4/transcript_9x16.json (Whisper on the delivered file), round4/logs/negative_scan_9x16.json.
"""
import hashlib, json, os, sys
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09")
import ra01lib as L

FPS = L.FPS
R4 = os.path.abspath("r1/gate")
MASTER = os.path.abspath(os.environ.get("MASTER", "deliver_r1/do you think ai is changing the world | claude | 9x16 | RA-09 R1.mp4"))
PL = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
MAN = {m["id"]: m for m in json.load(open("r1/gfx/manifest.json"))}
CAP = json.load(open("r1/cap_9x16/caption_states.json"))["states"]
CARDS = json.load(open("r1/cards/cards.json")); CL = json.load(open("r1/cards/clips.json"))
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

# ROUND 2: P1 is the prospect's generation: the phone (chip under it from the frame his AI-made before photo appears), then his AI
# result card (scene_photo chip). Both AI-GENERATED; no real picture anywhere in the ad (W1/D1 are real MOVING footage: no label).
p1a = CARD["P1"]["beat"][0]
log = CARDS["P1"]["log"]
nph = CARDS["P1"]["phone_frames"]
ph_f = [e["f"] for e in log if e.get("chip") == "AI-GENERATED" and e["f"] < nph]
assert ph_f == list(range(ph_f[0], nph)), ph_f
p1_phone_ai = [round(p1a + ph_f[0] / FPS, 6), round(p1a + nph / FPS, 6)]
p1_ai = [round(p1a + nph / FPS, 6), CARD["P1"]["beat"][1]]

chip = lambda k: dict(chip=CH[k]["png"], pos=CH[k]["pos"])
i1a, i1b = CARD["I1"]["beat"]; i1m = round(i1a + 34 / FPS, 6)      # RA-07's A1 card: piece 0 (34 frames) then piece 1 (28), same chip spot
ai_inserts = ([dict(name=k, beat=CARD[k]["beat"], **chip(k)) for k in ("H1", "G1", "G2", "M1")] +
              [dict(name="P1_phone", beat=p1_phone_ai, **chip("P1_phone")),
               dict(name="P1_result", beat=p1_ai, **chip("P1_ai")), dict(name="A1", beat=CARD["A1"]["beat"], **chip("A1")),
               dict(name="I1_p0", beat=[i1a, i1m], **chip("I1_p0")), dict(name="I1_p1", beat=[i1m, i1b], **chip("I1_p1"))])
real_photos = []
OV = ("L1", "C1")
CARDN = ("H1", "G1", "W1", "P1", "T1", "I1", "G2", "M1")
graphics = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], mov=MAN[k]["mov"]) for k in OV] +
            [dict(name=k, beat=CARD[k]["beat"], mov=os.path.abspath(f"r1/cards/{k}.mp4")) for k in CARDN] +
            [dict(name="A1", beat=CARD["A1"]["beat"], mov=MAN["A1"]["mov"])])
p1_phone_end = round(p1a + CARDS["P1"]["phone_frames"] / FPS, 6)
graphic_regions = ([dict(name=k, beat=[MAN[k]["a"], MAN[k]["b"]], rect=rect(MAN[k]["box"])) for k in OV] +
                   [dict(name="W1_card", beat=CARD["W1"]["beat"], rect=rect(CL["W1"]["hole"]))] +
                   [dict(name=f"{k}_chip", beat=CARD[k]["beat"], rect=rect(CH[k]["box"])) for k in ("H1", "G2", "M1")] +
                   [dict(name="I1_p0_chip", beat=[i1a, i1m], rect=rect(CH["I1_p0"]["box"])), dict(name="I1_p1_chip", beat=[i1m, i1b], rect=rect(CH["I1_p1"]["box"])),
                    dict(name="P1_phone", beat=[p1a, p1_phone_end], rect=rect(PH["P1"]["rect"])),
                    dict(name="P1_phone_chip", beat=p1_phone_ai, rect=rect(CH["P1_phone"]["box"])),
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
    "_cards_why": ("RA-09 R1: no beat is a full-screen card a caption may not sit on. H1, I1, G2 and M1 are full-screen AI footage and carry "
                   "captions like footage (their chips sit above the caption line, measured); W1 is a media card ending above the caption line; the "
                   "P1/T1 phones end above it (s94_phonebox.py, every card frame); A1's card ends above it. G1 and P1's result card are photo "
                   "scenes whose caption runs over the bottom of the photo by design (RA-01 rule 5; RA-12 R2, Dan accepted 2026-10-21). Every card, "
                   "phone and chip is in graphic_regions with its measured rectangle."),
    "_labels_why": ("T1 (app tour) is not in ai_inserts: its only AI picture is the app's own Push-Up demo of a clothed "
                    "trainer (beats.json physique false), which carries the app's own AI-GENERATED chip inside the screen "
                    "recording at phone-screen size. The independent reviewer checks it by eye."),
    "label_chips": {"ai": CH["P1_phone"]["png"], "real": CH["P1_real"]["png"]},
    "label_pos": {"ai": CH["P1_phone"]["pos"], "real": CH["P1_real"]["pos"]},
    "srt": os.path.abspath("r1/cap_9x16/captions.srt"),
    "evidence_contract": {"version": 2, "video_sha256": SHA},
    "caption_states": states, "graphic_regions": graphic_regions,
    "speech_words": SPEECH, "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
    "words": [dict(w=w["w"], t=w["t"], e=w["e"]) for w in WORDS],
    "transcript_words": [dict(w=w) for w in TX],
    "source_audio": os.path.abspath("cut_audio.wav"),
    "banned_source": ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                      "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4"),
    "banned_times": [26.5, 27.5, 29.5, 31.0],
    "watch_log": os.path.abspath("deliver_r1/logs/watch_pass.json"),
    "negative_events_scan": json.load(open(f"{R4}/logs/negative_scan_9x16.json")),
    "junk_report": os.path.abspath("r1/gate/junk_9x16.json"),
}
assert plan["negative_events_scan"]["sha256"] == SHA, "negative scan was made on another file"
json.dump(plan, open(f"{R4}/plan.json", "w"), indent=1)
print(f"plan.json  sha {SHA[:12]}  joins {len(joins)}  punch {len(punch)}  ai {len(ai_inserts)} real {len(real_photos)}  "
      f"graphics {len(graphics)}  states {len(states)}  speech {len(SPEECH)}  tx {len(TX)}")
print("P1 phone ai", p1_phone_ai, "P1 result", p1_ai)
