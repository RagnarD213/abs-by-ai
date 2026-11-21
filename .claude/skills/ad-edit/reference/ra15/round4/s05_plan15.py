#!/usr/bin/env python3
"""RA-01 beat sheet + framing schedule — the single source of truth for both aspects.

ROUND 2. The first twelve seconds are rebuilt to plan section 12, R1, and the framing levels and
their centres to R2. Every beat is anchored to a PHRASE in the tight word list, never to a second
(ad-edit lesson 38), and every phrase lookup searches AFTER a time because this script repeats
"tap the button below".
"""
import json, os, re, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
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
# ---------------------------------------------------------------- RA-15 beat map (phrases, never seconds)
t_ait  = at("ai just took their job")
t_one  = at("one ai can look")
t_know = at("and know exactly", after=t_one)
t_gen  = at("generate an image of yourself", after=t_know)
t_meas = at("and it measures", after=t_gen)
t_two  = at("two ai builds", after=t_meas)
t_not  = at("not a printout", after=t_two)
t_plan = at("a plan youll", after=t_not)
t_three= at("and three", after=t_plan)
t_every= at("every single meal", after=t_three)
t_eat  = at("eating at a restaurant", after=t_every)
t_anut = at("a nutritionist charges", after=t_eat)
t_start= at("start with a picture", after=t_anut)
t_twice= at("twice", after=t_anut)
t_tap  = at("tap the button below", after=t_start)
t_togen= at("to generate", after=t_tap)
t_and  = at("and to get", after=t_tap)
e_last = max(w["e"] for w in W)
TOTAL  = snapf(DUR + END_HOLD)
SPL    = _sp                                           # every pause splice and take join, in film time
s_gen  = snap_to(t_gen, SEAMS)                         # R1|R2: the hidden restart is cut here; a card covers the join
s_start= snap_to(t_start, SEAMS)                       # R2|R3
s_tap  = snap_to(t_tap, SPL, 0.2)
CARDS = [
 {"name": "opener",   "kind": "clip",  "beat": [0.0, snap_to(t_ait, SPL, 0.3)],                      "asset": "A0016", "chip": "ai"},
 {"name": "flow",     "kind": "phone", "beat": [s_gen, snapf(t_meas)],                                "asset": "B0049", "chip": "ai"},
 {"name": "analysis", "kind": "scan",  "beat": [snapf(t_meas), snap_to(t_two, SPL, 0.2)],             "asset": "after", "chip": "ai"},
 # ROUND 2 (Dan, 2026-10-14: "yes to all four ideas except for the cleared-out idea"): I2 replaces the A0017 factory
 {"name": "fridge",   "kind": "clip",  "beat": [snap_to(t_not, SPL, 0.2), snap_to(t_plan, SPL, 0.2)], "asset": "I2", "chip": "ai"},
 {"name": "enjoy",    "kind": "clip",  "beat": [snap_to(t_plan, SPL, 0.2), snap_to(t_three, SPL, 0.2)], "asset": "A0086", "chip": "ai"},
 {"name": "macro",    "kind": "phone", "beat": [snapf(t_every), snapf(t_eat)],                        "asset": "B0038", "chip": None},
 {"name": "restaurant", "kind": "clip", "beat": [snapf(t_eat), snap_to(t_anut, SPL, 0.2)],            "asset": "I4", "chip": "ai"},
 # ROUND 3 (review D1): "twice" is back in the cut (+0.62 s). I5 take 1 has no frames left after shot B (take frame 143 is its last), and
 # a clip is never slowed or held to fill a slot, so the card ends where its frames do (just before "twice") and Dan says "twice." on
 # camera; the lock card still starts on the R2|R3 seam.
 # ROUND 4 (Dan, 2026-10-16: "everything ... except for the cardboard nutritionist cutout. I want to use a camera scene during that. That clip
 # didn't really land."): the I5 cutout card (39.01-42.54) is OUT. Dan is on camera from the restaurant card to the lock card; the pause splice
 # at 41.742 inside that span is now an uncovered splice, so EXTRA_CUTS splits the span into two holds with a size change on it.
 # (round 3 had: {"name": "cutout", "kind": "clip", "beat": [snap_to(t_anut, SPL, 0.2), min(t_twice - 0.03, snap_to(t_anut, SPL, 0.2) + 3.54)], "asset": "I5", "chip": "ai"})
 {"name": "lock",     "kind": "clip",  "beat": [s_start, snapf(t_togen)],                             "asset": "A0074", "chip": "ai"},
]
# Round 1 ideas, all decided by Dan on 2026-10-14: I1 rejected (A0016 stays), I2/I4/I5 placed above as fridge/restaurant/cutout.
IDEAS = {"I1": "rejected: A0016 museum opener kept", "I2": "fridge", "I4": "restaurant", "I5": "rejected round 4: Dan on camera instead ('That clip didn't really land')"}
_cov = lambda t: any(c["beat"][0] - 0.02 <= t <= c["beat"][1] + 0.02 for c in CARDS)
EXTRA_CUTS = sorted(set([snapf(t_and)] + [snapf(x) for x in SPL if not _cov(x)]))
LT = [
 {"id": "LT1", "a": snap_to(t_one, SPL, 0.3), "b": snapf(t_gen - 1.2), "topic": "1 of 3", "parts": [["Knows The Fat You Need To Lose", t_one + 0.15]]},
 {"id": "LT2", "a": snap_to(t_two, SPL, 0.2), "b": snap_to(t_not, SPL, 0.2), "topic": "2 of 3", "parts": [["Built Around Foods You Like", t_two + 0.15]]},
 {"id": "LT3", "a": snap_to(t_three, SPL, 0.2), "b": snapf(t_every), "topic": "3 of 3", "parts": [["With You At Every Meal", t_three + 0.15]]},
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
if os.path.exists("framing_holdstart.json"):          # ROUND 3 (RA-14 round 2 lesson 6): one measurement on the exact first and last frame of each hold
    SAM = sorted(SAM + json.load(open("framing_holdstart.json"))["samples"], key=lambda x: x["t"])
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
    if i == 0: desired = "NEAR"
    # ROUND 3 (independent review): with the crop following him, his arms still left the TIGHT frame in the big-gesture holds (7.51,
    # 24.99) and both elbows in the last second. LEVELS sets each hold's level; the wide level goes to those three, and the alternation
    # across every uncovered join is kept (holds 0-3 one run, 4 / 5 / 6 each between cards, 7-8 one run). Checked below.
    _LV = [x for x in os.environ.get("LEVELS", "FAR,NEAR,FAR,NEAR,FAR,NEAR,FAR,NEAR,NEAR,FAR").split(",") if x]
    if len(_LV) == len(segs): desired = _LV[i]
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
W16 = {"NEAR": 1504, "FAR": 1696}      # ROUND 3: = ra01lib.Aspect("16x9").levels widths (the no-wide-level gate row)


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

# ------------------------------------------------------------------ ROUND 3: land, then hold (Dan, 2026-10-03, locked 10-05)
# round3/landing_check.json measured his head 3.5-16.5 % of the crop width off the fixed centre in 6 of 8 holds. The 9:16 crop
# now lands on his measured head centre at each cut, holds inside the dead band, and follows only when he leaves it, through
# _shared/cut/landing.py with RA-14 round 3's settings (approved 2026-10-14). One centre per output frame of the hold in
# punch[i]["track"]; s10_render05.py crops from it. The 16:9 keeps its fixed cx16 (horizontal stays static, 2026-09-17).
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import landing
_sn = np.array([frx(x["t"]) for x in SAM]); _sx = np.array([x["cx"] for x in SAM], float)
_o = np.argsort(_sn, kind="stable"); _sn, _sx = _sn[_o], _sx[_o]
_u = np.concatenate([[True], np.diff(_sn) > 0]); _sn, _sx = _sn[_u], _sx[_u]
_hold = {it["name"]: it for it in _items if it["kind"] == "dan"}
_BODY = json.load(open("framing_body.json"))["samples"] if os.path.exists("framing_body.json") else []
for lvl in ("NEAR", "FAR"):
    idx = [i for i, p in enumerate(punch) if p["level"] == lvl]
    if not idx: continue
    segs_l = [{"n0": _hold[f"dan{i:02d}"]["f0"], "n1": _hold[f"dan{i:02d}"]["f1"]} for i in idx]
    # ROUND 3 b (watch-pass judge, 2026-10-14): RA-14's settings (170 px/s, 20 px band) panned 163 px at 7.54 s and 120 px at 25.69 s
    # with no easing. A slower follow, RA-14's 6.6 % hold band and a Gaussian ease inside each hold, the landing frame kept exact.
    # ROUND 3 (review): centre on his BODY (arms included, s04c_body.py), held within 8 % of the crop width of his head, so a wide
    # gesture no longer leaves one arm off the edge with the other side empty. Head samples are the fallback.
    _tsn, _tsx = _sn, _sx
    if _BODY:
        _bn = np.array([frx(x["t"]) for x in _BODY]); _bm = np.array([x["mid"] for x in _BODY], float)
        _o2 = np.argsort(_bn, kind="stable"); _bn, _bm = _bn[_o2], _bm[_o2]; _u2 = np.concatenate([[True], np.diff(_bn) > 0]); _bn, _bm = _bn[_u2], _bm[_u2]
        _hd = np.interp(_bn, _sn, _sx); _tsn, _tsx = _bn, np.clip(_bm, _hd - 0.08*CW[lvl], _hd + 0.08*CW[lvl])
    _SL, _TOL, _SIG = (float(v) for v in os.environ.get("TRACK", "170,20,8").split(","))
    n_all, x_all, _info = landing.track(_tsn, _tsx, segs_l, slope_px_s=_SL*CW[lvl]/608, k=3, fixed_under=_TOL*CW[lvl]/608,
                                        fps=FPSX, tolerance=_TOL*CW[lvl]/608)
    n_all, x_all = np.asarray(n_all), np.asarray(x_all)
    # TRACK_HOLD "4:260,20,5;...": one hold with its own follow settings (final review: hold 4 lagged him 70 px at 25.3-26.0 s and his
    # elbow left the frame). The hold is tracked on its own; landing.track treats every segment independently anyway.
    _TH = {int(k): tuple(float(x) for x in v.split(",")) for k, v in (e.split(":") for e in os.environ.get("TRACK_HOLD", "4:0,0,9").split(";") if e)}
    for i, sg in zip(idx, segs_l):
        _sl_i, _tol_i, _sig_i = _TH.get(i, (_SL, _TOL, _SIG))
        if i in _TH:
            _cl = float(dict(e.split(":") for e in os.environ.get("CLAMP_HOLD", "4:0.13").split(";") if e).get(str(i), 0.08))
            _tsx_i = np.clip(_bm, _hd - _cl*CW[lvl], _hd + _cl*CW[lvl]) if _BODY else _tsx
            if _sl_i == 0:      # direct: the crop follows the (clamped) body middle itself, smoothed below; no hold band
                _n1, _x1 = _tsn, _tsx_i
            else:
              _n1, _x1, _ = landing.track(_tsn, _tsx_i, [sg], slope_px_s=_sl_i*CW[lvl]/608, k=3, fixed_under=_tol_i*CW[lvl]/608, fps=FPSX,
                                        tolerance=_tol_i*CW[lvl]/608)
            _n1, _x1 = np.asarray(_n1), np.asarray(_x1)
        else:
            _n1, _x1 = n_all, x_all
        m = (_n1 >= sg["n0"]) & (_n1 < sg["n1"])
        fr_ = np.arange(sg["n0"], sg["n1"])
        cxf = np.interp(fr_, _n1[m], _x1[m]) if m.sum() > 1 else np.full(len(fr_), float(_x1[m][0]) if m.any() else punch[i]["cx"])
        _SIGi = _sig_i
        if _SIGi > 0 and len(cxf) > 3:
            _k = np.arange(-3*int(_SIGi), 3*int(_SIGi)+1); _w = np.exp(-_k**2/(2*_SIGi**2)); _w /= _w.sum()
            _c0 = cxf[0]; cxf = np.convolve(np.pad(cxf, (len(_k)//2, len(_k)//2), mode="edge"), _w, "valid")
            cxf = cxf - (cxf[0] - _c0)*np.exp(-np.arange(len(cxf))/_SIGi)          # the landing frame stays exactly on him
        cxf = np.clip(cxf, CW[lvl]/2, 2160 - CW[lvl]/2)
        head = np.interp(fr_, _sn, _sx)
        p = punch[i]; p["cx_fixed_r2"] = p["cx"]
        p["track"] = [round(float(v), 2) for v in cxf]; p["cx"] = round(float(cxf[0]), 1)
        off = np.abs(head - cxf)/CW[lvl]*100; sp = np.abs(np.diff(cxf))*FPSX if len(cxf) > 1 else np.zeros(1)
        p.update(track_travel_px=round(float(np.abs(np.diff(cxf)).sum()), 1), landing_err_px=round(float(abs(head[0] - cxf[0])), 1),
                 off_centre_pct_med=round(float(np.median(off)), 2), off_centre_pct_max=round(float(off.max()), 2),
                 pan_p90_px_s=round(float(np.percentile(sp, 90)), 1), moving_frac=round(float((sp > 5*CW[lvl]/608).mean()), 3),
                 off_centre_pct_signed_med=round(float(np.median((head - cxf)/CW[lvl]*100)), 2), track_max_px_s=round(float(sp.max()), 1), track_settings=[_sl_i, _tol_i, _sig_i])

CTA = [[s_tap, TOTAL]]
_hb = {round(p["beat"][0], 3) for p in punch} | {round(p["beat"][1], 3) for p in punch}
_bare = [x for x in SPL if not _cov(x) and not any(abs(snapf(x) - h) < 0.02 for h in _hb)]
assert not _bare, f"bare pause splices inside a hold: {_bare}"
plan = {"ideas": IDEAS, "total": TOTAL, "total_frames": TOTALF, "timeline": _items, "dur_talk": DUR,
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
