#!/usr/bin/env python3
"""RA-07 round 4: the clips of the injury run, conformed to beats_r4.json, 1080x1920 at 29.97, with the AI-GENERATED chip.
G1 (gym closed) and O1 (leg press out of order) are NEW AI clips whose frames wait for Dan's yes: no file, a labelled placeholder
in the film. I5 is round 3's file, unchanged (same slot).

  python3 s75r4_clips.py [A1 M1 H2]      -> round4/clips/<ID>.mp4 + round4/clips/clips.json

A1 is library clip A0179 (RA-04's finished clip) in two pieces joined by the clip's own scene change: frames 0-33 (he walks into the gym
toward the rack) and 102-128 (the leg press), source frame numbers. The clip is already sped 1.249x by RA-04:
it plays at its own rate, never stretched or held. Source frame N is seeked at (N - 0.5) / 29.97 s (an input seek half a frame
early lands on exactly N, RA-14 round 2 lesson 4).
Chip: placed by the person mask over each piece's first, middle and last frames (ra01lib.place_chip), never at a fixed corner.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB

A = L.Aspect("9x16"); FPS = L.FPS; VW, VH = A.VW, A.VH
PL = json.load(open(os.environ.get("PLAN", "beats_r4.json")))
OUT = "round4/clips"; os.makedirs(OUT, exist_ok=True)
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips"
MO = "round2/motion"; M3 = "round3/motion"
A0179 = f"{LIB}/concepts-and-gags/A0179_man-broken-arm-squat-rack-then-leg-press-phone_9x16_4s.mp4"
HALF = lambda n: round((n - 0.5) / 29.97, 4)
SRC = {
 "A1":  dict(file=A0179, why="library clip A0179, two pieces joined by its own scene change", pieces=[
             dict(t_in=0.0167, start_frame=0, frames=34, why="frames 0-33: he walks into the gym toward the squat rack in his cast and sling, an unimpressed look (frames 32-67 and 8-43 failed the take review: no head shake, a hand in his pocket pulling out a smeared phone, then his arm rising to his hip from frame 35; this window ends before all three; clipcheck and review on frames 0-34, one frame wider)"),
             dict(t_in=3.3667, start_frame=101, frames=28, why="frames 101-128: the leg press, from the shot's first frame (the clip's scene change is between frames 100 and 101) to the clip's last (clipcheck and review on frames 102-128; frame 101 is the same shot, 1.0 mean change to 102)")]),
 "M1":  dict(file=f"{LIB}/gym-and-exercise/A0039_man-living-room-dumbbell-curls-beginner_16x9_5s.mp4", t_in=1.0, cx_frac=0.5,
             why="round 2's in-point; the slot is now 39.81-41.01 ('one day,' and the pause), 1.20 s",
             chip_xy=(646, 200), chip_anchor="lt", chip_size=15,
             chip_why="right of his head: the person mask over every 3rd frame spans x 331-615 at rows 150-300 and his arms sweep x 146-983 below; size 15 (289 px) fits the 30 px clear gap (the R3 watch judge found the corner spot on his cheek)"),
 "H2":  dict(file="round3/motion/I4bW_v1.mp4", t_in=1.17,
             why="round 3's reviewed take (I4bW_v1, PASS for source frames 22-67) from 1.17 s, 48 frames: he pulls the towel off, tosses it onto the machine, grips the handle and lifts a knee to step on; ends at 2.77 s, before the take's baked cut at 2.896 s and before the ghosted shoe of frames 69-70",
             chip_xy=(600, 1285), chip_anchor="lt", chip_size=18,
             chip_why="low right, beside his legs and above the captions (round 3's spot from the person mask over every 2nd frame)"),
}
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
        masks = [L.person_mask(frame_at(s["file"], s["t_in"] + f * dur, pre)) for f in (0.02, 0.5, 0.85)]
        (x, y), where = L.place_chip(masks, cwh, A, box=A.CHIP_BOX)
        SB.disclosure(chip, "AI-GENERATED", xy=(x - bb[0], y - bb[1]))
    chip_png = out[:-4] + "_chip.png"; chip.save(chip_png)
    sharp = "unsharp=5:5:0.55:5:5:0" if min(w, h) < 1080 else "null"      # a 1080x1920 library clip was upscaled once already
    trim = f"trim=start_frame={s['start_frame']}:end_frame={s['start_frame'] + n},setpts=PTS-STARTPTS," if s.get("start_frame") is not None else ""
    seek = [] if trim else ["-ss", f"{s['t_in']:.4f}"]
    fc = (f"[0:v]{trim}fps=30000/1001,{pre}scale={VW}:{VH}:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=rgb24,"
          f"{sharp}[v];[1:v]format=rgba[c];[v][c]overlay=0:0:format=rgb,"
          f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[o]")
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error"] + seek + ["-i", s["file"], "-i", chip_png,
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
