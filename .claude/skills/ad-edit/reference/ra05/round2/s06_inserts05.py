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
if want("lock"):
    meta["lock"] = {"chip": "AI-GENERATED", "chip_box": fill_card("lock", [(P["A0074"], 0.5, dur("lock"))], "null", chip=("AI-GENERATED", (60, 236)))}
if want("curls"):      # Dan's real dumbbell curls by the pool (library B0458, 16:9): a steady 608 px window on him, full height
    fill_card("curls", [(P["B0458"], float(os.environ.get("CURLS_T", "0.9")), dur("curls"))], f"crop=608:1080:{os.environ.get('CURLS_X', '656')}:0,eq=gamma=0.94:saturation=1.10,colorbalance=rm=0.02:bm=-0.03")   # colour brought toward the presenter look (sunny-day clip)
if want("pose"):       # Dan's real physique poses from the same pool shoot (library B0435, native 9:16): hair to mid thigh, steady window. From 4.3 s: he faces the camera to the end (between 2 and 4 s he looks away).
    # Colour matched to the presenter's FAR shot in the C2 look (chest skin 137/92/66 there; 137/95/64 here after the eq).
    fill_card("pose", [(P["B0435"], float(os.environ.get("POSE_T", "4.3")), dur("pose"))], os.environ.get("POSE_VF", "crop=630:1120:332:300,eq=gamma=1.04:saturation=1.26,colorbalance=rm=0.03:bm=-0.02"))
if want("flow_b"):
    # B0049's banned "Meet the new you" BEFORE/AFTER screen runs to about 27.6 s; the result screen alone starts at 28.0 s
    # (confetti, then it holds to 34 s). The crop keeps the email form out.
    FLOW_B_T0 = 28.0
    assert FLOW_B_T0 >= 27.9 and dur("flow_b") <= 5.5, dur("flow_b")
    plate_card("flow_b", [(P["B0049"], FLOW_B_T0, dur("flow_b"))], "crop=1320:1600:0:170")
if want("tour"):       # the approved app tour (B0544): the AI Trainer exercise sheet first, then the meal photo analysed
    d = dur("tour"); a = min(2.2, d * 0.47)
    plate_card("tour", [(P["B0544"], 6.05, a), (P["B0544"], 2.6, d - a)], "null")
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
# ---------------------------------------------------------------- ROUND 2
import s06_open as O
def plate_frames(name, rows, out_media):
    """rows = [(path, src_in, src_out, out_frames, crop_vf)] -> each row sped to fill exactly out_frames, concatenated, under
    the plate. A row whose source span is longer than its frames is played fast (setpts), never held or slowed."""
    pl = PL[name]; n = by[name]["frames"]; x0, y0, x1, y1 = pl["hole"]; wh = (x1 - x0, y1 - y0)
    assert sum(r[3] for r in rows) == n, (name, sum(r[3] for r in rows), n)
    ins, ch = [], []
    for i, (pth, a, b, nf, vf) in enumerate(rows):
        od = nf * 1001 / 30000; k = od / (b - a)
        assert k <= 1.01 or nf <= 2, (name, i, "a row may be sped up, never slowed")
        ins += ["-ss", f"{a:.3f}", "-t", f"{b - a + 0.25:.3f}", "-i", pth]
        ch.append(f"[{i}:v]setpts=(PTS-STARTPTS)*{k:.6f},fps={FPSS},{vf},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1,"
                  f"trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]")
    ch.append("".join(f"[v{i}]" for i in range(len(rows))) + f"concat=n={len(rows)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.2[v]")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n)] + ENC + [out_media], check=True)
    e = writer(f"cards_9x16/{name}.mp4")
    for f, ov in zip(frames(out_media, wh, n), CP.reader(pl["mov"], 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes())
    e.stdin.close(); e.wait(); print(name, n, "frames, hole", pl["hole"], flush=True)

if want("open"):
    n = by["open"]["frames"]; rows = [(P["B0049"], a, b, nf, f"crop=1320:1600:0:{y}") for a, b, nf, y, _ in O.SEGS]
    rn = n - O.RESULT_F; assert rn * 1001 / 30000 >= 1.0, "the result must hold at least 1.0 s"
    assert O.RESULT_T0 >= 27.9
    rows.append((P["B0049"], O.RESULT_T0, O.RESULT_T0 + rn * 1001 / 30000, rn, f"crop=1320:1600:0:{O.RESULT_Y}"))
    plate_frames("open", rows, "media/open.mp4")
    meta["open"] = {"segments": [dict(src=[a, b], frames=nf, crop_y=y, what=w) for a, b, nf, y, w in O.SEGS] +
                    [dict(src=[O.RESULT_T0, round(O.RESULT_T0 + rn * 1001 / 30000, 3)], frames=rn, crop_y=O.RESULT_Y, what="the AI result alone, AI-GENERATED")],
                    "result_frame": O.RESULT_F}
if want("scan"):       # A0044 = the start VSL's version A body scan (WV-01 round 4 SCAN-readable.mp4, sha 68ef87d8)
    n = by["scan"]["frames"]; d = n * 1001 / 30000
    assert O.SCAN_T0 + d <= 5.0, ("the scan clip would run out", O.SCAN_T0 + d)
    plate_frames("scan", [("/Volumes/Extreme/_edit_work/wv01-edit/round4/motion/SCAN-readable.mp4", O.SCAN_T0, O.SCAN_T0 + d, n,
                           f"crop={O.SCAN_W}:1080:{O.SCAN_X0}:0")], "media/scan.mp4")
if want("A1"):         # the HyperFrames analysis card is OPAQUE in the compositor; the concat only needs a slot of the right length
    n = by["A1"]["frames"]
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPSS}", "-frames:v", str(n)] + ENC + ["cards_9x16/A1.mp4"], check=True)
if want("couch"):      # LABELLED START/END-frame placeholder (VIDEO-RULES "Future contextual previews"); no motion before approval
    from PIL import ImageDraw, ImageFont
    import motionlib as ML
    c = by["couch"]; n = c["frames"]; k = int(round((c["cut_at"] - c["beat"][0]) * 30000 / 1001))
    ims = {}
    for tag in ("START", "END"):
        im = Image.open(os.environ.get(f"COUCH_{tag}", f"frames/couch_{tag}.png")).convert("RGB")
        sw, sh = im.size; tw = round(sh * 9 / 16)
        if tw < sw: im = im.crop(((sw - tw) // 2, 0, (sw - tw) // 2 + tw, sh))
        ims[tag] = im.resize((W, H), Image.LANCZOS)
    e = writer("cards_9x16/couch.mp4")
    for g in range(n):
        tag = "START" if g < k else "END"; im = ims[tag].copy()
        d = ImageDraw.Draw(im); f = ML.font(40, "ExtraBold"); txt = f"PREVIEW: {tag} FRAME  (motion after you approve)"
        tw_ = ML.text_size(txt, f)[0]; bx = (W - tw_) // 2 - 24
        d.rounded_rectangle([bx, 200, bx + tw_ + 48, 268], radius=14, fill=(255, 196, 0))
        d.text((W // 2, 212), txt, font=f, fill=(20, 20, 20), anchor="mt")
        SB.disclosure(im, "AI-GENERATED", (60, 290))
        e.stdin.write(np.ascontiguousarray(np.asarray(im)).tobytes())
    e.stdin.close(); e.wait(); print("couch placeholder", n, "frames, cut at", k, flush=True)
json.dump(meta, open("cards_9x16/meta.json", "w"), indent=1)
print("INSERTS_COMPLETE")
