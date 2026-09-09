#!/usr/bin/env python3
"""Overlay pass: cutaways first, then graphics + watermark.

Two passes rather than one 53-input graph. Each pass opens one decoder per overlay and
holds it until concat reaches it; splitting keeps the peak decoder count at ~27 and
makes a failure re-runnable without redoing the other half.

Alpha is added IN THE GRAPH for the cutaways (`format=rgba,fade=alpha=1`) rather than
stored on disk -- a 3-second 1080p ProRes 4444 insert is ~120 MB and 26 of them would be
3 GB of alpha video for a 0.15 s dissolve. The graphics are already QTRLE with real alpha.

Audio is COPIED through both passes: Dan's voice runs continuously underneath.
usage: composite.py inserts|gfx
"""
import os, subprocess, sys, time
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
os.environ["MOTIONLIB_FFMPEG"] = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
from PIL import Image, ImageDraw
import motionlib as M
import spec

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FPS = "30000/1001"
FADE_INS, FADE_GFX = 0.14, 0.0        # graphics animate their own in/out

def watermark():
    p = "gfx/wm.png"
    if os.path.exists(p): return p
    im = Image.new("RGBA", (M.W, M.H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = M.font(30, "Bold")
    txt = "AbsByAI.com"
    w = M.text_size(txt, f)[0]
    x0, y0 = M.W - w - 48, M.H - 64
    d.text((x0 + 2, y0 + 2), txt, font=f, fill=(0, 0, 0, 150))
    d.text((x0, y0), txt, font=f, fill=(255, 255, 255, 205))
    im.save(p); return p

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

def pass_inserts(src, out):
    _audio_tripwire(src)
    clips = [(a, d, f"inserts/ins_{i:02d}_{k}.mp4")
             for i, (a, d, kind, k, _) in enumerate(spec.INSERTS)]
    end = [g for g in spec.G if g[2] == "endcard"][0]
    clips.append((end[0], end[1], f"inserts/ins_{len(spec.INSERTS):02d}_endcard.mp4"))
    cmd = [FF, "-nostdin", "-y", "-v", "error", "-i", src]
    for _, _, p in clips: cmd += ["-i", p]
    parts, last = [], "0:v"
    for i, (a, d, p) in enumerate(clips, start=1):
        parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE_INS}:alpha=1,"
                     f"fade=t=out:st={d-FADE_INS:.3f}:d={FADE_INS}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
        parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{a+d:.3f})'[v{i}]")
        last = f"v{i}"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", FPS, "-c:a", "copy", out]
    return cmd, len(clips)

def pass_gfx(src, out):
    _audio_tripwire(src)
    gs = [(a, d, f"gfx/{k}.mov") for a, d, kind, k, _ in spec.G if kind != "endcard"]
    wm = watermark()
    cmd = [FF, "-nostdin", "-y", "-v", "error", "-i", src]
    for _, _, p in gs: cmd += ["-i", p]
    cmd += ["-loop", "1", "-framerate", FPS, "-i", wm]
    parts, last = [], "0:v"
    for i, (a, d, p) in enumerate(gs, start=1):
        parts.append(f"[{i}:v]format=rgba,setpts=PTS+{a}/TB[c{i}]")
        parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{a+d:.3f})'[v{i}]")
        last = f"v{i}"
    n = len(gs) + 1
    parts.append(f"[{last}][{n}:v]overlay=0:0:shortest=1[vout]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", FPS, "-c:a", "copy", out]
    return cmd, len(gs)

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "inserts": cmd, n = pass_inserts("tight.mov", "_p1_inserts.mov")
    else:                  cmd, n = pass_gfx("_p1_inserts.mov", "_p2_gfx.mov")
    print(f"{which}: {n} overlays")
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("rc", r.returncode, f"{time.time()-t0:.0f}s")
    if r.returncode: print(r.stderr[-2500:])
