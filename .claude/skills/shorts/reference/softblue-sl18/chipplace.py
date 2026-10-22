"""chipplace.py S..: where the AI-GENERATED chip can sit on each AI clip of a short without touching a person.
Renders 8 frames across the clip's used range exactly as the short shows them, takes the union of the person mask
(Vision), and tries the corners of the picture area with the chip's REAL box (it is 505 x 80 at size 30, not 280 x 60).
Prints the clear positions, best first; put the first in the cover's ai=(x, y)."""
import json, os, subprocess, sys, glob
import numpy as np
from PIL import Image
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import cv2, batch as Bt, plans as P
Bt.cv2 = cv2
W, H, DROP = 1080, 1920, 310
def chip_box(xy, size=23):
    return Bt.chip_png("AI-GENERATED", xy, size)[1]
for S in sys.argv[1:]:
    T = json.load(open(f"{Bt.D(S)}/timeline.json")); shots = json.load(open(f"{Bt.D(S)}/shots.json"))
    for sh in shots:
        if sh["kind"] != "clip" or not sh["cover"].get("ai"): continue
        c = sh["cover"]; d = f"{Bt.D(S)}/chip/{c['id']}"; os.makedirs(d + "/m", exist_ok=True)
        for f in glob.glob(d + "/*.png") + glob.glob(d + "/m/*"): os.remove(f)
        seq = Bt.clip_seq(c); bx, by, bw, bh = Bt.clip_box(c); n = len(sh["raw"])
        for k in range(8):
            j = int((k + 0.5) * n / 8); fr = np.zeros((H, W, 3), np.uint8); fr[by:by + bh, bx:bx + bw] = seq.get(int(np.floor(sh["raw"][j] * Bt.FPS + 0.25)))
            Image.fromarray(fr).resize((540, 960)).save(f"{d}/f_{k}.png")
        seq.close()
        fs = sorted(glob.glob(d + "/f_*.png")); subprocess.run([Bt.PM, d + "/m"] + fs, check=True, capture_output=True)
        U = np.zeros((960, 540), bool)
        for f in fs:
            mp = f"{d}/m/{os.path.basename(f)[:-4]}.mask.png"
            if os.path.exists(mp): U |= np.array(Image.open(mp).resize((540, 960))) > 127      # no file = no person in that frame
        U = np.kron(U, np.ones((2, 2), bool)); best = []
        for size in (23,):
            x0, y0, x1, y1 = chip_box((40, 340), size); cw, ch = x1 - x0, y1 - y0
            for y in list(range(336, 700, 36)) + list(range(1150, 1320, 30)):
                for name, x in (("left", 40), ("right", W - 40 - cw)):
                    a_, b_, c2, d2 = chip_box((x, y), size); m = 16
                    if d2 > 1396: continue                                                     # stay above the captions
                    hit = float(U[max(0, b_ - m):d2 + m, max(0, a_ - m):c2 + m].mean())
                    best.append((hit, -size, abs(y - 340) if y < 700 else 400 + abs(y - 1300), name, (x, y, size), (cw, ch)))
        best.sort(); h, _, _, name, pos, wh = best[0]
        print(S, c["id"], "| now", c["ai"], "| best:", pos, name, "chip", wh, "overlap with a person", round(h, 3), "| next:", [(round(b[0], 3), b[4]) for b in best[1:4]])
