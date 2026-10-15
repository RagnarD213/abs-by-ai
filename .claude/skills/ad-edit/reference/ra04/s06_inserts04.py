#!/usr/bin/env python3
"""RA-04 insert cards at 9:16 -> cards_9x16/<name>.mp4, each exactly its timeline frame count.

  lock      A0074 fills the frame (AI goal picture on a phone lock screen) + the Soft Blue AI-GENERATED chip
  flow_a/b  B0049 (the app's own generate flow, same man before and after) under a HyperFrames media-card plate
  analysis  the approved adkit analysis card, recoloured to Soft Blue Light (ANALYSIS=olive keeps RA-01's colours)
  tour      B0544 (the approved app tour) under a media-card plate: workout sheet first, then the meal analysis
  brokenarm  the AI broken-arm clip (round 3, media/ai1.mp4) + chip; knee  B0126 (round 1-2, retired);  home  B0464 (Dan's real squats on the lawn), a steady 608 px window on him
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
if want("lock"):
    meta["lock"] = {"chip": "AI-GENERATED", "chip_box": fill_card("lock", [(P["A0074"], 0.5, dur("lock"))], "null", chip=("AI-GENERATED", (60, 236)))}
if want("knee"):
    fill_card("knee", [(P["B0126"], 0.4, dur("knee"))], "null")
if want("brokenarm"):
    # round 3: the AI broken-arm clip (assemble04.py -> media/ai1.mp4, already the card's exact frames). The chip sits top left,
    # above and beside the man in all three shots (he stands centre-left at the rack, then lies with his head at mid-left).
    meta["brokenarm"] = {"chip": "AI-GENERATED", "chip_box": fill_card("brokenarm", [("media/ai1.mp4", 0.0, dur("brokenarm"))], "null", chip=("AI-GENERATED", (60, 236)))}
if want("home"):
    X0 = int(os.environ.get("HOME_X", "704")); T0 = float(os.environ.get("HOME_T", "0.2"))
    fill_card("home", [(P["B0464"], T0, dur("home"))], f"crop=608:1080:{X0}:0")
if want("flow_a"):
    d = dur("flow_a"); a = min(1.5, d * 0.4)
    plate_card("flow_a", [(P["B0049"], 6.3, a), (P["B0049"], 13.0, d - a)], "crop=1320:2420:0:170")
if want("flow_b"):
    # ⚠ B0049's banned "Meet the new you" BEFORE/AFTER screen runs to about 27.6 s (found 2026-10-13 by RA-05: a start at
    # 27.3 s put it on screen for the card's first 0.3 s). The result screen alone starts at 28.0 s and holds to 34 s.
    FLOW_B_T0 = 28.0
    assert FLOW_B_T0 >= 27.9 and dur("flow_b") <= 5.5, dur("flow_b")      # the crop keeps the email form out
    plate_card("flow_b", [(P["B0049"], FLOW_B_T0, dur("flow_b"))], "crop=1320:1600:0:170")
if want("tour"):
    d = dur("tour"); a = min(2.5, d * 0.47)
    plate_card("tour", [(P["B0544"], 6.05, a), (P["B0544"], 2.1, d - a)], "null")
if want("analysis"):
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
