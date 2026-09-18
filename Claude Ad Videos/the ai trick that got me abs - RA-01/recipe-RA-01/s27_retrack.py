#!/usr/bin/env python3
"""Re-key the framing track onto a new cut. The samples were measured on SOURCE frames, so a
re-cut changes only their position on the tight timeline -- re-measuring 222 frames would be
waste, and a stale track would frame the video (website-video lesson 102: a stale track must fail
the build, not silently shift it)."""
import json
CUT = json.load(open("cut.json"))
TRK = json.load(open("framing_src.json")) if __import__("os").path.exists("framing_src.json") \
      else json.load(open("framing.json"))
json.dump(TRK, open("framing_src.json", "w"), indent=1)      # keep the source-keyed original
P = CUT["pieces"]
out, dropped = [], 0
for s in TRK["samples"]:
    hit = next((p for p in P if p["src_in"] - 1e-6 <= s["src"] < p["src_out"] + 1e-6), None)
    if hit is None:
        dropped += 1; continue
    s = dict(s); s["t"] = round(hit["t_in"] + (s["src"] - hit["src_in"]), 3)
    out.append(s)
out.sort(key=lambda x: x["t"])
TRK["samples"] = out; TRK["rekeyed_from_source"] = True; TRK["dropped_outside_the_cut"] = dropped
json.dump(TRK, open("framing.json", "w"), indent=1)
print(f"re-keyed {len(out)} samples onto the new cut ({dropped} now outside it); "
      f"t {out[0]['t']:.2f}..{out[-1]['t']:.2f}")
