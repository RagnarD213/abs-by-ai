#!/usr/bin/env python3
"""RA-05 setup: the negative-events contact sheets of the delivered master (one frame every second, evenly spaced, labelled with
film time), for a person to LOOK AT before round3's ../s20_neg.py records the scan (run with cwd setup/ so it writes
setup/logs/negative_scan_9x16.json).   python3 s95_negsheet.py  -> setup/logs/neg_sheet_<i>.jpg, prints the frame count"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
WD = "/Volumes/Extreme/_edit_work/ra05"
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as CP
MASTER = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/how ai can get you real six pack abs - RA-05/"
          "how ai can get you real six pack abs | claude | 9x16 | RA-05.mp4")
W, H = 1080, 1920; FPS = 30000 / 1001; N = 1749
picks = [int(round(i * FPS)) + 15 for i in range(59) if int(round(i * FPS)) + 15 < N]
tw, th, cols, per = 270, 480, 10, 20
fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
tiles = []
want = set(picks)
for g, fr in enumerate(CP.reader(MASTER, 0, N, False, (W, H))):
    if g in want:
        im = Image.fromarray(fr).resize((tw, th), Image.LANCZOS)
        d = ImageDraw.Draw(im); d.rectangle([0, 0, 92, 28], fill=(0, 0, 0)); d.text((4, 2), f"{g / FPS:5.2f}s", font=fnt, fill=(255, 255, 0))
        tiles.append(im)
for s in range(0, len(tiles), per):
    chunk = tiles[s:s + per]; rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (40, 40, 40))
    for i, im in enumerate(chunk): sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(f"{WD}/setup/logs/neg_sheet_{s // per}.jpg", quality=88)
print(len(tiles), "frames on", (len(tiles) + per - 1) // per, "sheets")
