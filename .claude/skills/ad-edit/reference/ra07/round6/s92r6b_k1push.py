#!/usr/bin/env python3
"""RA-07 round 6 (round 5's, written to round6/chips). Round 5: K1's label-chip references in 3-frame windows (round 3 used 9-frame windows).

Delivery gate 2.6.1 samples whole frames at the start, middle and end of every declared beat, so a window's first and last frame
must match its single reference: the 2.5 % push moves the chip about 0.3 px per 3 frames (1.2 px per 9), and a crisp chip loses
correlation at 1 px (K1_0 and K1_4 read 0.838 and 0.833 against 0.85). Each reference is the component's own chip (softblue
disclosure at (540, 1580) "mt") pushed with s83_phone07.push at the window's middle frame, never read off the delivered file.
  python3 s92r5b_k1push.py   -> round6/chips/K1_push.json + K1_<n>.png
"""
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

W, H = 1080, 1920; N = 54; AMP = 0.025; WIN = 3
a0 = json.load(open("round2/cards/cards.json"))["K1"]["a"]
chip = Image.new("RGBA", (W, H), (0, 0, 0, 0)); B.disclosure(chip, "AI-GENERATED", xy=(W // 2, 1580), anchor="mt")
out = []
for i in range(0, N, WIN):
    frames = list(range(i, min(N, i + WIN))); k = frames[len(frames) // 2]
    s = 1.0 + AMP * k / (N - 1); cw, ch = W / s, H / s
    im = chip.resize((W, H), Image.LANCZOS, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
    al = np.asarray(im.split()[-1]); ys, xs = np.nonzero(al > 0)
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    name = f"K1_{i // WIN}"; im.crop(box).save(f"round6/chips/{name}.png")
    out.append(dict(name=name, beat=[round(a0 + frames[0] * L.FD, 6), round(a0 + (frames[-1] + 1) * L.FD, 6)],
                    chip=os.path.abspath(f"round6/chips/{name}.png"), pos=[box[0], box[1]], box=list(box)))
for old in range(0, 6):
    p = f"round6/chips/K1_{old}.png"
json.dump(out, open("round6/chips/K1_push.json", "w"), indent=1)
print(len(out), "windows", out[0]["beat"], out[-1]["beat"])
