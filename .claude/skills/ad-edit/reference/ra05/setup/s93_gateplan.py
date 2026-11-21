#!/usr/bin/env python3
"""RA-05 setup: the delivery-gate plan for the APPROVED 9:16 master (RA-14 round 4 s93_gateplan.py / RA-04 round 4 s_gateplan04.py
method).   python3 s93_gateplan.py   (any cwd)  -> /Volumes/Extreme/_edit_work/ra05/setup/plan.json

Built only from the locked round 3 parts (read, never written) and measurements on the delivered file, nothing typed in:
  round3/beats.json (timeline, punch, cards, cta, lt, seams), cut.json (audio pieces), hf9/manifest.json (LT1, LT2, CTA, A1 boxes
  and MOVs), cards_9x16/meta.json (open result frame, couch cut frame + chip boxes, scan chip box + note boxes),
  cap_9x16/caption_states.json (the PNG states the compositor laid), words_aligned.json, cut_audio.wav;
  setup/chips/chips.json (s92_chips.py, each chip correlated against the master), setup/holes.json (s94_holes.py, the plates'
  windows measured on every frame), setup/speech_9x16.json (CTC on the delivered audio), setup/transcript_9x16.json (Whisper on
  the delivered file), setup/logs/negative_scan_9x16.json, setup/junk_9x16.json (s90_measure.sh).
"""
import hashlib, json, os, sys
WD = "/Volumes/Extreme/_edit_work/ra05"; R3 = f"{WD}/round3"; S = f"{WD}/setup"
sys.path.insert(0, R3)
import ra01lib as L
FPS = L.FPS; W, H = 1080, 1920
MASTER = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/how ai can get you real six pack abs - RA-05/"
          "how ai can get you real six pack abs | claude | 9x16 | RA-05.mp4")
APPROVED_SHA = "c0a57092fc85b01575d507ec3dcedf28cd1d60b35c1e56ef96f9a298acbcaceb"
PL = json.load(open(f"{R3}/beats.json")); CUT = json.load(open(f"{R3}/cut.json"))
MAN = {m["id"]: m for m in json.load(open(f"{R3}/hf9/manifest.json"))}
META = json.load(open(f"{R3}/cards_9x16/meta.json"))
CAP = json.load(open(f"{R3}/cap_9x16/caption_states.json"))["states"]
CH = json.load(open(f"{S}/chips/chips.json")); HOLE = json.load(open(f"{S}/holes.json"))
CARD = {c["name"]: c for c in PL["cards"]}
END_F = PL["total_frames"]; END_T = round(END_F / FPS, 6)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


SHA = sha256(MASTER); assert SHA == APPROVED_SHA, "the master is not the approved file"
rect = lambda b: [int(b[0]), int(b[1]), int(b[2] - b[0]), int(b[3] - b[1])]
beat = lambda nm: [round(v, 6) for v in CARD[nm]["beat"]]

# the audio was joined at each piece's end (film time; the talk is sped 1.06x inside the pieces); the take seams are R1|R2 ...
audio_joins = [round(p["t_out"], 3) for p in CUT["pieces"][:-1]]
joins = sorted(set(audio_joins) | {round(s["t"], 3) for s in PL["seams"]})
card_beats = [beat(c["name"]) for c in PL["cards"]]
# `punch` lists every span in film order with the full-screen cards as COVERED segments (RA-14 round 4: a NEAR either side of a
# card is a cutaway, not a jump)
spans = sorted([(p["beat"][0], min(p["beat"][1], END_T), p["level"], False) for p in PL["punch"]] + [(a, b, "CARD", True) for a, b in card_beats])
assert all(abs(spans[i][1] - spans[i + 1][0]) < 1e-3 for i in range(len(spans) - 1)) and spans[0][0] == 0 and abs(spans[-1][1] - END_T) < 1e-3
windows = [dict(name=it["name"], beat=[round(it["f0"] / FPS, 6), min(END_T, round(it["f1"] / FPS, 6))], rect=[0, 0, W, H], motion="tracking")
           for it in PL["timeline"] if it["kind"] == "dan"]

# open: the generation flow (the demo man's REAL before photo, not Dan) to the result frame, then the AI result with the plate's chip
o0, o1 = beat("open"); open_ai = [round(o0 + META["open"]["result_frame"] / FPS, 6), o1]
# couch: two Veo takes joined by a cut at meta's cut_frame; both carry the same chip
c0, c1 = beat("couch"); cut_t = round(c0 + META["couch"]["cut_frame"] / FPS, 6)
assert abs(cut_t - CARD["couch"]["cut_at"]) < 1 / FPS, (cut_t, CARD["couch"]["cut_at"])
chip = lambda k: dict(chip=CH[k]["png"], pos=CH[k]["pos"])
ai_inserts = [dict(name="open_result", beat=open_ai, **chip("open")),
              dict(name="couch_A2", beat=[c0, cut_t], **chip("couch")),
              dict(name="couch_B5", beat=[cut_t, c1], **chip("couch")),
              dict(name="lock", beat=beat("lock"), **chip("lock")),
              dict(name="A1", beat=beat("A1"), **chip("A1")),
              dict(name="scan", beat=beat("scan"), **chip("scan"))]

graphics = ([dict(name=k, beat=[MAN[k]["a"], min(MAN[k]["b"], END_T)], mov=MAN[k]["mov"]) for k in ("LT1", "LT2", "CTA", "A1")] +
            [dict(name=nm, beat=beat(nm), mov=f"{R3}/cards_9x16/{nm}.mp4") for nm in ("open", "couch", "lock", "tour", "scan")])
assert [MAN["CTA"]["a"], MAN["CTA"]["b"]] == PL["cta"][0]

a1 = MAN["A1"]; sc0, sc1 = beat("scan")
regions = ([dict(name=k, beat=[MAN[k]["a"], min(MAN[k]["b"], END_T)], rect=rect(MAN[k]["box"])) for k in ("LT1", "LT2", "CTA")] +
           [dict(name="open_window", beat=[o0, o1], rect=rect(HOLE["open"]["rect"])),
            dict(name="open_chip", beat=open_ai, rect=rect(CH["open"]["box"])),
            dict(name="couch_chip", beat=[c0, c1], rect=rect(CH["couch"]["box"])),
            dict(name="lock_chip", beat=beat("lock"), rect=rect(CH["lock"]["box"])),
            dict(name="A1_photo", beat=beat("A1"), rect=rect(a1["photo"])),
            dict(name="A1_chip", beat=beat("A1"), rect=rect(a1["chip"])),
            dict(name="A1_card", beat=beat("A1"), rect=rect(a1["card"])),
            dict(name="tour_window", beat=beat("tour"), rect=rect(HOLE["tour"]["rect"])),
            dict(name="scan_chip", beat=[sc0, sc1], rect=rect(CH["scan"]["box"]))] +
           [dict(name=f"scan_note_{n['dot']}", beat=[round(sc0 + n["lands_card_t"], 6), sc1], rect=rect(n["box"])) for n in META["scan"]["notes"]])

states = [dict(name=s["name"], beat=s["beat"], image=s["image"], image_sha256=sha256(s["image"]), rect=s["rect"], word=s["word"]) for s in CAP]
SPEECH = json.load(open(f"{S}/speech_9x16.json"))["words"]
TX = json.load(open(f"{S}/transcript_9x16.json"))["words"]
WORDS = json.load(open(f"{R3}/words_aligned.json"))["words"]
NEG = json.load(open(f"{S}/logs/negative_scan_9x16.json")); assert NEG["sha256"] == SHA, "negative scan was made on another file"

plan = {
    "target_seconds": END_T, "target_frames": END_F,
    "joins": joins, "audio_joins": audio_joins, "covered": card_beats,
    "punch": [[a, b, lv] for a, b, lv, _ in spans], "punch_covered": [cv for *_, cv in spans], "talking_head_windows": windows,
    "graphics": graphics, "ai_inserts": ai_inserts, "real_photos": [], "cards": [],
    "_cards_why": ("`cards` lists FULL-SCREEN beats a caption may not sit on. None here: the open and tour media-card windows end at "
                   "y 1228 and 1376 (measured on every plate frame, s94_holes.py), the open plate's chip at 1376 and the A1 analysis card "
                   "at 1376, all above the caption line at 1400; couch (AI clip), lock (A0074) and the vertical scan fill the frame and "
                   "carry captions over the picture by design (RA-01 rule 5: captions run from the first word to the last). Dan approved "
                   "the whole film this way on 2026-10-14. Every window, chip, note, lower third, the CTA button and the analysis card "
                   "are in graphic_regions with measured rectangles, so captions:graphic_clearance grades them in delivered pixels."),
    "_labels_why": ("Not in ai_inserts: open before %.3f s (B0049, the app's generate flow with its demo man's REAL before photo; he is "
                    "not Dan and the picture is not AI; the AI result after it is labelled) and tour (B0544, the app's real screens; its "
                    "Push-Up exercise demo is the app's own screen at phone-screen size, as approved on RA-04 round 2; the independent "
                    "reviewer checks it by eye). No real photo of Dan appears in this film; the real chip is a reference only. "
                    "couch is two entries because it is two AI takes joined by a cut at %.3f s." % (open_ai[0], cut_t)),
    "label_chips": {"ai": CH["lock"]["png"], "real": CH["real"]["png"]},
    "label_pos": {"ai": CH["lock"]["pos"], "real": CH["real"]["pos"]},
    "srt": f"{R3}/cap_9x16/captions.srt",
    "evidence_contract": {"version": 2, "video_sha256": SHA},
    "caption_states": states, "graphic_regions": regions,
    "speech_words": SPEECH, "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
    "words": [dict(w=w["w"], t=w["t"], e=w["e"]) for w in WORDS],
    "transcript_words": [dict(w=w) for w in TX],
    "source_audio": f"{R3}/cut_audio.wav",
    "banned_source": json.load(open(f"{R3}/clip_paths.json"))["B0049"], "banned_times": [26.5, 27.5, 29.5, 31.0],
    "watch_log": f"{S}/watch/logs/watch_pass.json",
    "source_picture": f"{R3}/seg_9x16/base.mp4",
    "negative_events_scan": NEG,
    "junk_report": f"{S}/junk_9x16.json",
}
json.dump(plan, open(f"{S}/plan.json", "w"), indent=1)
print(f"plan.json  sha {SHA[:12]}  joins {len(joins)}  punch {len(plan['punch'])}  windows {len(windows)}  ai {len(ai_inserts)}  "
      f"graphics {len(graphics)}  regions {len(regions)}  states {len(states)}  speech {len(SPEECH)}  tx {len(TX)}")
print("open AI result", open_ai, " couch cut", cut_t)
