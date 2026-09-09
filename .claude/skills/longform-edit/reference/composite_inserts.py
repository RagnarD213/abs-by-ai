#!/usr/bin/env python3
"""REV1 pass 1: overlay the stock cutaways onto the finished graded cut.

Inserts are pre-rendered to exact-duration 1920x1080 MP4s (build_inserts.py), so
this opens ~70 decoders but each holds only ~4 seconds of frames. Alpha is added
IN THE GRAPH (`format=rgba,fade=alpha=1`) rather than stored on disk: a 4-second
1080p ProRes 4444 insert is ~165 MB and 70 of them would be 11 GB of alpha video
for a 0.15s dissolve.
Audio is COPIED - Dan's voice runs continuously underneath every cutaway.
usage: composite_inserts.py <in.mp4> <out.mp4>
"""
import importlib.util, subprocess, sys, time
from pathlib import Path

B = Path("/Volumes/Extreme/_edit_work/spraytan")
SRC, OUT = B / "roughcuts" / sys.argv[1], B / "roughcuts" / sys.argv[2]
import os as _os, sys as _sys; _sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
def _audio_tripwire(src):
    """2026-09-02: this script copies audio through untouched (-c:a copy). If the input has no PASS
    stamp from _shared/audio/audio_gate.py, it is the comb-filtered/roomy audio that shipped three
    times, and compositing over it only makes it more expensive to fix.

    ⚠ THE `AUDIO_UNGATED=1` ESCAPE WAS REMOVED 2026-09-09 (Phase 0 of the video-quality programme).
    It existed for the case "the audio finish runs after this step", and it was the wrong shape for
    that: an environment variable set once in a shell silently disarms this tripwire for everything
    that shell runs afterwards, and leaves no mark on the file. The correct order costs nothing --
    finish and gate the audio FIRST (voice_chain.py -> audio_gate.py), then composite. The composite
    output has a different sha256 either way, so it is re-gated before delivery regardless; gating
    the input first is what stops bad audio being carried three renders deep before anyone measures it."""
    from require_stamp import require_stamp
    try: require_stamp(str(src)); return
    except SystemExit as e:
        raise SystemExit(f"{e}" + "\n  -> finish and gate the audio BEFORE compositing "
                         f"(voice_chain.py -> audio_gate.py). There is no override: "
                         f"the AUDIO_UNGATED=1 escape was removed 2026-09-09.")
_audio_tripwire(SRC)
spec = importlib.util.spec_from_file_location("i", B / "inserts.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FADE, FPS = 0.15, "30000/1001"

clips = [(a, d, key) for a, d, k, key, _ in m.INSERTS if k == "clip"]
cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(SRC)]
for _, _, key in clips:
    cmd += ["-i", str(B / "inserts" / f"ins_{key}.mp4")]
parts, last = [], "0:v"
for i, (a, d, key) in enumerate(clips, start=1):
    parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                 f"fade=t=out:st={d-FADE:.3f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{a+d:.3f})'[v{i}]")
    last = f"v{i}"
cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
print(f"{len(clips)} video cutaways -> {OUT.name}")
t0 = time.time()
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode, f"{time.time()-t0:.0f}s")
print(r.stderr[-2000:] if r.returncode else f"OK -> {OUT}")
