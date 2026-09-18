#!/usr/bin/env python3
"""RA-01 beat sheet + framing schedule — the single source of truth for both aspects.

ROUND 2. The first twelve seconds are rebuilt to plan section 12, R1, and the framing levels and
their centres to R2. Every beat is anchored to a PHRASE in the tight word list, never to a second
(ad-edit lesson 38), and every phrase lookup searches AFTER a time because this script repeats
"tap the button below".
"""
import json, os, re
import numpy as np

CUT = json.load(open("cut.json"))
TRK = json.load(open("framing.json"))
W = json.load(open("words_aligned.json"))["words"]; DUR = CUT["dur"]
FD = 1001/30000
snapf = lambda t: round(round(t/FD)*FD, 6)
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
SEQ = [norm(w["w"]) for w in W]

def _find(ph, after=0.0):
    toks = norm(ph).split()
    i0 = next((i for i, w in enumerate(W) if w["t"] >= after), 0)
    for i in range(i0, len(SEQ)-len(toks)+1):
        if SEQ[i:i+len(toks)] == toks: return i
    raise KeyError(f"phrase not found after {after}: {ph!r}")

def at(ph, after=0.0, pad=-0.06):  return round(W[_find(ph, after)]["t"] + pad, 3)
def end(ph, after=0.0, pad=0.10):
    i = _find(ph, after) + len(norm(ph).split()) - 1
    return round(W[i]["e"] + pad, 3)

HAS_L11 = any(r["name"] == "R3B" for r in CUT["ranges"])
END_HOLD = 1.65

# ---------------------------------------------------------------- R1: the new L1-L4 beat map
# | "This picture got me abs."              | the AI image card, from frame 0
# | "And it's not even real!"               | Dan on camera, NEAR (a face inside the first 3 s)
# | "I generated this picture with AI"      | the AI image card again
# | "back when I was 200 pounds."           | the BEFORE picture, from the word "back", >= 1.2 s
# | "And this is what I"                    | Dan on camera, FAR, >= 0.8 s  (the "other" beat)
# | "look like today." + pause + "Seeing this" | the three real after pictures, >= 0.6 s each
# | "AI image of myself with abs changed me." | the AI image card, landing on "AI image"
t_hook_end = at("and its not even real")
t_gen      = at("i generated this picture", after=t_hook_end)
t_back     = at("back when i was", after=t_gen)
e_pounds   = end("pounds", after=t_back, pad=0.0)
t_aiimg    = at("ai image of myself", after=e_pounds)
e_l4       = end("changed me", after=t_aiimg)
t_look     = at("look like today", after=e_pounds)

# The ruling's own floors: BEFORE >= 1.2 s, the Dan "other" >= 0.8 s, each after picture >= 0.6 s.
# ⚠ DEVIATION, MEASURED. With the word split exactly as the table draws it -- Dan over "And this
# is what I", the photographs from "look" -- the photographs get only t_aiimg - t_look = 1.38 s,
# i.e. 0.46 s each, which breaks the ruling's own 0.6 s floor; and even starting Dan on the word
# "and" leaves 2.60 s for a 0.80 + 1.80 requirement, exactly zero margin. Both cuts are therefore
# taken two words earlier, into the PAUSES on either side of "and this" (6.52-7.02 and 7.40-7.82),
# which also puts both of them in silence instead of on a word.
BEFORE_MIN, OTHER_MIN, PHOTO_MIN = 1.20, 0.80, 0.60
SPAN = t_aiimg - t_back
before_len, other_len = 1.68, 0.90
photo_span = SPAN - before_len - other_len
if photo_span < 3*PHOTO_MIN:                       # take it from BEFORE first, then from the other
    need = 3*PHOTO_MIN - photo_span
    give = min(need, before_len - BEFORE_MIN); before_len -= give; need -= give
    give = min(need, other_len - OTHER_MIN);  other_len -= give;  need -= give
    photo_span = SPAN - before_len - other_len
    assert need <= 1e-6, f"cannot meet the R1 floors in {SPAN:.2f}s"
elif photo_span > 2.40:                            # spare time goes back to the BEFORE picture
    before_len += photo_span - 2.40; photo_span = 2.40
before  = [snapf(t_back), snapf(t_back + before_len)]
other   = [before[1], snapf(t_back + before_len + other_len)]
after_in, after_out = other[1], snapf(t_aiimg)
ai1     = [0.0, snapf(t_hook_end)]
hook_dan = [ai1[1], snapf(t_gen)]
ai2     = [hook_dan[1], before[0]]
# ⚠ CARD TAILS. R1 takes 2.3 s of card time out of the hook (round 1 ran one AI card from 0.00 to
# 6.27; the new map splits it with a Dan beat and a second AI beat), and `style:coverage` measures
# almost exactly the card fraction of runtime -- round 1: 42.2 % of runtime on cards, gate read
# 42 % -- against a 38 % floor. Each full card therefore holds through the pause AFTER its own
# sentence rather than cutting on the word, which is also where the cut belongs: it lands in
# silence, and it covers the blink a cut back to camera lands on (the MACRO_TAIL lesson).
TAIL = 0.40
ai3     = [after_out, snapf(e_l4 + TAIL)]

t_scan     = at("ai analyzed it", after=e_l4)
e_scan     = end("goal physique", after=t_scan)
t_macro    = at("i even started", after=e_scan)
e_macro    = end("track my macros", after=t_macro)
t_cta1     = at("tap the button below", after=e_l4)
e_cta1     = end("tap the button below", after=t_cta1)
t_cta2     = at("tap the button below", after=e_cta1 + 1.0)
e_cta2     = end("tap the button below", after=t_cta2)

scan = [snapf(t_scan), snapf(e_scan + TAIL)]
# A pause splice 2 frames before a card cut reads as a pop, not as the cut. Snap the card's
# in-point ONTO the splice so there is one visual event, not two.
_acc, _sp = 0.0, []
for _a, _b in CUT["keeps"][:-1]:
    _acc += _b - _a; _sp.append(round(_acc, 3))
def snap_to_splice(t, win=0.30):
    near = [x for x in _sp if 0 <= t - x <= win]
    return snapf(max(near)) if near else snapf(t)
scan = [snap_to_splice(scan[0]), scan[1]]

# ---------------------------------------------------------------- R3: the macro-tracker beat
# The recording is only STABLE (itemized list + calorie total, no recalculation, no screen change)
# between 40.5 s and 43.8 s of its own timeline; 43.8 is where it changes screen, so the slice must
# end at least 3 frames before that. MACRO_LEN is what is actually available, and the beat is built
# to it rather than the other way round. Round 1's slice ran 34.6-38.1 and walked straight into the
# 458 -> 342 recalculation, the Log Meal press and a 3-frame flash of a different screen (D4).
MACRO_SLICE_IN, MACRO_SLICE_OUT = 40.50, 43.70   # 43.80 is the screen change; 43.70 is 3 frames early
MACRO_LEN = 3.10                                 # the beat length; the slice has 0.10 s of margin
# ⚠ WHERE THE CARD LETS GO. Round 1 gave the card a 0.60 s tail because the cut back to camera
# landed on an eye-squeeze; R3's stable-slice cap took that tail away and the cut landed on the
# same moment again -- measured with s40_blink.py over f1168-1200 of the round-2 picture, his eyes
# stay open (EAR 0.23-0.29, never a blink) but his HEAD IS DOWN and his gaze with it until about
# f1185 (39.54 s), which is the checklist's `visual_junk` look-away. The card therefore holds until
# 39.60 s at the earliest; its length is still the slice's 3.10 s, so the IN point moves with it --
# onto "I even started", which is where the line actually begins.
MACRO_OUT_MIN = 39.75
macro_out = snapf(max(t_macro + MACRO_LEN, MACRO_OUT_MIN))
macro_in = snapf(macro_out - MACRO_LEN)
macro = [macro_in, macro_out]
assert macro_in >= scan[1] + 0.25, (macro_in, scan[1], "the macro card would crowd the stats card")
assert macro[1] >= e_macro + 0.05, (macro, e_macro, "the card must outlast the line it covers")

endcard = [snapf(e_cta2 + 0.05), snapf(DUR + END_HOLD)]
TOTAL = round(endcard[1], 3)

assert other[1] - other[0] >= OTHER_MIN - 1e-6, other
assert before[1] - before[0] >= BEFORE_MIN - 1e-6, before
assert after_out - after_in >= 3*PHOTO_MIN - 1e-6, (after_in, after_out)

photo_slots = []
n3 = 3
span = (after_out - after_in)/n3
for i in range(n3):
    photo_slots.append([snapf(after_in + i*span), snapf(after_in + (i+1)*span)])

CARDS = [
 {"name": "ai_hook",   "kind": "ai",     "beat": ai1,      "asset": "ai",     "chip": "ai"},
 {"name": "ai_gen",    "kind": "ai",     "beat": ai2,      "asset": "ai",     "chip": "ai"},
 {"name": "before",    "kind": "before", "beat": before,   "asset": "before", "chip": None},
 {"name": "after_1",   "kind": "real",   "beat": photo_slots[0], "asset": "after1", "chip": "real"},
 {"name": "after_2",   "kind": "real",   "beat": photo_slots[1], "asset": "after2", "chip": "real"},
 {"name": "after_3",   "kind": "real",   "beat": photo_slots[2], "asset": "after3", "chip": "real"},
 {"name": "ai_again",  "kind": "ai",     "beat": ai3,      "asset": "ai",     "chip": "ai"},
 {"name": "stats_scan","kind": "scan",   "beat": scan,     "asset": "ai",     "chip": "ai"},
 {"name": "macro",     "kind": "clip",   "beat": macro,    "asset": "macro",  "chip": None},
 {"name": "end_card",  "kind": "endcard","beat": endcard,  "asset": "ai",     "chip": "ai"},
]
for c in CARDS:
    c["beat"] = [snapf(c["beat"][0]), snapf(c["beat"][1])]
    assert c["beat"][1] - c["beat"][0] > 0.35, c
CARDS.sort(key=lambda c: c["beat"][0])
for i in range(len(CARDS)-1):
    assert CARDS[i]["beat"][1] <= CARDS[i+1]["beat"][0] + 1e-6, (CARDS[i], CARDS[i+1])

# ------------------------------------------------------------------ Dan segments and framing
gaps, prev = [], 0.0
for c in CARDS:
    if c["beat"][0] - prev > 0.28: gaps.append([snapf(prev), c["beat"][0]])
    prev = max(prev, c["beat"][1])
if TOTAL - prev > 0.28: gaps.append([snapf(prev), snapf(TOTAL)])

# A LEVEL CHANGE ON EVERY VISIBLY HARD SPLICE, plus one on a sentence boundary at least every
# ~12 s of uninterrupted talk. `hard_splices.json` records the WORD PAIRS s25_hard.py measured on
# a delivered render, not its times -- the times belong to that render and this is a different cut,
# so they are re-derived from THIS word list (evidence never crosses renders).
import hashlib
CUT_SIG = hashlib.sha256(json.dumps(_sp).encode()).hexdigest()[:16]
FORCED = []
if os.path.exists("hard_splices.json"):
    HS = json.load(open("hard_splices.json"))
    if HS.get("cut_sig") == CUT_SIG:
        # measured on a render of THIS cut: the times are directly usable
        FORCED = [round(float(t), 3) for t in HS.get("forced", [])]
        print(f"  hard splices: {len(FORCED)} forced, measured on {HS.get('measured_on')} "
              f"(cut signature matches)")
    for a, b in ([] if FORCED else HS.get("pairs", [])):
        try:
            i = next(k for k in range(len(W)-1)
                     if norm(W[k]["w"]) == norm(a) and norm(W[k+1]["w"]) == norm(b))
        except StopIteration:
            print(f"  hard splice pair {a!r}->{b!r} is not in this cut — skipped"); continue
        FORCED.append(round((W[i]["e"] + W[i+1]["t"])/2, 3))
    FORCED = sorted(set(FORCED))
# ⚠ R3 (plan section 13) is a TARGETED revision: the cut, the beat map and the hold boundaries stay
# round 2's, and only the four listed items change. s25_hard.py re-ran on the round-2 master AFTER
# that plan was built and added one more forced splice (36.003 s); adopting it now would add a 14th
# hold and a level change the ruling does not ask for. The forced list is therefore pinned to the
# splices round 2 actually delivered.
_R2 = "round2/beats.json"
if os.path.exists(_R2) and FORCED:
    _keep = {round(p["beat"][0], 3) for p in json.load(open(_R2))["punch"]}
    _drop = [f for f in FORCED if round(f, 3) not in _keep]
    FORCED = [f for f in FORCED if round(f, 3) in _keep]
    if _drop:
        print(f"  R3: forced splices measured after the round-2 plan, NOT adopted: {_drop}")
SENT_ENDS = [w["e"] for w in W if w["w"].strip().endswith((".", "?", "!"))]
segs, seg_gap = [], []
for gi, (a, b) in enumerate(gaps):
    cuts = [a] + [snapf(f) for f in FORCED if a + 0.35 < f < b - 0.35]
    while b - cuts[-1] > 12.0:
        cand = [s for s in SENT_ENDS if cuts[-1] + 4.5 < s < min(cuts[-1] + 11.0, b - 3.0)]
        if not cand: break
        cuts.append(snapf(max(cand)))
    cuts = sorted(set(cuts))
    cuts.append(b)
    for i in range(len(cuts)-1):
        if cuts[i+1] - cuts[i] >= 0.25:
            segs.append([cuts[i], cuts[i+1]]); seg_gap.append(gi)
        elif segs:
            segs[-1][1] = cuts[i+1]

SAM = TRK["samples"]
def hold_stats(a, b):
    s = [x for x in SAM if a - 0.26 <= x["t"] <= b + 0.26]
    if not s: s = SAM
    return s

# ---------------------------------------------------------------- R2: level + fixed centre
# The crop is hair-anchored and FIXED per hold (AGENTS.md 2026-09-16). On top of that, R2 requires
# his FACE BOX to stay inside 8-92 % of the frame width on EVERY frame; round 1's NEAR was 504 px
# wide and his lean put an ear on the right edge at 98.2 %. Feasibility is arithmetic:
#     x <= min(fx0) - 0.08*cw   and   x >= max(fx1) - 0.92*cw
# so a hold fits a level iff max(fx1) - min(fx0) <= 0.84*cw. A hold that does not fit NEAR is cut
# at FAR instead. The preferred centre is still the MEDIAN face centre (round 1 measured
# framing:centering at +1.9 % that way); it is only moved as far as the inequality demands.
CW = {"NEAR": 594, "FAR": 702}          # 9:16 crop widths; the 16:9 windows are far wider
EDGE = 0.08

# ---------------------------------------------------------------- R3 (plan section 13), D4
# Round 2 still broke 8-92 % on 11 frames at 00:22.15-00:22.26 because the constraint was fed by
# the 5 Hz landmark track, whose "face box" is the cheek-to-cheek span (234<->454) -- about 19 %
# narrower than the face box measured on the DELIVERED frame, and sampled 6x more coarsely than a
# 0.37 s lean. `face_src_r3.json` carries the per-hold extremes measured on EVERY frame of the
# round-2 masters and mapped back into source pixels; the wider of the two is what the fit obeys.
# And when the preferred centre is outside the legal band the crop is placed MARGIN_PX inside the
# violated edge rather than hard on it, so a few pixels of detector disagreement cannot put it back
# out. ⚠ MARGIN_PX IS SMALL ON PURPOSE. Two bounds pull against each other on a leaning hold: the
# face box wants the crop to FOLLOW the lean (x up), `framing:centering` wants his head within 6 %
# of the window centre (x down). Measured on the delivered round-3 9:16, hold 4 at x = 962 read face
# 12.4..88.7 % (inside 8-92 with 3.3 % to spare) but a head centre of 43.3 % = -6.7 % off, which
# fails centering. At x = 950 both hold with ~1.3 %: face max ~90.7 %, head centre ~45.3 % = -4.7 %.
FACE_OVR = {}
if os.path.exists("face_src_r3.json"):
    for r in json.load(open("face_src_r3.json"))["holds"]:
        FACE_OVR[round(float(r["beat"]), 2)] = (float(r["sx0"]), float(r["sx1"]))
MARGIN_PX = 4.0


def fit(level, s, beat=None):
    cw = CW[level]
    fx0 = min(x["fx0"] for x in s); fx1 = max(x["fx1"] for x in s)
    ovr = FACE_OVR.get(round(float(beat), 2)) if beat is not None else None
    if ovr:
        fx0 = min(fx0, ovr[0]); fx1 = max(fx1, ovr[1])
    lo = fx1 - (1-EDGE)*cw
    hi = fx0 - EDGE*cw
    cx_med = float(np.median([x["cx"] for x in s]))
    x_pref = cx_med - cw/2
    if hi >= lo:
        if x_pref < lo:   x = min(hi, lo + MARGIN_PX)
        elif x_pref > hi: x = max(lo, hi - MARGIN_PX)
        else:             x = x_pref
    else:
        x = None
    if x is not None:
        x = max(0.0, min(2160.0 - cw, x))
    return {"ok": hi >= lo and x is not None and lo - 1e-6 <= x <= hi + 1e-6,
            "x": x, "lo": lo, "hi": hi, "need": fx1-fx0, "room": 0.84*cw,
            "cx_pref": cx_med, "cx": (x + cw/2) if x is not None else None,
            "moved": None if x is None else round(abs(x - x_pref), 1)}

punch, notes = [], []
last_level = None
for i, (a, b) in enumerate(segs):
    s = hold_stats(a, b)
    desired = "NEAR" if last_level != "NEAR" else "FAR"
    if i == 0: desired = "NEAR"                     # R1 names the hook beat NEAR
    if i == 1: desired = "FAR"                      # R1 names the before->after "other" beat FAR
    f = fit(desired, s, beat=a)
    level = desired
    if not f["ok"]:
        other_l = "FAR" if desired == "NEAR" else "NEAR"
        f2 = fit(other_l, s, beat=a)
        notes.append(f"hold {i} ({a:.2f}-{b:.2f}) does not fit {desired} "
                     f"(face box {f['need']:.0f}px needs {f['room']:.0f}px of the 84 % band) "
                     f"-> cut at {other_l}" + ("" if f2["ok"] else "  ⚠ IT DOES NOT FIT EITHER"))
        level, f = other_l, f2
    hair = min(x["hair"] for x in s)
    punch.append({"beat": [a, b], "level": level, "hair_min": round(hair, 1),
                  "cx": round(f["cx"], 1), "samples": len(s),
                  "face_span": round(f["need"], 1), "cx_pref": round(f["cx_pref"], 1),
                  "cx_moved": f["moved"], "gap": seg_gap[i]})
    last_level = level
# ---------------------------------------------------------------- R3 (plan section 13), D5
# THE 16:9 ZOOM-CUT HOP. In 16:9 the FAR window is 2144 px of a 2160 px source, so its x is pinned
# to 0..16 and its centre cannot be moved; the NEAR window (1888) was centred on each hold's own
# face median, which sat 128 px right of the FAR centre, and Dan stepped 4-7 % of the width sideways
# at every zoom cut. Round 3 gives every 16:9 NEAR hold its neighbouring FAR hold's MEASURED centre,
# so the two levels share a centre line and the cut is a pure zoom. (9:16 is unaffected: there the
# FAR window is 702 px of 2160 and both levels are centred on him.)
W16 = {"NEAR": 1888, "FAR": 2144}


def x16(cx, level):
    w = W16[level]
    x = int(round(cx - w/2)); x = max(0, min(2160-w, x))
    return x - x % 2


far_c = {i: x16(p["cx"], "FAR") + W16["FAR"]/2.0
         for i, p in enumerate(punch) if p["level"] == "FAR"}
for i, p in enumerate(punch):
    if p["level"] == "FAR":
        p["cx16"] = far_c[i]; p["cx16_from"] = i
    else:
        prev = max([j for j in far_c if j < i], default=None)
        nxt = min([j for j in far_c if j > i], default=None)
        j = prev if nxt is None else (nxt if prev is None else (prev if i-prev <= nxt-i else nxt))
        p["cx16"] = far_c[j] if j is not None else p["cx"]
        p["cx16_from"] = j
    # the 8-92 % face-box rule must still hold in 16:9 at that centre
    cw = W16[p["level"]]; x = x16(p["cx16"], p["level"])
    o = FACE_OVR.get(round(float(p["beat"][0]), 2))
    if o:
        l, r = (o[0]-x)/cw, (o[1]-x)/cw
        p["face16"] = [round(l*100, 1), round(r*100, 1)]
        if l < EDGE or r > 1-EDGE:
            notes.append(f"⚠ 16:9 hold {i} face box {l*100:.1f}..{r*100:.1f} % at the shared centre")

# no two VISIBLE (uncovered) joins may have the same level on both sides: inside one gap the join
# is naked, between gaps a card covers it.
for i in range(len(punch)-1):
    if punch[i]["gap"] == punch[i+1]["gap"] and punch[i]["level"] == punch[i+1]["level"]:
        notes.append(f"⚠ holds {i}/{i+1} share {punch[i]['level']} across an UNCOVERED join")

FPSX = 30000/1001
frx = lambda t: int(round(t*FPSX))
TOTALF = frx(TOTAL)
_items = ([{"kind": "card", "name": c["name"], "a": c["beat"][0]} for c in CARDS] +
          [{"kind": "dan", "name": f"dan{i:02d}", "a": p["beat"][0]} for i, p in enumerate(punch)])
_items.sort(key=lambda x: x["a"])
for i, it in enumerate(_items):
    it["f0"] = frx(it["a"])
    it["f1"] = TOTALF if i == len(_items)-1 else frx(_items[i+1]["a"])
    it["n"] = it["f1"] - it["f0"]
    assert it["n"] > 0, it
FRAMES = {it["name"]: it["n"] for it in _items}
for c in CARDS: c["frames"] = FRAMES[c["name"]]
for i, p in enumerate(punch): p["frames"] = FRAMES[f"dan{i:02d}"]

# ⚠ THE CTA PILL MUST BE OFF BEFORE THE END CARD, which carries its own CTA and URL.
CTA = [[snapf(t_cta1 - 0.10), snapf(e_cta1 + 0.35)],
       [snapf(t_cta2 - 0.10), snapf(min(e_cta2 + 0.35, endcard[0] - FD))]]
assert CTA[1][1] <= endcard[0] - FD + 1e-6, (CTA[1], endcard[0])
assert CTA[1][1] > CTA[1][0], CTA[1]

plan = {"total": TOTAL, "total_frames": TOTALF, "timeline": _items, "dur_talk": DUR,
        "end_hold": END_HOLD, "has_L11": HAS_L11,
        "cards": CARDS, "punch": punch, "cta": CTA, "seams": CUT["seams"],
        "macro_slice": {"in": MACRO_SLICE_IN, "out": MACRO_SLICE_OUT, "len": MACRO_LEN},
        "framing_notes": notes,
        "r1_beats": {"ai_hook": ai1, "dan_near": hook_dan, "ai_gen": ai2, "before": before,
                     "dan_other": other, "after": [after_in, after_out], "ai_again": ai3}}
json.dump(plan, open("beats.json", "w"), indent=2)
cov = sum(c["beat"][1]-c["beat"][0] for c in CARDS)
print(f"total {TOTAL:.2f}s   talk {DUR:.2f}s + {END_HOLD:.2f}s end hold")
print(f"cards {len(CARDS)}  covering {cov:.2f}s = {cov/TOTAL*100:.1f}% of runtime (gate min 38%)")
for c in CARDS: print(f"   {c['name']:<11} {c['beat'][0]:6.2f} -> {c['beat'][1]:6.2f}  ({c['beat'][1]-c['beat'][0]:.2f}s)")
print(f"R1 hook: AI {ai1[1]-ai1[0]:.2f}s | Dan NEAR {hook_dan[1]-hook_dan[0]:.2f}s | "
      f"AI {ai2[1]-ai2[0]:.2f}s | BEFORE {before[1]-before[0]:.2f}s | Dan FAR {other[1]-other[0]:.2f}s | "
      f"3 photos {(after_out-after_in)/3:.2f}s each | AI {ai3[1]-ai3[0]:.2f}s")
print(f"Dan segments {len(punch)}:")
for i, p in enumerate(punch):
    print(f"   {i:2d} {p['level']:<4} {p['beat'][0]:6.2f} -> {p['beat'][1]:6.2f}  "
          f"hair_min {p['hair_min']:6.1f}  cx {p['cx']:6.1f} (pref {p['cx_pref']:6.1f}, "
          f"moved {p['cx_moved']})  face span {p['face_span']:5.1f}  n={p['samples']}  "
          f"cx16 {p['cx16']:7.1f} (from hold {p['cx16_from']})  face16 {p.get('face16')}")
for n in notes: print("  !", n)
print("CTA pill:", plan["cta"])
if TOTAL > 59.0: print(f"\n*** OVER THE 59.00 s CEILING by {TOTAL-59.0:.2f}s — drop L11 (DROP=R3B) ***")
