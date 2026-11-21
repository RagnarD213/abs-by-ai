#!/usr/bin/env python3
"""RA-15 round 3: the 16:9 insert cards -> cards_16x9/<name>.mp4, each exactly its timeline frame count (the same plan as the 9:16).

  opener, enjoy           the 16:9 AI clips (A0016 museum, A0086 steak) fill the frame; AI-GENERATED chip placed clear of every person
  fridge, restaurant,     the 9:16 AI clips (I2, I4, I5 approved round 2; A0074 lock screen) whole, full height, in a media-card plate on the
  cutout, lock            field (hf16/plates.json); never cropped, so the fridge door, the phone and finger on the menu, and the cutout on the
                          floor all stay in the picture (VIDEO-RULES: a vertical clip in a horizontal frame)
  flow, macro             the app recordings in the same plate (B0049 crop as the 9:16; B0038 salmon, Dan 2026-10-14)
  analysis                round3/s_analysis.py (the Soft Blue HyperFrames card)
Same in- and out-points as s06_inserts15.py for every clip."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
import softblue as SB
import composite as CP
import ra01lib as L
FF = SB.FF; FPSS = "30000/1001"; W, H = 1920, 1080
B = json.load(open("beats.json")); P = json.load(open("clip_paths.json")); PL = json.load(open("hf16/plates.json"))
by = {c["name"]: c for c in B["cards"]}
os.makedirs("cards_16x9", exist_ok=True); os.makedirs("media16", exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"
dur = lambda k: by[k]["frames"] * 1001 / 30000

def media(name, segs, vf, wh, n):
    out = f"media16/{name}.mp4"; ins, ch = [], []
    for i, sg in enumerate(segs):
        p, t0, d = sg[:3]; vfi = sg[3] if len(sg) > 3 else vf          # round 3: a segment may carry its own crop
        ins += ["-ss", f"{t0:.3f}", "-t", f"{d + 0.2:.3f}", "-i", p]
        ch.append(f"[{i}:v]fps={FPSS},{vfi},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1,trim=end_frame={round(d * 30000 / 1001)},setpts=PTS-STARTPTS[v{i}]")
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
    m = media(name, segs, vf, wh, n); e = writer(f"cards_16x9/{name}.mp4")
    for f, ov in zip(frames(m, wh, n), CP.reader(pl["mov"], 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes())
    e.stdin.close(); assert e.wait() == 0; print(name, n, "frames, hole", pl["hole"], "chip", pl["chip"], flush=True)

def fill_card(name, segs, vf):
    """A 16:9 clip full frame; the chip goes in whichever top corner no person reaches over every used frame (measured)."""
    n = by[name]["frames"]; m = media(name, segs, vf, (W, H), n)
    fs = list(frames(m, (W, H), n))
    union = np.zeros((H, W), bool)
    for f in fs[::6] + [fs[-1]]:
        pm = L.person_mask(Image.fromarray(f))
        if pm is not None: union |= pm
    cw, chh = 420, 84
    cand = {"top left": (54, 54), "top right": (W - 54 - cw, 54)}
    clear = {k: int(union[y:y + chh + 30, x:x + cw].sum()) for k, (x, y) in cand.items()}
    spot = min(clear, key=clear.get); xy = cand[spot]
    e = writer(f"cards_16x9/{name}.mp4"); box = None
    for f in fs:
        im = Image.fromarray(f); box = SB.disclosure(im, "AI-GENERATED", xy); e.stdin.write(np.ascontiguousarray(np.asarray(im)).tobytes())
    e.stdin.close(); assert e.wait() == 0
    print(name, n, "frames, chip", spot, box, "person px under the spots", clear, flush=True)
    return dict(chip="AI-GENERATED", chip_box=box, chip_spot=spot, person_px_under=clear)

only = set(sys.argv[1:]); want = lambda k: not only or k in only
meta = json.load(open("cards_16x9/meta.json")) if os.path.exists("cards_16x9/meta.json") else {}
# round 3 (review): in the full 16:9 frame a boy stands at the left for take frames 0-5, vanishes at frame 6, then walks in;
# from 0.25 s he is absent and then walks in (the 9:16's 560 px window never shows him)
if want("opener"): meta["opener"] = fill_card("opener", [(P["A0016"], float(os.environ.get("OPEN_T", "0.25")), dur("opener"))], "null")
if want("enjoy"):  meta["enjoy"] = fill_card("enjoy", [(P["A0086"], float(os.environ.get("ENJ_T", "0.0")), dur("enjoy"))], "null")
if want("fridge"): plate_card("fridge", [(P["I2"], 33/24, dur("fridge"))], "null")
if want("restaurant"): plate_card("restaurant", [(P["I4"], 32/24, dur("restaurant"))], "null")
# ROUND 4: the cutout card is out (Dan on camera).
# round 3 (review): A0074 carries a screen-glare haze from 2.17 s; 0.0-2.13 s is clear
if want("lock"): plate_card("lock", [(P["A0074"], float(os.environ.get("LOCK_T", "0.0")), dur("lock"))], "null")
if want("flow"):
    d = dur("flow"); a = min(1.6, d * 0.45)
    # round 3 (review): the generating screen scrolls; y 440 keeps the photo card, "Refining your silhouette" and its subtitle whole
    plate_card("flow", [(P["B0049"], 13.0, a, "crop=1320:1600:0:440"), (P["B0049"], 28.0, d - a)], "crop=1320:1600:0:205")   # round 3: y 205 clears the app header text "Your future self" (ends y ~192; review D3), and ends above the email form (y ~1832)
if want("macro"):
    d = dur("macro"); a = 0.55; b = 0.25
    plate_card("macro", [(P["B0038"], 0.0, a), (P["B0038"], 2.2, b), (P["B0038"], 2.8, d - a - b)], "crop=538:1016:18:32")
for k in ("fridge", "restaurant", "lock", "flow", "macro"):
    if PL[k].get("chip"): meta[k] = dict(chip=PL[k]["chip"]["s"], chip_box=[PL[k]["chip"]["x"], PL[k]["chip"]["y"], PL[k]["chip"]["x"] + PL[k]["chip"]["w"], PL[k]["chip"]["y"] + 80], hole=PL[k]["hole"])
    else: meta[k] = dict(chip=None, hole=PL[k]["hole"])
json.dump(meta, open("cards_16x9/meta.json", "w"), indent=1)
print("INSERTS16_COMPLETE")
