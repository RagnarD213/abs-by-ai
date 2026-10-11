"""QC contact sheets of the round 1 stills, 5 x 4 per sheet with each item's ID burned in. usage: qcsheets.py <letter> [letter ...]"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round1/qc"; os.makedirs(O, exist_ok=True)
rows = json.load(open(f"{W}/round1/stills.json")); f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
for L in sys.argv[1:]:
    ids = [r["id"] for r in rows if (len(r["id"]) == 4 and r["id"][1] == L) or (L == "x" and len(r["id"]) != 4)]
    for n in range(0, len(ids), 20):
        im = Image.new("RGB", (1920, 1080), (0, 0, 0))
        for k, i in enumerate(ids[n:n+20]):
            t = Image.open(f"{W}/round1/stills/{i}.jpg").convert("RGB").resize((384, 216), Image.LANCZOS); x, y = (k % 5) * 384, (k // 5) * 270
            im.paste(t, (x, y)); d = ImageDraw.Draw(im); d.rectangle((x, y + 216, x + 384, y + 270), fill=(13, 22, 38)); d.text((x + 6, y + 222), i, font=f, fill=(143, 208, 255))
            r = next(q for q in rows if q["id"] == i); d.text((x + 70, y + 222), (r["copy"].get("point") or (r.get("note") or ""))[:34], font=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15), fill=(230, 230, 230))
            d.text((x + 70, y + 244), f"{int(r['t0']//60)}:{int(r['t0']%60):02d}  {r['kind']}" + (f" over {r['over']}" if r.get("over") else ""), font=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13), fill=(159, 178, 204))
        p = f"{O}/{L}_{n//20+1}.jpg"; im.save(p, quality=80); print(p)
