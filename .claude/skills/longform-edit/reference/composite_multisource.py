#!/usr/bin/env python3
"""Overlay pass: J2 chips (0.35s alpha fades) + AbsByAI.com watermark over the
finished graded cut. One encode at CRF 18, audio COPIED (loudnorm preserved).
usage: composite.py <slug> <OUTPUT_NAME.mp4>"""
import json, subprocess, sys
from pathlib import Path

slug, outname = sys.argv[1], sys.argv[2]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
SRC = BASE / "roughcuts" / "CUT_v2_graded.mp4"
OUT = BASE / "roughcuts" / outname
G = BASE / "gfx"
FADE = 0.35
FPS = "30000/1001"

chips = json.load(open(BASE / "chip_timings.json"))
import importlib.util as _il
_sp = _il.spec_from_file_location("pip", str(BASE / "pip.py"))
_pm = _il.module_from_spec(_sp); _sp.loader.exec_module(_pm)
PIPS = _pm.PIPS
cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(SRC)]
for c in chips:
    cmd += ["-loop", "1", "-framerate", FPS, "-t", f"{c['end']-c['start']:.2f}",
            "-i", str(G / f"chip_{c['key']}.png")]
for p_ in PIPS:
    cmd += ["-i", str(G / p_["file"])]
cmd += ["-loop", "1", "-framerate", FPS, "-i", str(G / "wm.png")]

parts = []; last = "0:v"
for i, c in enumerate(chips, start=1):
    a, b = c["start"], c["end"]; dur = b - a
    parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                 f"fade=t=out:st={dur-FADE:.2f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
    last = f"v{i}"
base = len(chips) + 1
for j, p_ in enumerate(PIPS):
    a, b = p_["start"], p_["end"]; dur = b - a
    parts.append(f"[{base+j}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                 f"fade=t=out:st={dur-FADE:.2f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[p{j}]")
    parts.append(f"[{last}][p{j}]overlay={p_['x']}:{p_['y']}:enable='between(t,{a},{b})'[q{j}]")
    last = f"q{j}"
wm = len(chips) + len(PIPS) + 1
parts.append(f"[{last}][{wm}:v]overlay=0:0:shortest=1[vout]")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode)
print(r.stderr[-1500:] if r.returncode else f"OK -> {OUT}")
