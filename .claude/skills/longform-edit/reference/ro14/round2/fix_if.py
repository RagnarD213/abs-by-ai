"""RO-14 round 2 review fix 1 (ROUND-2-REVIEW.md, 7:57.98): round 1 cut the only 'If' (src 743.58-743.64, a quiet 60 ms word) off
"If the trend line is not moving...", taking the 743.72 'the' for a second 'If'. s5e now starts 5 frames earlier (src 743.509), so
the film grows by 5 frames from 477.978 s; later shots and words move with it (items resolve from words)."""
import json
W = "/Volumes/Extreme/_edit_work/RO-14/round2"; FPS = 30000/1001; D = 5
S = json.load(open(f"{W}/shots.json")); k = next(i for i, s in enumerate(S) if s["id"] == "s5e.0")
J = S[k]["out_f0"] / FPS
S[k]["src_f0"] -= D; S[k]["out_f1"] += D
for s in S[k+1:]: s["out_f0"] += D; s["out_f1"] += D
json.dump(S, open(f"{W}/shots.json", "w"), indent=1)
wo = json.load(open(f"{W}/words_out.json"))
for w in wo:
    for key in ("t0", "t1"):
        if w.get(key) is not None and w[key] >= J - 0.001: w[key] = round(w[key] + D / FPS, 3)
# the restored word and the two after it, timed on the lav level strip (src 743.58 If, 743.72 the, 743.88 trend)
s0 = (S[k]["src_f0"]) / FPS
fix = {"If": (743.58, 743.64), "the": (743.72, 743.80), "trend": (743.88, 744.10)}
seen = set()
for w in wo:
    if w.get("t0") is not None and J - 0.01 <= w["t0"] < J + 0.7 and w["w"] in fix and w["w"] not in seen:
        a, b = fix[w["w"]]; w["t0"] = round(J + a - s0, 3); w["t1"] = round(J + b - s0, 3); seen.add(w["w"])
json.dump(wo, open(f"{W}/words_out.json", "w"), indent=1)
print("join", round(J, 3), "s5e src", round(s0, 3), "film frames", S[-1]["out_f1"], "fixed", sorted(seen))
