#!/usr/bin/env python3
"""REV1 pass 2: J2 graphics over the cutaway pass.

Order is load-bearing: cards and before/after panels go on FIRST, then the
lower-third chips, then the watermark last. A chip must never end up underneath
a full-frame photo panel - which is why the title chip was moved from source
138.0 to 147.4, out of the item-1 panels' window.
All inputs are PNGs, so this pass is cheap despite ~50 overlays.
Audio COPIED: loudnorm from the render is preserved.
usage: composite_gfx.py <in.mp4> <out.mp4>
"""
import importlib.util, json, subprocess, sys, time
from pathlib import Path

B = Path("/Volumes/Extreme/_edit_work/spraytan")
SRC, OUT = B / "roughcuts" / sys.argv[1], B / "roughcuts" / sys.argv[2]
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
G = B / "gfx"
spec = importlib.util.spec_from_file_location("i", B / "inserts.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
chips = json.load(open(B / "chip_timings.json"))
FADE, FPS = 0.35, "30000/1001"

layers = []   # (start, dur, png)
fullframe = []
for a, d, k, key, _ in m.INSERTS:
    if k == "card":  layers.append((a, d, G / f"card_{key}.png"))
    elif k == "photo":
        layers.append((a, d, G / f"photo_{key}.png")); fullframe.append((a, a + d))
for c in chips:
    layers.append((c["start"], round(c["end"] - c["start"], 2), G / f"chip_{c['key']}.png"))

# a full-frame photo panel must not have a chip drawn over it
photos = [(a, a + d) for a, d, k, _, _ in m.INSERTS if k == "photo"]
clash = [c["key"] for c in chips for (pa, pb) in photos if c["start"] < pb and c["end"] > pa]
assert not clash, f"chip(s) {clash} land on top of a full-frame photo panel"

missing = [p.name for _, _, p in layers if not p.exists()]
assert not missing, f"missing graphics: {missing}"

cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(SRC)]
for _, d, p in layers:
    cmd += ["-loop", "1", "-framerate", FPS, "-t", f"{d:.3f}", "-i", str(p)]
cmd += ["-loop", "1", "-framerate", FPS, "-i", str(G / "wm.png")]
parts, last = [], "0:v"
for i, (a, d, p) in enumerate(layers, start=1):
    fi = min(FADE, d / 3)
    # A layer that another full-frame panel takes over from gets NO fade-out:
    # the successor is later in the chain, so it draws on top and the handover
    # is a clean cross-dissolve instead of a dip through to the video.
    fo = 0.0 if any(s < a + d + 0.05 and s > a for s, _ in fullframe) else fi
    fade_out = f",fade=t=out:st={d-fo:.3f}:d={fo:.2f}:alpha=1" if fo > 0 else ""
    parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={fi:.2f}:alpha=1"
                 f"{fade_out},setpts=PTS+{a}/TB[g{i}]")
    parts.append(f"[{last}][g{i}]overlay=0:0:enable='between(t,{a},{a+d:.3f})'[v{i}]")
    last = f"v{i}"
wm = len(layers) + 1
parts.append(f"[{last}][{wm}:v]overlay=0:0:shortest=1[vout]")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "-movflags", "+faststart", str(OUT)]
print(f"{len(layers)} graphics ({sum(1 for _,_,p in layers if p.name.startswith('card'))} cards, "
      f"{sum(1 for _,_,p in layers if p.name.startswith('photo'))} panels, {len(chips)} chips) + watermark")
t0 = time.time()
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode, f"{time.time()-t0:.0f}s")
print(r.stderr[-2000:] if r.returncode else f"OK -> {OUT}")
