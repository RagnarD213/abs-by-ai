#!/usr/bin/env python3
"""A contact sheet of the 16:9 CTA pill over BOTH beats, on the frames the render will deliver,
with the person mask outlined -- so the pill's clearance is looked at, not asserted.
Writes r3/pill16.jpg and r3/pill16.json (minimum gap in px, per beat, per probe)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect

A = Aspect("16x9"); B = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
CTA = json.load(open("cta_16x9/cta.json")); GRADE = L.grade()
BOX = CTA["boxes"]
N = 8


def src_at(t):
    for p in CUT["pieces"]:
        if p["t_in"]-1e-6 <= t < p["t_out"]+1e-6: return p["src_in"]+(t-p["t_in"])
    p = min(CUT["pieces"], key=lambda p: min(abs(t-p["t_in"]), abs(t-p["t_out"])))
    return p["src_in"] + min(max(t-p["t_in"], 0.0), p["t_out"]-p["t_in"]-1e-3)


def seg_at(t):
    s = next((p for p in B["punch"] if p["beat"][0]-1e-6 <= t < p["beat"][1]+1e-6), None)
    return s or min(B["punch"], key=lambda p: min(abs(t-p["beat"][0]), abs(t-p["beat"][1])))


tiles, rep = [], []
for bi, (a, b) in enumerate(B["cta"]):
    x0, y0, x1, y1 = BOX[bi]
    for k in range(N):
        t = min(a + (b-a)*k/(N-1), b-1e-3)
        s = seg_at(t); cw, ch = A.levels[s["level"]]
        cy = int(round(s["hair_min"]-0.04*ch)); cy = max(0, min(3840-ch, cy - cy % 2))
        cx = s.get("cx16", s["cx"]); cx = int(round(cx - cw/2)); cx = max(0, min(2160-cw, cx - cx % 2))
        p = f"r3/pill_{bi}_{k}.png"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{src_at(t):.3f}", "-i", L.ROLL,
                        "-frames:v", "1", "-vf",
                        f"crop={cw}:{ch}:{cx}:{cy},{L.DECODE},{GRADE},scale=1920:1080:flags=lanczos",
                        "-y", p], check=True)
        # distance from the pill box to the nearest person pixel
        m = L.person_mask(Image.open(p))
        ys, xs = np.where(m)
        gap = None
        if len(xs):
            inside = (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
            if inside.any():
                gap = -int(inside.sum())
            else:
                band = (ys >= y0) & (ys <= y1)
                gap = int(xs[band].min() - x1) if band.any() else 9999
        im = Image.open(p).convert("RGB")
        d = ImageDraw.Draw(im)
        mm = Image.fromarray((m*255).astype(np.uint8)).convert("L")
        im.paste(Image.new("RGB", im.size, (255, 0, 0)), (0, 0), mm.point(lambda v: 60 if v else 0))
        d.rectangle([x0, y0, x1, y1], outline=(0, 255, 0), width=5)
        d.rectangle([int(1920*0.156), int(1080*0.861), int(1920*0.844), int(1080*0.963)],
                    outline=(0, 160, 255), width=3)
        d.text((20, 20), f"beat{bi} t={t:.2f} {s['level']} gap={gap}", fill=(255, 255, 0))
        tiles.append(im.resize((640, 360)))
        rep.append(dict(beat=bi, t=round(t, 3), level=s["level"], gap_px=gap, png=p))
        print(f"  beat{bi} t={t:6.2f} {s['level']:<4} pill-to-person gap {gap} px")
sheet = Image.new("RGB", (640*4, 360*((len(tiles)+3)//4)), (0, 0, 0))
for i, tl in enumerate(tiles): sheet.paste(tl, (640*(i % 4), 360*(i//4)))
sheet.save("r3/pill16.jpg", quality=90)
json.dump(dict(boxes=BOX, pill_size=CTA["pill_size"], probes=rep,
               min_gap_px=min(r["gap_px"] for r in rep)), open("r3/pill16.json", "w"), indent=1)
print(f"min pill-to-person gap over both beats: {min(r['gap_px'] for r in rep)} px  -> r3/pill16.jpg")
