#!/usr/bin/env python3
"""RA-06 insert cards (fired, pose, flow_a, flow_b, tour, tour2; the split opener is s06_split.py). From RA-04:
RA-04 insert cards at 9:16 -> cards_9x16/<name>.mp4, each exactly its timeline frame count.

  lock      A0074 fills the frame (AI goal picture on a phone lock screen) + the Soft Blue AI-GENERATED chip
  flow_a/b  B0049 (the app's own generate flow, same man before and after) under a HyperFrames media-card plate
  analysis  the approved adkit analysis card, recoloured to Soft Blue Light (ANALYSIS=olive keeps RA-01's colours)
  tour      B0544 (the approved app tour) under a media-card plate: workout sheet first, then the meal analysis
  knee      B0126 fills the frame;  home  B0464 (Dan's real squats on the lawn), a steady 608 px window on him
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes"); sys.path.insert(0, SH + "/adkit")
import softblue as SB
import composite as CP
FF = SB.FF; FPSS = "30000/1001"; W, H = 1080, 1920
B = json.load(open("beats.json")); P = json.load(open("clip_paths.json"))
PL = json.load(open("hf9/plates.json")) if os.path.exists("hf9/plates.json") else {}
by = {c["name"]: c for c in B["cards"]}
os.makedirs("cards_9x16", exist_ok=True); os.makedirs("media", exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"

def media(name, segs, vf, wh, n):
    """segs = [(path, t0, dur)] -> media/<name>.mp4, wh, exactly n frames at 29.97."""
    out = f"media/{name}.mp4"; ins, ch = [], []
    for i, (p, t0, d) in enumerate(segs):
        ins += ["-ss", f"{t0:.3f}", "-t", f"{d + 0.2:.3f}", "-i", p]
        ch.append(f"[{i}:v]fps={FPSS},{vf},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1,trim=end_frame={round(d * 30000 / 1001)},setpts=PTS-STARTPTS[v{i}]")
    ch.append("".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=1[v]")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n)] + ENC + [out], check=True)
    return out

def frames(path, wh, n):
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", path, "-vf", f"{D709},format=rgb24", "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = wh[0] * wh[1] * 3
    for _ in range(n):
        b = p.stdout.read(size); assert len(b) == size, (path, _)
        yield np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3)
    p.stdout.close(); p.wait()

def writer(out):
    return subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", FPSS, "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + ENC + [out], stdin=subprocess.PIPE)

def plate_card(name, segs, vf):
    pl = PL[name]; n = by[name]["frames"]; x0, y0, x1, y1 = pl["hole"]; wh = (x1 - x0, y1 - y0)
    m = media(name, segs, vf, wh, n); e = writer(f"cards_9x16/{name}.mp4")
    for f, ov in zip(frames(m, wh, n), CP.reader(pl["mov"], 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes())
    e.stdin.close(); e.wait(); print(name, n, "frames, hole", pl["hole"], flush=True)

def fill_card(name, segs, vf, chip=None):
    n = by[name]["frames"]; m = media(name, segs, vf, (W, H), n); e = writer(f"cards_9x16/{name}.mp4"); box = None
    for f in frames(m, (W, H), n):
        if chip:
            im = Image.fromarray(f); box = SB.disclosure(im, chip[0], chip[1]); f = np.asarray(im)
        e.stdin.write(np.ascontiguousarray(f).tobytes())
    e.stdin.close(); e.wait(); print(name, n, "frames", "chip box", box, flush=True)
    return box

only = set(sys.argv[1:]); want = lambda k: not only or k in only
dur = lambda k: by[k]["frames"] * 1001 / 30000
meta = json.load(open("cards_9x16/meta.json")) if os.path.exists("cards_9x16/meta.json") else {}
R3M = "/Volumes/Extreme/_edit_work/ra06/round3/motion"
# ROUND 3: the AI clips Dan approved on frames (I1, I3, I4; I5 out). Each shot plays at 1.0x (24 fps takes conformed to
# 29.97 by frame repeat, never slowed); a shot is (take, in s, out s, crop w:h:x:y in the 720x1280 take or None).
AI_SHOTS = {
 "I3": [("I3_v1", 0.0, 5.0, None)],
 # four takes could not draw three hand-offs (sheets appeared in two men's hands): two shots and a cut instead
 "I1": [("I1_v1", 0.0, 2.05, None), ("I1_v2", 3.10, 4.55, "576:1024:0:150")],
 # v2: he pushes the bar, the door swings open and he steps into the doorway glancing back while the robot waves;
 # after ~2.5 s the door drifts shut and he pushes it again, so the shot ends at 2.35 s
 "I4": [("I4_v2", 0.25, 2.35, None)],
}
AI_CHIP = {"I3": (60, 1236), "I1": (470, 1236), "I4": (60, 1532)}   # ROUND 4: I4 1492 -> 1532, the gate measured the chip 13 px INTO the caption ink at 41.5 s (needs 20 clear)   # placed by looking at each clip's people: floor, desk; I4 under the captions (the towel wave fills the wall above)


def ai_card(name):
    n = by[name]["frames"]; ins, ch = [], []
    for i, (take, a, b, crop) in enumerate(AI_SHOTS[name]):
        ins += ["-i", f"{R3M}/{take}.mp4"]
        cr = f"crop={crop}," if crop else ""
        ch.append(f"[{i}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps={FPSS},{cr}scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5,setsar=1[v{i}]")
    k = len(AI_SHOTS[name])
    ch.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.1[v]")
    want_s = sum(b - a for _, a, b, _c in AI_SHOTS[name]); assert abs(want_s - n * 1001 / 30000) < 0.05, (name, want_s, n)
    out = f"media/{name}.mp4"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n)] + ENC + [out], check=True)
    e = writer(f"cards_9x16/{name}.mp4"); box = None
    for f in frames(out, (W, H), n):
        im = Image.fromarray(f); box = SB.disclosure(im, "AI-GENERATED", AI_CHIP[name]); e.stdin.write(np.asarray(im).tobytes())
    e.stdin.close(); e.wait(); print(name, n, "frames, chip", box, flush=True)
    return box


for _ai in ("I3", "I1", "I4"):
    if want(_ai) and _ai in by:
        meta[_ai] = {"chip": "AI-GENERATED", "chip_box": ai_card(_ai), "shots": AI_SHOTS[_ai]}
if want("fired"):      # A0147 (clip library, used in Ad 13): the fired trainer carries his box out while a robot spots the lifter.
    # 720x1280 original, lanczos to 1080x1920 with a light unsharp (no local upscaler on this Mac). Faces are in the top
    # third, so the AI chip sits on the empty floor below their feet (RA-07 lesson 7: never a fixed corner on this clip).
    meta["fired"] = {"chip": "AI-GENERATED", "chip_box": fill_card("fired", [(P["A0147"], 0.0, dur("fired"))], "unsharp=5:5:0.5", chip=("AI-GENERATED", (60, 1236)))}
if want("pose") and "pose" in by:       # Dan's real physique poses from the same pool shoot (library B0435, native 9:16), RA-05's crop and colour match
    fill_card("pose", [(P["B0435"], float(os.environ.get("POSE_T", "4.3")), dur("pose"))], os.environ.get("POSE_VF", "crop=630:1120:332:300,eq=gamma=1.04:saturation=1.26,colorbalance=rm=0.03:bm=-0.02"))
if want("flow_a"):     # the same man's own photo on the Generating screen (B0049 13.0 s: scan line over his upload)
    plate_card("flow_a", [(P["B0049"], 13.0, dur("flow_a"))], "crop=1320:1600:0:170")
if want("flow_b"):
    # B0049's banned "Meet the new you" BEFORE/AFTER screen runs to about 27.6 s; the result screen alone starts at 28.0 s
    FLOW_B_T0 = 28.0
    assert FLOW_B_T0 >= 27.9 and dur("flow_b") <= 5.5, dur("flow_b")
    plate_card("flow_b", [(P["B0049"], FLOW_B_T0, dur("flow_b"))], "crop=1320:1600:0:170")
if want("tour"):       # the real AI Trainer: Monday's workout list (B0034 0-3.7 s, before the exercise sheet opens)
    plate_card("tour", [(P["B0034"], 0.0, dur("tour"))], "null")
if want("tour2"):      # the meal photo analysed to 775 cal (B0544 from 1.0 s: home, tap Macro Tracker, photo, analysing, result)
    d = dur("tour2"); a = min(1.75, d * 0.42)
    plate_card("tour2", [(P["B0544"], 6.05, a), (P["B0544"], 5.2 - (d - a), d - a)], "null")
if want("analysis") and "analysis" in by:
    import analysis_card as AC, cardlib as L
    if os.environ.get("ANALYSIS") != "olive":
        AC.LIME = SB.SPECULAR; AC.OLIVE = SB.CYAN; AC.PLAN_GREEN = (22, 70, 124); L.OLIVE = SB.GLASS_LINE
        L.field = lambda A: SB.field(0.0, *A.size).convert("RGBA")
    if not os.path.exists("media/after_man.png"):
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", "29.6", "-i", P["B0049"], "-frames:v", "1", "-vf", "crop=856:1090:230:634", "media/after_man.png"], check=True)
    tag = "analysis" + ("_olive" if os.environ.get("ANALYSIS") == "olive" else "")
    m = AC.build("media/after_man.png", "9x16", dur("analysis"), f"cards_9x16/{tag}", label="ai")
    assert m["frames"] == by["analysis"]["frames"], (m["frames"], by["analysis"]["frames"])
    meta[tag] = {k: m[k] for k in ("chip_pos", "chip_why", "photo_box", "card_rect")}; print(tag, meta[tag], flush=True)
json.dump(meta, open("cards_9x16/meta.json", "w"), indent=1)
print("INSERTS_COMPLETE")
