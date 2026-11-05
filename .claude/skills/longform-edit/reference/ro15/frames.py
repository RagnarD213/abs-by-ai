"""Graded frames on the RO-15 output timeline. ONE ROLL: C1709 (9/23 studio set, Sony FX30 4K 29.97p S-Cinetone).
 Locked studio look reused from WV-01 (same 9/23 set, Dan-approved), as on RO-10 to RO-18:
Color C (grade-C.cube), W2 crop 3552x1998@144,162, T2 crop 2608x1466@616,184, BT.709 decode.
GRADES: the round-1 colour options (look C is the baseline; B and D vary one property on it)."""
import json, subprocess, os, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/RO-15/round1"; FPS = 30000/1001
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RD = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content"
C1709 = f"{RD}/C1709.MP4"
ROLLS = {"C1709": dict(path=C1709, f0=0)}          # the edit sheet writer reads this
def roll_of(f): return (C1709, f)
def roll_t(ts): return (C1709, ts)
LUT = "/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube"
# round-1 colour options: the locked look C, then one property varied on it (VIDEO-RULES 2026-10-16: vary a useful property)
GRADES = {"C": "", "C-rich": ",eq=saturation=1.12:contrast=1.03", "C-bright": ",eq=brightness=0.025:gamma=1.06"}
GRADE = os.environ.get("RO15_GRADE", "C")
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W4": (2800, 1575, 520, 183),
        "W4S": (2690, 1513, 110, 183)}   # W4S: W4 slid left (side cards only); RO-17 measured the backdrop edge on this set
CROP_Y = json.load(open(f"{W}/framing/crop_y.json")) if os.path.exists(f"{W}/framing/crop_y.json") else {}
def crop(framing, shot=None):
    """The locked crop, lifted for one shot only where his hair top would sit under 4 % of the crop height (framing standard;
    measured every 0.5 s on the source by hair_pre.py). Never lowered."""
    cw, ch, x, y = CROP[framing]
    if shot and framing in CROP_Y.get(shot, {}): y = min(y, CROP_Y[shot][framing])
    return (cw, ch, x, y)
def vf(framing, shot=None, grade=None):
    cw, ch, x, y = crop(framing, shot); g = GRADES[grade or GRADE]
    return (f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,"
            f"format=gbrpf32le,lut3d=file='{LUT}':interp=tetrahedral,format=rgb24{g}")
S = json.load(open(f"{W}/shots.json")) if os.path.exists(f"{W}/shots.json") else []
def shot_at(t):
    f = int(round(t*FPS))
    return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def src_time(t):
    s = shot_at(t); return (s["src_f0"] + int(round(t*FPS)) - s["out_f0"])/FPS, s
def frame_src(ts, framing, shot=None, grade=None):
    src, ts = roll_t(ts)
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", src, "-ss", f"{min(1, ts):.4f}", "-frames:v", "1",
                        "-vf", vf(framing, shot, grade), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing=None):
    ts, s = src_time(t); return frame_src(ts, framing or s["framing"], s["id"])
