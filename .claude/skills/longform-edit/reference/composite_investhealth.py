#!/usr/bin/env python3
"""Two composite passes over the graded cut, then the mux (04 Invest In Your Health).

  A  the 124 stock cutaways planned in inserts.json     -> picture_inserts.mp4
  B  27 lower thirds + 34 fact cards + 4 app cards,
     flattened into ONE alpha track                     -> picture_final.mp4
  C  mux picture_final with the new mix                 -> FINAL_invest_health.mp4

Pass B is ONE overlay of a pre-flattened track, and it carries NO burned captions and NO
watermark. Dan 2026-08-27: organic longforms ship a CLEAN FRAME plus an .srt sidecar, and
qc_style.py now FAILS a video whose frames carry burned captions. A 65-deep chain of
setpts-shifted alpha overlays also runs at 0.08x realtime (five hours on a 19-minute
programme); reference/build_gfx_track.py spends that once, offline, as a stream copy.

usage: composite.py A|B|C
"""
import json, os, subprocess, sys, time
from pathlib import Path

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
S  = Path(__file__).resolve().parent
BASE = S.parent / "sub30f" / "out" / "CUT_sub30f_graded.mp4"
FADE, FPS = 0.15, "30000/1001"


def run(cmd, label):
    print(label, flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("rc", r.returncode, f"{time.time()-t0:.0f}s", flush=True)
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(1)


def pass_a():
    P = json.load(open(S / "inserts.json"))
    cmd = [FF, "-nostdin", "-y", "-v", "error", "-i", str(BASE)]
    for i, x in enumerate(P):
        cmd += ["-i", str(S / "inserts" / f"ins_{i:03d}.mp4")]
    parts, last = [], "0:v"
    for i, x in enumerate(P, start=1):
        a, d = x["t"], x["dur"]
        parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                     f"fade=t=out:st={d-FADE:.3f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
        parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{a+d:.3f})'[v{i}]")
        last = f"v{i}"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", FPS, str(S / "picture_inserts.mp4")]
    run(cmd, f"pass A: {len(P)} cutaways")


def pass_b():
    cmd = [FF, "-nostdin", "-y", "-v", "error",
           "-i", str(S / "picture_inserts.mp4"),
           "-i", str(S / "gfx_track.mov"),
           "-filter_complex", "[0:v][1:v]overlay=0:0[vout]",
           "-map", "[vout]", "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-r", FPS, str(S / "picture_final.mp4")]
    run(cmd, "pass B: flattened graphics track (clean frame, no captions, no watermark)")


def pass_c():
    cmd = [FF, "-nostdin", "-y", "-v", "error",
           "-i", str(S / "picture_final.mp4"), "-i", str(S / "audio" / "final_mix_v2.wav"),
           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
           "-movflags", "+faststart", str(S / "FINAL_invest_health.mp4")]
    run(cmd, "pass C: mux")


if __name__ == "__main__":
    {"A": pass_a, "B": pass_b, "C": pass_c}[sys.argv[1]]()
