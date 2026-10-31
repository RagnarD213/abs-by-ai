"""RO-37 round 2 common pieces: Dan cut out of the upright pool footage (BiRefNet per frame, 3-frame temporal median on
the alpha: the method Dan approved on the 2026-10-29 cutout test) and placed on the locked long-form green-screen
background template (.claude/skills/_shared/greenscreen-bg). Round 1's cut, words, colour F, voice A, gym B-roll tune and
HyperFrames graphics are reused unchanged (round1/recipe is imported read-only).

Placements (output 1920x1080; source is the upright 2160x3840 picture; screen = source * k + offset):
  centre W  k 0.394, body centre x 960,  hair top y 44     (hair to waistband: the test's wide)
  centre T  k 0.532 (1.35x), body centre x 960, hair top y 43 (4 % of the frame)
  right  W  k 0.394, body centre x 1400, hair top y 44     (the approved test layout beside a card)
  right  T  k 0.532, body centre x 1330, hair top y 43
  corner W  k 0.200, body centre x 1640, hair top y 560    (the approved test ending: small, lower right, over his clip)
  corner T  k 0.270, body centre x 1610, hair top y 470
  closeup   round 1's full-frame 16:9 window of the upright picture (no cutout): Dan, rarely.
Every shot keeps one placement; the round's W/T alternation at every cut is kept. A lower third puts Dan in W on the right
(the strip ends left of his torso); a side list puts him right on the moving field (Dan's approved test look)."""
import json, os, sys, glob, math, subprocess
import numpy as np
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
R1 = "/Volumes/Expansion/_edit_work/RO-37/round1"; W2 = "/Volumes/Expansion/_edit_work/RO-37/round2"
W3 = "/Volumes/Expansion/_edit_work/RO-37/round3"; M3 = f"{W3}/matte2"     # round 3: the refined (ViTMatte) matte
sys.path.insert(0, f"{R1}/recipe")
import frames as F, build as B                       # noqa: E402  round 1 (read-only)
FF = F.FF; FPS = F.FPS
def fr(t): return int(round(t * FPS))
EDL = json.load(open(f"{W3}/edl3.json")); R = json.load(open(f"{R1}/plan_resolved.json"))
WORDS = json.load(open(f"{R1}/words_out.json"))
END_F = B.make_shots(EDL)[-1]["out_f1"]
MW, MH = 1152, 2048                                   # matte resolution (the size sent to BiRefNet)
SW, SH = 2160, 3840
PLACE = {("center", "W"): (0.394, 960, 44), ("center", "T"): (0.532, 960, 43),
         ("right", "W"): (0.394, 1400, 44), ("right", "T"): (0.532, 1330, 43), ("right", "W2"): (0.460, 1440, 40),
         ("corner", "W"): (0.200, 1640, 560), ("corner", "T"): (0.270, 1610, 470)}
TYPE_PLACE = {"soft": "center", "cards": "center", "wall": "center", "side": "right", "bigtype": "right", "list": "right",
              "corner": "corner", "closeup": "closeup"}
# the full-frame pool close-up, used rarely (Dan: "just use that super close-in shot sparingly"): film seconds
CLOSEUPS = [(371.06, 374.70, "I'm just keeping it real with you guys. That's the most common reason why people quit"),
            (464.70, 468.168, "Don't worry about going hard. Just worry about showing up.")]
# Round 3: Dan's picks on the AI clips (A1, A6 killed; A2 gets the fast-forward sit-ups in front of it; A7 rebuilt, 5.9 s, ending on BG40's cut).
# Each is a finished 1080p file from ai_prep.py, full screen, AI-GENERATED chip on.
AI3 = [dict(id="A2b", kind="ai3", t0=35.0355, t1=38.2, file=f"{W3}/ai/final/A2b.mp4"), dict(id="A2", kind="ai3", t0=38.2, t1=41.053, file=f"{W3}/ai/final/A2.mp4"),
       dict(id="A3", kind="ai3", t0=56.501, t1=58.961, file=f"{W3}/ai/final/A3.mp4"), dict(id="A4", kind="ai3", t0=65.784, t1=69.484, file=f"{W3}/ai/final/A4.mp4"),
       dict(id="A7r", kind="ai3", t0=411.1446, t1=417.0, file=f"{W3}/ai/final/A7r.mp4")]
# Round 3: his arm runs off the side of the upright frame on these right-placed shots, so the frame edge goes to the screen edge (px)
DX = {"why.1": 124, "wb.0": 112}
# Round 3 trim: the 4:47 repair needs a real cut, not a pause. 12 frames come out at the join, so everything from there on plays 0.4 s earlier.
CUT_T, CUT_D = 288.0, 12 * 1001 / 30000
def sh(t): return t - CUT_D if t >= CUT_T else t
for r in R + AI3:
    if "t0" in r: r["t0"], r["t1"] = sh(r["t0"]), sh(r["t1"])
for w in WORDS: w["t0"], w["t1"] = sh(w["t0"]), sh(w["t1"])
CLOSEUPS = [(sh(a), sh(b), c) for a, b, c in CLOSEUPS]
CLIPS = sorted([r for r in R if r["kind"] == "clip"] + AI3, key=lambda r: r["t0"])
LTS = [r for r in R if r["kind"] == "lt"]
L3S = [r for r in R if r["kind"] == "l3"]


def speech(a, b):
    return " ".join(w["w"] for w in WORDS if a <= w["t0"] < b).replace(" -", "-").replace("6packabs .com", "SixPackAbs.com")


def word_t(phrase, lo, hi):
    """Start of the first word of `phrase` spoken in [lo, hi] (film seconds)."""
    ws = [w for w in WORDS if lo <= w["t0"] <= hi]; p = phrase.lower().split()
    norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
    for i in range(len(ws) - len(p) + 1):
        if all(norm(ws[i + j]["w"]) == norm(p[j]) for j in range(len(p))): return ws[i]["t0"]
    raise KeyError(f"{phrase!r} not spoken in {lo}-{hi}")


# ------------------------------------------------------------------ shots
def shots2():
    """Round 1's shots (one per piece, long pieces split at word gaps, W/T alternating from the opening W), without its
    'close-up under every lower third' rule, then split at every forced cut: lower third in/out (a zoom cut on a word start,
    Dan goes W on the right), side list in/out, close-up windows. Full-screen clips are not shots (they cover the picture)."""
    sh = B.make_shots(EDL)
    cuts = set()
    for r in LTS: cuts |= {fr(r["t0"]) - 2, fr(r["t1"]) + 2}
    for r in L3S: cuts |= {fr(r["t0"]), fr(r["t1"])}
    for a, b, _ in CLOSEUPS: cuts |= {fr(a), fr(b)}
    for r in CLIPS: cuts |= {fr(r["t0"]), fr(r["t1"])}
    out = []
    for s in sh:
        cs = sorted(c for c in cuts if s["out_f0"] < c < s["out_f1"])
        edges = [s["out_f0"]] + cs + [s["out_f1"]]
        for k, (x, y) in enumerate(zip(edges, edges[1:])):
            out.append(dict(s, out_f0=x, out_f1=y, src0=round(s["src0"] + (x - s["out_f0"]) / FPS, 4),
                            reframe=s["reframe"] if k == 0 else True))
    for s in out:
        m = (s["out_f0"] + s["out_f1"]) / 2
        s["lt"] = next((r["id"] for r in LTS if fr(r["t0"]) - 2 <= m < fr(r["t1"]) + 2), None)
        s["l3"] = next((r["id"] for r in L3S if fr(r["t0"]) <= m < fr(r["t1"])), None)
        s["closeup"] = any(fr(a) <= m < fr(b) for a, b, _ in CLOSEUPS)
        s["covered"] = next((r["id"] for r in CLIPS if fr(r["t0"]) <= s["out_f0"] and s["out_f1"] <= fr(r["t1"])), None)
        if s["lt"] and not s["covered"]: s["framing"] = "W"
    # a remnant under 1.2 s beside a lower-third piece of the same take joins it (round 1's min_rem rule); same-take
    # pieces under one lower third are one shot
    merged = []
    for s in out:
        if merged:
            p = merged[-1]
            same = (s["reframe"] and s["roll"] == p["roll"] and not s["covered"] and not p["covered"] and not s["l3"]
                    and not p["l3"] and not s["closeup"] and not p["closeup"])
            short_s, short_p = s["out_f1"] - s["out_f0"] < fr(1.2), p["out_f1"] - p["out_f0"] < fr(1.2)
            if same and ((short_s and p["lt"] and not s["lt"]) or (short_p and s["lt"] and not p["lt"]) or (s["lt"] and s["lt"] == p["lt"])):
                base = p if p["lt"] else s
                merged[-1] = dict(base, out_f0=p["out_f0"], out_f1=s["out_f1"], src0=p["src0"], reframe=p["reframe"]); continue
        merged.append(dict(s))
    for p, s in zip(merged, merged[1:]):          # a take join under one lower third: a 1.17x punch-in hides it (round 1's T2)
        if s["lt"] and s["lt"] == p["lt"] and not s["reframe"] and p["out_f1"] == s["out_f0"]: s["framing"] = "W2"
    for i, s in enumerate(merged):
        s["src1"] = round(s["src0"] + (s["out_f1"] - s["out_f0"]) / FPS, 4); s["id"] = f"{s['id'].split('~')[0]}~{i}"
    return [s for s in merged if s["out_f1"] > s["out_f0"]]


# ------------------------------------------------------------------ the matte store (per roll frame, grade-independent)
def mpath(roll, k): return f"{W2}/matte/{roll}/{k:06d}.png"


def src_index(t): return int(round(t * FPS))


def needed_frames(f0, f1, shots=None, plan=None):
    """{roll: set(source frame index)} for every cut-out presenter frame in film frames [f0, f1), plus the neighbours the
    3-frame median reads."""
    shots = shots or shots2(); need = {}
    for s in shots:
        if s["covered"] or s["closeup"]: continue
        a, b = max(f0, s["out_f0"]), min(f1, s["out_f1"])
        if a >= b: continue
        k0 = src_index(s["src0"]) + (a - s["out_f0"])
        need.setdefault(s["roll"], set()).update(range(k0 - 1, k0 + (b - a) + 1))
    return need


def alpha_birefnet(roll, k, lo, hi): return alpha(roll, k, lo, hi, mpath)
def mpath3(roll, k): return f"{M3}/{roll}/{k:06d}.png"


def alpha(roll, k, lo, hi, path=None):
    """The 3-frame temporal median alpha at roll frame k (neighbours inside [lo, hi] only: never across a take join).
    Round 3: the refined matte where it exists, else the BiRefNet one."""
    from PIL import Image
    path = path or (mpath3 if os.path.exists(mpath3(roll, k)) else mpath)
    ks = [j for j in (k - 1, k, k + 1) if lo <= j <= hi and os.path.exists(path(roll, j))]
    a = [np.asarray(Image.open(path(roll, j)), np.float32) * (1 / 255) for j in ks]
    assert a, f"no matte for {roll} {k}"
    return np.median(np.stack(a), 0) if len(a) == 3 else a[ks.index(k)] if k in ks else a[0]


def geometry(roll, k0, k1, step=6):
    """(hair top, body centre x) in SOURCE pixels over roll frames k0..k1 (from the mattes): the highest hair row of the
    whole shot (a fixed placement per shot never clips a taller moment) and the median torso centre."""
    from PIL import Image
    tops, cxs = [], []
    for k in list(range(k0, k1 + 1, step)) + [k1]:
        if not os.path.exists(mpath(roll, k)): continue
        a = np.asarray(Image.open(mpath(roll, k)), np.float32) / 255
        rows = np.where((a > 0.5).sum(1) >= 4)[0]
        if not len(rows): continue
        tops.append(rows[0] * SH / MH)
        band = a[int(MH * 0.30):int(MH * 0.45)] > 0.5                    # chest band: the torso, not the hands
        xs = np.where(band.any(0))[0]
        if len(xs): cxs.append((xs[0] + xs[-1]) / 2 * SW / MW)
    assert tops, f"no matte geometry {roll} {k0}-{k1}"
    return float(min(tops)), float(np.median(cxs)) if cxs else SW / 2


def affine(place, framing, top, cx):
    k, hx, hy = PLACE[(place, framing)]
    return k, hx - cx * k, hy - top * k


# ------------------------------------------------------------------ placement per shot
GEO_STEP = 15


def geo_frames(shots=None):
    """{roll: set(frames)}: every 15th roll frame of every cut-out shot (and its last), the sparse matte pass that fixes
    each shot's placement over the WHOLE shot before any part of it is rendered."""
    need = {}
    for s in shots or shots2():
        if s["covered"] or s["closeup"]: continue
        k0 = src_index(s["src0"]); n = s["out_f1"] - s["out_f0"]
        need.setdefault(s["roll"], set()).update(list(range(k0, k0 + n, GEO_STEP)) + [k0 + n - 1])
    return need


_GEO = {}
def shot_geo(s):
    key = f"{s['roll']}@{s['src0']}@{s['out_f1'] - s['out_f0']}"
    gp = f"{W3}/geo.json"
    if not _GEO and os.path.exists(gp): _GEO.update(json.load(open(gp)))
    if key not in _GEO:
        k0 = src_index(s["src0"]); _GEO[key] = geometry(s["roll"], k0, k0 + s["out_f1"] - s["out_f0"] - 1, step=GEO_STEP)
        json.dump(_GEO, open(gp, "w"), indent=0)
    return _GEO[key]


def seg_at(plan, t):
    return next((g for g in plan if g["t0"] - 1e-3 <= t < g["t1"] - 1e-3), None)


def seg_type(plan, s):
    g = seg_at(plan, (s["out_f0"] + s["out_f1"]) / 2 / FPS)
    return g["type"] if g else "soft"


def placement(s, typ):
    if typ == "closeup" or s["closeup"]: return "closeup", "T"
    fm = "T" if s["framing"] in ("T", "T2") else ("W2" if s["framing"] == "W2" else "W")
    if typ == "corner": return "corner", "T" if fm == "T" else "W"
    if s["lt"]: return "right", fm if fm in ("W", "W2") else "W"
    return TYPE_PLACE.get(typ, "center"), "W" if fm == "W2" else fm


def final_shots(plan=None):
    """shots2 with the framing flipped (W<->T) on the first shot of a background segment wherever the cut into it would
    otherwise keep Dan exactly where he was: the template changes the background on a picture cut, never under a still
    Dan. A flip that would leave a take join with no framing change is refused (asserted by checks())."""
    plan = plan or json.load(open(f"{W2}/bg_plan.json"))["segments"]
    S = shots2(); P = [s for s in S if not s["covered"]]
    for a, b in zip(P, P[1:]):
        if a["out_f1"] != b["out_f0"] or b["lt"] or b["closeup"]: continue
        if seg_at(plan, a["out_f0"] / FPS + 0.01) is seg_at(plan, b["out_f0"] / FPS + 0.01): continue
        if placement(a, seg_type(plan, a)) == placement(b, seg_type(plan, b)):
            b["framing"] = "T" if b["framing"] in ("W", "W2") else "W"; b["flipped"] = True
    for a, b in zip(P, P[1:]):                    # a flip that lands on a take join with no change: flip the next shot too
        if a.get("flipped") and a["out_f1"] == b["out_f0"] and not b["reframe"] and not b["lt"] and not b["closeup"] \
                and placement(a, seg_type(plan, a)) == placement(b, seg_type(plan, b)):
            b["framing"] = "T" if b["framing"] in ("W", "W2") else "W"; b["flipped"] = True
    return S


def checks(plan=None):
    plan = plan or json.load(open(f"{W2}/bg_plan.json"))["segments"]
    P = [s for s in final_shots(plan) if not s["covered"]]; out = dict(jump=[], still_bg_swap=[])
    for a, b in zip(P, P[1:]):
        if a["out_f1"] != b["out_f0"]: continue
        same = placement(a, seg_type(plan, a)) == placement(b, seg_type(plan, b))
        if same and not b["reframe"]: out["jump"].append(round(b["out_f0"] / FPS, 2))
        if same and seg_at(plan, a["out_f0"] / FPS + 0.01) is not seg_at(plan, b["out_f0"] / FPS + 0.01): out["still_bg_swap"].append(round(b["out_f0"] / FPS, 2))
    return out
