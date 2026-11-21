#!/usr/bin/env python3
"""RA-04 round 5 plan: round5/beats_r4final.json (round 4's delivered plan, after r4_home -> r4_split -> r4_track) -> beats.json.

Applied AFTER r4_track.py, so its per-hold overrides (keyed by hold index) are already baked into every hold's track and level;
nothing here re-runs the tracker, and every hold except the last keeps its exact round 4 crop and track.

  1. Dan's holds dan01 (3.20-3.87, "Number one,") and dan02 (3.87-6.84, "use AI to generate a picture of yourself with abs.")
     become the card `gen`: the white man's real app generation (round5/gen_white_man_rec.mp4), frames 96-205 (109 frames).
     The holds are re-indexed (s10_render04r4.py maps timeline name danNN to punch[NN]).
  2. The lock card keeps its slot (205-298); its picture becomes the white man's AI result (round5/r5_lock.py).
  3. The film ends at frame END_F (1736 frames, 57.92 s): about 1 s earlier (Dan). His last word "app." ends 57.51 s, the mix is
     at -47 dB from 57.6 s, and he holds a still smile from 57.66 to 58.17 s (frame strip, work dir round5/end_strip.jpg); the last frame
     (1735) is inside that held smile. The CTA hold's track is truncated, not recomputed.
"""
import json
FD = 1001 / 30000
END_F = 1736
B = json.load(open("round5/beats_r4final.json"))
assert B["total_frames"] == 1765 and [t["name"] for t in B["timeline"][1:3]] == ["dan01", "dan02"]
gen_a, gen_b = B["timeline"][1]["a"], B["timeline"][3]["a"]          # 3.2032, 6.840167 (the lock card's start)
assert abs(gen_a - 3.2032) < 1e-3 and abs(gen_b - 6.840167) < 1e-3

# 1. timeline + punch
tl, punch, k = [], [], 0
for it in B["timeline"]:
    if it["name"] in ("dan01", "dan02"):
        if it["name"] == "dan01":
            tl.append(dict(kind="card", name="gen", a=gen_a, f0=96, f1=205, n=109))
        continue
    it = dict(it)
    if it["kind"] == "dan":
        p = B["punch"][int(it["name"][3:])]
        assert abs(p["beat"][0] - it["a"]) < 1e-6
        it["r4_name"] = it["name"]; it["name"] = f"dan{k:02d}"; k += 1; punch.append(p)
    tl.append(it)
cards = []
for c in B["cards"]:
    if c["name"] == "lock":
        cards.append(dict(name="gen", kind="phone", beat=[gen_a, gen_b], asset="gen_white_man_rec", chip="ai", frames=109,
                          r5="the white man's real absbyai.com generation (AI before photo, real AI result); loader 3.30-5.70 s, result 47.10 s on"))
        c = dict(c, asset="A0074+after_white_man", r5="A0074's hand and phone; the screen picture replaced by the white man's AI result")
    cards.append(c)

# 3. the end
total = round(END_F * FD, 6)
last = tl[-1]; assert last["kind"] == "dan" and last["f0"] < END_F
last["f1"] = END_F; last["n"] = END_F - last["f0"]
p = punch[-1]; p["beat"] = [p["beat"][0], total]; p["frames"] = last["n"]
if "track" in p: p["track"] = p["track"][:last["n"]]
B.update(timeline=tl, punch=punch, cards=cards, total=total, total_frames=END_F, cta=[[B["cta"][0][0], total]],
         end_hold=round(total - 57.51, 3), r5_note="round 5: gen card replaces dan01+dan02; end 1 s earlier (frame 1736)")
for i, it in enumerate(tl):
    assert it["n"] > 0 and (i == 0 or it["f0"] == tl[i - 1]["f1"]), it
assert tl[-1]["f1"] == END_F and len([t for t in tl if t["kind"] == "dan"]) == len(punch) == 14
json.dump(B, open("beats.json", "w"), indent=1)

# the CTA overlays end with the film (the movs are longer; the compositor reads only the window's frames)
for m in ("hf9/manifest.json", "hf16/manifest.json"):
    M = json.load(open(m))
    for x in M:
        if x["template"] == "cta": x["b"] = total
    json.dump(M, open(m, "w"), indent=1)
print("R5_PLAN", total, END_F, [t["name"] for t in tl])
