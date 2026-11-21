#!/usr/bin/env python3
"""RA-14 round 4: the phone's REAL rectangle on the P1 and T1 cards, measured on the locked card files.

cards.json's phone_box [228, 96, 852, 1386] is the shell IMAGE's box, transparent padding included. The visible phone
body ends at y 1347 (measured: rows 1348 on differ from the field outside the phone by no more than its own gradient).
The gate's caption clearance must grade the pixels the phone occupies, so this measures the lowest row of the phone on
every frame the phone is up and writes round4/phone_rects.json {P1: [x0, y0, x1, y1], T1: ...}.
A row belongs to the phone when, across x 240..840, more than 40 px differ from the field at x 150 on that row by > 60.
"""
import json, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L

W, H = 1080, 1920
CARDS = json.load(open("round3/cards/cards.json"))
out = {}
for cid in ("P1", "T1"):
    n = CARDS[cid]["phone_frames"] if cid == "P1" else CARDS[cid]["n"]
    x0, y0, x1, y1 = CARDS[cid]["phone_box"]
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", f"round3/cards/{cid}.mp4", "-frames:v", str(n),
                          "-vf", "scale=in_color_matrix=bt709:in_range=tv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
    bottoms = []
    for im in fr:
        d = np.abs(im[1200:1420, 240:840] - im[1200:1420, 150:151]).sum(2)
        rows = np.nonzero((d > 60).sum(1) > 40)[0]
        bottoms.append(1200 + int(rows.max()) + 1)
    out[cid] = dict(rect=[x0, y0, x1, max(bottoms)], frames=len(bottoms), bottom_min=min(bottoms), bottom_max=max(bottoms),
                    declared_box=CARDS[cid]["phone_box"])
    print(cid, out[cid])
json.dump(out, open("round4/phone_rects.json", "w"), indent=1)
