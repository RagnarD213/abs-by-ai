#!/usr/bin/env python3
"""RA-07 round 3: the clips whose slot moved (I3a, M1, I5) and the new ones (I4a, I4b, I3b), conformed to beats_r3.json, 1080x1920
at 29.97, with the AI-GENERATED chip. H1 and I2 are round 2's files, unchanged (same slots).

  python3 s75r3_clips.py [I3a M1 I5 I4a I4b I3b]      -> round3/clips/<ID>.mp4 + round3/clips/clips.json

I3b is two single-image takes joined by a cut (handoff: "he changes place"): piece A = the phone and the nod, piece B = the
lateral raise. Each piece is conformed alone, then the two are joined frame-exactly.

Each clip plays at its own speed from an in-point chosen by watching it (never stretched or held). The 24 fps sources
are conformed with fps=30000/1001. Upscale: Lanczos plus a light unsharp. Real-ESRGAN (handoff step 6) is not installed
on this Mac and the only other A0147 copy (Ad 13's assets_sbl/opener_motion_9x16.mp4) is slowed to 4.54 s, so neither
was usable. The chip is placed by the person mask over the clip's first, middle and last frames (ra01lib.place_chip),
never at a fixed corner (RA-07 round 1 lesson 7); H1 keeps round 1's spot on the empty floor, which Dan has seen.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB

A = L.Aspect("9x16"); FPS = L.FPS; VW, VH = A.VW, A.VH
PL = json.load(open(os.environ.get("PLAN", "beats_r3.json")))
OUT = "round3/clips"; os.makedirs(OUT, exist_ok=True)
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips"
MO = "round2/motion"; M3 = "round3/motion"
SRC = {
 "M1":  dict(file=f"{LIB}/gym-and-exercise/A0039_man-living-room-dumbbell-curls-beginner_16x9_5s.mp4", t_in=1.0, cx_frac=0.5,
             why="round 2's in-point; the slot is now 39.21-40.44 ('it to the gym one day,'), 1.23 s",
             chip_xy=(646, 200), chip_anchor="lt", chip_size=15,
             chip_why="right of his head: the person mask over every 3rd frame spans x 331-615 at rows 150-300 and his arms sweep x 146-983 below; size 15 (289 px) fits the 30 px clear gap (the R3 watch judge found the corner spot on his cheek)"),
 "I2":  dict(file=f"{MO}/I2_v3.mp4", t_in=0.375, chip_xy=(940, 214), chip_anchor="rt",
             why="take 3, source frames 9-44 (1.47 s): its frames 0-8 carry a phantom shoe and its paper stack turns cloth-like from frame 48 (take reviews I2_v3.f0-45, f0-64)"),
 "I3a": dict(file=f"{MO}/I3a_v1.mp4", t_in=0.55,
             why="take 1 from 0.55 s: arm still up, the wince, the dumbbell lowered in his hand, the grip on the shoulder lands in the slot's last 0.2 s"),
 "I5":  dict(file=f"{MO}/I5_v1.mp4", t_in=1.03,
             why="take 1 from 1.03 s to its end: he reads BACK NEXT WEEK, turns and shrugs on 'confused until next week'",
             chip_xy=(600, 200), chip_anchor="lt", chip_size=18,
             chip_why="above the sign, right of his head (person x 60-564 at rows 150-300); the corner spot touched his hair at 45.0 s"),
}
for _k, _f in json.load(open(f"{M3}/picks.json")).items() if os.path.exists(f"{M3}/picks.json") else []:
    SRC[_k] = _f
ONLY = set(sys.argv[1:]) or set(SRC)
CB = {c["name"]: c for c in PL["cards"]}


def probe(path):
    r = subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate", "-of", "json", path], capture_output=True, text=True, check=True)
    s = json.loads(r.stdout)["streams"][0]; return s["width"], s["height"], s["r_frame_rate"]


def vf_fill(w, h, cx_frac=0.5):
    if w * 16 >= h * 9 + 2:                 # wider than 9:16: keep the full height, crop the sides on the subject
        cw = int(round(h * 9 / 16)) // 2 * 2; x0 = int(round(w * cx_frac - cw / 2)); x0 = max(0, min(w - cw, x0)) // 2 * 2
        return f"crop={cw}:{h}:{x0}:0,"
    return ""


def frame_at(path, t, pre):
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t:.4f}", "-i", path, "-frames:v", "1", "-vf",
                          f"{pre}scale={VW}:{VH}:flags=lanczos:in_color_matrix=bt709:in_range=tv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return Image.frombuffer("RGB", (VW, VH), raw, "raw", "RGB", 0, 1)


meta = json.load(open(f"{OUT}/clips.json")) if os.path.exists(f"{OUT}/clips.json") else {}


def pieces(cid):
    s = SRC[cid]
    if "pieces" in s:
        return [dict(s, **p) for p in s["pieces"]]
    return [dict(s, frames=CB[cid]["frames"])]


def conform(cid, s, n, out):
    """One source span -> exactly n frames at 29.97 with its chip; returns (where the chip went, source size, rate)."""
    dur = n / FPS
    w, h, r = probe(s["file"])
    pre = vf_fill(w, h, s.get("cx_frac", 0.5))
    chip = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    if s.get("chip_xy"):
        SB.disclosure(chip, "AI-GENERATED", xy=tuple(s["chip_xy"]), anchor=s.get("chip_anchor", "mt"), size=s.get("chip_size", 23)); where = "fixed: " + s.get("chip_why", s["why"])
    else:
        probe_im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); SB.disclosure(probe_im, "AI-GENERATED", xy=(0, 0))
        bb = probe_im.getbbox(); cwh = (bb[2] - bb[0], bb[3] - bb[1])
        masks = [L.person_mask(frame_at(s["file"], s["t_in"] + f * dur, pre)) for f in (0.02, 0.5, 0.97)]
        (x, y), where = L.place_chip(masks, cwh, A, box=A.CHIP_BOX)
        SB.disclosure(chip, "AI-GENERATED", xy=(x - bb[0], y - bb[1]))
    chip_png = out[:-4] + "_chip.png"; chip.save(chip_png)
    fc = (f"[0:v]fps=30000/1001,{pre}scale={VW}:{VH}:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=rgb24,"
          f"unsharp=5:5:0.55:5:5:0[v];[1:v]format=rgba[c];[v][c]overlay=0:0:format=rgb,"
          f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[o]")
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s['t_in']:.4f}", "-i", s["file"], "-i", chip_png,
                    "-filter_complex", fc, "-map", "[o]", "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                    "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                    "-x264-params", "keyint=30:min-keyint=1:scenecut=0", out], check=True)
    got = int(subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
    assert got == n, (cid, got, n, "the source ran out before the slot: never hold a clip")
    return where, [w, h], r


for cid in [c for c in SRC if c in ONLY]:
    ps = pieces(cid); out = f"{OUT}/{cid}.mp4"
    assert sum(p["frames"] for p in ps) == CB[cid]["frames"], (cid, [p["frames"] for p in ps], CB[cid]["frames"])
    rec = []
    for i, p in enumerate(ps):
        po = out if len(ps) == 1 else f"{OUT}/{cid}_p{i}.mp4"
        where, wh, r = conform(cid, p, p["frames"], po)
        rec.append(dict(src=p["file"], src_size=wh, src_rate=r, t_in=p["t_in"], t_out=round(p["t_in"] + p["frames"] / FPS, 3),
                        frames=p["frames"], chip=where, why=p["why"]))
    if len(ps) > 1:      # a straight cut between the pieces: decode both, re-encode once with the same settings
        lst = f"{OUT}/{cid}_concat.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(f'{OUT}/{cid}_p{i}.mp4')}'\n" for i in range(len(ps))))
        subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-preset", "medium",
                        "-crf", "15", "-r", "30000/1001", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0", out], check=True)
        got = int(subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
        assert got == CB[cid]["frames"], (cid, got)
    meta[cid] = dict(pieces=rec, frames=CB[cid]["frames"], slot=CB[cid]["beat"], upscale="lanczos + unsharp 0.55 (Real-ESRGAN not installed)")
    print(cid, CB[cid]["frames"], "frames", [x["chip"] for x in rec], flush=True)
json.dump(meta, open(f"{OUT}/clips.json", "w"), indent=1)
