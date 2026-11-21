#!/usr/bin/env python3
"""Square label gate on the DELIVERED bytes (the START HERE rule A of [S1]): on every 3rd frame of
every labelled beat, the chip rectangle may not come within 8 px of the person mask.
  sq_labelcheck.py master_1x1.mp4
"""
import hashlib, json, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01-sq")
import ra01lib as L
M = sys.argv[1]
B = json.load(open("beats.json")); META = json.load(open("cards_1x1/meta.json"))
TL = {it["name"]: it for it in json.load(open("timeline_1x1.json"))["items"]}
PAD = 8
res, ok = [], True
for c in B["cards"]:
    if not c["chip"]: continue
    m = META["cards"][c["name"]]; x, y = m["chip_pos"]; w, h = Image.open(m["chip_png"]).size
    it = TL[c["name"]]
    frames = sorted(set(list(range(it["f0"], it["f1"], 3)) + [it["f1"]-1]))
    expr = "+".join(f"eq(n\\,{f})" for f in frames)
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", M, "-vf", f"select='{expr}'", "-vsync", "0",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 1080, 1080, 3)
    assert len(a) == len(frames), (c["name"], len(a), len(frames))
    worst = 0
    for fr in a:
        pm = L.person_mask(Image.fromarray(fr))
        if pm is None: raise SystemExit(f"{c['name']}: person mask failed on a delivered frame")
        worst = max(worst, int(pm[max(0, y-PAD):y+h+PAD, max(0, x-PAD):x+w+PAD].sum()))
    good = worst == 0; ok &= good
    res.append({"beat": c["name"], "label": c["chip"], "chip_rect": [x, y, w, h], "frames_checked": len(frames),
                "person_px_within_8px": worst, "ok": good})
    print(f"  {c['name']:<11} {c['chip']:<4} chip {x},{y} {w}x{h}  {len(frames)} frames  contact {worst} px  {'PASS' if good else 'FAIL'}")
h = hashlib.sha256(open(M, "rb").read()).hexdigest()
json.dump({"sha256": h, "verdict": "PASS" if ok else "FAIL", "pad_px": PAD, "beats": res},
          open(M + ".labelcheck.json", "w"), indent=1)
print("LABELCHECK", "PASS" if ok else "FAIL", h[:12])
sys.exit(0 if ok else 1)
