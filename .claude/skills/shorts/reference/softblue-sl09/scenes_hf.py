"""SL-09 round 2: our moving Soft Blue scenes, rendered with HyperFrames at the 1080 x 1610 picture area (under the title band):
  chart  (short I, 'Your Sleep Score Shows Who's Toxic'): Dan's real Oura sleep-score chart from Zeeshan's card (frame 1023.0,
         cropped under its cut-off title) on top with a slow push, the glass fact card under it (his card's words, title case),
         landing on Dan's words. Template: the approved before-card (canvas 1080x1610).
  compare (short J, 'Oura Ring Or WHOOP?'): two stacked glass panels, rows landing on the words that name them. New template
         compare-card/ (this folder; added to _shared/hyperframes after review).
  python3 scenes_hf.py [chart] [compare] [--snap]"""
import json, re, sys, pathlib
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H
HF = pathlib.Path(__file__).resolve().parent / "hf"
SHARED = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
W, PH = 1080, 1610
nz = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
def at(S, phrase, after=0.0):
    ws = json.load(open(f"build/{S}/words.json")); want = [nz(x) for x in phrase.split()]
    for i in range(len(ws) - len(want) + 1):
        if ws[i]["t"] >= after and all(nz(ws[i + j]["w"]) == want[j] for j in range(len(want))): return ws[i]["t"]
    raise ValueError(phrase)
def chart_cfg():
    S = "I"; a = round(1008.007 - 989.16, 3); b = at(S, "I didn't realize") - 0.06      # a: on his cut to the card
    photo = str(HF / "assets/oura_chart_1023.png"); pw = 920; ph = round(pw * 560 / 756)
    py = 36; card_y = py + ph + 30; ch = 300
    x0 = 40; cx = x0 + 54
    c = dict(id="I_chart", dur=round(b - a, 3), push=1.04, drift=-8, canvas=[W, PH],
             photo=dict(x=(W - pw) / 2, y=py, w=pw, h=ph, src="assets/photo.png"), chip=None,
             card=[x0, card_y, W - 2 * x0, ch],
             eyebrow=dict(x=cx, y=card_y + 30, s="My Oura Sleep Score", t=round(at(S, "my sleep score") - a, 3)),
             head=[dict(x=cx, y=card_y + 112, s="Toxic Relationship", t=round(at(S, "goes off a cliff") - a, 3))],
             detail=dict(x=cx + 2, y=card_y + 218, s="During It, And After It Ended", t=round(at(S, "I ended up breaking") - a, 3)),
             sweep=round(at(S, "one of the worst") - a, 3))
    assert card_y + ch <= 1066, card_y + ch
    return (SHARED / "before-card/before-card.template.htm", c, [(photo, "photo.png")]), (a, b)
def compare_cfg():
    S = "J"; a = round(1087.553 - 1066.95, 3); b = round(json.load(open(f"build/{S}/timeline.json"))["total"], 3)      # R3: b is the short's real end (a pause trim shortened it)      # a: on his cut at 18:07.55; b: the end of the short (the card holds over "And for some people, there's no subscription and the cost is low")
    x, wd, pad, hp, rp, ck, rh = 48, 984, 44, 54, 42, 48, 78
    def panel(head, t_head, rows, y, until):
        rs = []; ry = 128
        for s, t in rows:
            assert H.text_w(s, rp) <= wd - 2 * pad - ck - 26 - 10, (s, H.text_w(s, rp))
            rs.append(dict(s=s, y=ry, h=rh, ty=round((rh - rp * 1.4) / 2, 1), t=round(t - a, 3))); ry += rh + 6
        return dict(head=head, head_px=hp, pad=pad, head_y=22, div_y=104, x=x, y=y, w=wd, h=ry + 10, ck=ck, row_px=rp, rows=rs,
                    t=round(t_head - a, 3), until=round(until - a, 3))
    tb = at(S, "Advantages of the WHOOP") - 0.1
    p1 = panel("Oura Ring", a + 0.0, [("More Accurate", at(S, "More accuracy")), ("On Your Finger: The Better Spot", at(S, "It's on your finger")),
                                     ("Better App", at(S, "Better app")), ("More Actionable Insights", at(S, "More actionable insights"))], 150, tb)
    p2 = panel("WHOOP", tb, [("Better For Workout Tracking", at(S, "better for workout")), ("Comfier When Gripping Or Typing", at(S, "more comfortable when")),
                             ("Wrist-Based, Easy To Move", at(S, "Some people prefer"))], 150 + p1["h"] + 26, b)
    assert p2["y"] + p2["h"] <= 1066, p2["y"] + p2["h"]
    c = dict(id="J_compare", dur=round(b - a, 3), drift=-10, canvas=[W, PH], accent=[64, 40, 78], eyebrow=dict(x=64, y=62, px=34, s="Advantages"),
             panels=[p1, p2])
    return (HF / "compare-card/compare-card.template.htm", c, []), (a, b)
if __name__ == "__main__":
    which = [x for x in sys.argv[1:] if not x.startswith("--")] or ["chart", "compare"]
    man = json.load(open(HF / "manifest.json")) if (HF / "manifest.json").exists() else {}
    for k in which:
        (tpl, cfg, assets), (a, b) = {"chart": chart_cfg, "compare": compare_cfg}[k]()
        d = H.make_scene(tpl, cfg, HF / "proj", assets); H.lint_check(d)
        if "--snap" in sys.argv:
            for t in (0.5, cfg["dur"] / 2, cfg["dur"] - 0.4):
                for x in H.snapshot(d, [round(t, 2)]): pass
        mov = HF / "renders" / f"{cfg['id']}.mov"
        if "--render" in sys.argv: H.render(d, mov)
        man[k] = dict(id=cfg["id"], a=round(a, 3), b=round(b, 3), mov=str(mov), cfg=cfg)
        print(k, cfg["id"], "a", round(a, 3), "b", round(b, 3), "dur", cfg["dur"])
    json.dump(man, open(HF / "manifest.json", "w"), indent=1)
