#!/usr/bin/env python3
"""RA-05 round 3: the couch clip from Dan's approved START and END frames (2026-10-14), two Veo 3.1 Fast takes joined by a CUT.
  shot A  motion/A2_locked.mp4 (take A2, phone picture held still by lockscreen.py): he holds the phone toward the camera, tilts it a
          little closer, settles into a half smile. Film 3.47 -> cut_at.
  shot B  motion/B5_locked.mp4 (take B5, locked the same way): shirtless, phone beside his abs, grins with a proud tilt of the head.
          cut_at -> 7.91.
Natural speed (24 -> 29.97 by frame repeat), never slowed or held. AI-GENERATED chip on both, clear of the face (measured).
usage: s06_couch3.py [still]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH)
import softblue as SB
FF = SB.FF; FPSS = "30000/1001"; W, H = 1080, 1920
B = json.load(open("beats.json")); c = next(x for x in B["cards"] if x["name"] == "couch")
n = c["frames"]; k = int(round((c["cut_at"] - c["beat"][0]) * 30000 / 1001))
SHOTS = [("motion/A2_locked.mp4", 0.0, k), ("motion/B5_locked.mp4", 0.0, n - k)]
CHIP = {0: json.loads(os.environ.get("CHIP_A", "[40, 96]")), 1: json.loads(os.environ.get("CHIP_B", "[40, 96]"))}
for p, t0, nf in SHOTS:
    assert t0 + nf * 1001 / 30000 <= 2.5 + 1e-6, (p, "the take would run out: never hold or slow it")
ch, ins = [], []
for i, (p, t0, nf) in enumerate(SHOTS):
    ins += ["-ss", f"{t0:.3f}", "-i", p]
    ch.append(f"[{i}:v]fps={FPSS},trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]")
ch.append("[v0][v1]concat=n=2:v=1:a=0[v]")
os.makedirs("media", exist_ok=True)
subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n),
                "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-color_range", "tv", "media/couch.mp4"], check=True)
rd = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", "media/couch.mp4", "-vf",
                       "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
still = len(sys.argv) > 1 and sys.argv[1] == "still"
if not still:
    e = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", FPSS, "-i", "-",
                          "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                          "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                          "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0", "cards_9x16/couch.mp4"], stdin=subprocess.PIPE)
boxes = {}
for g in range(n):
    b = rd.stdout.read(W * H * 3); assert len(b) == W * H * 3, g
    im = Image.fromarray(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()); s = 0 if g < k else 1
    boxes[s] = SB.disclosure(im, "AI-GENERATED", tuple(CHIP[s]), size=20)
    if still and g in (0, k - 1, k, n - 1): im.save(f"motion/couch_still_{g}.png")
    if not still: e.stdin.write(np.ascontiguousarray(np.asarray(im)).tobytes())
rd.wait()
if not still:
    e.stdin.close(); assert e.wait() == 0
    meta = json.load(open("cards_9x16/meta.json"))
    meta["couch"] = {"shots": [{"take": p, "src_in": t0, "frames": nf} for p, t0, nf in SHOTS], "cut_frame": k,
                     "chip": "AI-GENERATED", "chip_box": {str(s_): [round(v) for v in bx] for s_, bx in boxes.items()}}
    json.dump(meta, open("cards_9x16/meta.json", "w"), indent=1)
print("couch", n, "frames, cut at", k, "chip boxes", boxes)
