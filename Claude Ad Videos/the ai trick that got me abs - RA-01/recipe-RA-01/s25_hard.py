#!/usr/bin/env python3
"""Which pause-removal splices are VISIBLY discontinuous on the DELIVERED picture.

ad-edit lessons 64/68/80: measure the frame difference across every splice against the file's own
p99 control; a splice above it is a naked jump cut unless a card covers it or a punch boundary
lands on it. Compute the forced set WITHOUT reference to the punch plan (lesson 68: testing against
the previous iteration's plan makes the result oscillate), thin HARDEST-FIRST inside a spacing
floor (lesson 80), and never inside the hook.
"""
import json, re, subprocess, sys
import statistics
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L

MASTER = sys.argv[1] if len(sys.argv) > 1 else "master_9x16.mp4"
FLOOR = float(sys.argv[2]) if len(sys.argv) > 2 else 1.40
HOOK_SAFE = 2.0
tmp = "/tmp/_ra01_hs.txt"
subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", MASTER, "-vf",
                "scale=320:180,tblend=all_mode=difference,signalstats,"
                f"metadata=print:key=lavfi.signalstats.YAVG:file={tmp}", "-an", "-f", "null", "-"],
               check=True)
vals = []
for blk in open(tmp).read().split("frame:")[1:]:
    t = re.search(r"pts_time:([\d.]+)", blk); v = re.search(r"YAVG=([\d.]+)", blk)
    if t and v: vals.append((float(t.group(1)), float(v.group(1))))
CUT = json.load(open("cut.json")); B = json.load(open("beats.json"))
acc, sp = 0.0, []
for a, b in CUT["keeps"][:-1]:
    acc += b - a; sp.append(round(acc, 3))
cards = [tuple(c["beat"]) for c in B["cards"]]
covered = lambda t: any(a - 0.15 <= t <= b + 0.15 for a, b in cards)
# ⚠ THE CONTROL IS DAN'S OWN CAMERA MOVEMENT, NOT THE WHOLE FILE. Nine hard cuts between totally
# different pictures drag a whole-file p99 to 12.5, which then declares almost every jump cut
# "normal". The control is the frame difference inside the talking-head segments only, away from
# every card edge and every splice.
dan = [tuple(p["beat"]) for p in B["punch"]]
ctrl = [v for t, v in vals
        if any(a + 0.35 <= t <= b - 0.35 for a, b in dan)
        and all(abs(t - s) > 0.25 for s in sp)]
ys = sorted(ctrl); p99 = ys[int(len(ys)*0.99)]
hard = []
for s in sp:
    if covered(s) or s <= HOOK_SAFE: continue
    d = max([v for t, v in vals if abs(t - s) < 0.06] or [0])
    if d > p99: hard.append((s, round(d, 2)))
hard.sort(key=lambda x: -x[1])
forced, taken = [], []
for s, d in hard:
    if any(abs(s - t) < FLOOR for t in taken): continue
    taken.append(s); forced.append([s, d])
forced.sort()
print(f"control median {statistics.median(ys):.2f}  p99 {p99:.2f}")
print(f"{len(sp)} splices, {len([s for s in sp if not covered(s) and s > HOOK_SAFE])} outside cards "
      f"and the hook, {len(hard)} above the ceiling, {len(forced)} forced after a {FLOOR}s floor")
for s, d in forced: print(f"   {s:7.3f}  diff {d}")
# The times belong to THIS cut, so they are stamped with the cut's own join signature; s05_plan.py
# refuses to reuse them against a different cut (evidence never crosses renders).
import hashlib
sig = hashlib.sha256(json.dumps(sp).encode()).hexdigest()[:16]
W_ = json.load(open("words_aligned.json"))["words"]
pairs = []
for s_, _ in forced:
    prev = max((w for w in W_ if w["e"] <= s_ + 0.12), key=lambda w: w["e"], default=None)
    nxt = min((w for w in W_ if w["t"] >= s_ - 0.12), key=lambda w: w["t"], default=None)
    pairs.append([prev["w"].strip() if prev else "?", nxt["w"].strip() if nxt else "?"])
json.dump({"p99": p99, "forced": [s for s, _ in forced], "hard": hard, "floor": FLOOR,
           "measured_on": MASTER, "cut_sig": sig, "pairs": pairs,
           "by": "s25_hard.py on the delivered picture"},
          open("hard_splices.json", "w"), indent=1)
print("cut_sig", sig)
