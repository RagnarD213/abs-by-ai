"""Graded frames on the RO-16 output timeline. Locked studio look reused from WV-01 (same 9/23 set, Dan-approved):
Color C (grade-C.cube), W2 crop 3552x1998@144,162, T2 crop 2608x1466@616,184, BT.709 decode."""
import json, subprocess, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro16"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1710.MP4"
LUT = "/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube"
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W3": (3120, 1755, 360, 172)}   # W3: in-between size, only under side cards
def vf(framing):
    cw, ch, x, y = CROP[framing]
    return (f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,"
            f"format=gbrpf32le,lut3d=file='{LUT}':interp=tetrahedral,format=rgb24")
S = json.load(open(f"{W}/shots.json"))
def shot_at(t):
    f = int(round(t*FPS))
    return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def src_time(t):
    s = shot_at(t); return (s["src_f0"] + int(round(t*FPS)) - s["out_f0"])/FPS, s
def frame_src(ts, framing):
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", SRC, "-ss", f"{min(1, ts):.4f}", "-frames:v", "1",
                        "-vf", vf(framing), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing=None):
    ts, s = src_time(t); return frame_src(ts, framing or s["framing"])
