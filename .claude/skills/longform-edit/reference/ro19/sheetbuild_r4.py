"""RO-19 round 4: the shadow build folder the edit sheet writer reads (README, round 3: the writer reads hf/manifest.json, hf/beats.json and the lower third
configs as they are, so after a timeline shift it must be handed shifted copies). Made from round 3's shadow folder (already on the round 3 timeline) with the
round 4 shift: every time at or after the end of the removed stretch moves 63 frames earlier. The manifest is hf/manifest.r4.json. Everything else is a symlink
to the work folder. usage: sheetbuild_r4.py  -> round4/sheetbuild/"""
import json, os
W = "/Volumes/Extreme/_edit_work/ro19"; FPS = 30000/1001; SRC = f"{W}/round3/sheetbuild"; OUT = f"{W}/round4/sheetbuild"
SH = json.load(open(f"{W}/round4-plan/timeline_shift.json")); AT = SH["at_out_frame"]/FPS; DT = -SH["frames"]/FPS
def mv(t):
    assert not (AT + 0.011 < t < AT + DT - 0.011), ("a time sits inside the removed stretch", t)
    return round(t - DT, 3) if t >= AT + DT - 0.011 else t
os.makedirs(f"{OUT}/hf/configs/lower-third", exist_ok=True)
for n in os.listdir(W):
    if n.startswith("._") or n in ("hf", "round4") or os.path.lexists(f"{OUT}/{n}"): continue
    os.symlink(f"{W}/{n}", f"{OUT}/{n}")
if not os.path.lexists(f"{OUT}/hf/renders"): os.symlink(f"{W}/hf/renders", f"{OUT}/hf/renders")
M = json.load(open(f"{W}/hf/manifest.r4.json")); json.dump(M, open(f"{OUT}/hf/manifest.json", "w"), indent=1); MA = {m["id"]: m for m in M}
B = json.load(open(f"{SRC}/hf/beats.json")); n = 0
for b in B:
    a0 = b["a"]; b["a"], b["b"] = mv(b["a"]), mv(b["b"]); n += b["a"] != a0
    for r in b["rows"]: r["t"] = round(mv(r["t"]), 2)
    if b["id"] in MA: assert abs(b["a"] - MA[b["id"]]["a"]) < 0.002 and abs(b["b"] - MA[b["id"]]["b"]) < 0.002, b["id"]
json.dump(B, open(f"{OUT}/hf/beats.json", "w"), indent=1); k = 0
for f in sorted(os.listdir(f"{SRC}/hf/configs/lower-third")):
    if f.startswith("._"): continue
    C = json.load(open(f"{SRC}/hf/configs/lower-third/{f}"))
    for c in C:
        a0 = c["a"]; c["a"], c["b"] = mv(c["a"]), mv(c["b"]); k += c["a"] != a0; c["parts"] = [[p[0], mv(p[1])] + p[2:] for p in c["parts"]]
        assert abs(c["a"] - MA[c["id"]]["a"]) < 0.002 and abs(c["b"] - MA[c["id"]]["b"]) < 0.002, c["id"]
    json.dump(C, open(f"{OUT}/hf/configs/lower-third/{f}", "w"))
print("sheet build folder:", OUT, "|", len(B), "beats,", n, "moved |", k, "configs moved | manifest", len(M))
