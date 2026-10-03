#!/usr/bin/env python3
"""AD 13, THE NEW 16:9 IN SOFT BLUE LIGHT: THE WHOLE FILM (round 3, 2026-10-02). Extends ad13-r2/h16x9.py (the first
minute Dan approved) to all 7,339 frames. A new build path, not a kit stage.

  base.mp4            the raw roll conformed to HIS cut and graded with HIS grade, 1920x1080, every frame (read only)
  auto/framing.json   his zoom on every talking frame, measured against his master
  his audio           his own mix, stream-copied whole (never processed)

Every graphic is drawn fresh at 16:9 in Soft Blue Light with HyperFrames:
  lower thirds and the 3A list cards: `_shared/hyperframes/from_plan.py`
  price cards with their bill rows, the corner running total, picture / phone cards, the closing CTA: the template
  files the vertical uses, laid out at 1920x1080 through a second copy of vertical.py. Wording: sbl_copy.json.
What is on screen when follows HIS master (content_auto.json = what his master shows, frame-accurate), except Dan's
changes: the AI opener (0:00), the Crazy 3 Min Home Abs YouTube page (0:24), the AI exercise demo phone (2:38).
His white flashes are measured off his master (15 of them) and redrawn in Soft Blue white.

  python3 h16x9.py graphics | picture | proof | all
"""
import importlib.util
import json
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
OUT = pathlib.Path(B_) / "round3" / "h16x9"
R2A = B_ + "/round2/assets"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
MASTER = PROJ + "/Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/i added up what getting abs was supposed to cost | muhammad | 16x9 | ad 13.mp4"
FPS = 30000 / 1001
W, H = 1920, 1080
N = 7339
END = N / FPS
fr = lambda t: int(round(t * FPS))
T = lambda n: round(n / FPS, 3)
NAME = "DRAFT - Ad 13 16x9 Soft Blue Light round 3b - full"

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
AA = B_ + "/assets_auto/"                              # lifts of his own full-screen stock (no graphic burned in)
AS = B_ + "/assets_sbl/"
# every picture, in his master's frames: (n0, n1, how, source, start offset s, chip, tally stays on)
PICS = [
    (0, fr(3.70), "full", B_ + "/round3/assets/opener_motion_16x9.mp4", 0.0, AI, False),
    (356, 461, "card", A9 + "A0009_trainer-and-client-in-gym-with-phone_9x16_5s.mp4", 0.0, AI, False),
    (461, 600, "card", A9 + "A0013_man-overhead-press-with-robot-coach_9x16_5s.mp4", 0.0, AI, False),
    (736, 946, "full", R2A + "/yt3min_16x9.mp4", 0.0, None, False),
    (1147, 1186, "card", LIB + "/01 Before and After Images/00_ORIGINAL_deckchair_upscaled3x.jpg", 0, None, False),
    (1233, 1266, "card", LIB + "/06 Dan Photo Shoot Stills/photo-137_FINAL_PRIMARY.jpg", 0, REAL, False),
    (1266, 1297, "card", LIB + "/06 Dan Photo Shoot Stills/Dan-flag-FINAL.jpg", 0, REAL, False),
    (1956, 2070, "card", A9 + "A0009_trainer-and-client-in-gym-with-phone_9x16_5s.mp4", 1.0, AI, False),
    (2070, 2158, "card", A9 + "A0010_trainer-hands-client-generic-sheet_9x16_5s.mp4", 0.5, AI, False),
    (2356, 2382, "full", AA + "auto_02356.mp4", 0.0, None, False),          # his broccoli, rice, plate: kept (16:9 scope)
    (2382, 2409, "full", AA + "auto_02382.mp4", 0.0, None, False),
    (2409, 2430, "full", AA + "auto_02409.mp4", 0.0, None, False),
    (2510, 2591, "full", AA + "auto_02510.mp4", 0.0, None, False),          # his nutritionist desk
    (2890, 2921, "full", AA + "auto_02890.mp4", 0.0, None, False),          # his three supplement shots
    (2921, 2943, "full", AA + "auto_02921.mp4", 0.0, None, False),
    (2943, 2979, "full", AA + "auto_02943.mp4", 0.0, None, False),
    (3320, 3427, "full", PROJ + "/Media/codex-video-trial/06-ad-r1/assets/pexels-6326748.mp4", 2.0, None, True),
    (4196, 4346, "card", AA + "auto_04196.mp4", 0.0, AI, False),            # the phone-in-hand AI clip
    (4453, 4514, "phone", AS + "phone_04453.mp4", 0.0, None, False),
    (4514, 4587, "card", LIB + "/01 Before and After Images/dan by pool - AI GOAL IMAGE.png", 0, AI, False),
    (4741, 4915, "phone", AS + "phone_workout_crunch.mp4", 0.0, None, False),   # P20: the approved AI exercise demo
    (5640, 5811, "phone", AS + "phone_05640.mp4", 0.0, None, False),
    (6186, 6375, "phone", AS + "phone_06186.mp4", 0.0, None, False),        # his meal tracker (P22 swap was vertical only)
    (6914, 6945, "phone", AA + "auto_06914.mp4", 0.0, None, False),
    (6945, 7028, "phone", AA + "auto_06945.mp4", 0.0, None, False),
    (7028, 7099, "card", LIB + "/01 Before and After Images/dan by pool - AI GOAL IMAGE.png", 0, AI, False),
]
# his text screens: the 3A card, Dan moved right. Start on the roll's own cut (the shift is never seen as a jump),
# end on his flash or his next picture.
WINS = [("W01", "0", 1297, 1467), ("W02", "1", 3427, 3638), ("W03", "2", 5036, 5385), ("W04", "3", 5995, 6186), ("W05", "4", 6543, 6849)]
LTS = [("L01", "0", 0.334, 7.04), ("L02", "1", 21.521, 24.558), ("L03", "2", 58.725, 61.862), ("L04", "3", 87.9, 92.96),
       ("L05", "4", 103.103, 106.74), ("L06", "5", 130.797, 134.868), ("L07", "6", 145.178, 148.482), ("L08", "7", 182.516, 187.954),
       ("L09", "8", 213.547, 216.783), ("L10", "9", 237.037, 241.308)]
TITLES = [("T01", "0", 52.419, 55.756), ("T02", "1", 72.005, 74.975), ("T03", "2", 93.06, 96.43), ("T04", "3", 106.74, 110.777),
          ("T05", "4", 121.388, 124.458)]
# the corner running total, where his master shows "So Far: $N/Month" (hidden on his full-screen stock, as his is)
TALLIES = [("S01", 55.756, T(1956), 400, 0), ("S02", 74.975, 93.06, 700, 400), ("S03", T(2979), 106.74, 850, 700), ("S04", T(3320), T(3427), 1050, 850)]   # S04 ends where the 3A card takes the top-left corner
CTA = ("C03", 241.641, END)
FLASH_PEAKS = [599, 944, 1295, 1469, 1669, 2245, 3728, 4344, 4586, 4914, 5384, 5808, 6372, 6848, 7097]   # measured on his master
# base.mp4 carries the WRONG raw footage for picture segments 60 and 61 (frames 6844 to 7099: src 266.9 s of the roll,
# where his audio there is src 371.0 s, found by cross-correlating his mix with the lav and confirmed against his
# frames). Frames 6914+ are under pictures; 6844 to 6913 are Dan on camera, so they are re-read from the raw roll at
# the right place (his audio's offset, +1 frame to land on his picture) with his grade. base.mp4 itself is not touched.
RAW = "/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1602.MP4"
# Round 3b: the reviewer found his cut at 2:14.87 lands on frame 4042; base.mp4 (segment 37) starts the new shot at
# 4044, so 4042 and 4043 are read from the raw roll too, two frames before segment 37's own first raw frame.
PATCHES = [(4042, 4044, 232.78626666666668 - 2 / FPS),                      # (film n0, n1, raw seconds at n0)
           (6844, 6914, 6844 / FPS + 370.974 - 228.7 + 1 / FPS)]
# Round 3b: his phone lifts carry his own bezel and his olive grid in the corners. Only the SCREEN is used (measured
# inner edge of his black bezel ring on the median frame, 2 px inside), its rounded corners filled with the screen's own edge colour, and it sits in
# the same blue card as the workout demo, so every phone in the film is one device: (x, y, w, h, corner radius px).
PHONE_CROP = {"phone_04453.mp4": (36, 36, 410, 893, 58), "phone_05640.mp4": (35, 36, 381, 827, 54),
              "phone_06186.mp4": (35, 36, 381, 827, 54), "auto_06914.mp4": (27, 10, 431, 938, 60),
              "auto_06945.mp4": (27, 10, 431, 938, 60)}
# His lifts open on his own blur-in (measured, Laplacian variance): the screen holds its first sharp frame instead,
# under our card's own rise.
SHARP_FROM = {"phone_05640.mp4": 12, "phone_06186.mp4": 18, "auto_06914.mp4": 2}
# Round 3b: two-part lower thirds go through vertical.py's lower third (the same template; it wraps at a part
# boundary when one line is too narrow), with the browser's missing gap after the full stop added back.
LT_OWN = ("L01", "L04", "L08")
PART_GAP = 14                                            # px added before every part after the first
SHIFT = dict(dx=430, c0=330, wall_w=300)                # Dan clear of the card (x 752) with both arms in frame


def plan():
    lt = COPY["lower_thirds"]
    items = []
    for gid, k, t0, t1 in LTS:
        if gid in LT_OWN:
            continue
        x = dict(lt[k])
        if gid == "L01":                               # the 16:9 strip is one line: 12 px over with the leading "I"
            x["parts"] = [["Fired My Trainer And Nutritionist.", "fired"], x["parts"][1]]
        if gid == "L04":                               # 1,808 px of 1,632 at 16:9: the first sentence loses "If You Quit,"
            x["parts"] = [["You'll Be Back.", "quit"], x["parts"][1]]
        items.append(dict(id=gid, kind="lt", t0=t0, t1=t1, topic=x["topic"], point=" ".join(p for p, _ in x["parts"]), parts=x["parts"]))
    for gid, k, n0, n1 in WINS:
        w = COPY["windows"][k]
        items.append(dict(id=gid, kind="l3", t0=T(n0) if gid != "W01" else 43.277, t1=T(n1), heading=w["heading"], points=w["items"], reveal=w["reveal"]))
    return items


def own_lower_thirds():
    """L01, L04, L08 through vertical.py's lower third at 1920x1080: the part times are the words' own (from_plan's
    Words), the strip wraps at a part boundary only when the line is too long (L04), and every part after the first
    moves right by PART_GAP so a full stop is followed by a visible space (the browser sets the text about 1 % wider
    than the PIL measure the layout uses, which ate the space)."""
    spec = importlib.util.spec_from_file_location("from_plan_h", HF / "from_plan.py"); FP = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(FP)
    Wd = FP.Words(str(OUT / "words_out.json"))
    out = []
    for gid, k, a, b in LTS:
        if gid not in LT_OWN:
            continue
        x = dict(COPY["lower_thirds"][k])
        parts = x["parts"]
        if gid == "L01":                               # Dan approved the hook line without the leading "I" (round 2)
            parts = [["Fired My Trainer And Nutritionist.", "fired"], parts[1]]
        ps = [[p, round(max(a, Wd.at(ph, a - 1.0, b, f"{gid} {p}")), 3)] for p, ph in parts]
        sc, meta = V.lt_scenes(dict(id=gid, a=a, b=b, topic=x["topic"], parts=ps, drift=-4))
        for _tpl, cfg, _as in sc:
            ys = {}
            for q in cfg["parts"]:                     # per line: every part after the line's first moves right
                if q["y"] in ys:
                    q["x"] = round(q["x"] + PART_GAP * ys[q["y"]], 1)
                ys[q["y"]] = ys.get(q["y"], 0) + 1
            assert all(q["x"] < W - 200 for q in cfg["parts"])
        movs = V.build(sc, OUT / "hf2")
        out.append(dict(id=gid, a=a, b=b, mov=str(movs[gid]), mask=str(movs[gid + "_mask"]), kind="glass", band=meta["band"], lines=meta["lines"]))
        print(gid, "lines", meta["lines"], [(q["s"], q["x"], q["y"]) for q in sc[0][1]["parts"]], flush=True)
    return out


def cta_scenes(gid, dur, top, big):
    """The closing button at 16:9: the vertical's glass button (same template, same type sizes), 860 px wide, centred,
    its bottom 64 px from the frame edge (the lower third's line). His master's pill sits in the same place."""
    U = V.U
    bw, bh = 860, 110 * U
    x0 = (W - bw) / 2; by = H - 32 * U - bh
    big_px, top_px = 64, 30
    assert V.H.text_w(big, big_px) <= bw - 200 and V.H.text_w(top, top_px) <= bw - 80
    bx_ = x0 + (bw - V.H.text_w(big, big_px) - 56) / 2
    L = dict(btn=[x0, by, bw, bh], radius=22 * U, top=dict(x=round(x0 + (bw - V.H.text_w(top, top_px)) / 2), y=round(by + 24 * U), px=top_px, s=top),
             big=dict(x=round(bx_), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px, s=big),
             arrow=dict(x=round(bx_ + V.H.text_w(big, big_px) + 22), y=round(by + 24 * U + top_px * 1.4 + 6), px=big_px))
    out = [(HF / "cta" / "cta.template.htm", dict(id=gid + ("_mask" if m == "mask" else ""), mode=m, dur=round(dur, 3), canvas=[W, H],
                                                  hold_out=True, full=False, **L), ()) for m in ("content", "mask")]
    return out, dict(band=[int(by - 12), int(min(H, by + bh + 60))])


def graphics():
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(plan(), open(OUT / "plan_resolved.json", "w"), indent=1)
    json.dump(WORDS, open(OUT / "words_out.json", "w"))
    subprocess.run([sys.executable, str(HF / "from_plan.py"), "--plan", str(OUT / "plan_resolved.json"), "--words", str(OUT / "words_out.json"),
                    "--out", str(OUT / "hf"), "--render"], check=True)
    man = json.load(open(OUT / "hf" / "manifest.json"))
    man += own_lower_thirds()
    for gid, k, t0, t1 in TITLES:
        x = COPY["titles"][k]
        sc, meta = V.title_scenes(gid, t0, t1, x.get("eyebrow"), x["headline"], x.get("items"))
        movs = V.build(sc, OUT / "hf2")
        man.append(dict(id=gid, a=t0, b=t1, mov=str(movs[gid]), kind="opaque"))
    for gid, t0, t1, val, frm in TALLIES:
        sc, meta = V.tally_scenes(gid, t1 - t0, "So far", val, frm, y=56)
        movs = V.build(sc, OUT / "hf2")
        man.append(dict(id=gid, a=t0, b=t1, mov=str(movs[gid]), mask=str(movs[gid + "_mask"]), kind="glass", band=meta["band"], tally=True, box=meta["box"]))
    gid, t0, t1 = CTA
    sc, meta = cta_scenes(gid, t1 - t0, COPY_CTA[0], COPY_CTA[1])
    movs = V.build(sc, OUT / "hf2")
    man.append(dict(id=gid, a=t0, b=t1, mov=str(movs[gid]), mask=str(movs[gid + "_mask"]), kind="glass", band=meta["band"]))
    plates = {}
    for i, (n0, n1, how, src, off, chip, _) in enumerate(PICS):
        if how == "full":
            continue
        ar = media_ar(src)
        gid = f"P{i:02d}"
        scene, hole = V.media_card_scene(gid, (n1 - n0) / FPS, ar, label=chip, max_h=800 if chip else 900, max_w=1500)
        movs = V.build([scene], OUT / "hf2")
        plates[str(i)] = dict(mov=str(movs[gid]), hole=hole)
        man.append(dict(id=gid, a=n0 / FPS, b=n1 / FPS, mov=str(movs[gid]), kind="overlay"))
    json.dump(sorted(man, key=lambda m: m["a"]), open(OUT / "manifest.json", "w"), indent=1)
    json.dump(plates, open(OUT / "plates.json", "w"), indent=1)
    print("graphics done:", [m["id"] for m in man])


COPY_CTA = ("Get A FREE AI Image Of Yourself", "With Abs")   # beats.json cta_top / cta_big (his pill's words)


def media_ar(src):
    c = PHONE_CROP.get(pathlib.Path(src).name)
    if c:
        return c[2] / c[3]
    if src.lower().endswith((".jpg", ".png")):
        w, h = Image.open(src).size
        return w / h
    o = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]) / int(o[1])


def corner_fill(a, r):
    """Rounded screen corners: pixels outside a radius-r arc in each corner take the screen's own colour just inside
    the arc, so nothing of his bezel or his grid survives under the card's (smaller) rounding."""
    h, w = a.shape[:2]
    r = int(round(r))
    yy, xx = np.mgrid[0:r, 0:r]
    out = np.array(a)
    k = int(round(r - (r - 4) / np.sqrt(2)))           # a point on the diagonal, 4 px inside the arc
    for fy, fx in ((0, 0), (0, 1), (1, 0), (1, 1)):
        ys = slice(h - r, h) if fy else slice(0, r); xs = slice(w - r, w) if fx else slice(0, r)
        dy = (yy - (0 if fy else r - 1)) if fy else (r - 1 - yy); dx = (xx - (0 if fx else r - 1)) if fx else (r - 1 - xx)
        m = np.hypot(dy, dx) > r - 1
        py = (h - 1 - k) if fy else k; px = (w - 1 - k) if fx else k
        col = np.median(a[max(0, py - 1):py + 2, max(0, px - 1):px + 2].reshape(-1, 3), axis=0)
        blk = out[ys, xs]; blk[m] = col
    return out


def frames_of(src, off, n, w, h):
    """n rgb frames of `src` at w x h (cover, centred), from `off` seconds; a still repeats; a short clip holds.
    A phone lift in PHONE_CROP is cut to its screen first and its corners filled."""
    pc = PHONE_CROP.get(pathlib.Path(src).name)
    if pc:
        cx, cy, cw, ch, cr = pc
        raw = subprocess.run([FF, "-v", "error", "-ss", str(off), "-i", src, "-vf",
                              f"fps=30000/1001,crop={cw}:{ch}:{cx}:{cy},scale={w}:{h}:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=rgb24",
                              "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True).stdout
        k = len(raw) // (w * h * 3)
        assert k >= n - 2, f"{src}: {k} frames, the slot needs {n}"
        a = np.frombuffer(raw[:k * w * h * 3], np.uint8).reshape(k, h, w, 3)
        sf = SHARP_FROM.get(pathlib.Path(src).name, 0)
        fs = [corner_fill(a[max(i, sf)], cr * w / cw) for i in range(k)]
        return [fs[min(i, k - 1)] for i in range(n)]
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
    assert k >= n - 2, f"{src}: {k} frames, the slot needs {n} (a picture never freezes for more than 2 frames)"
    a = np.frombuffer(raw[:k * w * h * 3], np.uint8).reshape(k, h, w, 3)
    return [a[min(i, k - 1)] for i in range(n)]


def zoom_track():
    """His push on every frame: s(n). Measured samples that sit on plain talk (framing.json), interpolated inside each
    picture segment and lightly smoothed. The zoom is centred in x and anchored near the top in y."""
    F = json.load(open(B_ + "/auto/framing.json"))
    s = np.ones(N)
    for sg in SEGS:
        n0, n1 = sg["n0"], min(sg["n1"], N)
        pts = [(f["n"], f["s"]) for f in F if n0 <= f["n"] < sg["n1"] and f["frac"] >= 0.6 and 0.97 <= f["s"] <= 1.3 and abs(f["dx"] - (f["s"] - 1) * 128) <= 4]
        if len(pts) < 3:
            continue
        xs, ys = zip(*pts)
        seg = np.interp(np.arange(n0, n1), xs, ys)
        k = np.ones(9) / 9
        pad = np.concatenate([np.full(4, seg[0]), seg, np.full(4, seg[-1])])
        s[n0:n1] = np.convolve(pad, k, "valid")
    s[4042:4044] = s[4044]                                # the two patched frames belong to the next shot
    return np.clip(s, 1.0, 1.3)


def flash_alpha():
    """His flash at each of his 15 measured peaks, the first minute's envelope (0.44 s, starting 2 frames before his peak)."""
    import vlib
    out = {}
    frames, _ = vlib.overlay_flash(0.44)
    al = [np.asarray(x.resize((W, H)) if x.size != (W, H) else x)[..., 3:4].astype(np.float32) / 255 for x in frames]
    for p in FLASH_PEAKS:
        for i, a in enumerate(al):
            if p - 2 + i < N:
                out[p - 2 + i] = a
    return out


def patch_frames(n0, n1, t0):
    import grade
    src = round(t0 * FPS) / FPS - 0.0002
    raw = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{src:.5f}", "-i", RAW, "-an", "-frames:v", str(n1 - n0), "-vf",
                          grade.CURVES + ",scale=1920:1080,scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    assert len(a) == n1 - n0, f"raw patch: {len(a)} frames of {n1 - n0}"
    return a


def load_pic(i, plates):
    n0, n1, how, src, off, chip, _ = PICS[i]
    if how == "full":
        fs = frames_of(src, off, n1 - n0, W, H)
        if chip:
            fs2 = []
            for a in fs:
                im = Image.fromarray(a).copy(); SB.disclosure(im, chip, xy=(W - 60, 44), anchor="rt"); fs2.append(np.asarray(im))
            fs = fs2
        return [("full", a, None) for a in fs]
    x0, y0, x1, y1 = plates[str(i)]["hole"]
    return [("card", a, (x0, y0, x1, y1)) for a in frames_of(src, off, n1 - n0, x1 - x0, y1 - y0)]


def picture():
    man = json.load(open(OUT / "manifest.json"))
    plates = json.load(open(OUT / "plates.json"))
    C = HC.Compositor([m for m in man if not m.get("tally")], wh=(W, H))
    CT = HC.Compositor([m for m in man if m.get("tally")], wh=(W, H))
    S = zoom_track()
    FL = flash_alpha()
    start = {p[0]: i for i, p in enumerate(PICS)}
    hide_tally = np.zeros(N, bool)
    for n0, n1, how, *_r in PICS:
        if not _r[-1]:
            hide_tally[n0:n1] = True
    shifted = np.zeros(N, bool)
    for _g, _k, n0, n1 in WINS:
        shifted[n0:n1] = True
    cur, cur0, cur1 = None, 0, 0
    PT = {}
    dec = subprocess.Popen([FF, "-v", "error", "-i", B_ + "/base.mp4", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                            "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    pv = str(OUT / "picture_full.mp4")
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-video_track_timescale", "30000", "-an", pv],
                           stdin=subprocess.PIPE)
    size = W * H * 3
    for n in range(N):
        buf = dec.stdout.read(size)
        if len(buf) < size:
            raise SystemExit(f"base.mp4: short read at frame {n}")
        if n in start:
            cur, cur0, cur1 = load_pic(start[n], plates), n, PICS[start[n]][1]
        if cur is not None and n >= cur1:
            cur = None
        if cur is not None:
            kind, a, hole = cur[n - cur0]
            if kind == "full":
                frame = a
            else:
                frame = np.zeros((H, W, 3), np.uint8)
                frame[hole[1]:hole[3], hole[0]:hole[2]] = a
        else:
            frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            for pi, (p0, p1, pt) in enumerate(PATCHES):
                if p0 <= n < p1:
                    if pi not in PT:
                        PT[pi] = patch_frames(p0, p1, pt)
                    frame = PT[pi][n - p0]
            if shifted[n]:
                frame = np.asarray(SB.shift_presenter(Image.fromarray(frame), **SHIFT))
            elif S[n] > 1.002:
                s = float(S[n])
                M = np.float32([[s, 0, -(s - 1) * W / 2], [0, s, -(s - 1) * 36]])
                frame = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LANCZOS4)
        if C.active(n):
            frame = C.apply(np.ascontiguousarray(frame), n)
        if CT.active(n) and not hide_tally[n] and not C.opaque(n):
            frame = CT.apply(np.ascontiguousarray(frame), n)
        if n in FL:
            al = FL[n]
            frame = (frame.astype(np.float32) * (1 - al) + np.array([244, 250, 255], np.float32) * al + 0.5).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(frame).tobytes())
        if n % 300 == 0:
            print("frame", n, flush=True)
    enc.stdin.close(); enc.wait(); dec.kill(); dec.wait()
    out = str(OUT / (NAME + ".mp4"))
    subprocess.run([FF, "-v", "error", "-y", "-i", pv, "-i", MASTER, "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(OUT / (NAME + " - REVIEW 540p.mp4"))], check=True)
    print("picture done:", out)


PROOF_T = (8.2, 9.6, 21.0, 33.0, 35.5, 37.0, 50.5, 57.2, 76.5, 82.5, 101.0, 126.5, 137.0, 155.5, 166.0, 181.0, 196.5, 198.5, 215.5, 230.0, 239.0, 243.5)


def proof():
    """The grade and the zoom, proven against his master on plain talking frames across the whole film."""
    out = str(OUT / (NAME + ".mp4"))
    rows, tiles = [], []
    for t in PROOF_T:
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
    for k in range(0, len(tiles), 6):
        sheet = np.concatenate([np.asarray(Image.fromarray(x).resize((1920, 540))) for x in tiles[k:k + 6]], axis=0)
        Image.fromarray(sheet).save(OUT / f"grade_proof_{k // 6 + 1}.jpg", quality=88)
    for r in rows:
        print(r)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["all"]):
        for fn in (["graphics", "picture", "proof"] if step == "all" else [step]):
            globals()[fn]()
