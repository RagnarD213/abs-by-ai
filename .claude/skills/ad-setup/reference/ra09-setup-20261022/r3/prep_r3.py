#!/usr/bin/env python3
"""RA-09 thumbnails round 3 prep (2026-10-22): place each real pool photo on its 9:16 / 16:9 canvas and paint the empty
area flat grey; Codex then continues the photo's own scenery into the grey (trees, sky, water only). The real photo is
pasted back over its region afterwards (build_r3.py), so Dan is never redrawn. Writes <key>_<fmt>_canvas.png + place.json."""
import json
from PIL import Image
PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
PH = PROJ + "/photos/finalized social media photos"
HERE = PROJ + "/social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World/_build-2026-10-22/r3"
GREY = (128, 128, 128)
# per photo and format: source columns x0..x1 and top y0 (fractions), and where its top-left lands (x, y) at width w.
# The bottom of the crop is computed so the photo always reaches the canvas bottom: Codex never has to draw his legs.
PLACE = {
    "p247": {"src": "photo-247", "9x16": dict(crop=(0, 0, 1), at=(0, 520, 1080)),
             "16x9": dict(crop=(0, 0, 1), at=(510, 0, 900))},
    "p230": {"src": "photo-230", "9x16": dict(crop=(0.255, 0, 0.745), at=(0, 470, 1080)),
             "16x9": dict(crop=(0.07, 0.04, 1), at=(0, 0, 1920))},
    "p13":  {"src": "photo-13", "9x16": dict(crop=(0.13, 0.10, 0.87), at=(0, 380, 1080)),   # R3 pick C: moved up 120
             "16x9": dict(crop=(0.0, 0.10, 1.0), at=(670, 0, 1080))},                      # R3 pick C: bigger, right
}
FMT = {"16x9": (1920, 1080), "9x16": (1080, 1920)}
out = {}
for k, p in PLACE.items():
    im = Image.open(f"{PH}/{p['src']}_FINAL_PRIMARY.jpg").convert("RGB"); W0, H0 = im.size
    for fmt, (W, H) in FMT.items():
        c = p[fmt]; x0, y0, x1 = c["crop"]; x, y, w = c["at"]
        sc = w / ((x1 - x0) * W0); need = (H - y) / sc
        assert y0 * H0 + need <= H0 + 1, f"{k} {fmt}: photo too short to reach the bottom"
        cr = im.crop((round(x0 * W0), round(y0 * H0), round(x1 * W0), round(y0 * H0 + need))); h = H - y
        canvas = Image.new("RGB", (W, H), GREY); canvas.paste(cr.resize((w, h), Image.LANCZOS), (x, y))
        canvas.save(f"{HERE}/{k}_{fmt}_canvas.png")
        out[f"{k}_{fmt}"] = dict(src=p["src"], crop=c["crop"], x=x, y=y, w=w, h=h, needs_fill=(x > 0 or y > 0 or x + w < W or y + h < H))
        print(k, fmt, out[f"{k}_{fmt}"])
json.dump(out, open(f"{HERE}/place.json", "w"), indent=1)
