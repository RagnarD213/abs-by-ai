"""Round 5 (length trim): words on the new output timeline WITHOUT a new ASR pass. The medium.en words keep their source
times; a word in a shot whose source range did not change keeps its round 4 output time plus that shot's shift (so every
word before the first trim is identical to the approved round); a word in a new or changed shot is mapped from its source
time, kept only when its middle survives the cut (edges clamped to the shot)."""
import json
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001
old = json.load(open(f"{W}/round5/snap4/shots.json")); S = json.load(open(f"{W}/shots.json")); WO = json.load(open(f"{W}/round5/snap4/words_out.json"))
new = {s["id"]: s for s in S}
def old_shot(t): return next((s for s in old if s["out_f0"]/FPS - 0.021 <= t <= s["out_f1"]/FPS + 0.021), None)
def shot_of(x): return next((s for s in S if s["src_f0"]/FPS <= x < s["src_f1"]/FPS), None)
out = []; kept = moved = remap = gone = 0
for w in WO:
    n = dict(w); o = old_shot(w["t0"]) if w["t0"] is not None else None
    s = new.get(o["id"]) if o else None
    if s and (s["src_f0"], s["src_f1"]) == (o["src_f0"], o["src_f1"]):
        d = (s["out_f0"] - o["out_f0"])/FPS
        n["t0"] = round(w["t0"] + d, 3); n["t1"] = None if w["t1"] is None else round(w["t1"] + d, 3)
        kept += d == 0; moved += d != 0
    else:
        sh = shot_of((w["src0"] + w["src1"])/2)
        if sh is None and w["src1"] - w["src0"] > 0.8:          # a stretched word (Whisper folded a pause or a cut into it): keep the end that survives
            e = shot_of(w["src1"] - 0.05) or shot_of(w["src0"] + 0.05)
            if e is not None:
                late = shot_of(w["src1"] - 0.05) is e; x1 = w["src1"] if late else min(e["src_f1"]/FPS, w["src0"] + 0.4); x0 = max(e["src_f0"]/FPS, x1 - 0.42) if late else w["src0"]
                n["t0"] = round(e["out_f0"]/FPS + x0 - e["src_f0"]/FPS, 3); n["t1"] = round(e["out_f0"]/FPS + x1 - e["src_f0"]/FPS, 3); remap += 1; out.append(n); continue
        if sh is None: n["t0"] = n["t1"] = None; gone += w["t0"] is not None
        else:
            a, b = sh["src_f0"]/FPS, sh["src_f1"]/FPS
            n["t0"] = round(sh["out_f0"]/FPS + min(max(w["src0"], a), b) - a, 3); n["t1"] = round(sh["out_f0"]/FPS + min(max(w["src1"], a), b) - a, 3); remap += 1
    out.append(n)
json.dump(out, open(f"{W}/words_out.json", "w"), indent=0)
print(len(out), "words; unchanged", kept, "shifted", moved, "remapped in changed shots", remap, "cut", gone, "unmapped", sum(1 for x in out if x["t0"] is None))
