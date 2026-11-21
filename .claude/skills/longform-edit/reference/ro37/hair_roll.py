"""Hair top and body box per roll: one frame every 0.5 s (540x960 of the 2160x3840 portrait picture), Vision person mask.
Writes framing/hair_roll.json: per roll a list of (t, top_px4k, left_px4k, right_px4k, waist?)."""
import json, os, glob, subprocess, sys
import numpy as np
from PIL import Image
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; FF = f"{P}/Media/video_edit/bin/ffmpeg"
PM = f"{P}/.claude/skills/shorts/reference/recentre/personmask"
RD = "/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content"
SC = "/tmp/absbyai-scratch/RO-37/hair"; out = {}
for r in ["C1893", "C1894", "C1895", "C1897"]:
    d = f"{SC}/{r}"; os.makedirs(d, exist_ok=True)
    if not glob.glob(f"{d}/f_*.jpg"):
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{RD}/{r}.MP4", "-vf", "fps=2,scale=540:960", "-q:v", "3", f"{d}/f_%05d.jpg"], check=True)
    fs = sorted(glob.glob(f"{d}/f_*.jpg"))
    if not os.path.isdir(f"{d}/m") or len(glob.glob(f"{d}/m/*.png")) < len(fs):
        subprocess.run([PM, f"{d}/m"] + fs, check=True, capture_output=True)
    rows = []
    for k, f in enumerate(fs):
        mp = f"{d}/m/" + os.path.basename(f)[:-4] + ".mask.png"
        if not os.path.exists(mp): continue
        m = np.asarray(Image.open(mp).convert("L")) > 127
        ys = np.where(m.sum(1) >= 3)[0]; xs = np.where(m.sum(0) >= 3)[0]
        if not len(ys): rows.append((round((k+0.5)/2, 2), None, None, None)); continue
        rows.append((round((k+0.5)/2, 2), int(ys[0])*4, int(xs[0])*4, int(xs[-1])*4))
    out[r] = rows
    v = [x[1] for x in rows if x[1] is not None]
    print(r, len(rows), "frames; hair top min", min(v), "median", int(np.median(v)), "; misses", sum(1 for x in rows if x[1] is None), flush=True)
json.dump(out, open(f"{W}/framing/hair_roll.json", "w"))
