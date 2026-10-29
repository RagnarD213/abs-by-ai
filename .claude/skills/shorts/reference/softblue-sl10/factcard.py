#!/usr/bin/env python3
"""SL-10 B: the film's approved G15 fact card (wine photo, "2 GLASSES A NIGHT / 1,700 CALORIES / a week + 7 nights of bad sleep.",
same copy, same word timing, same push/drift/sweep) rebuilt with the approved before-card template (HyperFrames) at the Short's
1080 x 1610 picture area under the title band (the SL-16 tyson_card.py method). Plays as a fill cover (plans COVERS B "fact").
Card ends at picture y 1050 (canvas 1360): the captions keep their normal line at 1412.
  python3 factcard.py [--render]"""
import json, pathlib, sys
sys.path.insert(0, "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H
WORK = pathlib.Path("/Volumes/Expansion/_edit_work/SL-10")
A = 236.77                                   # film time of the cover's first frame (the film's G15 t0)
T = lambda film: round(film - A, 3)
photo = dict(x=40, y=30, w=1000, h=560, src="assets/photo.jpg")
card = [40, 620, 1000, 430]
cx = card[0] + 54
x2 = round(cx + H.text_w("1,700 ", 84), 1)
cfg = dict(id="winefact", dur=round(249.87 - A, 3), push=1.06, drift=-8, canvas=[1080, 1610], photo=photo, chip=None, card=card,
           eyebrow=dict(x=cx, y=card[1] + 30, s="2 GLASSES A NIGHT", t=T(236.80)),
           head=[dict(x=cx, y=card[1] + 128, s="1,700", t=T(240.46)), dict(x=x2, y=card[1] + 128, s="CALORIES", t=T(241.84))],
           detail=dict(x=cx + 2, y=card[1] + 262, s="a week + 7 nights of bad sleep.", t=T(243.76)), sweep=T(246.38))
assert H.text_w("1,700 CALORIES", 84) <= card[2] - 54 - 30 and H.text_w(cfg["detail"]["s"], 46, False) <= card[2] - 84
tpl = pathlib.Path("/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/before-card/before-card.template.htm")
out = WORK / "build/B/hf"; out.mkdir(parents=True, exist_ok=True)
json.dump(cfg, open(out / "wine_fact.json", "w"), indent=1)
pd = H.make_scene(tpl, cfg, out / "proj_winefact", [(str(WORK / "clips/wine.jpg"), "photo.jpg")])
print("scene", pd, "dur", cfg["dur"])
if "--render" in sys.argv:
    H.lint_check(pd); H.render(pd, str(WORK / "clips/wine_fact.mov")); print("rendered", WORK / "clips/wine_fact.mov")
