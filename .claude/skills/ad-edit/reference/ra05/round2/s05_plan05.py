#!/usr/bin/env python3
"""RA-01 beat sheet + framing schedule — the single source of truth for both aspects.

ROUND 2. The first twelve seconds are rebuilt to plan section 12, R1, and the framing levels and
their centres to R2. Every beat is anchored to a PHRASE in the tight word list, never to a second
(ad-edit lesson 38), and every phrase lookup searches AFTER a time because this script repeats
"tap the button below".
"""
import json, os, re, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/round2")
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

HAS_L11 = False
END_HOLD = 0.85

# ---------------------------------------------------------------- RA-04 beat map (phrases, never seconds)
_acc, _sp = 0.0, []
for _a, _b in CUT["keeps"][:-1]:
    _acc += _b - _a; _sp.append(round(_acc, 3))
SEAMS = [round(x["t"], 3) for x in CUT["seams"]]
def snap_to(t, pts, win=0.35):
    near = [x for x in pts if abs(t - x) <= win]
    return snapf(min(near, key=lambda x: abs(x - t))) if near else snapf(t)
TAIL = 0.25
# ---------------------------------------------------------------- RA-05 beat map (phrases, never seconds)
t_gen  = at("generate an image")                       # the result appears as he says what AI makes
t_but  = at("but now guys")
t_ser  = at("seriously")
t_step = at("the first step is generating yourself")
t_use  = at("using ai", after=t_step)
t_shows= at("that also shows", after=t_use)
t_cre  = at("the ai creates", after=t_shows)
t_itll = at("itll determine", after=t_cre)
t_see  = at("it will see", after=t_itll)
t_wh   = at("where you need to gain", after=t_see)
t_make = at("to make you look", after=t_wh)
t_fs2  = at("the first step is generating an image", after=t_make)
t_free = at("its free", after=t_fs2)
t_once = at("and once you have", after=t_free)
t_get  = at("get the personalized", after=t_once)
e_real = end("abs real", after=t_get, pad=0.0)
t_so   = at("so take the first step", after=e_real)
t_tap  = at("tap the button below", after=t_so)
t_and  = at("and to get your", after=t_tap)
e_last = max(w["e"] for w in W)
TOTAL  = snapf(DUR + END_HOLD)
SPL    = _sp                                           # every pause splice and take join, in film time
s_step = snap_to(t_step, SEAMS)                        # R1|R2
s_itll = snap_to(t_itll, SEAMS)                        # R2|R3
s_fs2  = snap_to(t_fs2, SEAMS)                         # R3|R3B: the line cut. Dan to Dan, covered by a level change
s_once = snap_to(t_once, SEAMS)                        # R3B|R4
s_tap  = snap_to(t_tap, SEAMS)                         # R4|R5
flow_end = snapf(t_but - 0.02)
t_inreal = at("sixpack abs in real life", after=t_but)   # the END shot lands on "six-pack abs in real life" (2.1 s, not 1.1 s)
# ROUND 2 (Dan, 2026-10-14). OPEN: the app's whole generation from frame 0, sped up, the result alone for >= 1 s, to "but".
# COUCH: the approved concept "Steps out of the phone", frames only this round (a labelled START/END placeholder plays here).
# A1: the Soft Blue HyperFrames analysis card. SCAN: the start VSL's body scan (A0044) replaces the curls clip B1.
CARDS = [
 {"name": "open",     "kind": "phone",    "beat": [0.0, flow_end],                                      "asset": "B0049", "chip": "ai"},
 {"name": "couch",    "kind": "ai_clip",  "beat": [flow_end, snap_to(t_ser, SPL, 0.2)],                 "asset": "pending", "chip": "ai",
  "pending": True, "cut_at": snapf(t_inreal - 0.02)},
 {"name": "lock",     "kind": "clip",     "beat": [snapf(t_use), snap_to(t_shows, SPL, 0.2)],           "asset": "A0074", "chip": "ai"},
 {"name": "A1",       "kind": "analysis", "beat": [snap_to(t_shows, SPL, 0.2), snap_to(t_cre, SPL, 0.2)], "asset": "after", "chip": "ai"},
 {"name": "tour",     "kind": "phone",    "beat": [snap_to(t_cre, SPL, 0.2), s_itll],                   "asset": "B0544", "chip": None},
 {"name": "scan",     "kind": "clip",     "beat": [snap_to(t_see, SPL, 0.2), snapf(t_make)],            "asset": "A0044", "chip": "ai"},
 {"name": "pose",     "kind": "clip",     "beat": [snapf(t_get), snap_to(t_so, SPL, 0.2)],              "asset": "B0435", "chip": None},
]
# analysis card rows land on the words that start their clause (analysis-card/build.py)
t_exact = at("exactly where you are", after=t_shows, pad=0.0)
t_rnow  = at("right now", after=t_exact, pad=0.0)
t_want  = at("where you want", after=t_rnow, pad=0.0)
e_be    = end("to be", after=t_want, pad=0.0)
A1_CFG = {"reveal": [t_exact, t_rnow, t_want], "band": ["YOUR WORKOUT PLAN", None], "e_be": e_be}
# A pause splice inside a same-size shot is a jump cut (Dan, 2026-09-24). EVERY splice that is not under a card gets a level
# change ON it; the plan asserts it below. One more size change on a sentence break inside the 7 s call to action.
_cov = lambda t: any(c["beat"][0] - 0.02 <= t <= c["beat"][1] + 0.02 for c in CARDS)
EXTRA_CUTS = sorted(set([snapf(t_and)] + [snapf(x) for x in SPL if not _cov(x)]))
LT = [
 {"id": "LT1", "a": s_step, "b": snapf(t_use), "topic": "STEP 1", "parts": [["Generate Your Goal Body", t_step + 0.15]]},
 {"id": "LT2", "a": s_itll, "b": snap_to(t_see, SPL, 0.2), "topic": "STEP 2", "parts": [["Get A Plan Built For Your Goal", t_itll + 0.15]]},
]
for c in CARDS:
    c["beat"] = [snapf(c["beat"][0]), snapf(c["beat"][1])]
    assert c["beat"][1] - c["beat"][0] > 0.35, c
_a1 = next(c for c in CARDS if c["name"] == "A1")
A1_CFG["band"][1] = round(min(max(A1_CFG["e_be"] - 0.25, A1_CFG["reveal"][-1] + 0.35), _a1["beat"][1] - 0.52), 3)
_a1["config"] = {"reveal": A1_CFG["reveal"], "band": A1_CFG["band"]}
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
_R2 = "round2/NONE.json"
if os.path.exists(_R2) and FORCED:
    _keep = {round(p["beat"][0], 3) for p in json.load(open(_R2))["punch"]}
    _drop = [f for f in FORCED if round(f, 3) not in _keep]
    FORCED = [f for f in FORCED if round(f, 3) in _keep]
    if _drop:
        print(f"  R3: forced splices measured after the round-2 plan, NOT adopted: {_drop}")
SENT_ENDS = [w["e"] for w in W if w["w"].strip().endswith((".", "?", "!"))]
segs, seg_gap = [], []
for gi, (a, b) in enumerate(gaps):
    cuts = [a] + [snapf(f) for f in sorted(set(FORCED) | set(EXTRA_CUTS)) if a + 0.35 < f < b - 0.35]
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
from ra01lib import Aspect as _A
CW = {k: v[0] for k, v in _A("9x16").levels.items()}   # 9:16 crop widths from framing_choice.json
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
    if i == 0: desired = "NEAR"                     # his first shot has his abs in frame ("six-pack abs in real life")
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

CTA = [[s_tap, TOTAL]]
_hb = {round(p["beat"][0], 3) for p in punch} | {round(p["beat"][1], 3) for p in punch}
_bare = [x for x in SPL if not _cov(x) and not any(abs(snapf(x) - h) < 0.02 for h in _hb)]
assert not _bare, f"bare pause splices inside a hold: {_bare}"
plan = {"speed": CUT.get("speed"), "total": TOTAL, "total_frames": TOTALF, "timeline": _items, "dur_talk": DUR,
        "end_hold": END_HOLD, "cards": CARDS, "punch": punch, "cta": CTA, "lt": LT, "seams": CUT["seams"],
        "framing_notes": notes}
json.dump(plan, open("beats.json", "w"), indent=2)
cov = sum(c["beat"][1]-c["beat"][0] for c in CARDS)
print(f"total {TOTAL:.2f}s   talk {DUR:.2f}s + {END_HOLD:.2f}s end hold")
print(f"cards {len(CARDS)}  covering {cov:.2f}s = {cov/TOTAL*100:.1f}% of runtime (gate min 38%)")
for c in CARDS: print(f"   {c['name']:<11} {c['beat'][0]:6.2f} -> {c['beat'][1]:6.2f}  ({c['beat'][1]-c['beat'][0]:.2f}s)")
print(f"Dan segments {len(punch)}:")
for i, p in enumerate(punch):
    print(f"   {i:2d} {p['level']:<4} {p['beat'][0]:6.2f} -> {p['beat'][1]:6.2f}  "
          f"hair_min {p['hair_min']:6.1f}  cx {p['cx']:6.1f} (pref {p['cx_pref']:6.1f}, "
          f"moved {p['cx_moved']})  face span {p['face_span']:5.1f}  n={p['samples']}  "
          f"cx16 {p['cx16']:7.1f} (from hold {p['cx16_from']})  face16 {p.get('face16')}")
for n in notes: print("  !", n)
print("CTA pill:", plan["cta"])
print("LT", [(l["id"], l["a"], l["b"]) for l in LT]); assert TOTAL <= 59.0, TOTAL
