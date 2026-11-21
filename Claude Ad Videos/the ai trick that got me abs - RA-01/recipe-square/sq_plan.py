#!/usr/bin/env python3
"""RA-01 SQUARE plan: the approved 9:16 beat sheet, UNCHANGED, plus the 1:1 crop centre per hold.

Nothing about the timeline is re-derived: beats_9x16_approved.json is the round-3 beats.json Dan
approved (cards, punch levels, hold boundaries, CTA beats, frame counts). The only addition is
`cx_sq`, the fixed horizontal centre of each hold's 1:1 crop.

The vertical moved one hold's centre (hold 4, 17.6 px) because a 594 px NEAR window could not keep
his face box inside 8-92 % of the width while he leaned. A 1056 px window has that room, so every
square hold sits on its own MEDIAN face centre (cx_pref): steady per hold, never tracked
(_shared/framing-motion.md). The 8-92 % face-box rule is still asserted here against the per-frame
extremes measured on the round-2 masters (face_src_r3.json), and again on the delivered frames.
"""
import json
B = json.load(open("beats_9x16_approved.json"))
OVR = {round(float(r["beat"]), 2): (float(r["sx0"]), float(r["sx1"]))
       for r in json.load(open("face_src_r3.json"))["holds"]}
W = {"NEAR": 1056, "FAR": 1248}
for i, p in enumerate(B["punch"]):
    cw = W[p["level"]]
    x = int(round(p["cx_pref"] - cw/2)); x = max(0, min(2160-cw, x - x % 2))
    p["cx_sq"] = x + cw/2.0
    o = OVR.get(round(float(p["beat"][0]), 2))
    if o:
        l, r = (o[0]-x)/cw, (o[1]-x)/cw
        p["face_sq"] = [round(l*100, 1), round(r*100, 1)]
        assert 0.08 <= l and r <= 0.92, (i, p["face_sq"])
    print(f"hold {i:2d} {p['level']:<4} {p['beat'][0]:6.2f}-{p['beat'][1]:6.2f}  crop x {x:4d} w {cw}  "
          f"cx_sq {p['cx_sq']:.1f}  face {p.get('face_sq')}")
B["square"] = {"levels": W, "note": "timeline identical to the approved 9:16; cx_sq added"}
json.dump(B, open("beats.json", "w"), indent=2)
print("beats.json written; total", B["total"], "frames", B["total_frames"])

# ---------------------------------------------------------------------------------------------
# SQUARE WATCH-PASS FIXES (2026-10-02). Two independent judges failed three pause-removal splices
# on the first square render as same-framing presenter jumps: 3.07 s, 19.02 s and 36.00 s. All
# three are in the approved 9:16 as well (s25_hard.py scored 19.019 and 36.003 "hard" but below the
# forced line; round 3 pinned them out). The 1:1 frame shows his arms and hands, which a 594 px
# vertical window crops off, so the same splice reads as a jump here. The CUT (cut.json) and the
# audio are untouched; only the picture's cover changes, per VIDEO-RULES 2026-09-29 (a jump is
# covered by a distinct fixed wide/tight cut or by a card):
#   * 3.07 s  -> the ai_gen card comes in ON the splice (frame 92), 3 frames earlier than the 9:16
#               (the same snap_to_splice rule s05_plan.py already applies to the stats card);
#   * 19.02 s -> a level change on the splice (frame 570). To keep every visible join a level
#               change, the two holds after it swap levels (hold 20.25-23.19 FAR, 23.19-24.86 NEAR);
#   * 36.00 s -> a level change on the splice (frame 1079): FAR until it, NEAR to the macro card
#               (FAR first so the level also alternates across the stats card and the macro card).
import numpy as np
FPS = 30000/1001; FD = 1001/30000
TRK = json.load(open("framing.json"))["samples"]
fr = lambda t: int(round(t*FPS)); ft = lambda f: round(f*FD, 6)

def stats(a, b):
    s = [x for x in TRK if a - 0.26 <= x["t"] <= b + 0.26] or TRK
    return min(x["hair"] for x in s), float(np.median([x["cx"] for x in s])), len(s), s

def mk(a_f, b_f, level, parent):
    a, b = ft(a_f), ft(b_f)
    hair, cxm, n, s = stats(a, b)
    cw = W[level]
    x = int(round(cxm - cw/2)); x = max(0, min(2160-cw, x - x % 2))
    lo = min(min(q["fx0"] for q in s), parent["_ovr"][0]) if parent.get("_ovr") else min(q["fx0"] for q in s)
    hi = max(max(q["fx1"] for q in s), parent["_ovr"][1]) if parent.get("_ovr") else max(q["fx1"] for q in s)
    l, r = (lo-x)/cw, (hi-x)/cw
    assert 0.08 <= l and r <= 0.92, (a, b, level, l, r)
    return {"beat": [a, b], "level": level, "hair_min": round(hair, 1), "cx": x + cw/2.0, "cx_pref": round(cxm, 1),
            "cx_sq": x + cw/2.0, "samples": n, "gap": parent["gap"], "frames": b_f - a_f,
            "face_sq": [round(l*100, 1), round(r*100, 1)], "square_fix": True}

P = B["punch"]
for p in P: p["_ovr"] = OVR.get(round(float(p["beat"][0]), 2))
new = []
for i, p in enumerate(P):
    a_f, b_f = fr(p["beat"][0]), fr(p["beat"][1])
    if i == 0:                       # dan00 ends on the splice; the card takes the 3 frames after it
        q = mk(a_f, 92, "NEAR", p); new.append(q)
    elif i == 3:   new += [mk(a_f, 570, "FAR", p), mk(570, b_f, "NEAR", p)]
    elif i == 4:   new.append(mk(a_f, b_f, "FAR", p))
    elif i == 5:   new.append(mk(a_f, b_f, "NEAR", p))
    elif i == 6:   new += [mk(a_f, 1079, "FAR", p), mk(1079, b_f, "NEAR", p)]   # FAR first: the level also alternates ACROSS the stats and macro cards (cut:jump_cut)
    else:
        p = dict(p); p.pop("_ovr", None); new.append(p)
for i in range(len(new)-1):
    if new[i]["gap"] == new[i+1]["gap"]:
        assert new[i]["level"] != new[i+1]["level"], (i, "same level across a visible join")
B["punch"] = new
for c in B["cards"]:
    if c["name"] == "ai_gen":
        c["beat"][0] = ft(92); c["frames"] = fr(c["beat"][1]) - 92
B["r1_beats"]["ai_gen"][0] = ft(92); B["r1_beats"]["dan_near"][1] = ft(92)
items = ([{"kind": "card", "name": c["name"], "a": c["beat"][0]} for c in B["cards"]] +
         [{"kind": "dan", "name": f"dan{i:02d}", "a": p["beat"][0]} for i, p in enumerate(new)])
items.sort(key=lambda x: x["a"])
for i, it in enumerate(items):
    it["f0"] = fr(it["a"]); it["f1"] = B["total_frames"] if i == len(items)-1 else fr(items[i+1]["a"])
    it["n"] = it["f1"] - it["f0"]; assert it["n"] > 0, it
B["timeline"] = items
n = {it["name"]: it["n"] for it in items}
for c in B["cards"]: assert c["frames"] == n[c["name"]], (c["name"], c["frames"], n[c["name"]])
for i, p in enumerate(new): assert p["frames"] == n[f"dan{i:02d}"], (i, p["frames"], n[f"dan{i:02d}"])
B["square"]["fixes"] = ["ai_gen card in at frame 92 (on the 3.07 s splice)", "level change at frame 570 (19.02 s splice); holds 607-695 / 695-745 swap to FAR / NEAR",
                        "level change at frame 1079 (36.00 s splice): 957-1078 FAR, 1079-1097 NEAR"]
json.dump(B, open("beats.json", "w"), indent=2)
print("SQUARE FIXES applied:")
for i, p in enumerate(new):
    print(f"  dan{i:02d} {p['level']:<4} f{fr(p['beat'][0])}-{fr(p['beat'][1])}  hair {p['hair_min']}  cx_sq {p['cx_sq']}  face {p.get('face_sq')}")
