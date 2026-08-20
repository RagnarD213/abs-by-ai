#!/usr/bin/env python3
"""Overlay pass: J2 chips (0.35s alpha fades) + AbsByAI.com watermark over the
finished graded cut. One encode at CRF 18, audio copied (loudnorm preserved)."""
import json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RC = HERE.parent / "roughcuts"
SRC = RC / "CUT_v1_graded.mp4"
OUT = RC / "INVEST_HEALTH_v1.mp4"
G = HERE / "gfx"
FADE = 0.35
FPS = "30000/1001"

chips = json.load(open(HERE / "chip_timings.json"))
cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(SRC)]
for c in chips:
    cmd += ["-loop", "1", "-framerate", FPS, "-t", f"{c['end']-c['start']:.2f}",
            "-i", str(G / f"chip_{c['key']}.png")]
cmd += ["-loop", "1", "-framerate", FPS, "-i", str(G / "wm.png")]

parts = []; last = "0:v"
for i, c in enumerate(chips, start=1):
    a, b = c["start"], c["end"]; dur = b - a
    parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                 f"fade=t=out:st={dur-FADE:.2f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
    last = f"v{i}"
wm = len(chips) + 1
parts.append(f"[{last}][{wm}:v]overlay=0:0:shortest=1[vout]")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode)
print(r.stderr[-1500:] if r.returncode else f"OK -> {OUT}")
