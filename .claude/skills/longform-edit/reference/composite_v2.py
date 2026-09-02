#!/usr/bin/env python3
"""Overlay pass: J2 chips (0.35s alpha fades) + AbsByAI.com watermark over the
finished graded cut. One encode at CRF 18, audio copied (loudnorm preserved)."""
import json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RC = HERE.parent / "roughcuts"
SRC = RC / "CUT_v1_graded.mp4"
import os as _os, sys as _sys; _sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
def _audio_tripwire(src):
    """2026-09-02: this script copies audio through untouched (-c:a copy). If the input has no PASS
    stamp from _shared/audio/audio_gate.py, either the audio is not finished yet (set AUDIO_UNGATED=1
    and finish + gate it on the OUTPUT before delivery) or it is the comb-filtered/roomy audio that
    shipped three times. Either way the delivered file cannot pass QC without its own stamp."""
    from require_stamp import require_stamp
    try: require_stamp(str(src)); return
    except SystemExit as e:
        if _os.environ.get("AUDIO_UNGATED") == "1":
            print(f"  ⚠ AUDIO_UNGATED=1: compositing over UNGATED audio ({e}). The output MUST go through voice_chain/audio_gate before delivery."); return
        raise SystemExit(f"{e}\n  -> gate the input first, or set AUDIO_UNGATED=1 if the audio finish runs after this step")
_audio_tripwire(SRC)
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
