"""Graded frames on the RO-17 output timeline. Locked studio look reused from WV-01 (same 9/23 set, Dan-approved):
Color C (grade-C.cube), W2 crop 3552x1998@144,162, T2 crop 2608x1466@616,184, BT.709 decode."""
import json, subprocess, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/RO-17/round2"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1713.MP4"
LUT = "/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube"
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W3": (3120, 1755, 360, 172),   # W3: in-between size (retired round 2: only 1.14x W2, read as a jump cut under G20)
        "W4": (2800, 1575, 520, 183),
        "W4S": (2690, 1513, 110, 183)}  # RO-17: 4 % in from the 4K frame's left edge so the backdrop's edge (two orange clamps, a wall strip) never shows; side-card clearance 127-178 px before, about 90 after  # W4S: W4 slid left 520 px (all the room; the cycle card is 24 px wider than 3A) inside the 4K frame, only under side cards (HyperFrames round 2)  # W4: 1.27x W2, side cards only; hair 50-69 px, body x 517-1460 over s7d.0 (round-2 measure)
import os
CROP_Y = json.load(open(f"{W}/framing/crop_y.json")) if os.path.exists(f"{W}/framing/crop_y.json") else {}
def crop(framing, shot=None):
    """The locked crop, lifted for one shot only where his hair top would sit under 4 % of the crop height (framing standard;
    measured every 0.5 s on the source by hair_pre.py). Never lowered."""
    cw, ch, x, y = CROP[framing]
    if shot and framing in CROP_Y.get(shot, {}): y = min(y, CROP_Y[shot][framing])
    return (cw, ch, x, y)
def vf(framing, shot=None):
    cw, ch, x, y = crop(framing, shot)
    return (f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,"
            f"format=gbrpf32le,lut3d=file='{LUT}':interp=tetrahedral,format=rgb24")
S = json.load(open(f"{W}/shots.json"))
def shot_at(t):
    f = int(round(t*FPS))
    return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def src_time(t):
    s = shot_at(t); return (s["src_f0"] + int(round(t*FPS)) - s["out_f0"])/FPS, s
def frame_src(ts, framing, shot=None):
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", SRC, "-ss", f"{min(1, ts):.4f}", "-frames:v", "1",
                        "-vf", vf(framing, shot), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing=None):
    ts, s = src_time(t); return frame_src(ts, framing or s["framing"], s["id"])

