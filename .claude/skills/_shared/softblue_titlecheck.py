"""Soft Blue Shorts title band: descender clearance check (2026-10-22, SL-17 reviewer B5).

The band's picture starts at y 310 (DROP) under a 2 px glass line at 308-309. With title-case titles, a second
line's descenders (g, j, p, q, y) at 88 px ran to y 312 under the old geometry (y 96, step 100) and were cut off.
The fixed geometry (y 86, step 96) puts the lowest glyph row at 298 at 88 px. This check keeps it that way.

Library use (every softblue batch.py calls it before gfx / proof / render):
    import softblue_titlecheck as TC; TC.check(lib.band, P.TITLE[S], S)

CLI:
    python3 softblue_titlecheck.py titles <batch dir> [S ...]   render each short's TITLE with that batch's lib.band
    python3 softblue_titlecheck.py frame <video.mp4> [...]      measure a delivered short's band (frame 1, else 1.5-8 s in) (audit)
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

W, H, DROP = 1080, 1920, 310
LIMIT = 299          # lowest white text row must be < 299: at least 10 px above the glass line at 309
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FFMPEG = ROOT + "/Media/video_edit/bin/ffmpeg"


def white_rows(a, y0=0, y1=None):
    """Rows holding white type (WHITE 244,250,255 and its anti-aliased edges) in an RGB array. Cyan eyebrow
    (104,197,255) and the glass line (64,112,153) are excluded by the red/blue ratio."""
    a = a[y0:y1].astype(np.int32); r, b = a[..., 0], a[..., 2]
    return np.where(((r > 40) & (r * 10 > b * 8)).any(1))[0] + y0


def lowest_row(band, title):
    """Render the band onto a black full frame (so glyphs past DROP stay visible) and return its lowest white row."""
    im = Image.new("RGB", (W, H), (0, 0, 0)); band(im, *title)
    rows = white_rows(np.asarray(im), 0, DROP + 40)
    return int(rows.max()) if len(rows) else -1


def check(band, title, label=""):
    low = lowest_row(band, title)
    assert low < LIMIT, (f"title band {label}: lowest glyph row {low} >= {LIMIT} (descenders reach the glass line at 309 / "
                         f"picture at {DROP}); lift the title (y 86, step 96) or shorten it: {title}")
    return low


def frame1(path, t=0.0):
    b = subprocess.run([FFMPEG, "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf",
                        "scale=1080:1920:flags=lanczos,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(H, W, 3) if len(b) == W * H * 3 else None


def frame_report(path):
    """Delivered-frame audit. Soft Blue band present = navy field in the band and the glass line at 308-309.
    White type measured with a stricter threshold (compression noise on the drifting field)."""
    for t in (0.0, 1.5, 3.0, 5.0, 8.0):                    # frame 1 first; a short that opens on a full-frame hook shows the band a few seconds in
        a = frame1(path, t)
        if a is None: return dict(file=path, band=False, note="no frame")
        rowm = a[306:311, 60:1020].astype(np.float64).mean(1); top = a[10:40, 600:1000].reshape(-1, 3).mean(0)
        line = any(abs(r[0] - 64) < 30 and abs(r[1] - 112) < 30 and abs(r[2] - 153) < 30 for r in rowm)      # the 1-2 px glass line (row 309 after encode)
        if line and top[2] > top[0] + 10 and top.mean() < 120: break
    else: return dict(file=path, band=False)
    s = a[100:308].astype(np.int32); m = (s[..., 0] > 150) & (s[..., 1] > 150) & (s[..., 0] * 10 > s[..., 2] * 8)
    rows = np.where(m.sum(1) >= 2)[0] + 100
    low = int(rows.max()) if len(rows) else -1
    ink_near_line = int(m[300 - 100:308 - 100].sum())      # white pixels in rows 300-307
    verdict = "CLIPPED" if low >= 305 else ("TIGHT" if low >= LIMIT else "OK")
    return dict(file=path, band=True, t=t, lowest=low, ink_300_307=ink_near_line, verdict=verdict)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "titles":
        d = os.path.abspath(sys.argv[2]); sys.path.insert(0, d); import lib, plans as P
        bad = 0
        for S in sys.argv[3:] or list(P.TITLE):
            low = lowest_row(lib.band, P.TITLE[S]); ok = low < LIMIT; bad += not ok
            print(f"{S:4} lowest {low:3}  {'OK' if ok else 'FAIL'}  {P.TITLE[S][1]}")
        sys.exit(1 if bad else 0)
    if mode == "frame":
        for p in sys.argv[2:]: print(json.dumps(frame_report(p)))
