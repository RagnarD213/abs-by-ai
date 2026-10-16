#!/usr/bin/env python3
"""RA-06 round 4: the 16:9 insert cards -> cards_16x9/<name>.mp4, each exactly its timeline frame count (the same plan as the 9:16).
Every insert in this ad is a 9:16 picture, so each one goes WHOLE and full height (852 px) in a media-card plate on the Soft Blue field
(hf16/plates.json), never cropped to 16:9 (ad-edit lesson 61; VIDEO-RULES, a vertical clip in a horizontal frame). The AI-GENERATED chip
is part of the plate, on the field right of the hole, so it never touches a person in the clip.
  I3, I1, I4   the approved Kling takes, the 9:16's exact shots, in- and out-points (s06_inserts06.py AI_SHOTS)
  fired        A0147 from 0.0 s, as the 9:16
  tour, tour2  B0034 / B0544, flow_a, flow_b  B0049: the 9:16's in-points and crops
Same in- and out-points as s06_inserts06.py for every clip; only the frame changes."""
import json, os, subprocess, sys
import numpy as np
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
import softblue as SB
import composite as CP
FF = SB.FF; FPSS = "30000/1001"; W, H = 1920, 1080
B = json.load(open("beats.json")); P = json.load(open("clip_paths.json")); PL = json.load(open("hf16/plates.json"))
by = {c["name"]: c for c in B["cards"]}
os.makedirs("cards_16x9", exist_ok=True); os.makedirs("media16", exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"
dur = lambda k: by[k]["frames"] * 1001 / 30000
R3M = "/Volumes/Extreme/_edit_work/ra06/round3/motion"
AI_SHOTS = {   # copied from s06_inserts06.py (round 3, approved): (take, in s, out s, crop in the 720x1280 take)
 "I3": [("I3_v1", 0.0, 5.0, None)],
 "I1": [("I1_v1", 0.0, 2.05, None), ("I1_v2", 3.10, 4.55, "576:1024:0:150")],
 "I4": [("I4_v2", 0.25, 2.35, None)],
}

def media(name, segs, vf, wh, n):
    out = f"media16/{name}.mp4"; ins, ch = [], []
    for i, (p, t0, d) in enumerate(segs):
        ins += ["-ss", f"{t0:.3f}", "-t", f"{d + 0.2:.3f}", "-i", p]
        ch.append(f"[{i}:v]fps={FPSS},{vf},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1,trim=end_frame={round(d * 30000 / 1001)},setpts=PTS-STARTPTS[v{i}]")
    ch.append("".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=1[v]")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n)] + ENC + [out], check=True)
    return out

def ai_media(name, wh, n):
    ins, ch = [], []
    for i, (take, a, b, crop) in enumerate(AI_SHOTS[name]):
        ins += ["-i", f"{R3M}/{take}.mp4"]
        cr = f"crop={crop}," if crop else ""
        ch.append(f"[{i}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps={FPSS},{cr}scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1[v{i}]")
    k = len(AI_SHOTS[name])
    ch.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.1[v]")
    want_s = sum(b - a for _, a, b, _c in AI_SHOTS[name]); assert abs(want_s - n * 1001 / 30000) < 0.05, (name, want_s, n)
    out = f"media16/{name}.mp4"
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

def plate_card(name, segs=None, vf="null"):
    pl = PL[name]; n = by[name]["frames"]; x0, y0, x1, y1 = pl["hole"]; wh = (x1 - x0, y1 - y0)
    m = ai_media(name, wh, n) if segs is None else media(name, segs, vf, wh, n)
    e = writer(f"cards_16x9/{name}.mp4"); k = 0
    for f, ov in zip(frames(m, wh, n), CP.reader(pl["mov"], 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes()); k += 1
    e.stdin.close(); assert e.wait() == 0 and k == n, (name, k, n)
    print(name, n, "frames, hole", pl["hole"], "chip", pl["chip"], flush=True)

only = set(sys.argv[1:]); want = lambda k: not only or k in only
for k in ("I3", "I1", "I4"):
    if want(k): plate_card(k)
if want("fired"): plate_card("fired", [(P["A0147"], 0.0, dur("fired"))])
if want("flow_a"): plate_card("flow_a", [(P["B0049"], 13.0, dur("flow_a"))], "crop=1320:1600:0:170")
if want("flow_b"):
    FLOW_B_T0 = 28.0      # B0049's banned "Meet the new you" BEFORE/AFTER screen runs to about 27.6 s
    plate_card("flow_b", [(P["B0049"], FLOW_B_T0, dur("flow_b"))], "crop=1320:1600:0:170")
if want("tour"): plate_card("tour", [(P["B0034"], 0.0, dur("tour"))])
if want("tour2"):
    d = dur("tour2"); a = min(1.75, d * 0.42)
    plate_card("tour2", [(P["B0544"], 6.05, a), (P["B0544"], 5.2 - (d - a), d - a)])
meta = {}
for k, pl in PL.items():
    c = pl.get("chip")
    meta[k] = dict(chip=c["s"] if c else None, chip_box=[c["x"], c["y"], c["x"] + c["w"], c["y"] + 80] if c else None, hole=pl["hole"])
json.dump(meta, open("cards_16x9/meta.json", "w"), indent=1)
print("INSERTS16_COMPLETE")
