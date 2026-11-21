#!/usr/bin/env python3
"""RA-07 round 5 beat sheet (round 4's, PENDING empty: G1 and O1 are real clips) + framing schedule (9:16). Dan's round 3 answers: round4-plan/decisions.json.

  python3 s70r4_plan.py      -> beats_r4.json + round4/gfx_sheet_r4.json

Round 4 re-lays 36.47-47.01 only (Dan: the broken-arm clip at the injury; "He goes to the gym, and it's closed... then he does
dumbbell curls"; the equipment out of order is a LEG PRESS, then the hack squat). Each fix follows its problem:

  A1  library clip A0179 (RA-04's broken-arm man: the rack and the head shake, then the leg press)  "when life gets in the way, when you get injured"
  G1  NEW AI clip 'Gym closed' (frames pending Dan's yes: labelled placeholder)                     "or you can't make it to the gym"
  M1  library clip A0039 (home dumbbell curls)                                                       "one day,"
  O1  NEW AI clip 'Leg press out of order' (frames pending Dan's yes: labelled placeholder)         "or when the equipment you need is broken."
  H2  round 3's hack squat take I4bW_v1 (nod, towel, steps on)                                       "AI adjusts your plan in seconds"
  I5  AI clip 'Back next week', unchanged                                                            "while human trainers leave you confused until next week."

I3a, I3b and I4a (the tweaked shoulder, the lateral raise, the Smith machine) are dropped. The first 30 s must come out
frame-identical to round 2 (s88 checks it). Built from s70r3_plan.py (RA-07 round 3) with RA-14 round 3's land-then-hold track.
"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
OUTP = os.environ.get("OUT", "beats_r5.json")
I4B_DAN = os.environ.get("H2", "clip") == "dan"
I2_DAN = os.environ.get("I2", "dan") == "dan"       # round 3: no 1.2 s window of I2_v3 passes the take review; camera until a retake     # Dan on camera in I4b's slot (VIDEO-RULES: "if you can't make it look natural, then just use the camera scene")

CUT = json.load(open("cut.json"))
TRK = json.load(open("framing.json"))
W = json.load(open("words_aligned.json"))["words"]; DUR = CUT["dur"]
FD = L.FD; FPS = L.FPS
snapf = lambda t: round(round(t/FD)*FD, 6)
frx = lambda t: int(round(t*FPS))
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).strip()
SEQ, IDX = [], []
for i, w in enumerate(W):
    for tok in norm(w["w"]).split():
        SEQ.append(tok); IDX.append(i)


def _find(ph, after=0.0):
    toks = norm(ph).split()
    for k in range(len(SEQ)-len(toks)+1):
        if W[IDX[k]]["t"] >= after - 1e-6 and SEQ[k:k+len(toks)] == toks:
            return IDX[k], IDX[k+len(toks)-1]
    raise KeyError(f"phrase not found after {after}: {ph!r}")


def at(ph, after=0.0, pad=-0.06):  return round(W[_find(ph, after)[0]]["t"] + pad, 3)
def end(ph, after=0.0, pad=0.10):  return round(W[_find(ph, after)[1]]["e"] + pad, 3)
def word_t(ph, after=0.0):         return round(W[_find(ph, after)[0]]["t"], 3)


END_HOLD = L.END_HOLD
TOTAL = snapf(DUR + END_HOLD)
_acc, SPL = 0.0, []
for _a, _b in CUT["keeps"][:-1]:
    _acc += _b - _a; SPL.append(round(_acc, 3))
SEAMS = [s["t"] for s in CUT["seams"]]


def on_splice(t, win=0.30):
    near = [x for x in SPL + SEAMS if abs(t - x) <= win]
    return snapf(min(near, key=lambda x: abs(x - t))) if near else snapf(t)


_spl = lambda t: snapf(min(SPL + SEAMS, key=lambda x: abs(x - t)))

# ------------------------------------------------------------------ phrase anchors
t_why      = on_splice(at("why are thousands"))       # the "AI." | "Why" pause splice (3.437): H1 ends on it
t_because  = on_splice(at("because ai can"))
t_one      = on_splice(at("one ai can visualize"))
t_one_ai   = _spl(13.013)                             # "One," | "AI can visualize" pause splice
t_inseconds= on_splice(at("in seconds", after=t_one))
t_lock     = on_splice(at("on your lock"))
t_paper    = on_splice(at("a paper from"))
t_lose     = _spl(20.521)                             # "says, goal," | "lose 20 pounds" pause splice (I1 used to cover it)
t_two      = on_splice(at("two ai can design"))
t_two_ai   = _spl(23.423)                             # "Two," | "AI can design"
t_andwhen  = on_splice(at("and when you have"))
t_youll    = on_splice(at("youll get far"))
t_than     = on_splice(at("than the generic"))
t_three    = on_splice(at("and three"))
# round 3: I2_v3's paper stack turns cloth-like from its frame 48 (take review I2_v3.f0-64, FAIL) and a phantom shoe lifts and
# vanishes in its frames 0-8 (review I2_v3.f0-45, FAIL): I2 plays source frames 9-44 (1.47 s) and Dan is on camera for the rest
# of "...a human trainer will give you."
t_i2end    = snapf(t_than + 1.47)
t_three_ai = _spl(35.068)                             # "And three," | "AI can adjust"
t_life     = on_splice(at("when life gets"))
# round 4 slot edges (handoff table, checked against words_aligned.json): every clip at least 1.2 s
t_gym      = round(snapf(word_t("or you cant make it")) - FD, 6)   # A1 ends one frame before "or" (38.58): the clean part of A0179 is 62 frames; G1 starts on "or you can't make it to the gym"
t_curls    = snapf(39.80)                              # G1 ends after "gym" (39.50-39.62); M1 the home curls on "one day," (39.76-40.06)
t_oo       = snapf(41.02)                              # M1 ends; O1 the leg press out of order, on "equipment you need is broken." (40.90-41.98)
t_hack     = snapf(42.40)                              # O1 ends; H2 the hack squat, as "AI adjusts your plan in seconds" (42.22-43.74) plays
t_while    = snapf(word_t("while human trainers"))    # I5 on "while human trainers leave you confused until next week."
t_cta      = on_splice(at("get started building"))
t_tap      = on_splice(at("tap the button"))
A0147_LEN  = 4.04
assert t_why <= A0147_LEN, "H1 plays from its first frame at its own speed: the slot must fit the clip"

PENDING = set()                            # round 5: G1 and O1 are real clips (frames approved by Dan in round 4)
CARDS = [
 {"name": "H1",  "kind": "clip",  "beat": [0.0, t_why], "what": "library clip A0147: the fired trainer walks out with his box while a robot spots the lifter",
  "label": "ai", "people": "other", "physique": False},
 {"name": "P1",  "kind": "phone", "beat": [t_inseconds, t_lock], "what": "approved self-generation demo: generating over his photo, then the result",
  "label": "ai", "people": "dan", "physique": True},
 {"name": "K1",  "kind": "phone", "beat": [t_lock, t_paper], "what": "the goal picture as a phone lock screen",
  "label": "ai", "people": "dan", "physique": True},
 {"name": "W1",  "kind": "phone", "beat": [t_andwhen, t_youll], "what": "real AI Trainer screens B0034: the exercise sheet with its demo video",
  "label": "ai", "people": "ai-dan", "physique": False},
 {"name": "I2",  "kind": "ai_clip", "beat": [t_than, t_i2end], "what": "AI clip 'Same sheet for everyone'", "label": "ai", "people": "other", "physique": False},
 {"name": "A1",  "kind": "ai_clip", "beat": [t_life, t_gym], "what": "library clip A0179: the man with the broken arm in a sling at the squat rack shakes his head, then does the leg press",
  "label": "ai", "people": "other", "physique": False},
 {"name": "G1",  "kind": "ai_clip", "beat": [t_gym, t_curls], "what": "NEW AI clip 'Gym closed': he walks up to the gym door, reads the CLOSED sign and shrugs",
  "label": "ai", "people": "other", "physique": False},
 {"name": "M1",  "kind": "clip",  "beat": [t_curls, t_oo], "what": "library clip A0039: a man curling dumbbells in his living room",
  "label": "ai", "people": "other", "physique": False},
 {"name": "O1",  "kind": "ai_clip", "beat": [t_oo, t_hack], "what": "NEW AI clip 'Leg press out of order': he walks up to the leg press, sees the OUT OF ORDER sign and shrugs",
  "label": "ai", "people": "other", "physique": False},
 {"name": "H2",  "kind": "ai_clip", "beat": [t_hack, t_while], "what": "AI clip 'Hack squat instead' (round 3's approved take): he nods, hangs his towel on it and steps on",
  "label": "ai", "people": "other", "physique": False},
 {"name": "I5",  "kind": "ai_clip", "beat": [t_while, t_cta], "what": "AI clip 'Back next week'", "label": "ai", "people": "other", "physique": False},
]
if I4B_DAN:
    CARDS = [c for c in CARDS if c["name"] != "H2"]
if I2_DAN:
    CARDS = [c for c in CARDS if c["name"] != "I2"]
for c in CARDS:
    c["beat"] = [snapf(c["beat"][0]), snapf(c["beat"][1])]
    c["pending"] = c["name"] in PENDING
    assert c["beat"][1] - c["beat"][0] >= 1.2, (c["name"], c["beat"], "a clip under 1.2 s is a flash")
for a, b in zip(CARDS, CARDS[1:]):
    assert a["beat"][1] <= b["beat"][0] + 1e-6, (a["name"], b["name"])

# ROUND 2 check (Gemini watch, confirmed by eye at 23.25 s): with the headline on "AI can ..." the glass strip sat EMPTY over his chest
# for 0.6 / 0.55 / 0.9 s after it appeared, reading as a stray blur box. Each headline now lands on its number word.
OVER = [
 {"id": "L1", "template": "lower-third", "t0": t_one, "t1": t_inseconds,
  "config": {"topic": "1 OF 3", "parts": [["See Your Goal Physique", word_t("one ai can visualize")]]}},
 {"id": "L2", "template": "lower-third", "t0": t_two, "t1": t_andwhen,
  "config": {"topic": "2 OF 3", "parts": [["A Program Built For Your Goal", word_t("two ai can design")]]}},
 {"id": "L3", "template": "lower-third", "t0": t_three, "t1": t_life,
  "config": {"topic": "3 OF 3", "parts": [["A Plan That Adjusts To Your Life", word_t("three ai can adjust")]]}},
 {"id": "C1", "template": "cta", "t0": t_cta, "t1": TOTAL,
  "config": {"top": "Tap The Button Below", "big": "Get Started", "hold_out": True}},
]
for g in OVER:
    g["t0"], g["t1"] = snapf(g["t0"]), snapf(g["t1"])
    g["config"].update(id=g["id"], a=g["t0"], b=g["t1"])
    assert g["t1"] - g["t0"] >= 2.0, (g["id"], g["t1"] - g["t0"], "too short to read")

# ------------------------------------------------------------------ Dan holds
# Every pause splice on this roll measured as a visible jump (round2/splices/splices.json: join 2.4-11x the roll's own
# frame-to-frame motion), so each one inside a Dan stretch gets a size change ON it. The three numbered points fall out
# as one grammar: punch in on the number ("One," "Two," "And three,"), pull back for the point.
HOLDS = [
 (t_why,      "NEAR"),   # back from the clip, tight on the question
 (t_because,  "FAR"),    # 9.576 splice
 (t_one,      "NEAR"),   # "One,"          12.579 splice (7.7x)
 (t_one_ai,   "FAR"),    # "AI can visualize your goal physique"   13.013 splice
 (t_paper,    "NEAR"),   # after K1: "A paper from your trainer that says goal,"
 (t_lose,     "FAR"),    # "lose 20 pounds, does not."   20.521 splice
 (t_two,      "NEAR"),   # "Two,"          22.990 splice
 (t_two_ai,   "FAR"),    # "AI can design a personalized workout program..."   23.423 splice
 (t_youll,    "FAR"),    # after W1: "you'll get far better results"
 ] + ([(t_than, "NEAR")] if I2_DAN else []) + [   # I2's slot on camera: "than the generic program that a"
 (t_i2end,   "FAR"),    # after I2 (cut short): "...trainer will give you."
 (t_three,    "NEAR"),   # "And three,"    34.301 splice
 (t_three_ai, "FAR"),    # "AI can adjust your plan"   35.068 splice
] + ([(t_hack, "NEAR")] if I4B_DAN else []) + [   # camera in place of a clip
 (t_cta,      "FAR"),    # after I5, the R1|R2 seam: "Get started building your six pack abs" (abs in frame)
 (_spl(49.917), "NEAR"), # "Tap the button below to take the first step."   49.917 splice
]
card_spans = [tuple(c["beat"]) for c in CARDS]
segs = []
bounds = [h[0] for h in HOLDS] + [TOTAL]
for i, (a, lvl) in enumerate(HOLDS):
    b = bounds[i+1]
    for ca, cb in card_spans:
        if a < ca < b: b = ca
    a2 = a
    for ca, cb in card_spans:
        if ca <= a2 < cb: a2 = cb
    if b - a2 > 0.25:
        segs.append([snapf(a2), snapf(b), lvl])
segs.sort()
notes = []
SAM = list(TRK["samples"])
if os.path.exists("framing_holdstart.json"):
    SAM = sorted(SAM + json.load(open("framing_holdstart.json"))["samples"], key=lambda x: x["t"])
CW = {k: v[0] for k, v in L.Aspect("9x16").levels.items()}
punch = []
for i, (a, b, lvl) in enumerate(segs):
    s = [x for x in SAM if a - 0.05 <= x["t"] <= min(b, DUR) + 0.05] or \
        [x for x in SAM if a - 0.4 <= x["t"] <= b + 0.4] or SAM
    cxs = np.array([x["cx"] for x in s]); hair = min(x["hair"] for x in s); cw = CW[lvl]
    wander = float(cxs.max() - cxs.min()); cx = float(s[0]["cx"])
    fx0 = min(x["fx0"] for x in s); fx1 = max(x["fx1"] for x in s); x0 = cx - cw/2
    face = [round((fx0-x0)/cw*100, 1), round((fx1-x0)/cw*100, 1)]
    if face[0] < 8 or face[1] > 92: notes.append(f"hold {i} face box {face} % leaves the 8-92 % band")
    punch.append({"beat": [a, b], "level": lvl, "hair_min": round(hair, 1), "cx": round(cx, 1), "samples": len(s),
                  "wander_px": round(wander, 1), "wander_pct": round(wander/cw*100, 2), "face_pct": face})
for i in range(len(punch)-1):
    covered = any(abs(c[0] - punch[i]["beat"][1]) < 1e-3 for c in card_spans)
    if not covered and punch[i]["level"] == punch[i+1]["level"]:
        notes.append(f"holds {i}/{i+1} share {punch[i]['level']} across an UNCOVERED join")

# land, then hold (_shared/cut/landing.py), source pixels per level
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/cut")
import landing
sn = np.array([frx(x["t"]) for x in SAM]); sx = np.array([x["cx"] for x in SAM], float)
_o = np.argsort(sn, kind="stable"); sn, sx = sn[_o], sx[_o]
_u = np.concatenate([[True], np.diff(sn) > 0]); sn, sx = sn[_u], sx[_u]
for lvl in ("NEAR", "FAR"):
    idx = [i for i, p in enumerate(punch) if p["level"] == lvl]
    segs_l = [{"n0": frx(punch[i]["beat"][0]), "n1": frx(punch[i]["beat"][1])} for i in idx]
    n_all, x_all, info = landing.track(sn, sx, segs_l, slope_px_s=170*CW[lvl]/608, k=3, fixed_under=40*CW[lvl]/608,
                                       fps=FPS, tolerance=20*CW[lvl]/608)
    n_all, x_all = np.asarray(n_all), np.asarray(x_all)
    for i, sg in zip(idx, segs_l):
        m = (n_all >= sg["n0"]) & (n_all < sg["n1"])
        fr_ = np.arange(sg["n0"], sg["n1"])
        cxf = np.interp(fr_, n_all[m], x_all[m]) if m.sum() > 1 else np.full(len(fr_), float(x_all[m][0]) if m.any() else punch[i]["cx"])
        head = np.interp(fr_, sn, sx)
        punch[i]["track"] = [round(float(v), 2) for v in cxf]
        punch[i]["cx"] = round(float(cxf[0]), 1)
        off = np.abs(head - cxf)/CW[lvl]*100
        punch[i]["track_travel_px"] = round(float(np.abs(np.diff(cxf)).sum()), 1) if len(cxf) > 1 else 0.0
        punch[i]["landing_err_px"] = round(float(abs(head[0] - cxf[0])), 1)
        punch[i]["off_centre_pct_med"] = round(float(np.median(off)), 2); punch[i]["off_centre_pct_max"] = round(float(off.max()), 2)

TOTALF = frx(TOTAL)
items = ([{"kind": "card", "name": c["name"], "a": c["beat"][0]} for c in CARDS] +
         [{"kind": "dan", "name": f"dan{i:02d}", "a": p["beat"][0]} for i, p in enumerate(punch)])
items.sort(key=lambda x: x["a"])
for i, it in enumerate(items):
    it["f0"] = frx(it["a"]); it["f1"] = TOTALF if i == len(items)-1 else frx(items[i+1]["a"]); it["n"] = it["f1"] - it["f0"]
    assert it["n"] > 0, it
FR = {it["name"]: it["n"] for it in items}
for c in CARDS: c["frames"] = FR[c["name"]]
for i, p in enumerate(punch): p["frames"] = FR[f"dan{i:02d}"]
inside = [{"t": x, "hold": i} for x in SPL + SEAMS for i, p in enumerate(punch) if p["beat"][0] + 0.10 < x < p["beat"][1] - 0.10]
plan = {"total": TOTAL, "total_frames": TOTALF, "timeline": items, "dur_talk": DUR, "end_hold": END_HOLD,
        "cards": CARDS, "punch": punch, "overlays": OVER, "seams": CUT["seams"],
        "splices_inside_holds": inside, "framing_notes": notes, "cta": [[OVER[-1]["t0"], OVER[-1]["t1"]]]}
json.dump(plan, open(OUTP, "w"), indent=2)
os.makedirs("round5", exist_ok=True)
json.dump({"graphics": OVER}, open("round5/gfx_sheet_r5.json", "w"), indent=1)
print(f"total {TOTAL:.2f}s ({TOTALF} f)   talk {DUR:.2f}s + {END_HOLD:.2f}s end hold")
for c in CARDS: print(f"   {c['name']:<4} {c['kind']:<8} {c['beat'][0]:6.2f} -> {c['beat'][1]:6.2f} ({c['beat'][1]-c['beat'][0]:.2f}s){'  PENDING' if c['pending'] else ''}")
for g in OVER: print(f"   {g['id']:<4} {g['template']:<11} {g['t0']:6.2f} -> {g['t1']:6.2f}")
for i, p in enumerate(punch):
    print(f"   dan{i:02d} {p['level']:<4} {p['beat'][0]:6.2f} -> {p['beat'][1]:6.2f}  hair {p['hair_min']:6.1f}  cx {p['cx']:6.1f} (land err {p['landing_err_px']})  "
          f"wander {p['wander_pct']:4.1f}%  travel {p['track_travel_px']:5.1f}  off-centre max {p['off_centre_pct_max']:.1f}%  face {p['face_pct']}")
print("splices left inside holds:", inside)
for n in notes: print("  !", n)
