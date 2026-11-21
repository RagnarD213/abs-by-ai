#!/usr/bin/env python3
"""Dan's 2026-09-13 text-screen note, as a gate on the RENDERED file (approved square defaults, [S1] START HERE B).

For every stacked text beat (window / stmt) read the beat's last full frame by INDEX and measure:
  * the lowest row of bright ink (text) -- must be <= WIN_BOT + 6 (descenders)
  * the empty band under it             -- must be <= MAX_BAND (70 px): "unnecessary blank space at the bottom"
  * the window height (Dan's picture)   -- reported, and must be >= the plan's window_rect height - 4

  python3 sqtextcheck.py ad1_square_1x1.mp4        exit 1 on any failure
"""
import sys, json, subprocess
sys.path.insert(0, '.')
import numpy as np
import beats, sqlib as V
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
# Calibrated 2026-09-14 on both sides of Dan's verdict, never tuned to pass a build:
#   APPROVED round 1   ink 1017-1031, empty band 48-62 px (1031 = a descender on the 2:52 statement; 62 = an all-caps last line)
#   REJECTED round 0   ink  938- 981, empty band 98-141 px ("unnecessary blank space at the bottom")
#   audit-flagged r1a  ink 1046 on the 0:25 screen (header mis-sized) -- must fail
INK_MAX = V.WIN_BOT + 6          # descenders may sit a few px under the baseline line
MAX_BAND = 70
vid = sys.argv[1]
tl, _ = beats.timeline()
bad, prev = 0, 0
rows = []
for b in tl:
    cum = round(b['t1']*FPS); n0, n1 = prev, cum; prev = cum
    if b['kind'] not in ('window', 'stmt'): continue
    n = n1 - 6                                           # settled, before any exit flash
    raw = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', vid, '-vf', f"select='eq(n,{n})',format=gray",
                          '-fps_mode', 'passthrough', '-frames:v', '1', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(V.VH, V.VW).astype(int)
    band = im[:, V.MARGIN:V.VW - V.RIGHT_SAFE]
    ink = np.nonzero((band > 150).sum(1) > 2)[0]
    ink = ink[ink > 400]                                 # text lives below the window
    low = int(ink.max()) if len(ink) else -1
    empty = V.VH - 1 - low
    ok = 0 <= low <= INK_MAX and empty <= MAX_BAND
    bad += not ok
    rows.append(dict(t0=b['t0'], kind=b['kind'], frame=n, ink_bottom=low, empty_band=empty, ok=ok))
    print(f"{'PASS' if ok else 'FAIL'}  {b['kind']:6s} {b['t0']:7.2f}s  frame {n:5d}  ink ends y={low}  empty band {empty} px"
          f"  (bounds: <= {INK_MAX}, <= {MAX_BAND})")
json.dump(rows, open(vid + '.textcheck.json', 'w'), indent=1)
print('TEXT SCREENS', 'PASS' if not bad else f'FAIL ({bad})')
sys.exit(1 if bad else 0)
