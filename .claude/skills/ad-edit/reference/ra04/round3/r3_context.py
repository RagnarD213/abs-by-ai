#!/usr/bin/env python3
"""RA-04 round 3: the AI broken-arm clip IN CONTEXT, 0:35.5-0:45.5, built the way s10_render04.py builds the film: the round 2 base
timeline (Dan segments + cards, no overlays) with the new brokenarm card on its frames (1173-1301), the Soft Blue overlays from
hf9/manifest.json (LT3 now ends at 39.139), then the rebuilt caption MOV on top, with the round 2 mix (picture length unchanged).
Not rebuilt for this preview: the Dan hold before the clip (dan08) keeps its round 2 crop, whose centre the shorter hold moves by
10 source px (5 delivered px); the full-film round re-renders it.  -> round3/context/AI1-context-r3.mp4 (+ REVIEW 540p copy)"""
import json, subprocess, sys
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as CP
W = "/Volumes/Extreme/_edit_work/ra04"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; fr = lambda t: int(round(t*FPS))
B = json.load(open(f"{W}/beats.json")); c = next(x for x in B["cards"] if x["name"] == "brokenarm")
c0 = next(x for x in B["timeline"] if x["name"] == "brokenarm"); C0, CN = c0["f0"], c0["n"]
T0, T1 = 35.5, 45.5; G0, G1 = fr(T0), fr(T1); N = G1 - G0
Cp = CP.Compositor(json.load(open(f"{W}/hf9/manifest.json")), wh=(1080, 1920))
out = f"{W}/round3/context/AI1-context-r3.mp4"
e = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-framerate", "30000/1001", "-i", "-",
                      "-i", f"{W}/cap_9x16/captions.mov", "-ss", f"{G0/FPS:.6f}", "-t", f"{N/FPS:.6f}", "-i", f"{W}/mix_r2.wav",
                      "-filter_complex", f"[1:v]trim=start_frame={G0},setpts=PTS-STARTPTS[c];[0:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[b];[b][c]overlay=0:0:format=auto,format=yuv420p[v]",
                      "-map", "[v]", "-map", "2:a", "-frames:v", str(N), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "256k",
                      "-movflags", "+faststart", out], stdin=subprocess.PIPE)
card = CP.reader(f"{W}/cards_9x16/brokenarm.mp4", 0, CN, False, (1080, 1920))
for k, f in enumerate(CP.reader(f"{W}/seg_9x16/base.mp4", G0, N, False, (1080, 1920))):
    g = G0 + k
    if C0 <= g < C0 + CN: f = next(card)
    e.stdin.write(np.ascontiguousarray(Cp.apply(f, g)).tobytes())
e.stdin.close(); assert e.wait() == 0
subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", out, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "20", "-preset", "slow",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "copy", "-movflags", "+faststart",
                f"{W}/round3/context/AI1 broken arm in context 0-35 to 0-45 - REVIEW 540p.mp4"], check=True)
print(out, N, "frames; the clip is context frames", C0 - G0, "to", C0 - G0 + CN - 1, f"({C0/FPS:.3f}-{(C0+CN)/FPS:.3f} s in the ad)"); print("CONTEXT_R3_DONE")
