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
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/round2")
import ra01lib as L
from ra01lib import Aspect

KEY = sys.argv[1]; A = Aspect(KEY)
CUT = json.load(open("cut.json")); B = json.load(open("beats.json"))
GRADE = L.grade()                                    # grade.json: one baked look
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
SP = CUT.get("speed") or 1.0          # RA-05 round 2: film time -> source time is * SP inside the talk
def src_spans(a, b):
    """[(src_frame_in, src_frame_out)] covering film times [a,b) of the talk."""
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        s0 = p["src_in"] + (lo - p["t_in"])*SP; s1 = p["src_in"] + (hi - p["t_in"])*SP
        out.append((fr(s0), fr(s1)))
    return out

dan = [it for it in items if it["kind"] == "dan"]
# RA-05 (RA-14 round 2 lesson 4): no decode from frame 0. An input seek to half a frame before frame N0 lands on exactly N0.
N0 = max(0, min(a for it in dan for a, _ in src_spans(it["a"], min(it["b"], CUT["dur"]))) - 60)
chains, outs = [], []
nb = sum(len(src_spans(it["a"], min(it["b"], CUT["dur"]))) + (1 if it["b"] > CUT["dur"] + 1e-6 else 0) for it in dan)
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
    spans = src_spans(it["a"], min(it["b"], CUT["dur"]))
    # RA-05 round 2: the talk spans play at SP (setpts), then the END HOLD (film time past the talk) plays at normal speed
    # from where the last piece leaves off. fps resamples the sped talk onto the 29.97 grid; tpad + -frames pin the count.
    hold_n = max(0, it["n"] - int(round(min(it["b"], CUT["dur"])*FPS - it["a"]*FPS))) if it["b"] > CUT["dur"] + 1e-6 else 0
    for a_, b_ in spans:
        chains.append(f"[b{bi}]trim=start_frame={a_-N0}:end_frame={b_-N0},setpts=(PTS-STARTPTS)/{SP},"
                      f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{GRADE},"
                      f"scale={A.VW}:{A.VH}:flags=lanczos,setsar=1,format=yuv420p[p{bi}]")
        labs.append(f"[p{bi}]"); bi += 1
    if hold_n:
        h0 = spans[-1][1]
        chains.append(f"[b{bi}]trim=start_frame={h0-N0}:end_frame={h0-N0+hold_n+2},setpts=PTS-STARTPTS,"
                      f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{GRADE},"
                      f"scale={A.VW}:{A.VH}:flags=lanczos,setsar=1,format=yuv420p[p{bi}]")
        labs.append(f"[p{bi}]"); bi += 1
        it["hold_frames"] = hold_n
    chains.append("".join(labs) + f"concat=n={len(labs)}:v=1:a=0,fps=30000/1001,tpad=stop_mode=clone:stop_duration=0.1[{it['name']}]")
    outs.append(it)

cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{(N0-0.5)/FPS:.5f}", "-i", L.ROLL,
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
# RA-04: the Soft Blue overlays (lower thirds, CTA button: glass that blurs the footage under it) are composited in RGB
# by the shared HyperFrames compositor, then the caption MOV goes on top.
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as CP
base = f"{SEG}/base.mp4"
subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-frames:v", str(TOTALF),
                "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", base], check=True)
C = CP.Compositor(json.load(open("hf9/manifest.json")), wh=(A.VW, A.VH))
e = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{A.VW}x{A.VH}",
                      "-framerate", "30000/1001", "-i", "-", "-i", f"cap_{KEY}/captions.mov",
                      "-filter_complex", "[0:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
                      "-map", "[v]", "-frames:v", str(TOTALF), "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                      "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                      "-color_range", "tv", "-movflags", "+faststart", picture], stdin=subprocess.PIPE)
for g, f in enumerate(CP.reader(base, 0, TOTALF, False, (A.VW, A.VH))):
    e.stdin.write(np.ascontiguousarray(C.apply(f, g)).tobytes())
e.stdin.close(); assert e.wait() == 0
print("picture ->", picture)
json.dump({"items": [{k: v for k, v in it.items() if k != "punch"} for it in items],
           "punch": [{"beat": it["a"], "end": it["b"], "level": it["punch"]["level"],
                      "crop": it["crop"]} for it in dan],
           "total_frames": TOTALF, "grade": GRADE, "seek_frame": N0,
           "levels": {k: list(v) for k, v in A.levels.items()}},
          open(f"timeline_{KEY}.json", "w"), indent=1)
