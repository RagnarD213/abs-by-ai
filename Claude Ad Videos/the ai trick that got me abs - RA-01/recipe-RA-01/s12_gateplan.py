#!/usr/bin/env python3
"""Build the delivery-gate plan for one delivered master.  s12_gateplan.py 9x16|16x9 <master>

Every key the format's rows need is supplied, or the row FAILS as NOT MEASURED. Nothing here is
a claim: caption states are the PNGs the compositor drew, speech_words are aligned from the
DELIVERED file's own audio, and the transcript is a fresh pass over the delivered render.
"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect

KEY, MASTER = sys.argv[1], sys.argv[2]
A = Aspect(KEY)
B = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
TL = json.load(open(f"timeline_{KEY}.json"))
CAP = json.load(open(f"cap_{KEY}/caption_states.json"))
CTA = json.load(open(f"cta_{KEY}/cta.json"))
CARDMETA = json.load(open(f"cards_{KEY}/meta.json"))
sha = L.__dict__.get("_sha") or None

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SHA = sha256(MASTER)

# joins on the DELIVERED timeline: every pause-removal splice, plus the one take seam
acc, joins = 0.0, []
for a, b in CUT["keeps"][:-1]:
    acc += b - a; joins.append(round(acc, 3))
for s in CUT["seams"]:
    if round(s["t"], 3) not in joins: joins.append(round(s["t"], 3))
joins = sorted(set(joins))

cards_all = [[c["beat"][0], c["beat"][1]] for c in B["cards"]]
# ⚠ ROUND 2. `cards` is the gate's "full-screen beats a caption may not sit on" (gate.py
# --plan-keys; an empty list is a legal answer). R1 rebuilt every card except the end card to stop
# ABOVE the caption band -- A.CARD_RECT ends at y 1352 in 9:16 and 880 in 16:9, the caption ink
# starts at 1400 / 930 -- so the captions run on the J2AD field UNDER the card, by ruling, and no
# caption sits on a card. The one card that is still full-screen is the end card, and the last
# caption line's hold is clipped to its in-point so nothing overlaps it either.
# The real measurement of that clearance is `captions:graphic_clearance`, which is given each
# card's MEASURED picture rectangle in `graphic_regions` below and grades the gap in delivered
# pixels against a 20 px bound. Every card is also declared in `graphics`, so the framing rows
# still exclude those beats from the talking-head scene and the watch pass proves each card is
# present in the delivered picture.
ENDCARD = [c for c in B["cards"] if c["name"] == "end_card"]
cards = [[c["beat"][0], c["beat"][1]] for c in ENDCARD]
punch = [[p["beat"], p["end"], p["level"]] for p in TL["punch"]]
ai, real = [], []
for c in B["cards"]:
    m = CARDMETA["cards"].get(c["name"], {})
    if c["chip"] == "ai":
        ai.append({"name": c["name"], "beat": c["beat"], "chip": m.get("chip_png"), "pos": list(m["chip_pos"])})
    elif c["chip"] == "real":
        real.append({"name": c["name"], "beat": c["beat"], "chip": m.get("chip_png"), "pos": list(m["chip_pos"])})

def card_rect(c):
    """The MEASURED rectangle the card's picture actually occupies in the delivered frame."""
    m = CARDMETA["cards"].get(c["name"], {})
    if c["name"] == "end_card":
        return [0, 0, A.VW, A.VH]
    bx = m.get("photo_box") or m.get("placed")
    if not bx:
        raise SystemExit(f"{c['name']}: no measured picture rectangle in cards_{KEY}/meta.json")
    x0, y0, x1, y1 = bx
    return [int(x0), int(y0), int(x1-x0+1), int(y1-y0+1)]

graphics = ([{"name": f"cta{i}", "beat": b, "mov": CTA["beat_movs"][i]}
             for i, b in enumerate(B["cta"])] +
            [{"name": c["name"], "beat": c["beat"],
              "mov": os.path.abspath(f"cards_{KEY}/{c['name']}.mp4")} for c in B["cards"]])
# ⚠ 2026-09-17: this declared the STATIC fallback `A.CTA_BOX` for both CTA beats, but s11_cta.py
# places each pill by MEASURING him on that beat's own rendered frame and records the real boxes in
# cta.json["boxes"]. The two differ by up to 89 px vertically in 9:16 and by 752 px of WIDTH in
# 16:9, so `captions:graphic_clearance` was grading the captions against a rectangle the pixels do
# not occupy -- geometry bound to another render, which the evidence contract exists to forbid.
# Declare what was actually drawn. (True 9:16 clearance is 35 px, not the 68 px the stale rect
# reported; both are over the 20 px bound, so this corrects the NUMBER, not the verdict.)
_CTA_BOXES = CTA.get("boxes") or [list(A.CTA_BOX)] * len(B["cta"])
assert len(_CTA_BOXES) == len(B["cta"]), "cta.json boxes do not match the CTA beats"
graphic_regions = ([{"name": f"cta{i}", "beat": b,
                     "rect": [_CTA_BOXES[i][0], _CTA_BOXES[i][1],
                              _CTA_BOXES[i][2] - _CTA_BOXES[i][0],
                              _CTA_BOXES[i][3] - _CTA_BOXES[i][1]]}
                    for i, b in enumerate(B["cta"])] +
                   [{"name": c["name"], "beat": c["beat"], "rect": card_rect(c)}
                    for c in B["cards"]])

states = []
for s in CAP["states"]:
    states.append({"name": s["name"], "beat": s["beat"], "image": s["image"],
                   "image_sha256": sha256(s["image"]), "rect": s["rect"], "word": s["word"]})

WORDS = json.load(open("words_aligned.json"))["words"]
SPEECH = json.load(open(f"speech_{KEY}.json"))["words"]
TXW = json.load(open(f"transcript_{KEY}.json"))["words"]

# absolute paths only: the gate resolves relative contract paths against the PLAN's directory, so
# "cards_9x16/chip_ai.png" became "recipe-RA-01/cards_9x16/chip_ai.png" and compliance:labels read
# NOT MEASURED.
CARDMETA["chips"] = {k: os.path.abspath(v) for k, v in CARDMETA["chips"].items()}
for lst in (ai, real):
    for b in lst:
        if b.get("chip"): b["chip"] = os.path.abspath(b["chip"])
plan = {
 "target_seconds": B["total"], "target_frames": TL["total_frames"],
 "joins": joins, "covered": cards_all + [[p[0], p[1]] for p in punch],
 "punch": punch, "punch_covered": [False]*len(punch),
 "graphics": graphics, "ai_inserts": ai, "real_photos": real, "cards": cards,
 "_cards_why": ("`cards` is the gate's list of FULL-SCREEN beats a caption may not sit on. After "
                "round 2's R1 relayout only the end card is full-screen; every other card stops "
                "above the caption band (A.CARD_RECT) and the captions run under it on the J2AD "
                "field, by ruling. All ten card beats are declared in `graphics` and their measured "
                "picture rectangles in `graphic_regions`, so the clearance is measured, not assumed."),
 "_cards_all": cards_all,
 "label_chips": {"ai": CARDMETA["chips"]["ai"], "real": CARDMETA["chips"]["real"]},
 "srt": os.path.abspath(f"cap_{KEY}/captions.srt"),
 "evidence_contract": {"version": 2, "video_sha256": SHA},
 "caption_states": states, "graphic_regions": graphic_regions,
 "speech_words": SPEECH,
 "speech_words_evidence": {"method": "delivered_asr", "video_sha256": SHA},
 "words": [{"w": w["w"], "t": w["t"], "e": w["e"]} for w in WORDS],
 "transcript_words": [{"w": w} for w in TXW],
 "source_audio": os.path.abspath("cut_audio.wav"),
 "banned_source": ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                   "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4"),
 "banned_times": [26.5, 27.5, 29.5, 31.0],
 "watch_log": os.path.abspath(f"watchpass_{KEY}/watch_pass.json"),
 "negative_events_scan": json.load(open(f"logs/negative_scan_{KEY}.json")),
}
out = f"recipe-RA-01/gate_plan_{KEY}.json"
json.dump(plan, open(out, "w"), indent=1)
print(f"{out}  sha {SHA[:12]}  joins {len(joins)}  cards {len(cards)}  punch {len(punch)}  "
      f"ai {len(ai)} real {len(real)}  states {len(states)}  speech {len(SPEECH)}  tx {len(TXW)}")
