"""Per-shot crop lift from hair_pre.json (RO-17 method, written out here): for every shot and framing, the crop top may sit
at most at (lowest measured hair top in the shot) - 4 % of the crop height, so his hair keeps 4 % headroom on every sampled
frame. Lifted only, never lowered; written only where the locked y would leave less. -> framing/crop_y.json"""
import json, math
W = "/Volumes/Extreme/_edit_work/RO-14/round1"
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W4": (2800, 1575, 520, 183), "W4S": (2690, 1513, 110, 183)}
H = json.load(open(f"{W}/framing/hair_pre.json"))["rows"]
tops = {}
for r in H:
    if r["top"] is not None: tops.setdefault(r["shot"], []).append(r["top"])
out = {}
for sid, v in tops.items():
    t = min(v)
    for fm, (cw, ch, x, y) in CROP.items():
        need = math.floor(t - 0.04 * ch)
        if need < y: out.setdefault(sid, {})[fm] = max(0, need)
json.dump(out, open(f"{W}/framing/crop_y.json", "w"), indent=1)
print(len(out), "shots lifted"); print({k: v for k, v in list(out.items())[:12]})
lift = [(CROP["T2"][3] - v["T2"], k) for k, v in out.items() if "T2" in v]
print("largest T2 lifts", sorted(lift, reverse=True)[:6])
