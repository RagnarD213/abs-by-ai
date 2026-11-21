#!/usr/bin/env python3
"""Keep a short's true peak at or under Zeeshan's -1.0 dBTP after AAC encoding, without touching the level: try the AAC encoder
modes on build/S/audio.wav (his mix, cut only) and remux the rendered short with the first that measures <= -1.0 (picture copied,
frame count asserted). The overshoot differs per short: short I went -1.0 -> -0.8 in the default mode, short H -1.0 -> -0.9 in ABR."""
import re, subprocess, sys
import plans as P
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
MODES = [("aac_at 320k abr", ["-c:a", "aac_at", "-b:a", "320k", "-aac_at_mode", "abr"]), ("aac_at 320k", ["-c:a", "aac_at", "-b:a", "320k"]),
         ("aac_at 320k cbr", ["-c:a", "aac_at", "-b:a", "320k", "-aac_at_mode", "cbr"]), ("aac_at vbr q0", ["-c:a", "aac_at", "-aac_at_mode", "vbr", "-q:a", "0"]),
         ("aac 320k", ["-c:a", "aac", "-b:a", "320k"])]
def tp(f):
    o = subprocess.run([FF, "-nostdin", "-v", "info", "-i", f, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"True peak:\s*\n\s*Peak:\s*([-0-9.]+)", o)[-1])
for S in sys.argv[1:]:
    d = f"build/{S}"; V = f"{d}/{P.NAME[S]}.mp4"; now = tp(V)
    if now <= -1.0: print(S, "already", now); continue
    for name, args in MODES:
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{d}/audio.wav"] + args + [f"{d}/_tp.m4a"], check=True)
        v = tp(f"{d}/_tp.m4a")
        if v <= -1.0:
            subprocess.run(["./remux.sh", S, P.NAME[S]] + args, check=True); print(S, "remuxed with", name, "->", tp(V)); break
    else: print(S, "NO MODE reaches -1.0; was", now)
