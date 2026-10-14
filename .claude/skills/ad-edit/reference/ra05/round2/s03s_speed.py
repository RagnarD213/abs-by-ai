#!/usr/bin/env python3
"""RA-05 round 2: THE SPEED-UP, one factor everywhere (Dan, 2026-10-14: "don't cut any of the lines, but just accelerate the
video as necessary to get it under 60 seconds").

s03_edl.py writes the cut at normal speed (tight time). This step keeps that file as cut_tight.json and rewrites cut.json in
FILM time: every tight time / SPEED. Source times (src_in / src_out, ranges) are untouched, so a film span [lo, hi) of a piece
plays source [src_in + (lo - t_in)*SPEED, ...). Readers that map film time to source multiply by cut["speed"].
The end hold (ra01lib.END_HOLD) is appended at normal speed by the audio and picture builders, never sped.
"""
import json, os, shutil, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/round2")
import ra01lib as L
SP = L.SPEED
if not os.path.exists("cut_tight.json") or json.load(open("cut.json")).get("speed") is None:
    shutil.copy("cut.json", "cut_tight.json")
T = json.load(open("cut_tight.json")); assert T.get("speed") is None
f = lambda t: round(t / SP, 6)
C = dict(T)
C["speed"] = SP; C["dur_tight"] = T["dur"]; C["dur"] = f(T["dur"]); C["span_end"] = f(T["span_end"])
C["keeps"] = [[f(a), f(b)] for a, b in T["keeps"]]
C["pieces"] = [dict(p, t_in=f(p["t_in"]), t_out=f(p["t_out"])) for p in T["pieces"]]
C["cuts"] = [dict(c, film_in=f(c["in"]), film_out=f(c["out"])) for c in T["cuts"]]
C["seams"] = [dict(s, t=f(s["t"])) for s in T["seams"]]
C["words"] = [dict(w, t=f(w["t"]), e=f(w["e"])) for w in T["words"]]
for p in C["pieces"]:
    assert abs((p["t_out"] - p["t_in"]) * SP - (p["src_out"] - p["src_in"])) < 2e-3, p
json.dump(C, open("cut.json", "w"), indent=1)
tot = C["dur"] + L.END_HOLD
print(f"speed {SP}x: talk {T['dur']:.3f}s -> {C['dur']:.3f}s, + {L.END_HOLD}s end hold = {tot:.3f}s "
      f"(ceiling 59.00, margin {59.0 - tot:.2f}s); seams {[s['t'] for s in C['seams']]}")
assert tot <= 59.0
