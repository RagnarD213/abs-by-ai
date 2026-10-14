#!/usr/bin/env python3
"""RA-07 round 2: every full-screen clip conformed to its slot, 1080x1920 at 29.97, with its AI-GENERATED chip.

  python3 s75_clips.py [H1 M1 I2 I3a I5]      -> round2/clips/<ID>.mp4 + round2/clips/clips.json

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
PL = json.load(open(os.environ.get("PLAN", "beats_r2.json")))
OUT = "round2/clips"; os.makedirs(OUT, exist_ok=True)
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips"
MO = "round2/motion"
SRC = {
 "H1":  dict(file=f"{LIB}/concepts-and-gags/A0147_robot-spots-bench-press-fired-trainer-walks-out-9x16_9x16_4s.mp4", t_in=0.0,
             chip_xy=(VW//2, 1262), chip_anchor="mt", why="the clip from its first frame; chip on the empty floor (round 1 spot)"),
 "M1":  dict(file=f"{LIB}/gym-and-exercise/A0039_man-living-room-dumbbell-curls-beginner_16x9_5s.mp4", t_in=1.0, cx_frac=0.5,
             why="848x480 original, full height kept, sides cropped on him (VIDEO-RULES 2026-10-02)"),
 "I2":  dict(file=f"{MO}/I2_v3.mp4", t_in=0.0, chip_xy=(940, 214), chip_anchor="rt",   # mask search found no clear band (put it on the trainer's head); the wall above the clients is clear
             why="take 3: hands the sheet, all three read identical sheets, he turns away; from its first frame to 2.67 s (the reviewer saw a loose sheet appear at his hip at 2.9-3.07 s and the stack go soft after about 2.4 s; both cut)"),
 "I3a": dict(file=f"{MO}/I3a_v1.mp4", t_in=0.0,
             why="take 1 from its first frame: press, wince, the dumbbell lowered in his hand, the grip on the shoulder lands on 'injured'"),
 "I5":  dict(file=f"{MO}/I5_v1.mp4", t_in=1.94,
             why="take 1's last 2.1 s: he reads BACK NEXT WEEK, turns and shrugs on 'until next week' (its first 2 s, the knock then a long pause, do not fit the slot)"),
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
for cid in [c for c in SRC if c in ONLY]:
    s = SRC[cid]; n = CB[cid]["frames"]; dur = n / FPS
    w, h, r = probe(s["file"])
    pre = vf_fill(w, h, s.get("cx_frac", 0.5))
    chip = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    if "chip_xy" in s:
        SB.disclosure(chip, "AI-GENERATED", xy=s["chip_xy"], anchor=s["chip_anchor"]); where = "fixed: " + s["why"]
    else:
        probe_im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); SB.disclosure(probe_im, "AI-GENERATED", xy=(0, 0))
        bb = probe_im.getbbox(); cwh = (bb[2] - bb[0], bb[3] - bb[1])
        masks = [L.person_mask(frame_at(s["file"], s["t_in"] + f * dur, pre)) for f in (0.02, 0.5, 0.97)]
        (x, y), where = L.place_chip(masks, cwh, A, box=A.CHIP_BOX)
        SB.disclosure(chip, "AI-GENERATED", xy=(x - bb[0], y - bb[1]))
    chip.save(f"{OUT}/{cid}_chip.png")
    out = f"{OUT}/{cid}.mp4"
    fc = (f"[0:v]fps=30000/1001,{pre}scale={VW}:{VH}:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=rgb24,"
          f"unsharp=5:5:0.55:5:5:0[v];[1:v]format=rgba[c];[v][c]overlay=0:0:format=rgb,"
          f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[o]")
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s['t_in']:.4f}", "-i", s["file"], "-i", f"{OUT}/{cid}_chip.png",
                    "-filter_complex", fc, "-map", "[o]", "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                    "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                    "-x264-params", "keyint=30:min-keyint=1:scenecut=0", out], check=True)
    got = int(subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
    assert got == n, (cid, got, n, "the source ran out before the slot: never hold a clip")
    meta[cid] = dict(src=s["file"], src_size=[w, h], src_rate=r, t_in=s["t_in"], t_out=round(s["t_in"] + dur * float(eval(r)) / float(eval(r)), 3),
                     frames=n, slot=CB[cid]["beat"], chip=where, why=s["why"], upscale="lanczos + unsharp 0.55 (Real-ESRGAN not installed)")
    print(cid, n, "frames", where, flush=True)
json.dump(meta, open(f"{OUT}/clips.json", "w"), indent=1)
