#!/usr/bin/env python3
"""RA-14 round 2 stills: the framing pairs and the colour candidates on the SAME two moments, 1080x1920.

  close moment 7.57 s ("real abs", source 348.258)   wide moment 5.10 s ("I'm not talking about an AI picture", source 345.724)
  round2/stills/F<n>-close.jpg / -wide.jpg      framing pair n (0 = round 1), in the recommended colour, with the real caption
  round2/stills/K-<look>-close.jpg / -wide.jpg  each colour candidate in the recommended framing pair, no caption
  round2/stills/ref-*.jpg                       frames of the approved videos they were judged beside
The full graded frames come from the real pipeline filter (round2/colour/full, made with looks.json), cropped by the
hair rule: y0 = the hold's lowest hair top - 4 % of the crop height, x centred on his measured head.
"""
import json, sys
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import s71_opener_frames as OF
ST = "round2/stills"; FULL = "round2/colour/full"
SAM = json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"]
PAIRS = [dict(id="F0", name="Round 1 (what you saw)", near=(504, 896), far=(612, 1088)),
         dict(id="F1", name="A little wider", near=(540, 960), far=(666, 1184)),
         dict(id="F2", name="Wider", near=(576, 1024), far=(720, 1280)),
         dict(id="F3", name="Widest", near=(612, 1088), far=(756, 1344))]
REC_PAIR = "F2"; REC_LOOK = "C2_brighter_gold"
# the stills follow the round 2 plan: the CLOSE shot is "real abs in real life" (6.31 to 9.54 s), the WIDE shot is "I'm not
# talking about an AI picture" (4.44 to 6.31 s). `src` is the full-frame file's name in round2/colour/full.
MOM = {"close": dict(t=7.566, span=(6.306, 9.543), src="wide"), "wide": dict(t=5.098, span=(4.438, 6.306), src="close")}
for m in MOM.values():
    s = min(SAM, key=lambda x: abs(x["t"] - m["t"])); m["cx"] = s["cx"]
    m["hair_min"] = min(x["hair"] for x in SAM if m["span"][0] - 0.05 <= x["t"] <= m["span"][1] + 0.05); m["hair_here"] = s["hair"]
meta = {"moments": MOM, "pairs": [], "looks": {}}


def cut(look, which, cw, ch):
    m = MOM[which]; im = Image.open(f"{FULL}/{m['src']}_{look}.png").convert("RGB")
    y0 = int(round(m["hair_min"] - 0.04*ch)); x0 = int(round(m["cx"] - cw/2))
    return im.crop((x0, y0, x0+cw, y0+ch)).resize((1080, 1920), Image.LANCZOS), (x0, y0)


for p in PAIRS:
    row = dict(p)
    for which, key in (("close", "near"), ("wide", "far")):
        cw, ch = p[key]; im, (x0, y0) = cut(REC_LOOK, which, cw, ch)
        rgba = im.convert("RGBA"); OF.caption(rgba, MOM[which]["t"]); rgba.convert("RGB").save(f"{ST}/{p['id']}-{which}.jpg", quality=93)
        row[which] = dict(crop=[cw, ch], x0=x0, y0=y0, bottom=y0+ch, enlarge=round(1080/cw, 2),
                          hair_px_from_top=round((MOM[which]["hair_here"] - y0)*1080/cw))
    row["spread"] = round(p["far"][0]/p["near"][0], 3); meta["pairs"].append(row)
rp = next(p for p in PAIRS if p["id"] == REC_PAIR)
for look in json.load(open("round2/colour/looks.json")):
    for which, key in (("close", "near"), ("wide", "far")):
        im, _ = cut(look, which, *rp[key]); im.save(f"{ST}/K-{look}-{which}.jpg", quality=93)
# the approved videos, as delivered
for src, dst in (("ra01_15.png", "ref-ra01-a.jpg"), ("ra01_30.png", "ref-ra01-b.jpg"), ("ad1_33.png", "ref-ad1-a.jpg"), ("ad1_42.png", "ref-ad1-b.jpg"), ("web_60.png", "ref-web.jpg")):
    Image.open(f"round2/colour/ref/{src}").convert("RGB").save(f"{ST}/{dst}", quality=93)
json.dump(meta, open(f"{ST}/r2_meta.json", "w"), indent=1)
for r in meta["pairs"]: print(r["id"], r["name"], "close", r["close"], "wide", r["wide"], "spread", r["spread"])
