"""Graded frames on the RO-28 output timeline. ONE ROLL: C1771 (10/15 studio set, dark green backdrop, two cyan tubes, desk).
Sony FX30 4K 29.97p S-Cinetone, decoded as BT.709. Grade: the recommended round-1 colour (options/colour; GRADE below is the
provisional pick, "Rich Balanced", the grade of the approved RO-25 film on this set). Crops: W (wide, hair -> desk) and
T (tight, hair -> chest), sizes 1.31x apart (RO-25's approved sizes); the y of each is set per shot from the measured hair
top (hair_pre.py -> crop_y.json: 4 % of the crop height above the highest hair in the shot, never lower)."""
import json, os, subprocess
from PIL import Image
W = "/Volumes/Expansion/_edit_work/ro28/round1"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RD = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop"
C1771 = f"{RD}/C1771.MP4"; OFF_F = 10**9; OFF = OFF_F/FPS
def roll_of(f): return (C1771, f)
def roll_t(ts): return (C1771, ts)
GRADES = {
    "A": "eq=gamma=1.20:brightness=0.01:contrast=1.10:saturation=1.05,eq=contrast=1.03:brightness=-0.006:saturation=1.22",  # Rich Balanced (RO-25 approved film)
    "B": "eq=contrast=1.045:brightness=0.012:saturation=1.17",                                                                # Richer Colour (RO-27 pick, darker)
    "C": "eq=gamma=1.20:brightness=0.01:contrast=1.10:saturation=1.05,eq=contrast=1.03:brightness=-0.006:saturation=1.22,colorbalance=rs=.025:gs=.003:bs=-.018",  # A, warmer skin
}
GRADE_KEY = os.environ.get("RO28_GRADE", "A")
GRADE = GRADES[GRADE_KEY]
LUT = GRADE                                    # kept under this name: build.py's segment cache key carries it
CROP = json.load(open(f"{W}/framing/crops.json")) if os.path.exists(f"{W}/framing/crops.json") else \
       {"W2": [3552, 1998, 144, 30], "T2": [2704, 1521, 568, 50], "W4S": [2690, 1513, 0, 30], "W4": [2690, 1513, 0, 30]}
CROP = {k: tuple(v) for k, v in CROP.items()}
CROP_Y = json.load(open(f"{W}/framing/crop_y.json")) if os.path.exists(f"{W}/framing/crop_y.json") else {}
def crop(framing, shot=None):
    cw, ch, x, y = CROP[framing]
    if shot and framing in CROP_Y.get(shot, {}): y = min(y, CROP_Y[shot][framing])
    return (cw, ch, x, y)
def vf(framing, shot=None):
    cw, ch, x, y = crop(framing, shot)
    return (f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,"
            f"{GRADE},format=rgb24")
S = json.load(open(f"{W}/shots.json")) if os.path.exists(f"{W}/shots.json") else []
def shot_at(t):
    f = int(round(t*FPS))
    return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def src_time(t):
    s = shot_at(t); return (s["src_f0"] + int(round(t*FPS)) - s["out_f0"])/FPS, s
def frame_src(ts, framing, shot=None):
    src, ts = roll_t(ts)
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", src, "-ss", f"{min(1, ts):.4f}", "-frames:v", "1",
                        "-vf", vf(framing, shot), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing=None):
    ts, s = src_time(t); return frame_src(ts, framing or s["framing"], s["id"])
