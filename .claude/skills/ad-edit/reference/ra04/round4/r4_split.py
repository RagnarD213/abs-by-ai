#!/usr/bin/env python3
"""RA-04 round 4: split dan03 (9.94-12.21 s, cards on both sides) into two holds with a zoom cut between them at the word boundary
"make a | picture" (10.92 s, frame 327). The 9:16 judge (3rd pass) failed the follow there twice: he walks 1187 -> 1408 px of 4K in 1.6 s
(about a third of the NEAR width), so any crop that keeps him centred pans 23 % of the frame. Two holds that each land on him replace the
long pan with a cut. dan03 = FAR "It's easy to make a" (9.94-10.92), new dan04 = NEAR "picture of yourself like this." (10.92-12.21).
Reads and rewrites round4/beats_r4base.json (after r4_home.py)."""
import json
import numpy as np
P_ = "round4/beats_r4base.json"
B = json.load(open(P_)); FPS = 30000/1001
SAM = json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"]
SPLIT = 327
tl = B["timeline"]; P = B["punch"]
assert not any(p.get("r4_split") for p in P), "already split"
j = next(i for i, it in enumerate(tl) if it["name"] == "dan03")
it3 = tl[j]; f0, f1 = it3["f0"], it3["f1"]; assert f0 < SPLIT < f1 and tl[j-1]["kind"] == "card" and tl[j+1]["kind"] == "card"
for it in tl:
    if it["kind"] == "dan" and int(it["name"][3:]) >= 4: it["name"] = f"dan{int(it['name'][3:]) + 1:02d}"
it3["f1"] = SPLIT; it3["n"] = SPLIT - f0
tl.insert(j + 1, dict(kind="dan", name="dan04", a=round(SPLIT/FPS, 6), f0=SPLIT, f1=f1, n=f1 - SPLIT))
def hold(a, b, level, base):
    s = [x for x in SAM if a - 0.05 <= x["t"] <= b + 0.05]; assert s
    return dict(base, beat=[round(a, 6), round(b, 6)], level=level, hair_min=float(min(x["hair"] for x in s)),
                cx=round(float(np.median([x["cx"] for x in s])), 1), samples=len(s), frames=None, r4_split=True)
old = P[3]
P[3] = hold(f0/FPS, SPLIT/FPS, "FAR", {k: v for k, v in old.items() if k in ("cx16",)}); P[3]["frames"] = SPLIT - f0
P.insert(4, hold(SPLIT/FPS, f1/FPS, "NEAR", {"cx16": old.get("cx16", 1088.0)})); P[4]["frames"] = f1 - SPLIT
for i, it in enumerate(tl):
    assert abs(it["a"] - it["f0"]/FPS) < 0.02 and it["n"] > 0 and (i == 0 or it["f0"] == tl[i-1]["f1"]), it
assert [it["name"] for it in tl if it["kind"] == "dan"] == [f"dan{i:02d}" for i in range(len(P))]
for i, p in enumerate(P): assert p["frames"] == next(it["n"] for it in tl if it["name"] == f"dan{i:02d}"), i
json.dump(B, open(P_, "w"), indent=2)
print("dan03", P[3]["beat"], P[3]["level"], "dan04", P[4]["beat"], P[4]["level"], "holds", len(P))
