#!/usr/bin/env python3
"""RA-04 insert cards at 9:16 -> cards_9x16/<name>.mp4, each exactly its timeline frame count.

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
if want("opener"):     # A0016 museum gag (16:9): a steady window on the display case. 560x996 from the top puts the plaque (the punchline) BELOW the caption band; a full-height window put the opening caption on it
    meta["opener"] = {"chip": "AI-GENERATED", "chip_box": fill_card("opener", [(P["A0016"], float(os.environ.get("OPEN_T", "0.0")), dur("opener"))], f"crop=560:996:{os.environ.get('OPEN_X', '680')}:0", chip=("AI-GENERATED", (60, 236)))}
if want("factory"):    # A0017 'MEAL PLANS / ONE SIZE FITS ALL' conveyor (16:9). A full-frame window keeps only one of the two signs and the gag
    # needs both, so it is the centre-square rule (VIDEO-RULES 2026-10-01): a 1080 px square at x 440 holds both signs, in a card.
    plate_card("factory", [(P["A0017"], float(os.environ.get("FAC_T", "1.0")), dur("factory"))], "crop=1080:1080:440:0")
CH = json.load(open("round2/chip_place.json"))     # AI-GENERATED chip spots, measured clear of every person over the used frames
chip_at = lambda k: ("AI-GENERATED", tuple(CH[k]["chip_xy"][:2]))
if want("fridge"):     # I2 take 1 (Veo, 9:16, 24 fps), from take frame 33: the door is on its hinge swing, the full shelves are there from the
    # first frame of the open fridge, he stares at it. Take frames 0-26 are never shown (he lets go of the handle and the fridge slides toward him).
    meta["fridge"] = {"chip": "AI-GENERATED", "chip_box": fill_card("fridge", [(P["I2"], 33/24, dur("fridge"))], "null", chip=chip_at("I2"))}
if want("restaurant"): # I4 take 2, from take frame 32 (after a baked cut at 29/30, where the menu jumps flat): he picks up the one phone, looks, points
    # at the menu; the waiter writes the whole time.
    meta["restaurant"] = {"chip": "AI-GENERATED", "chip_box": fill_card("restaurant", [(P["I4"], 32/24, dur("restaurant"))], "null", chip=chip_at("I4"))}
if want("cutout"):     # I5 take 1 as TWO SHOTS on one locked camera (measured: scale 1.000, < 0.3 px between the parts). Shot A take frames 2-35: the
    # cutout stands across the table while he eats (from frame 6: the take brightens 4 % over frames 2-5, independent review). CUT. Shot B from
    # take frame 89 (the cutout moves under 0.3 px from there on, measured): she lies flat on the floor, he looks over at where she stood.
    # The fall itself (take frames 36-88) is never shown: in every take Veo spun her round and stood her back up (VIDEO-RULES 2026-10-13).
    a = 30/24; meta["cutout"] = {"chip": "AI-GENERATED", "chip_box": fill_card("cutout", [(P["I5"], 6/24, a), (P["I5"], 89/24, dur("cutout") - round(a*30000/1001)*1001/30000)], "null", chip=chip_at("I5"))}
if want("enjoy"):      # A0086 man enjoying a steak plate (16:9). Filling the screen cut his face or the plate he is enjoying, so it is
    # the centre square in a card (VIDEO-RULES 2026-10-01). 0.0-2.0 s: he smiles, takes the bite, savours it.
    plate_card("enjoy", [(P["A0086"], float(os.environ.get("ENJ_T", "0.0")), dur("enjoy"))], "crop=1080:1080:420:0")
if want("lock"):
    meta["lock"] = {"chip": "AI-GENERATED", "chip_box": fill_card("lock", [(P["A0074"], 0.5, dur("lock"))], "null", chip=("AI-GENERATED", (60, 236)))}
if want("flow"):
    # B0049: the man's own photo being refined (13.0 s), then HIS result alone from 28.0 s (the banned "Meet the new you"
    # before/after screen runs to about 27.6 s). The crop ends above the email form.
    d = dur("flow"); a = min(1.6, d * 0.45)
    plate_card("flow", [(P["B0049"], 13.0, a), (P["B0049"], 28.0, d - a)], "crop=1320:1600:0:170")
if want("macro"):      # B0035: the camera photographs a chicken-and-broccoli plate, Analyze Meal returns the itemized breakdown
    # 2 fps strip: camera 0-1.5 s (shutter at 1.5), Retake/Use Photo 2.0-3.0, the app with the photo 3.5, results from 4.0 to the end
    d = dur("macro"); a = min(1.3, d * 0.38); b = 0.5
    plate_card("macro", [(P["B0035"], 0.4, a), (P["B0035"], 3.5, b), (P["B0035"], 4.0, d - a - b)], "null")
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
