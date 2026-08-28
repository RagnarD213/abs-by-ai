#!/usr/bin/env python3
"""Per-shot geometry facts, so a crop can be CHOSEN rather than guessed.

Two measurements per shot, both as UNIONS over the whole shot rather than one mid-frame:

  subject  l..r      Apple Vision person mask, the full silhouette (not the torso block) -
                     because the rule Dan gave is "my entire body is visible when I'm doing
                     the exercise", which is about the extremes, not the centre.
  graphic  l..r,t..b Muhammad's burned overlays. Detected as the WHITE PILL fill (very bright,
                     low saturation, long horizontal runs) plus the olive lower-third/pill fill,
                     then widened by PANEL_PAD because his pills sit on a translucent olive panel
                     that extends past them and is what actually showed at the crop edge.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'recentre'))
from anchor import anchors  # noqa
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"], cwd=HERE).decode())['SRC']
W, H = 480, 270
PANEL_PAD = 0.042        # measured: pills end x~675, the panel behind them ends x~745

def graphic_box(t0, dur, fps=5, band=(0.0, 1.0)):
    p = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{t0:.2f}", "-i", SRC,
                        "-t", f"{dur:.2f}", "-vf", f"fps={fps},scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(a) // (W * H * 3)
    if not n: return None
    a = a[:n * W * H * 3].reshape(n, H, W, 3).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    white = (r > 235) & (g > 235) & (b > 228) & (abs(r - b) < 20) & (abs(r - g) < 12)
    olive = (abs(r - 122) < 42) & (abs(g - 140) < 42) & (abs(b - 70) < 46) & (g > b + 26) & (g > r + 8)
    r0, r1 = int(band[0] * H), int(band[1] * H)
    box = None
    for i in range(n):
        for m, need_ink in ((white[i], olive[i]), (olive[i], white[i])):
            rowsum = m.sum(1).copy()
            rowsum[:r0] = 0; rowsum[r1:] = 0
            rows = np.where(rowsum >= W * 0.16)[0]
            if len(rows) < 4: continue
            # a graphic carries TEXT of the other colour inside the same rows; sky and pool do not
            if need_ink[rows].sum() < 20: continue
            cols = np.where(m[rows].sum(0) >= max(3, len(rows) * 0.30))[0]
            if len(cols) < 20: continue
            bb = (cols[0] / W, cols[-1] / W, rows[0] / H, rows[-1] / H)
            box = bb if box is None else (min(box[0], bb[0]), max(box[1], bb[1]),
                                          min(box[2], bb[2]), max(box[3], bb[3]))
    if box is None: return None
    return (max(0.0, box[0] - PANEL_PAD), min(1.0, box[1] + PANEL_PAD), box[2], box[3])

def subject_span(shot):
    L_, R_ = [], []
    for f in sorted(glob.glob(os.path.join(HERE, 'recentre', 'mk', shot, '*.mask.png'))):
        if os.path.basename(f).startswith('._'): continue
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        a = anchors(m > 127)
        if a: L_.append(a['l']); R_.append(a['r'])
    if len(L_) < 3: return None
    return (float(np.min(L_)), float(np.max(R_)))

out = {}
for m in json.load(open(os.path.join(HERE, 'shots', 'manifest.json'))):
    n = m['name']
    # A bright sky fills the top band the way a white pill does, and a union over the whole
    # frame then merges a real BOTTOM lower third with a spurious TOP hit and reports one box
    # spanning the entire height. Measure the two regions separately.
    gt = graphic_box(m['absStart'], m['dur'], band=(0.0, 0.32))
    gb = graphic_box(m['absStart'], m['dur'], band=(0.58, 1.0))
    s = subject_span(n)
    out[n] = {'graphic_top': gt, 'graphic_bot': gb, 'subject': s,
              'start': m['absStart'], 'dur': m['dur']}
    f_ = lambda g: (f"x {g[0]:.3f}-{g[1]:.3f} y {g[2]:.2f}-{g[3]:.2f}" if g else "none")
    ss = f"x {s[0]:.3f}-{s[1]:.3f} (w {s[1]-s[0]:.3f})" if s else "none"
    print(f"{n:12s} {m['dur']:5.1f}s  subject {ss:30s}  top {f_(gt):28s}  bottom {f_(gb)}")
json.dump(out, open(os.path.join(HERE, 'shots', 'geom.json'), 'w'), indent=1)
