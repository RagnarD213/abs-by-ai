#!/usr/bin/env python3
"""Overlay pass v3: J2 chips + watermark + soup split-screen insert + the two
Ultimate-Home-Workout placeholders + the v3 inserts (Oura / WHOOP product cards,
the SUPPLEMENTS card over the recut supplements joint, and the Bryan Johnson
PiP window with its attribution), over the finished graded cut.
Every insert is keyed by SOURCE time and mapped through edl.json, so a re-cut
only needs this script re-run. One encode at CRF 18, audio copied."""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RC = HERE.parent / "roughcuts"
SRC = RC / (sys.argv[1] if len(sys.argv) > 1 else "CUT_v3_graded.mp4")
OUT = RC / (sys.argv[2] if len(sys.argv) > 2 else "INVEST_HEALTH_v3.mp4")
G = HERE / "gfx"
FADE = 0.35
FPS = "30000/1001"

edl = json.load(open(HERE / "edl.json"))
ranges = edl["ranges"]
def src_to_out(t):
    off = 0.0
    for r in ranges:
        d = round(r["end"] - r["start"], 3)
        if r["start"] <= t < r["end"]:
            return round(off + (t - r["start"]), 2)
        off = round(off + d, 3)
    return None

# ---- soup split-screen insert (video overlay, built from the cut itself) ----
SOUP_SRC_T = 1531.2; SOUP_DUR = 6.0
w0 = src_to_out(SOUP_SRC_T)
soup_split = G / "soup_split.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y",
    "-ss", f"{w0:.2f}", "-t", f"{SOUP_DUR:.2f}", "-i", str(SRC),
    "-i", str(G / "soup_column.mp4"),
    "-filter_complex",
    "[0:v]crop=1350:1080:285:0[cam];[1:v][cam]hstack[v]",
    "-map", "[v]", "-an", "-r", FPS,
    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
    str(soup_split)], check=True)
print(f"soup split-screen built at out {w0:.2f}s")

# ---- overlay table ----
chips = json.load(open(HERE / "chip_timings.json"))
# kind: img_fade (full-frame RGBA) | video (full-frame) | video_pip (placed)
overlays = []   # (path, start, end, kind, xy)
for c in chips:
    overlays.append((G / f"chip_{c['key']}.png", c["start"], c["end"], "img_fade", None))
PH_CORNER_T = src_to_out(1857.1); overlays.append((G / "ph_corner.png", PH_CORNER_T, PH_CORNER_T + 10.0, "img_fade", None))
PH_FULL_A = src_to_out(1890.5); PH_FULL_B = src_to_out(1902.5)
overlays.append((G / "ph_fullscreen.png", PH_FULL_A, PH_FULL_B, "img_fade", None))
overlays.append((soup_split, w0, w0 + SOUP_DUR, "video", None))

# ---- v3 inserts, all keyed by SOURCE time so a re-cut carries them ----
# 4b: product cards beside him as he names each tracker.
OURA_T = src_to_out(2669.3)                 # "...I personally wear the Oura ring"
overlays.append((G / "prod_oura.png", OURA_T, OURA_T + 5.5, "img_fade", None))
WHOOP_T = src_to_out(2717.0)                # "The Whoop is a thin wearable"
overlays.append((G / "prod_whoop.png", WHOOP_T, WHOOP_T + 5.5, "img_fade", None))
# 5: SUPPLEMENTS card across the recut joint (src 3058.20 -> 3062.38 removed);
# anchored on the last kept word before the cut so it spans the join.
SUPP_T = max(0.0, src_to_out(3057.6) - 0.6)
overlays.append((G / "supp_card.png", SUPP_T, SUPP_T + 3.2, "img_fade", None))
# 6: Bryan Johnson b-roll PiP + attribution frame, over "...dedicated to this
# idea of living forever". 7.8s, viewer-left, 600x338 at 60,330.
BJ_T = src_to_out(3800.4)
BJ_DUR = 7.8
overlays.append((G / "bj_insert.mp4", BJ_T, BJ_T + BJ_DUR, "video_pip", (60, 330)))
overlays.append((G / "bj_frame.png", BJ_T - 0.2, BJ_T + BJ_DUR + 0.2, "img_fade", None))

for path, a, b, kind, xy in overlays:
    assert a is not None and b is not None, f"overlay {path.name}: source time not inside a kept range"
overlays.sort(key=lambda o: o[1])

cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(SRC)]
for path, a, b, kind, xy in overlays:
    if kind in ("video", "video_pip"):
        cmd += ["-i", str(path)]
    else:
        cmd += ["-loop", "1", "-framerate", FPS, "-t", f"{b-a:.2f}", "-i", str(path)]
cmd += ["-loop", "1", "-framerate", FPS, "-i", str(G / "wm.png")]

parts = []; last = "0:v"
for i, (path, a, b, kind, xy) in enumerate(overlays, start=1):
    dur = b - a
    pos = "0:0"
    if kind in ("video", "video_pip"):
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS+{a}/TB[c{i}]")
        if kind == "video_pip":
            pos = f"{xy[0]}:{xy[1]}"
    else:
        parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                     f"fade=t=out:st={dur-FADE:.2f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    parts.append(f"[{last}][c{i}]overlay={pos}:enable='between(t,{a},{b})'[v{i}]")
    last = f"v{i}"
wm = len(overlays) + 1
parts.append(f"[{last}][{wm}:v]overlay=0:0:shortest=1[vout]")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode)
print(r.stderr[-1500:] if r.returncode else f"OK -> {OUT}")
