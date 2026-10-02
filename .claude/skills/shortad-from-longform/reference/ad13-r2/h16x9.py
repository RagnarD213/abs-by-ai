#!/usr/bin/env python3
"""AD 13, THE NEW 16:9 IN SOFT BLUE LIGHT: FIRST MINUTE ONLY (round 2, 2026-10-02). A new build path, not a kit stage.

Muhammad's graphics are burned into his master, so his master cannot be re-skinned. This rebuilds his first minute
from the pieces the vertical kit already recovered in this build dir:

  base.mp4            the raw roll conformed to HIS cut and graded with HIS grade (his.cube), 1920x1080, every frame
  auto/framing.json   his zoom on every talking frame (the slow push to 1.21x and back), measured against his master
  his audio           the first minute of his own mix, stream-copied (cut, never processed)

and draws every graphic fresh at 16:9 in Soft Blue Light with HyperFrames:
  lower thirds (Motivation) and the 3A list card: `_shared/hyperframes/from_plan.py` (the approved 16:9 templates)
  price card, corner running total, picture cards: the same template files the vertical uses, laid out at 1920x1080
  through a second copy of vertical.py (the way square.py does it). Wording is the vertical's copy file.
Dan's round 1 changes inside the first minute: the AI opener (START / END placeholders until the motion is approved)
and the Crazy 3 Min Home Abs Workout YouTube page at 0:24.

  python3 h16x9.py graphics | picture | proof | all
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
SHARED = PROJ + "/.claude/skills/_shared"
HF = pathlib.Path(SHARED) / "hyperframes"
FF = PROJ + "/Media/video_edit/bin/ffmpeg"
B_ = "/Volumes/Extreme/_edit_work/kit9x16/av11-ad13"
OUT = pathlib.Path(B_) / "round2" / "h16x9"
R2A = B_ + "/round2/assets"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
MASTER = PROJ + "/Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/i added up what getting abs was supposed to cost | muhammad | 16x9 | ad 13.mp4"
FPS = 30000 / 1001
W, H = 1920, 1080
END = 62.0
N = int(round(END * FPS))
fr = lambda t: int(round(t * FPS))

sys.path.insert(0, str(HF)); sys.path.insert(0, SHARED); sys.path.insert(0, B_)
_spec = importlib.util.spec_from_file_location("vertical_h", HF / "vertical.py")
V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)
SB = V.B                                               # softblue.py
V.W, V.Hh, V.CANVAS = W, H, [W, H]
V.U = SB.unit(W, H)
V.CAP_TOP = 10 ** 6                                    # no burned captions in the 16:9: a card is simply centred
import composite as HC  # noqa: E402

COPY = json.load(open(B_ + "/sbl_copy.json"))
WORDS = json.load(open(B_ + "/sbl_sheet.json"))["words"]["list"]
SEGS = json.load(open(B_ + "/edl_picture.json"))

REAL = "Real picture of me - not AI-generated"
AI = "AI-GENERATED"
A9 = LIB + "/04 AI-Generated Clips/concepts-and-gags/"
# the first minute's pictures: (t0, t1, how, source, start offset, chip)
PICS = [
    (0.0, 1.85, "full", R2A + "/opener_start_16x9_placeholder.png", 0, AI),
    (1.85, 3.70, "full", R2A + "/opener_end_16x9_placeholder.png", 0, AI),
    (11.879, 15.383, "card", A9 + "A0009_trainer-and-client-in-gym-with-phone_9x16_5s.mp4", 0.0, AI),
    (15.383, 20.02, "card", A9 + "A0013_man-overhead-press-with-robot-coach_9x16_5s.mp4", 0.0, AI),
    (24.558, 31.565, "full", R2A + "/yt3min_16x9.mp4", 0.0, None),
    (38.272, 39.573, "card", LIB + "/01 Before and After Images/00_ORIGINAL_deckchair_upscaled3x.jpg", 0, None),
    (41.141, 42.242, "card", LIB + "/06 Dan Photo Shoot Stills/photo-137_FINAL_PRIMARY.jpg", 0, REAL),
    (42.242, 43.277, "card", LIB + "/06 Dan Photo Shoot Stills/Dan-flag-FINAL.jpg", 0, REAL),
]
WIN = (43.277, 1467 / FPS)                              # his text screen: the 3A card, Dan moved right (to his cut)
TITLE = (52.419, 55.756)
TALLY = (55.756, END)
SHIFT = dict(dx=430, c0=330, wall_w=300)                # Dan clear of the card (x 752) with both arms in frame


def plan():
    lt = COPY["lower_thirds"]
    items = []
    for gid, k, t0, t1 in (("L01", "0", 0.334, 7.04), ("L02", "1", 21.521, 24.558), ("L03", "2", 58.725, 61.862)):
        x = dict(lt[k])
        if gid == "L01":                               # the 16:9 strip is one line: 12 px over with the leading "I"
            x["parts"] = [["Fired My Trainer And Nutritionist.", "fired"], x["parts"][1]]
        items.append(dict(id=gid, kind="lt", t0=t0, t1=t1, topic=x["topic"], point=" ".join(p for p, _ in x["parts"]), parts=x["parts"]))
    w = COPY["windows"]["0"]
    items.append(dict(id="W01", kind="l3", t0=WIN[0], t1=round(WIN[1], 3), heading=w["heading"], points=w["items"], reveal=w["reveal"]))
    return items


def graphics():
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(plan(), open(OUT / "plan_resolved.json", "w"), indent=1)
    json.dump(WORDS, open(OUT / "words_out.json", "w"))
    subprocess.run([sys.executable, str(HF / "from_plan.py"), "--plan", str(OUT / "plan_resolved.json"), "--words", str(OUT / "words_out.json"),
                    "--out", str(OUT / "hf"), "--render"], check=True)
    man = json.load(open(OUT / "hf" / "manifest.json"))
    x = COPY["titles"]["0"]
    sc, meta = V.title_scenes("T01", TITLE[0], TITLE[1], x.get("eyebrow"), x["headline"])
    movs = V.build(sc, OUT / "hf2")
    man.append(dict(id="T01", a=TITLE[0], b=TITLE[1], mov=str(movs["T01"]), kind="opaque"))
    sc, meta = V.tally_scenes("S01", TALLY[1] - TALLY[0], "So far", 400, 0, y=56)
    movs = V.build(sc, OUT / "hf2")
    man.append(dict(id="S01", a=TALLY[0], b=TALLY[1], mov=str(movs["S01"]), mask=str(movs["S01_mask"]), kind="glass", band=meta["band"]))
    plates = {}
    for i, (t0, t1, how, src, off, chip) in enumerate(PICS):
        if how != "card":
            continue
        ar = media_ar(src)
        gid = f"P{i:02d}"
        scene, hole = V.media_card_scene(gid, t1 - t0, ar, label=chip, max_h=800 if chip else 900, max_w=1500)
        movs = V.build([scene], OUT / "hf2")
        plates[str(i)] = dict(mov=str(movs[gid]), hole=hole)
        man.append(dict(id=gid, a=t0, b=t1, mov=str(movs[gid]), kind="overlay"))
    json.dump(sorted(man, key=lambda m: m["a"]), open(OUT / "manifest.json", "w"), indent=1)
    json.dump(plates, open(OUT / "plates.json", "w"), indent=1)
    print("graphics done:", [m["id"] for m in man])


def media_ar(src):
    if src.lower().endswith((".jpg", ".png")):
        w, h = Image.open(src).size
        return w / h
    o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]) / int(o[1])


def frames_of(src, off, n, w, h):
    """n rgb frames of `src` at w x h (cover, centred), from `off` seconds; a still repeats; a short clip holds."""
    if src.lower().endswith((".jpg", ".png")):
        im = Image.open(src).convert("RGB")
        s = max(w / im.width, h / im.height)
        im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
        x, y = (im.width - w) // 2, (im.height - h) // 2
        a = np.asarray(im.crop((x, y, x + w, y + h)))
        return [a] * n
    raw = subprocess.run([FF, "-v", "error", "-ss", str(off), "-i", src, "-vf",
                          f"fps=30000/1001,scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos:in_color_matrix=bt709:in_range=tv,"
                          f"crop={w}:{h},format=rgb24", "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True).stdout
    k = len(raw) // (w * h * 3)
    a = np.frombuffer(raw[:k * w * h * 3], np.uint8).reshape(k, h, w, 3)
    return [a[min(i, k - 1)] for i in range(n)]


def zoom_track():
    """His push on every frame: s(n). Measured samples that sit on plain talk (framing.json), interpolated inside each
    picture segment and lightly smoothed. The zoom is centred in x and anchored near the top in y (dx/(s-1) = 128 of
    256 on every sample; dy ~ 0), which is what his master shows."""
    F = json.load(open(B_ + "/auto/framing.json"))
    s = np.ones(N + 60)
    for sg in SEGS:
        n0, n1 = sg["n0"], min(sg["n1"], N + 60)
        if n0 >= N + 60:
            break
        pts = [(f["n"], f["s"]) for f in F if n0 <= f["n"] < sg["n1"] and f["frac"] >= 0.6 and 0.97 <= f["s"] <= 1.3 and abs(f["dx"] - (f["s"] - 1) * 128) <= 4]
        if len(pts) < 3:
            continue
        xs, ys = zip(*pts)
        seg = np.interp(np.arange(n0, n1), xs, ys)
        k = np.ones(9) / 9
        pad = np.concatenate([np.full(4, seg[0]), seg, np.full(4, seg[-1])])
        s[n0:n1] = np.convolve(pad, k, "valid")
    return np.clip(s, 1.0, 1.3)


def flash_alpha():
    import vlib
    out = {}
    for fa, fb in [f for f in json.load(open(B_ + "/beats.json"))["flashes"] if f[1] < END]:   # the vertical's schedule
        f0 = fr(fa)
        frames, _ = vlib.overlay_flash(fb - fa)
        for i, x in enumerate(frames):
            a = np.asarray(x.resize((W, H)) if x.size != (W, H) else x)[..., 3:4].astype(np.float32) / 255
            out[f0 + i] = a
    return out


def picture():
    man = json.load(open(OUT / "manifest.json"))
    plates = json.load(open(OUT / "plates.json"))
    C = HC.Compositor(man, wh=(W, H))
    S = zoom_track()
    FL = flash_alpha()
    pic = {}                                            # film frame -> (kind, array, hole)
    for i, (t0, t1, how, src, off, chip) in enumerate(PICS):
        n0, n1 = fr(t0), fr(t1)
        if how == "full":
            fs = frames_of(src, off, n1 - n0, W, H)
            if chip:
                tagged = {}
                for a in fs:
                    if id(a) not in tagged:
                        im = Image.fromarray(a).copy(); SB.disclosure(im, chip, xy=(W - 60, 44), anchor="rt"); tagged[id(a)] = np.asarray(im)
                fs = [tagged[id(a)] for a in fs]
            for k, a in enumerate(fs):
                pic[n0 + k] = ("full", a, None)
        else:
            x0, y0, x1, y1 = plates[str(i)]["hole"]
            fs = frames_of(src, off, n1 - n0, x1 - x0, y1 - y0)
            for k, a in enumerate(fs):
                pic[n0 + k] = ("card", a, (x0, y0, x1, y1))
    w0, w1 = fr(WIN[0]), fr(WIN[1])
    dec = subprocess.Popen([FF, "-v", "error", "-i", B_ + "/base.mp4", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                            "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    pv = str(OUT / "picture_first_minute.mp4")
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-video_track_timescale", "30000", "-an", pv],
                           stdin=subprocess.PIPE)
    size = W * H * 3
    for n in range(N):
        buf = dec.stdout.read(size)
        if len(buf) < size:
            raise SystemExit(f"base.mp4: short read at frame {n}")
        if n in pic:
            kind, a, hole = pic[n]
            if kind == "full":
                frame = a
            else:
                frame = np.zeros((H, W, 3), np.uint8)
                frame[hole[1]:hole[3], hole[0]:hole[2]] = a
        else:
            frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            if w0 <= n < w1:
                frame = np.asarray(SB.shift_presenter(Image.fromarray(frame), **SHIFT))
            elif S[n] > 1.002:
                s = float(S[n])
                M = np.float32([[s, 0, -(s - 1) * W / 2], [0, s, -(s - 1) * 36]])
                frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LANCZOS4)
        if C.active(n):
            frame = C.apply(np.ascontiguousarray(frame), n)
        if n in FL:
            al = FL[n]
            frame = (frame.astype(np.float32) * (1 - al) + np.array([244, 250, 255], np.float32) * al + 0.5).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(frame).tobytes())
        if n % 300 == 0:
            print("frame", n, flush=True)
    enc.stdin.close(); enc.wait(); dec.kill(); dec.wait()
    out = str(OUT / "DRAFT - Ad 13 16x9 Soft Blue Light round 2 - first minute.mp4")
    subprocess.run([FF, "-v", "error", "-y", "-i", pv, "-t", str(N / FPS), "-i", MASTER, "-map", "0:v", "-map", "1:a", "-c", "copy",
                    "-t", str(N / FPS), "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(OUT / "DRAFT - Ad 13 16x9 Soft Blue Light round 2 - first minute - REVIEW 540p.mp4")], check=True)
    print("picture done:", out)


def proof():
    """The grade and the zoom, proven against his master on plain talking frames (no graphic on either side)."""
    out = str(OUT / "DRAFT - Ad 13 16x9 Soft Blue Light round 2 - first minute.mp4")
    rows, tiles = [], []
    for t in (8.2, 9.6, 21.0, 33.0, 35.5, 37.0, 50.5, 57.2):
        fs = []
        for src in (MASTER, out):
            raw = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf",
                                  "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
            fs.append(np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32))
        m, o = fs
        box = (slice(60, 620), slice(500, 1500))                 # head and shoulders, clear of both sets of graphics
        d = np.abs(m[box] - o[box])
        rows.append(dict(t=t, mean_abs_levels=round(float(d.mean()), 2), median=round(float(np.median(d)), 2),
                         mean_rgb_master=[round(float(v), 1) for v in m[box].mean(axis=(0, 1))], mean_rgb_ours=[round(float(v), 1) for v in o[box].mean(axis=(0, 1))]))
        tiles.append(np.concatenate([m, o], axis=1).astype(np.uint8))
    json.dump(rows, open(OUT / "grade_proof.json", "w"), indent=1)
    sheet = np.concatenate([np.asarray(Image.fromarray(x).resize((1920, 540))) for x in tiles[:4]], axis=0)
    Image.fromarray(sheet).save(OUT / "grade_proof.jpg", quality=90)
    for r in rows:
        print(r)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["all"]):
        for fn in (["graphics", "picture", "proof"] if step == "all" else [step]):
            globals()[fn]()
