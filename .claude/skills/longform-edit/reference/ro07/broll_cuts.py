"""RO-07 round 2: new B-roll cut from the 8/28 blue-mat push-up roll C1680 (4K S-Log3), with the grade Dan approved for the
library clips of that roll (2026-10-01: 1.30 LUT, saturation 0.88, cooled; recipe broll-cuts-20260929/cut.py). Same crop
as library B0452 so the three push-up clips of the workout section match. usage: broll_cuts.py [--force]"""
import subprocess, os, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
R828 = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
LUT = "/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.30.cube"; OUT = "/Volumes/Extreme/_edit_work/ro07/broll"
CUTS = {  # name: (roll, in, out, crop x y w h)
 "handles_first_rep": ("C1680", 190.9, 202.2, (900, 640, 2560, 1440)),    # C22: push-ups on the handles, side on, from the first descent
 "pushups_regular":   ("C1680", 49.0, 60.0, (900, 640, 2560, 1440)),      # C23: flat-body push-ups on the mat, side on, from the first descent
 "handles_second":    ("C1680", 233.0, 237.2, (900, 640, 2560, 1440)),    # C18: the handles item of the equipment list (another take)
}
# round 3 (Dan: "start it immediately when I'm doing the reps ... I want to see the reps from the first second"): the opener's handstand
# push-up piece, re-cut from roll C1684 with library B0456's own crop and grade (1.45 LUT, saturation 0.88, not cooled). Measured on every
# frame (round3/work/measure_hs3.py): he holds the handstand until 15.88 s, rep 2 goes down 15.92 to 16.6 and up to 17.4, rep 3 starts down
# at 18.0. In at 15.949 s (source frame 478, already moving down), 1.2x so the 2.07 s slot holds the whole rep and most of the next descent.
CUTS3 = {  # name: (roll, in, out, crop, lut, cooled, speed)
 "handstand_reps": ("C1684", 478*1001/30000, 478*1001/30000 + 3.1, (520, 440, 2880, 1620), "/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube", False, 1.2),
}
JOBS = [(n, r, a, b, c, LUT, True, 1.0) for n, (r, a, b, c) in CUTS.items()] + [(n,) + v for n, v in CUTS3.items()]
for name, roll, a, b, (x, y, w, h), lut, cooled, speed in JOBS:
    out = f"{OUT}/{name}.mp4"
    if os.path.exists(out) and "--force" not in sys.argv: continue
    vf = f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos:in_color_matrix=bt709:in_range=tv,lut3d=file={lut}:interp=tetrahedral,eq=saturation=0.88" + (",colortemperature=temperature=8500:pl=1" if cooled else "") + (f",setpts=PTS/{speed}" if speed != 1.0 else "") + ",format=yuv420p,setsar=1"
    subprocess.run(["nice", "-n", "10", FF, "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", f"{R828}/{roll}.MP4", "-map", "0:v:0", "-vf", vf, "-r", "30000/1001",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart", "-an", out + ".tmp.mp4"], check=True)
    os.rename(out + ".tmp.mp4", out); print("cut", name, flush=True)
