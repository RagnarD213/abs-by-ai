#!/usr/bin/env python3
"""BACKGROUND-ARTIFACT SCAN. Per-pixel stdev across the unit; reports motion blobs OUTSIDE the
subject's own motion area -- a weight stack pumping on its own, a machine arm drifting, a ghost limb.

  ghost.py <id> [--dir <demos root>] [--work <scratch dir>]

⚠ PROMOTED INTO THE SKILL 2026-09-09 (Phase 0). This lived only in the gitignored
`Media/exercise-demos/_r2/`, while SKILL.md named it as a MANDATORY rule on every rep. `--dir` and
`--work` replaced the two relative paths; the measurement is unchanged.

⚠ KNOWN BLIND SPOT, MEASURED: the scan excludes the subject's whole bounding box, so machinery
INSIDE that box (a stack behind him, a pulley over his shoulder) is invisible to it. Dan caught
pumping stacks in the press and the side-lateral AFTER this said clean. Treat a clean result as
"no stray motion outside him", never as "the background is correct" -- watch the rep.
"""
import sys, subprocess, glob, os
import numpy as np
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
D = os.environ.get("DEMOS_DIR") or os.path.join(REPO, "Media/exercise-demos")
W = None
for flag, var in (("--dir", "D"), ("--work", "W")):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        globals()[var] = sys.argv[i + 1]; del sys.argv[i:i + 2]
if len(sys.argv) < 2: raise SystemExit(__doc__)
eid = sys.argv[1]
work = W or os.path.join(D, "_r2")
os.makedirs(work, exist_ok=True)

unit = os.path.join(D, eid, "r2-unit.mp4")
if not os.path.exists(unit): unit = os.path.join(D, eid, "b2-unit.mp4")
if not os.path.exists(unit): raise SystemExit(f"no r2-unit.mp4 or b2-unit.mp4 for {eid} under {D}")
for f in glob.glob(os.path.join(work, "gh*.png")): os.remove(f)
subprocess.run([FF, "-y", "-loglevel", "error", "-i", unit, "-vf", "fps=8,scale=480:-1",
                os.path.join(work, "gh%03d.png")], check=True)
fs = sorted(glob.glob(os.path.join(work, "gh*.png")))
sd = np.stack([np.asarray(Image.open(f).convert("L"), dtype=np.float32) for f in fs]).std(axis=0)
H, Wd = sd.shape
cell = 30; hot = []
for y in range(0, H - 10, cell):
    for x in range(0, Wd - 10, cell):
        m = sd[y:y + cell, x:x + cell].max()
        if m > 6: hot.append((x, y, round(float(m), 1)))
if not hot:
    print(f"{eid}: no motion at all?"); sys.exit()
mx = max(h[2] for h in hot)                        # dominant cluster = the subject
subj = [h for h in hot if h[2] > 0.35 * mx]
xs = [h[0] for h in subj]; ys = [h[1] for h in subj]
x0, x1, y0, y1 = min(xs) - cell, max(xs) + 2 * cell, min(ys) - cell, max(ys) + 2 * cell
stray = [h for h in hot if not (x0 <= h[0] <= x1 and y0 <= h[1] <= y1) and h[2] > 10]
print(f"{eid}: subject box x[{x0},{x1}] y[{y0},{y1}] maxsd={mx:.0f}  "
      f"STRAY={'NONE' if not stray else stray}")
sys.exit(1 if stray else 0)
