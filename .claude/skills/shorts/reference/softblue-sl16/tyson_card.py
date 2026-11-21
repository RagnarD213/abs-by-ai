#!/usr/bin/env python3
"""SL-16 R2 (Dan 2026-10-25): Short 4 opens on a full-screen Mike Tyson quote card: his photo and the quote, on the moving Soft Blue
field. The approved before-card template (HyperFrames, _shared/hyperframes/before-card/), drawn at the Short's 1080 x 1610 picture
area (the title band stays above it): photo top, glass card under it with the eyebrow and three quote lines, each landing on the word
Dan says it, card ending above the caption line. Photo: Glenn Francis, "Mike Tyson 2019" (Wikimedia Commons, CC BY-SA 4.0); credit
the photographer in the video description at setup. Output: build/D/hf/tyson_quote.mov (opaque, plays as a fill cover).
  python3 tyson_card.py [--render]"""
import json, pathlib, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H
WORK = pathlib.Path("/Volumes/Extreme/_edit_work/SL-16")
A = 196.99                                   # the scene starts on the Short's first frame (film time of "Mike")
W_, H_ = 1080, 1610
T = lambda film: round(film - A, 3)
photo = dict(x=140, y=30, w=800, h=800, src="assets/photo.jpg")
card = [40, 862, 1000, 452]                  # x, y, w, h: ends at y 1314 (canvas 1624); captions drop to y 1650 for this shot (plans SHOTS D 0: cap 1650)
cx = card[0] + 54
cfg = dict(id="tysonquote", dur=round(202.07 - A, 3), push=1.06, drift=-8, canvas=[W_, H_], photo=photo, chip=None, card=card,
           eyebrow=dict(x=cx, y=card[1] + 26, s="MIKE TYSON", t=0.15),
           head=[dict(x=cx, y=card[1] + 112, s="Everybody Has A", t=T(198.72)),
                 dict(x=cx, y=card[1] + 216, s="Plan Until They Get", t=T(199.50)),
                 dict(x=cx, y=card[1] + 320, s="Punched In The Face.", t=T(200.70))],
           detail=None, sweep=T(201.30))
for h in cfg["head"]: assert H.text_w(h["s"], 84) <= card[2] - 54 - 30, h["s"]
tpl = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/before-card/before-card.template.htm")
out = WORK / "build/D/hf"; out.mkdir(parents=True, exist_ok=True)
json.dump(cfg, open(out / "tyson_quote.json", "w"), indent=1)
pd = H.make_scene(tpl, cfg, out / "proj_tyson", [(str(WORK / "clips/tyson_glennfrancis_ccbysa4.jpg"), "photo.jpg")])
print("scene", pd, "dur", cfg["dur"])
if "--render" in sys.argv:
    H.lint_check(pd); H.render(pd, str(out / "tyson_quote.mov")); print("rendered", out / "tyson_quote.mov")
