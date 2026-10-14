"""words_out.json straight from the roll's medium.en words (no second ASR pass): every word whose midpoint lies inside a kept
source range is mapped src -> output through shots.json. Then a 4-word repeat scan inside +/- 30 s of the kept text."""
import json
W = "/Volumes/Extreme/_edit_work/RO-17/round2"; FPS = 30000/1001
WJ = json.load(open(f"{W}/words.json"))["words"]; S = json.load(open(f"{W}/shots.json"))
def to_out(s):
    for sh in S:
        a = sh["src_f0"]/FPS; b = sh["src_f1"]/FPS
        if a - 1e-6 <= s <= b + 1e-6: return sh["out_f0"]/FPS + (min(max(s, a), b) - a)
    return None
out = []
for w in WJ:
    # kept when at least 0.08 s (or 60 %) of the word lies inside one shot (a join's first word often starts a hair before the cut)
    sh = None
    for x in S:
        a, b = x["src_f0"]/FPS, x["src_f1"]/FPS; ov = min(b, w["end"]) - max(a, w["start"])
        if ov > 0 and (ov >= 0.08 or ov >= 0.6 * (w["end"] - w["start"])): sh = x; break
        if w["end"] - w["start"] < 0.02 and a <= w["start"] < b: sh = x; break      # a zero-length word (Whisper glitch) inside a shot
    if sh is None: continue
    a, b = sh["src_f0"]/FPS, sh["src_f1"]/FPS
    o0 = sh["out_f0"]/FPS + (max(w["start"], a) - a); o1 = sh["out_f0"]/FPS + (min(w["end"], b) - a)
    out.append(dict(w=w["word"].strip(), src0=w["start"], src1=w["end"], t0=round(o0, 3), t1=round(o1, 3)))
json.dump(out, open(f"{W}/words_out.json", "w"), indent=0)
txt = " ".join(x["w"] for x in out); print(len(out), "words mapped")
import re
toks = [re.sub(r"[^a-z0-9]", "", x["w"].lower()) for x in out]
seen = {}
for i in range(len(toks) - 3):
    k = " ".join(toks[i:i+4])
    if k in seen and out[i]["t0"] - out[seen[k]]["t0"] < 30: print(f"repeat {out[seen[k]]['t0']:.1f} / {out[i]['t0']:.1f}: {k}")
    seen[k] = i
