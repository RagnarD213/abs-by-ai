"""Round 4 backgrounds (Dan: no pictures around him in the first minute). The cards at 0:08-0:20 and 0:56-1:08 become sharp gym footage with him on the right,
machine and cable clips no other part of the film uses; the wall at 0:20 keeps its place behind them. crop = (x0, y0, width) as fractions of the master."""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2, prep_bg as PB
W4 = r2.W4; OUT = f"{W4}/bgclips4"
CL = {"BG02": ("B0584", 6.5, 13.5, (0.34, 0.02, 0.66), "captain's chair leg raises, a favorite, not used elsewhere, nobody else in frame: sharp beside him until the wall (Dan: footage, no pictures)"),
      "BG07": ("B0660", 1.0, 14.0, (0.20, 0.05, 0.72), "cables at the high pulley, a favorite, not used elsewhere: replaces the picture cards (Dan: keep them out of the first minute)")}
P = json.load(open(f"{W4}/bg_plan4_base.json")); S = P["segments"]
for g, (cid, ss, d, (x0, y0, c), why) in CL.items():
    out = f"{OUT}/{cid}.mp4"; p = PB.path(cid); vf = PB.tune(cid, ss, 6.0)
    if not os.path.exists(out) or "--force" in sys.argv:
        subprocess.run([r2.FF, "-nostdin", "-v", "error", "-y", "-ss", str(ss), "-i", p, "-t", str(d), "-an", "-vf",
                        f"crop=iw*{c}:ih*{c}:iw*{x0}:ih*{y0},{r2.F.DEC},{vf + ',' if vf else ''}scale=1920:1080:flags=lanczos,format=yuv420p",
                        "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", "30000/1001", out], check=True)
    s = next(x for x in S if x["id"] == g)
    for k in ("photos", "slots"): s.pop(k, None)
    s.update(type="side", why="round 4: " + why, clip=dict(id=cid, src=out, windows=[[0.0, d]], zoom=1.0, focus=[0.5, 0.45]))
    print(g, s["t0"], s["t1"], cid, flush=True)
b, c = next(x for x in S if x["id"] == "BG02"), next(x for x in S if x["id"] == "BG02b")
b["t1"] = c["t1"]; S.remove(c); print("BG02", b["t0"], b["t1"])
P["round"] = 4; json.dump(P, open(f"{W4}/bg_plan4.json", "w"), indent=1)
