#!/usr/bin/env python3
"""RA-04 round 5: the live-site screencast (r5_record.py, variable-rate JPEG frames with timestamps) -> one constant 60 fps
1320x2868 H.264 recording, BT.709 tagged and converted (the BT.601 trap, memory untagged-video-bt601-trap). Each output
frame shows the newest screencast frame at or before its time, exactly like a screen recorder.

Usage: python3 r5_cast2mp4.py REC_DIR OUT.mp4 [T_FROM T_TO]   (times in seconds from the recorder's T0)"""
import json, subprocess, sys
from bisect import bisect_right
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
rec, out = sys.argv[1], sys.argv[2]
L = json.load(open(f"{rec}/log.json")); T0 = L["T0"]
ts = [c["t"] - T0 for c in L["cast"]]
a = float(sys.argv[3]) if len(sys.argv) > 3 else ts[0]
b = float(sys.argv[4]) if len(sys.argv) > 4 else ts[-1]
lines, n = [], int((b - a) * 60)
for k in range(n):
    i = max(0, bisect_right(ts, a + k / 60) - 1)
    lines.append(f"file '{rec}/cast/{i:05d}.jpg'\nduration {1/60:.6f}")
open(f"{rec}/cfr.txt", "w").write("\n".join(lines) + "\n")
subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{rec}/cfr.txt",
                "-vf", "fps=60,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow",
                "-crf", "12", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                "-r", "60", out], check=True)
json.dump(dict(rec=rec, t_from=a, t_to=b, frames=n, marks=L["marks"]), open(out + ".json", "w"), indent=1)
print("CAST2MP4", out, n, "frames", f"{a:.3f}-{b:.3f} s")
