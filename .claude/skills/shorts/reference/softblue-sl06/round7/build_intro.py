#!/usr/bin/env python3
"""SL-06 R7: turn a chosen Veo take into clips/intro_S.mp4.
  1. fix_take.py (round6/fix): the S intro window (from OFF frames), static restores of text boxes from the approved still
     (labels only; the camera is locked and nothing moves there), no other repair;
  2. C only: the Soft Blue step badges overlay (hf/C_steps.mov, transparent ProRes 4444);
  3. the slow push-in the page showed: 1.00 -> 1.07 about a focus point, through a 2x upscale for sub-pixel smoothness.
  python3 build_intro.py S TAKE.mp4 OFF_FRAMES [--static x0,y0,x1,y1 ...]"""
import json, os, subprocess, sys
R = "/Volumes/Extreme/_edit_work/sl06/round7"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
N = {"A": 99, "B": 111, "C": 68, "E": 76, "F": 60}            # intro frames at 24 fps, as in R5/R6 (the plan cuts F at o1.93)
FOCUS = {"A": (550, 1035), "B": (540, 1030), "C": (540, 820), "E": (500, 1050), "F": (530, 1100)}   # reviewers' notes
PUSH = {"A": 0.03, "B": 0.07, "C": 0.07, "E": 0.03, "F": 0.03}   # Veo already creeps the camera on A, E, F
S, take, off = sys.argv[1], sys.argv[2], int(sys.argv[3])
statics = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--static"]
still = f"{R}/frames/{'E2' if S == 'E' else S}_r7.jpg"; n = N[S]
os.makedirs(f"{R}/intro", exist_ok=True); fixed = f"{R}/intro/{S}_fixed.mp4"; out = f"{R}/intro/{S}_intro.mp4"
if take == "STILL":                       # C: the approved still itself (Veo boiled the mat texture in every take)
    subprocess.run([FF, "-v", "error", "-y", "-loop", "1", "-i", still, "-frames:v", str(n), "-r", "24", "-c:v", "libx264", "-crf", "10",
                    "-pix_fmt", "yuv420p", fixed], check=True)
else:
    cmd = [sys.executable, f"{R}/../round6/fix/fix_take.py", take, still, fixed, "--frames", f"{off}:{off + n - 1}", "--seconds", f"{n / 24}"]
    for b in statics: cmd += ["--static", b]
    cmd += ["--log", f"{R}/intro/{S}_fix.json"]
    subprocess.run(cmd, check=True)
cx, cy = FOCUS[S]
zp = (f"scale=2160:3840:flags=lanczos,zoompan=z='1+{PUSH[S]}*on/{n - 1}':x='min(max({2 * cx}-iw/zoom/2,0),iw-iw/zoom)':"
      f"y='min(max({2 * cy}-ih/zoom/2,0),ih-ih/zoom)':d=1:s=1080x1920:fps=24")
if S == "C":
    fc = f"[1:v]format=yuva444p,setpts=PTS-STARTPTS[g];[0:v][g]overlay=0:0:eof_action=pass,{zp}[v]"
    inputs = ["-i", fixed, "-i", f"{R}/hf/C_steps.mov"]
else:
    fc = f"[0:v]{zp}[v]"; inputs = ["-i", fixed]
subprocess.run([FF, "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n), "-c:v", "libx264",
                "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                "-color_trc", "bt709", "-r", "24", out], check=True)
print("intro", S, out, n, "frames")
