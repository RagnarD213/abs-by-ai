#!/usr/bin/env python3
"""Render one aspect's picture and mux the master.  s10_render.py 9x16|16x9

Two ffmpeg jobs:
  1. ONE decode of the roll -> one file per Dan segment. Every trim is FRAME-INDEXED
     (trim=start_frame/end_frame on the un-seeked roll), so the timeline cannot drift by a frame.
     Per branch: crop (the hair-anchored level) -> BT.709 decode -> the approved 8/28 LUT ->
     saturation -> lanczos to the delivered size. The LUT runs on the CROP, which is the same
     pixels it would run on at full frame, at a fraction of the cost.
  2. The concat of [Dan segment | card | Dan segment | ...] with the caption and CTA alpha MOVs
     overlaid -- three inputs, so the deep-overlay livelock (ad-edit lesson 117) cannot bite.
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect

KEY = sys.argv[1]; A = Aspect(KEY)
CUT = json.load(open("cut.json")); B = json.load(open("beats.json"))
_G = json.load(open("grade.json"))
EXPO, SAT = _G["exposure"], _G["saturation"]        # R5: measured, not assumed (s32_grade.py)
GRADE = L.grade(EXPO, SAT)
FPS = L.FPS
fr = lambda t: int(round(t*FPS))
TOTALF = fr(B["total"])
SEG = f"seg_{KEY}"; os.makedirs(SEG, exist_ok=True)

# ---- frame-exact timeline (computed once, in s05_plan.py, and used by the card builder too) ----
TOTALF = B["total_frames"]
assert TOTALF == fr(B["total"]), (TOTALF, fr(B["total"]))
byname = {c["name"]: c for c in B["cards"]}
punchby = {f"dan{i:02d}": p for i, p in enumerate(B["punch"])}
items = []
for it in B["timeline"]:
    x = dict(it)
    x["b"] = punchby[it["name"]]["beat"][1] if it["kind"] == "dan" else byname[it["name"]]["beat"][1]
    if it["kind"] == "dan": x["punch"] = punchby[it["name"]]
    items.append(x)
for i, it in enumerate(items):
    assert it["n"] > 0 and (i == 0 or it["f0"] == items[i-1]["f1"]), it
assert items[-1]["f1"] == TOTALF

# ---- the tight-time -> source-frame map --------------------------------------------------------
PIECES = CUT["pieces"]
def src_spans(a, b):
    """[(src_frame_in, src_frame_out)] covering tight times [a,b)."""
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        s0 = p["src_in"] + (lo - p["t_in"]); s1 = p["src_in"] + (hi - p["t_in"])
        out.append((fr(s0), fr(s1)))
    return out

dan = [it for it in items if it["kind"] == "dan"]
chains, outs = [], []
nb = sum(len(src_spans(it["a"], it["b"])) for it in dan)
chains.append(f"[0:v]split={nb}" + "".join(f"[b{i}]" for i in range(nb)))
bi = 0
for it in dan:
    pu = it["punch"]; cw, ch = A.levels[pu["level"]]
    y = int(round(pu["hair_min"] - 0.04*ch)); y = max(0, min(3840-ch, y - y % 2))
    # R3 (plan section 13, D5): in 16:9 both levels share the FAR window's centre, so a zoom cut is
    # a pure zoom and he does not step sideways. 9:16 keeps its own per-hold centre.
    cxs = pu["cx16"] if (KEY == "16x9" and "cx16" in pu) else pu["cx"]
    x = int(round(cxs - cw/2));                x = max(0, min(2160-cw, x - x % 2))
    it["crop"] = [cw, ch, x, y]
    labs = []
    spans = src_spans(it["a"], it["b"])
    # pin the frame count: the last span absorbs any rounding so the segment is exactly `n` frames
    tot = sum(b_-a_ for a_, b_ in spans)
    if tot != it["n"]:
        a_, b_ = spans[-1]; spans[-1] = (a_, b_ + (it["n"] - tot))
    for a_, b_ in spans:
        chains.append(f"[b{bi}]trim=start_frame={a_}:end_frame={b_},setpts=PTS-STARTPTS,"
                      f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{GRADE},"
                      f"scale={A.VW}:{A.VH}:flags=lanczos,setsar=1,format=yuv420p[p{bi}]")
        labs.append(f"[p{bi}]"); bi += 1
    if len(labs) > 1:
        chains.append("".join(labs) + f"concat=n={len(labs)}:v=1:a=0[{it['name']}]")
    else:
        chains.append(f"{labs[0]}null[{it['name']}]")
    outs.append(it)

cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-i", L.ROLL,
       "-filter_complex", ";".join(chains)]
for it in outs:
    cmd += ["-map", f"[{it['name']}]", "-frames:v", str(it["n"]),
            "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
            "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-color_range", "tv",
            "-x264-params", "keyint=30:min-keyint=1:scenecut=0", f"{SEG}/{it['name']}.mp4"]
print(f"stage 1: {len(outs)} Dan segments, {nb} source branches, {TOTALF} frames total")
for it in outs:
    print(f"   {it['name']}  {it['a']:6.2f}->{it['b']:6.2f}  {it['n']:4d}f  {it['punch']['level']:<4} "
          f"crop {it['crop']}")
if os.environ.get("SKIP1") != "1":
    subprocess.run(cmd, check=True)

# ---- stage 2: concat + captions + CTA -----------------------------------------------------------
lst = f"{SEG}/timeline.txt"
with open(lst, "w") as f:
    for it in items:
        p = f"{SEG}/{it['name']}.mp4" if it["kind"] == "dan" else f"cards_{KEY}/{it['name']}.mp4"
        f.write(f"file '{os.path.abspath(p)}'\n")
for it in items:
    p = f"{SEG}/{it['name']}.mp4" if it["kind"] == "dan" else f"cards_{KEY}/{it['name']}.mp4"
    n = int(subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-count_frames",
                            "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                            "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
    if n != it["n"]:
        raise SystemExit(f"{it['name']} has {n} frames, the timeline wants {it['n']} -- a card that "
                         f"is the wrong length shifts every later caption through the concat")
picture = f"picture_{KEY}.mp4"
fc = ("[0:v][1:v]overlay=0:0:format=auto[c];"
      "[c][2:v]overlay=0:0:format=auto,format=yuv420p[v]")
subprocess.run([L.FF, "-nostdin", "-y", "-v", "error",
                "-f", "concat", "-safe", "0", "-i", lst,
                "-i", f"cap_{KEY}/captions.mov", "-i", f"cta_{KEY}/cta.mov",
                "-filter_complex", fc, "-map", "[v]", "-frames:v", str(TOTALF),
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709",
                "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart",
                picture], check=True)
print("picture ->", picture)
json.dump({"items": [{k: v for k, v in it.items() if k != "punch"} for it in items],
           "punch": [{"beat": it["a"], "end": it["b"], "level": it["punch"]["level"],
                      "crop": it["crop"]} for it in dan],
           "total_frames": TOTALF, "grade": GRADE, "expo": EXPO, "saturation": SAT,
           "levels": {k: list(v) for k, v in A.levels.items()}},
          open(f"timeline_{KEY}.json", "w"), indent=1)
