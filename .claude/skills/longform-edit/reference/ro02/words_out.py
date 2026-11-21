"""medium.en words on the assembled audio -> source seconds (piece_map) -> output seconds (shots.json). Writes words_out.json."""
import json
W = "/Volumes/Extreme/_edit_work/ro02"; FPS = 30000/1001
r = json.load(open(f"{W}/asr_assembled_medium.json")); M = json.load(open(f"{W}/piece_map.json")); S = json.load(open(f"{W}/shots.json"))
def to_src(t):
    m = next((m for m in M if m["t0"]-1e-6 <= t < m["t1"]+1e-6), M[-1]); return m["id"], m["roll"], m["src_f0"]/FPS+(t-m["t0"])
def to_out(pid, s):
    for sh in S:
        if sh["piece"] != pid: continue
        a = sh["src_f0"]/FPS; b = sh["src_f1"]/FPS
        if a-0.02 <= s <= b+0.02: return sh["out_f0"]/FPS+(min(max(s, a), b)-a)
    return None
out = []
for seg in r["segments"]:
    for w in seg["words"]:
        pid, roll, s0 = to_src(w["start"]); _, _, s1 = to_src(max(w["start"], w["end"]-0.001))
        o0 = to_out(pid, s0); o1 = to_out(pid, s1)
        out.append(dict(w=w["word"].strip(), piece=pid, roll=roll, src0=round(s0, 3), src1=round(s1, 3), t0=None if o0 is None else round(o0, 3), t1=None if o1 is None else round(o1, 3)))
json.dump(out, open(f"{W}/words_out.json", "w"), indent=0)
print(len(out), "words;", sum(1 for x in out if x["t0"] is None), "unmapped (inside a tightened pause)")
