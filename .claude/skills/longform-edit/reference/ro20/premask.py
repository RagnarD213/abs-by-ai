"""Person masks for the WHOLE roll at 2 fps (t0 = 0), in the layout framing.py reads, made while the take map is still being
built so framing can run the moment shots.json exists."""
import os, json, subprocess, glob
W = "/Volumes/Extreme/_edit_work/ro20"
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
SRC = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1511.MP4"
d = f"{W}/mask/C1511"; os.makedirs(d + "/m", exist_ok=True)
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", SRC, "-vf", "fps=2,scale=960:540", "-q:v", "4", f"{d}/f_%05d.jpg"], check=True)
fs = sorted(glob.glob(f"{d}/f_*.jpg"))
for i in range(0, len(fs), 200): subprocess.run([PM, d + "/m"] + fs[i:i+200], check=True, capture_output=True)
json.dump(dict(t0=0.0, n=len(fs)), open(d + "/done", "w")); print("PREMASK COMPLETE", len(fs), "frames", flush=True)
