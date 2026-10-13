#!/usr/bin/env python3
"""RA-14 beat sheet + framing schedule (9:16 first; the 16:9 reads the same beats in round 2).

Every beat is anchored to a PHRASE in the aligned word list, never to a second (ad-edit lesson 38).
Writes beats.json in the shape s07_captions.py / s10_render.py already read (RA-01 recipe), plus
`overlays` (the Soft Blue Light template graphics that sit OVER the picture) and `gfx_sheet.json`
(the input of _shared/hyperframes/vertical.py).

The map (round 1 proposal, every item is on the review page):
  0.00  Dan FAR   "Guys have figured out the cheat code for getting six pack abs."
        Dan NEAR  "It's AI."                                   (punch in on the answer)
  G1    AI goal picture, AI-GENERATED   "I'm not talking about an AI picture."
        Dan FAR   "I'm talking about getting real abs in real life with AI."
        Dan NEAR  "Here's how it works."
  L1    lower third STEP 1 over Dan NEAR  "Step one: upload a photo of yourself to Abs By AI"
  P1    phone demo (approved self-generation demo)  "and generate an image of you with your dream
        body. It takes seconds"
        Dan FAR   "and it's completely free."
  L2    lower third STEP 2 over Dan NEAR  "Step two: the AI analyzes your picture and your goal."
  A1    analysis card   "It measures exactly how much fat you have to lose and where you need to
        gain muscle."
        Dan FAR   "Then it builds you a personalized workout and nutrition plan to get you there."
  L3    lower third STEP 3 over Dan NEAR  "Step three: execute with AI coaching you the whole way."
  T1    app tour (approved B0544)  "Whatever problem comes up, AI solves it instantly. A home
        workout when you can't make it to the gym."
        Dan FAR   "An adjusted plan when you're injured."
  R1    recap list over Dan NEAR  "That's the cheat code. A goal you can see, a plan built just for
        you, and a coach that's always there."
  C1    CTA button over Dan FAR  "Tap the button below now to get started." + the end hold
"""
import json, re, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L

CUT = json.load(open("cut.json"))
TRK = json.load(open("framing.json"))
W = json.load(open("words_aligned.json"))["words"]; DUR = CUT["dur"]
FD = L.FD; FPS = L.FPS
snapf = lambda t: round(round(t/FD)*FD, 6)
frx = lambda t: int(round(t*FPS))
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).strip()
SEQ = []
IDX = []                       # token -> word index (a word like "six-pack" is two tokens)
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

# pause splices on the tight timeline: a cut in or out that lands within 0.30 s AFTER a splice is
# snapped onto it, so there is one visual event and not two (RA-01 lesson, kept)
_acc, SPL = 0.0, []
for _a, _b in CUT["keeps"][:-1]:
    _acc += _b - _a; SPL.append(round(_acc, 3))
SEAMS = [s["t"] for s in CUT["seams"]]


def on_splice(t, win=0.30):
    near = [x for x in SPL + SEAMS if abs(t - x) <= win]
    return snapf(min(near, key=lambda x: abs(x - t))) if near else snapf(t)


# ------------------------------------------------------------------ phrase anchors
t_its_ai   = on_splice(at("its ai"))
t_not      = on_splice(at("im not talking"))
e_picture  = end("an ai picture", pad=0.0)
t_talking  = on_splice(at("im talking about getting", after=e_picture - 0.2))
t_heres    = on_splice(at("heres how it works"))
t_step1    = on_splice(at("step one"))
t_generate = on_splice(at("and generate an image"))
e_seconds  = end("it takes seconds", pad=0.0)
t_free     = on_splice(at("and its completely free"), win=0.20)
t_step2    = on_splice(at("step two"))
t_measures = on_splice(at("it measures exactly"))
e_muscle   = end("gain muscle", pad=0.0)
t_then     = on_splice(at("then it builds"))
t_step3    = on_splice(at("step three"))
t_whatever = on_splice(at("whatever problem"))
e_gym      = end("to the gym", pad=0.0)
t_adjusted = on_splice(at("an adjusted plan"))
t_thats    = on_splice(at("thats the cheat code"))
e_there    = end("always there", pad=0.0)
t_tap      = on_splice(at("tap the button"))

# opaque inserts (they replace the picture; captions keep running under/over them)
CARDS = [
 {"name": "G1", "kind": "ai_photo", "beat": [t_not, t_talking],
  "what": "AI goal picture, AI-GENERATED", "label": "ai", "people": "dan", "physique": True},
 {"name": "P1", "kind": "phone",    "beat": [t_generate, t_free],
  "what": "approved self-generation demo: his photo, options, generating, the result",
  "label": "ai", "people": "dan", "physique": True},
 {"name": "A1", "kind": "analysis", "beat": [t_measures, t_then],
  "what": "analysis card on the goal picture", "label": "ai", "people": "dan", "physique": True},
 {"name": "T1", "kind": "phone",    "beat": [t_whatever, t_adjusted],
  "what": "approved app tour B0544: calorie tracking, then AI Trainer demo videos",
  "label": "ai", "people": "ai-dan", "physique": False},
]
for c in CARDS:
    c["beat"] = [snapf(c["beat"][0]), snapf(c["beat"][1])]
    assert c["beat"][1] - c["beat"][0] >= 1.2, (c, "a card under 1.2 s is a flash")
for a, b in zip(CARDS, CARDS[1:]):
    assert a["beat"][1] <= b["beat"][0], (a, b)

# template overlays over the picture (Soft Blue Light, HyperFrames)
OVER = [
 {"id": "L1", "template": "lower-third", "t0": t_step1, "t1": t_generate,
  "config": {"topic": "STEP 1", "parts": [["Generate Your Goal Picture", word_t("upload a photo")]]}},
 {"id": "L2", "template": "lower-third", "t0": t_step2, "t1": t_measures,
  "config": {"topic": "STEP 2", "parts": [["AI Builds Your Custom Plan", word_t("the ai analyzes")]]}},
 {"id": "L3", "template": "lower-third", "t0": t_step3, "t1": t_whatever,
  "config": {"topic": "STEP 3", "parts": [["AI Coaches You Every Day", word_t("execute with ai")]]}},
 {"id": "R1", "template": "side-list", "t0": t_thats, "t1": t_tap,
  "config": {"heading": "The Cheat Code",
             "items": ["A Goal You Can See", "A Plan Built Just For You", "A Coach That's Always There"],
             "reveal": [word_t("a goal you can see"), word_t("a plan built"), word_t("a coach thats")],
             "drift": 0}},
 {"id": "C1", "template": "cta", "t0": t_tap, "t1": TOTAL,
  "config": {"top": "Tap The Button Below", "big": "Get Started", "hold_out": True}},
]
for g in OVER:
    g["t0"], g["t1"] = snapf(g["t0"]), snapf(g["t1"])
    g["config"].update(id=g["id"], a=g["t0"], b=g["t1"])
    assert g["t1"] - g["t0"] >= 2.0, (g["id"], g["t1"] - g["t0"], "too short to read")

# ------------------------------------------------------------------ Dan holds: level per hold
# Two levels only, hair-anchored (FRAMING STANDARD 2026-09-08). Each entry: (start, level).
HOLDS = [
 (0.0,        "FAR"),    # the hook shows the proof: hair to shorts
 (t_its_ai,   "NEAR"),   # punch in on the answer
 (t_talking,  "FAR"),    # "real abs in real life": the abs are in frame
 (t_heres,    "NEAR"),
 (t_step1,    "FAR"),    # L1 is up: the strip sits low on a FAR frame, clear of his face
 (t_free,     "NEAR"),
 (t_step2,    "FAR"),    # L2
 (t_then,     "NEAR"),
 (t_step3,    "FAR"),    # L3
 (t_adjusted, "NEAR"),
 (t_thats,    "FAR"),    # R1 list card at the bottom
 (t_tap,      "NEAR"),   # C1
]
card_spans = [tuple(c["beat"]) for c in CARDS]
segs = []
bounds = [h[0] for h in HOLDS] + [TOTAL]
for i, (a, lvl) in enumerate(HOLDS):
    b = bounds[i+1]
    for ca, cb in card_spans:           # a card ends this hold
        if a < ca < b: b = ca
    a2 = a
    for ca, cb in card_spans:           # a hold that starts under a card starts when the card ends
        if ca <= a2 < cb: a2 = cb
    if b - a2 > 0.25:
        segs.append([snapf(a2), snapf(b), lvl])
segs.sort()
notes = []
SAM = TRK["samples"]
CW = {k: v[0] for k, v in L.Aspect("9x16").levels.items()}
punch = []
for i, (a, b, lvl) in enumerate(segs):
    s = [x for x in SAM if a - 0.05 <= x["t"] <= min(b, DUR) + 0.05] or \
        [x for x in SAM if a - 0.4 <= x["t"] <= b + 0.4] or SAM
    cxs = np.array([x["cx"] for x in s])
    hair = min(x["hair"] for x in s)
    cw = CW[lvl]
    # land-then-hold (2026-10-03): a hold where he wanders < 6.6 % of the crop width keeps ONE
    # fixed centre, anchored to its measured first-frame head centre, not its median.
    wander = float(cxs.max() - cxs.min())
    fixed_ok = wander < 0.066*cw
    cx = float(s[0]["cx"])
    off = np.abs(cxs - cx)/cw*100
    if not fixed_ok:
        notes.append(f"hold {i} ({a:.2f}-{b:.2f} {lvl}) wanders {wander:.0f} px = {wander/cw*100:.1f} % of the "
                     f"crop width (limit 6.6 %): needs landing.vertical_track in round 2")
    fx0 = min(x["fx0"] for x in s); fx1 = max(x["fx1"] for x in s)
    x0 = cx - cw/2
    face = [round((fx0-x0)/cw*100, 1), round((fx1-x0)/cw*100, 1)]
    if face[0] < 8 or face[1] > 92:
        notes.append(f"hold {i} face box {face} % leaves the 8-92 % band")
    punch.append({"beat": [a, b], "level": lvl, "hair_min": round(hair, 1), "cx": round(cx, 1),
                  "samples": len(s), "wander_px": round(wander, 1), "wander_pct": round(wander/cw*100, 2),
                  "off_centre_pct_med": round(float(np.median(off)), 2),
                  "off_centre_pct_max": round(float(off.max()), 2), "face_pct": face})
for i in range(len(punch)-1):
    covered = any(abs(c[0] - punch[i]["beat"][1]) < 1e-3 for c in card_spans)
    if not covered and punch[i]["level"] == punch[i+1]["level"]:
        notes.append(f"holds {i}/{i+1} share {punch[i]['level']} across an UNCOVERED join")

# ------------------------------------------------------------------ land, then hold (Dan, 2026-10-03, locked 10-05)
# The crop lands on his measured head centre at each cut, holds inside a 3.3 % dead band, follows only when he leaves
# it. _shared/cut/landing.py is the only tracker; coordinates are SOURCE pixels, per level's crop width.
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/cut")
import landing
sn = np.array([frx(x["t"]) for x in SAM]); sx = np.array([x["cx"] for x in SAM], float)
_o = np.argsort(sn); sn, sx = sn[_o], sx[_o]
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
        punch[i]["track"] = [round(float(v), 2) for v in cxf]              # one centre per output frame of the hold
        punch[i]["cx"] = round(float(cxf[0]), 1)
        off = np.abs(head - cxf)/CW[lvl]*100
        punch[i]["track_travel_px"] = round(float(np.abs(np.diff(cxf)).sum()), 1) if len(cxf) > 1 else 0.0
        punch[i]["landing_err_px"] = round(float(abs(head[0] - cxf[0])), 1)
        punch[i]["off_centre_pct_med"] = round(float(np.median(off)), 2); punch[i]["off_centre_pct_max"] = round(float(off.max()), 2)
        sp = np.abs(np.diff(cxf))*FPS if len(cxf) > 1 else np.zeros(1)
        punch[i]["pan_p90_px_s"] = round(float(np.percentile(sp, 90)), 1)
        punch[i]["moving_frac"] = round(float((sp > 5*CW[lvl]/608).mean()), 3)
notes = [n for n in notes if "wanders" not in n]      # the track above is the answer to a wandering hold

TOTALF = frx(TOTAL)
items = ([{"kind": "card", "name": c["name"], "a": c["beat"][0]} for c in CARDS] +
         [{"kind": "dan", "name": f"dan{i:02d}", "a": p["beat"][0]} for i, p in enumerate(punch)])
items.sort(key=lambda x: x["a"])
for i, it in enumerate(items):
    it["f0"] = frx(it["a"])
    it["f1"] = TOTALF if i == len(items)-1 else frx(items[i+1]["a"])
    it["n"] = it["f1"] - it["f0"]
    assert it["n"] > 0, it
FR = {it["name"]: it["n"] for it in items}
for c in CARDS: c["frames"] = FR[c["name"]]
for i, p in enumerate(punch): p["frames"] = FR[f"dan{i:02d}"]

# splices inside a hold are naked unless measured invisible (s25_hard.py, round 2): list them
inside = []
for x in SPL:
    for i, p in enumerate(punch):
        if p["beat"][0] + 0.10 < x < p["beat"][1] - 0.10:
            inside.append({"t": x, "hold": i})
plan = {"total": TOTAL, "total_frames": TOTALF, "timeline": items, "dur_talk": DUR, "end_hold": END_HOLD,
        "cards": CARDS, "punch": punch, "overlays": OVER, "seams": CUT["seams"],
        "splices_inside_holds": inside, "framing_notes": notes,
        "cta": [[OVER[-1]["t0"], OVER[-1]["t1"]]]}
json.dump(plan, open("beats.json", "w"), indent=2)
json.dump({"graphics": OVER}, open("gfx_sheet.json", "w"), indent=1)
cov = sum(c["beat"][1]-c["beat"][0] for c in CARDS)
ovc = sum(g["t1"]-g["t0"] for g in OVER)
print(f"total {TOTAL:.2f}s   talk {DUR:.2f}s + {END_HOLD:.2f}s end hold   ({59.0-TOTAL:.2f}s under the 59.00 ceiling)")
print(f"opaque cards {len(CARDS)} = {cov:.2f}s ({cov/TOTAL*100:.0f}%), overlays {len(OVER)} = {ovc:.2f}s; "
      f"something on screen besides Dan {((cov+ovc)/TOTAL*100):.0f}% of runtime")
for c in CARDS: print(f"   {c['name']} {c['kind']:<9} {c['beat'][0]:6.2f} -> {c['beat'][1]:6.2f} ({c['beat'][1]-c['beat'][0]:.2f}s)")
for g in OVER: print(f"   {g['id']} {g['template']:<11} {g['t0']:6.2f} -> {g['t1']:6.2f} ({g['t1']-g['t0']:.2f}s)")
print(f"Dan holds {len(punch)}:")
for i, p in enumerate(punch):
    print(f"   {i:2d} {p['level']:<4} {p['beat'][0]:6.2f} -> {p['beat'][1]:6.2f}  hair_min {p['hair_min']:6.1f}  lands cx {p['cx']:6.1f} (err {p['landing_err_px']} px)  "
          f"he wanders {p['wander_pct']:4.1f}%  crop travels {p['track_travel_px']:5.1f} px, p90 {p['pan_p90_px_s']:5.1f} px/s, moving {p['moving_frac']*100:3.0f}%  "
          f"off-centre med {p['off_centre_pct_med']:.1f}% max {p['off_centre_pct_max']:.1f}%")
print("pause splices inside holds (round 2 measures which are visible):", [(x['t'], x['hold']) for x in inside])
for n in notes: print("  !", n)
