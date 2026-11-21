#!/usr/bin/env python3
"""Flatten every graphic into ONE full-length alpha track, so the composite is a SINGLE
overlay instead of a 45-deep chain.

⚠ THIS IS THE DIFFERENCE BETWEEN A 20-MINUTE PASS AND A FOUR-HOUR ONE. Measured on a
20-second slice of the spray-tan build, same encoder settings throughout:

    45 time-shifted overlays + burned subtitles   0.08x realtime
    45 time-shifted overlays, no subtitles        0.05x
    NO overlays, burned subtitles                 1.12x
    NO overlays, no subtitles                     1.07x

The encoder preset is irrelevant (medium 261.8 s vs fast 244.0 s for the same 20 s) and
libass is free. What costs 14x is the chain itself: `[i:v]setpts=PTS+a/TB` moves each
five-second graphic to a late timestamp, and every overlay is a framesync filter, so all
45 of them are stepped for every frame of an 1134-second programme. The 71-cutaway pass
in the same build ran at 1.0x — because its inputs are H.264, but mostly because the
lesson is about DEPTH, and both are the same depth. The real difference is that the
cutaway inputs are consumed and closed as the timeline passes them, while an alpha
overlay chain holds all of them open.

The fix is to spend the time once, offline: lay the graphics end-to-end with transparent
filler between them and CONCATENATE, which is a stream copy. A transparent 1920x1080
QTRLE frame compresses to a few hundred bytes, so an hour of mostly-empty alpha track is
small. Then the composite is `[base][track]overlay=0:0` — one filter, full speed.

Requires the graphics NOT to overlap in time. That is already a rule (a full-frame card
must never cover a lower third), and it is asserted here.

usage:
  build_gfx_track.py --windows windows.json --gfxdir gfx --dur 1827.7 --out gfx_track.mov
                     [--fps 30000/1001]
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")


def dur_of(p):
    """Frame count and duration. `nb_frames` is absent on some muxes and present on
    others, so the fields are read by name, not by position."""
    o = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_frames,duration", "-of",
                        "default=noprint_wrappers=1", p],
                       capture_output=True, text=True).stdout
    kv = dict(l.split("=", 1) for l in o.strip().splitlines() if "=" in l)
    d = float(kv.get("duration", 0) or 0)
    n = kv.get("nb_frames", "N/A")
    if n in ("N/A", ""):
        n = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-count_frames",
                            "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", p],
                           capture_output=True, text=True).stdout.strip().split(",")[0]
    return int(n), d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--windows", required=True, help='json [[key, a, b], ...]')
    ap.add_argument("--gfxdir", default="gfx")
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", default="30000/1001")
    ap.add_argument("--prefix", default="", help="filename prefix for the .mov files")
    A = ap.parse_args()

    num, den = (int(x) for x in A.fps.split("/"))
    fd = den / num
    W = sorted(json.load(open(A.windows)), key=lambda x: x[1])
    for (k1, a1, b1), (k2, a2, b2) in zip(W, W[1:]):
        assert a2 >= b1 - 1e-6, f"graphics overlap: {k1} ends {b1}, {k2} starts {a2}"

    work = Path(tempfile.mkdtemp(prefix="gfxtrack_"))
    gap_cache = {}
    from PIL import Image
    transparent_png = work / "transparent.png"
    Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)).save(transparent_png)

    def gap(d):
        n = max(1, int(round(d / fd)))
        if n in gap_cache: return gap_cache[n]
        p = work / f"gap_{n:06d}.mov"
        # ⚠ The gap frames come from a transparent PNG, NOT from lavfi's `color` filter.
        # `color=c=black@0.0` produces an OPAQUE frame through QTRLE whether or not
        # `format=rgba` follows it -- measured mean alpha 255 both ways -- and every
        # transparent gap then lands on the programme as a black card. A PNG with a real
        # alpha channel measures 0.
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-loop", "1",
                        "-framerate", A.fps, "-i", str(transparent_png),
                        "-frames:v", str(n), "-c:v", "qtrle", "-pix_fmt", "argb", str(p)],
                       check=True)
        gap_cache[n] = p
        return p

    def normalise(src, i):
        """Restamp into ONE timebase. The graphics were written with a DECIMAL framerate
        ("29.970030"), which ffmpeg parses as 979001/32666 and stores with a 1/979001
        timebase; the lavfi gaps come out at 1/30000. Concatenating the two with -c copy
        does not rescale, and a 1827 s track reported itself as 59255 s."""
        dst = work / f"n_{i:04d}.mov"
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", str(src),
                        "-an", "-c", "copy", "-video_track_timescale", "30000", str(dst)],
                       check=True)
        return dst

    # Everything is counted in FRAMES, not seconds: summing float gaps leaves the track
    # a few frames short of the programme and the overlay ends early.
    total_n = int(round(A.dur / fd))
    have = 0
    parts, t, i = [], 0.0, 0
    for key, a, b in W:
        src = Path(A.gfxdir) / f"{A.prefix}{key}.mov"
        if not src.exists(): sys.exit(f"missing {src}")
        n, _ = dur_of(str(src))
        want = int(round(a / fd))
        if want > have:
            parts.append(gap((want - have) * fd)); have = want
        parts.append(normalise(src, i)); i += 1
        have += n
        t = have * fd
    if total_n > have: parts.append(gap((total_n - have) * fd))

    lst = work / "list.txt"
    lst.write_text("".join(f"file '{Path(p).resolve()}'\n" for p in parts))
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", A.out], check=True)
    n, d = dur_of(A.out)
    print(f"{len(W)} graphics + {len(parts)-len(W)} transparent gaps -> {A.out}")
    print(f"  {n} frames, {d:.3f}s (programme {A.dur:.3f}s), "
          f"{os.path.getsize(A.out)/1e6:.1f} MB")
    assert abs(n - total_n) <= 1, f"track is {n} frames, programme is {total_n}"
