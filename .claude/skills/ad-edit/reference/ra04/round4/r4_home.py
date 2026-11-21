#!/usr/bin/env python3
"""RA-04 round 4: the home card (B0464, Dan's real squats on the lawn) re-timed after the 9:16 watch-pass judge found his head leaving
the top of the frame at 47.07-47.30 s. The SOURCE clip cuts his head at the top of every rep (person mask, round4/b0464_mask.json:
top row 0 at 2.0-2.3, 3.3-3.4, 4.5-4.8, 5.7-6.0, 6.9-7.2, 9.5-9.7 s); the only clean stretch is 7.30-9.45 s (top >= 8 of 270).
So the card is 64 frames (2.135 s) = clip 7.30-9.435, on "Abs By AI design you a home workout" (frames 1360-1424, starting in the
gap after "have" at 45.37-45.53). dan09 (NEAR) runs on to frame 1360; Dan is back on camera at NEAR for "to do instead." (1424-1446),
then FAR at the 48.248 splice as before. No pause splice falls inside either changed hold.
Reads round4/backup/beats.json (round 3), writes round4/beats_r4base.json (r4_track.py reads it)."""
import json, sys
import numpy as np
B = json.load(open("round4/backup/beats.json")); FPS = 30000/1001
SAM = json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"]
C0, C1 = 1360, 1424
tl = B["timeline"]; P = B["punch"]
i9 = next(i for i, it in enumerate(tl) if it["name"] == "dan09"); ih = i9 + 1; i10 = ih + 1
assert tl[ih]["name"] == "home" and tl[i10]["name"] == "dan10" and tl[ih]["f0"] == 1354 and tl[ih]["f1"] == 1446
tl[i9]["f1"] = C0; tl[i9]["n"] = C0 - tl[i9]["f0"]
P[9]["beat"][1] = round(C0/FPS, 6); P[9]["frames"] = tl[i9]["n"]
tl[ih]["f0"], tl[ih]["f1"], tl[ih]["n"] = C0, C1, C1 - C0; tl[ih]["a"] = round(C0/FPS, 6)
card = next(c for c in B["cards"] if c["name"] == "home")
card.update(beat=[round(C0/FPS, 6), round(C1/FPS, 6)], frames=C1 - C0, asset="B0464", src_in=7.30)
# rename dan10.. -> dan11.. and insert the new NEAR hold as dan10
for it in tl:
    if it["kind"] == "dan" and int(it["name"][3:]) >= 10: it["name"] = f"dan{int(it['name'][3:]) + 1:02d}"
a, b = C1/FPS, 1446/FPS
s = [x for x in SAM if a - 0.05 <= x["t"] <= b + 0.05]
assert s, "no head samples in the new hold"
new = dict(beat=[round(a, 6), round(b, 6)], level="NEAR", hair_min=float(min(x["hair"] for x in s)),
           cx=round(float(np.median([x["cx"] for x in s])), 1), samples=len(s), cx16=1088.0, frames=1446 - C1, r4_new="home card shortened")
tl.insert(i10, dict(kind="dan", name="dan10", a=round(a, 6), f0=C1, f1=1446, n=1446 - C1))
P.insert(10, new)
assert P[11]["level"] == "FAR" and P[9]["level"] == "NEAR"
for i, it in enumerate(tl):
    assert abs(it["a"] - it["f0"]/FPS) < 0.02, it
    assert it["n"] > 0 and (i == 0 or it["f0"] == tl[i-1]["f1"]), it
assert [it["name"] for it in tl if it["kind"] == "dan"] == [f"dan{i:02d}" for i in range(len(P))]
for i, p in enumerate(P): assert p["frames"] == next(it["n"] for it in tl if it["name"] == f"dan{i:02d}"), i
json.dump(B, open("round4/beats_r4base.json", "w"), indent=2)
print("dan09", P[9]["beat"], "home", card["beat"], "dan10 new", new)
