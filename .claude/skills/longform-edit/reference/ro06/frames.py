"""Graded frames on the RO-06 output timeline (25 rolls on one global source timeline, mkglobal.py).
Three fixed sizes per shot (shot_framing.json): W = the camera frame as shot; T = the medium punch-in (1.5x on the wide
rolls, hair to mid-thigh; 1.3x on the closer rolls); X = Dan's tight shot (round 2: just above the hair to a little below
the shorts line, about 2x on the wide rolls). Top edge on the hair, fixed for the whole shot. Grade = the roll's skin-anchored curve (grades.json), option LOOK. Decode BT.709 (rolls are tagged)."""
import json, subprocess, os
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
ROLLS = json.load(open(f"{W}/rolls.json")); GR = json.load(open(f"{W}/grades.json"))
LOOK = open(f"{W}/look_option.txt").read().strip() if os.path.exists(f"{W}/look_option.txt") else "B"
S = json.load(open(f"{W}/shots.json")); SF = json.load(open(f"{W}/shot_framing.json"))
def roll_of(src_f):
    for r, v in ROLLS.items():
        if v["f0"] <= src_f < v["f0"]+v["n"]: return r, src_f-v["f0"]
    raise ValueError(src_f)
def crop_of(shot_id, framing):
    if framing == "W": return (1920, 1080, 0, 0)
    return tuple(SF[shot_id]["T2" if framing == "X" else "T"])
def vf(roll, crop, look=None):
    cw, ch, x, y = crop
    c = "" if (cw, ch) == (1920, 1080) else f"crop={cw}:{ch}:{x}:{y},"
    return (f"{c}scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrp,"
            f"{GR[roll][look or LOOK]},format=rgb24")
def shot_at(t):
    f = int(round(t*FPS)); return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def src_frame(t):
    s = shot_at(t); return s["src_f0"] + int(round(t*FPS)) - s["out_f0"], s
def frame_src(src_f, shot_id, framing, look=None, raw=False, crop=None):
    roll, lf = roll_of(src_f); ts = lf/FPS
    v = vf(roll, crop or crop_of(shot_id, framing), look)
    if raw: v = v.replace(GR[roll][look or LOOK] + ",", "")
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", ROLLS[roll]["path"], "-ss", f"{max(0, min(1, ts)-0.4/FPS):.4f}", "-frames:v", "1",
                        "-vf", v, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing=None, look=None, raw=False):
    sf, s = src_frame(t); return frame_src(sf, s["id"], framing or s["framing"], look, raw)
