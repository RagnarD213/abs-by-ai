#!/usr/bin/env python3
"""The extra frame-by-frame strips the round-2 brief names.  s34_strips.py 9x16|16x9 <master>

The shared watch pass gives -2..+2 at every boundary and contact sheets. This adds the three the
brief asks for by name and the watch pass does not cover at that density:

  * the LAST TEN FRAMES of the macro-tracker beat, one by one (R3: the slice must end before the
    recording changes screen);
  * the FIRST frame and the LAST frame of the film;
  * the first ten frames (R1: the film opens on the first word, and the hook card is up at frame 0).

Writes r2/strips_<key>/*.jpg.
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from PIL import Image, ImageDraw
from motionlib import font

KEY, MASTER = sys.argv[1], sys.argv[2]
TL = json.load(open(f"timeline_{KEY}.json"))
OUT = f"r2/strips_{KEY}"; os.makedirs(OUT, exist_ok=True)
TOTF = TL["total_frames"]
items = {it["name"]: it for it in TL["items"]}
macro = items["macro"]

GROUPS = {
    "macro_tail_10": list(range(macro["f1"]-10, macro["f1"]+2)),
    "open_10":       list(range(0, 10)),
    "first_last":    [0, 1, TOTF-2, TOTF-1],
}
W = 300 if KEY == "9x16" else 420

want = sorted({f for g in GROUPS.values() for f in g if 0 <= f < TOTF})
expr = "+".join(f"eq(n\\,{f})" for f in want)
raw = f"{OUT}/raw"
import shutil as _sh; _sh.rmtree(raw, ignore_errors=True); os.makedirs(raw)
subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", MASTER, "-vf",
                f"select='{expr}',scale={W}:-1", "-vsync", "0", "-y", f"{raw}/g%04d.png"],
               check=True)
# ⚠ the SSD writes AppleDouble "._" siblings; they end in .png and doubled the count
got = sorted(f for f in os.listdir(raw) if f.endswith(".png") and not f.startswith("._"))
assert len(got) == len(want), f"grabbed {len(got)} of {len(want)}"
byf = {f: os.path.join(raw, n) for f, n in zip(want, got)}

for name, frames in GROUPS.items():
    frames = [f for f in frames if 0 <= f < TOTF]
    tiles = [Image.open(byf[f]).convert("RGB") for f in frames]
    h = tiles[0].height
    cols = min(6, len(tiles)); rows = (len(tiles)+cols-1)//cols
    sheet = Image.new("RGB", (W*cols, h*rows), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, (f, t) in enumerate(zip(frames, tiles)):
        x, y = (i % cols)*W, (i//cols)*h
        sheet.paste(t, (x, y))
        d.rectangle([x, y, x+W, y+22], fill=(0, 0, 0))
        d.text((x+4, y+2), f"f{f}  {f*L.FD:.3f}s", font=font(16, "ExtraBold"), fill=(255, 220, 90))
    sheet.save(f"{OUT}/{name}.jpg", quality=92)
    print(f"{OUT}/{name}.jpg   frames {frames[0]}..{frames[-1]}")
print(f"macro beat: f{macro['f0']}..f{macro['f1']-1}  ({macro['a']:.3f}s, {macro['n']} frames)")
