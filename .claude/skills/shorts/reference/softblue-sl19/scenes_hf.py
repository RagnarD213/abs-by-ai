"""SL-19: the film's approved fact cards (RO-17 G04, G05, G15, G28b: the before-card template, same photo, same copy, same count-up)
re-laid for the Shorts picture area (1080 x 1610 under the title band), rendered with HyperFrames. Everything sits above y 1066
(canvas y 1376) so the burned captions (from canvas y 1412) land on the plain field, never on the card (SL-07 / SL-09 standard).
Photo on top, the AI chip under it where the film's photo is AI-generated, the glass fact card under that. Times land on Dan's
words in each short's build/<S>/words.json.
  python3 scenes_hf.py [A_G04 ...] [--snap] [--render]"""
import json, re, sys, pathlib
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import hfbuild as H
import plans as P
WORK = pathlib.Path("/Volumes/Extreme/_edit_work/SL-19")
HF = WORK / "hf"; TPL = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/before-card/before-card.template.htm")
W, PH = 1080, 1610
R = {x["id"]: x for x in json.load(open("/Volumes/Extreme/_edit_work/RO-17/round3/plan_resolved.json"))}
nz = lambda s: re.sub(r"[^a-z0-9$]", "", s.lower())
def words(S): return json.load(open(WORK / f"build/{S}/words.json"))
def at(S, phrase, after=0.0):
    ws = words(S); want = [nz(x) for x in phrase.split()]
    for i in range(len(ws) - len(want) + 1):
        if ws[i]["t"] >= after and all(nz(ws[i + j]["w"]) == want[j] for j in range(len(want))): return ws[i]["t"]
    raise ValueError((S, phrase))
def out_time(S, film_t):
    T = json.load(open(WORK / f"build/{S}/timeline.json"))
    for s in T["seg"]:
        if s["a"] - 1e-6 <= film_t <= s["b"] + 1e-6: return s["o0"] + film_t - s["a"]
    raise ValueError((S, film_t))
# the phrase each part lands on, as the words appear in the short's caption text (the film's phrases, re-spelled where the short writes a number)
PH_ = {"G04": dict(eyebrow="3 tablespoons", head=["170", "calories"], detail="14 grams"),
       "G05": dict(eyebrow="One cup of", head=["700", "calories"], detail="more calories than"),
       "G15": dict(eyebrow="big one-liter", head=["180", "calories"], detail="40 grams"),
       "G28b": dict(eyebrow="cup of chicken", head=["180", "calories"], detail="32 grams")}
def cfg(S, gid):
    g = R[gid]; cv = next(c for c in P.COVERS[S] if c["id"] == gid)
    a = round(out_time(S, cv["a"]), 3); b = round(out_time(S, cv["b"]), 3)
    rel = lambda t: round(max(0.0, t - a), 3)
    ph = PH_[gid]; lab = g.get("label")
    top, card_h, card_bottom = 36, 330, 1066
    gap = 120 if lab else 30
    pw = 1000; phh = card_bottom - top - card_h - gap
    px, py = (W - pw) / 2, top
    cy = py + phh + gap; card = [40, cy, W - 80, card_h]; cx = card[0] + 54
    eb = g["eyebrow"][0]; head = [p for p, _ in g["headline"]]
    inner = card[2] - 54 - 40
    assert H.text_w(eb, 64) <= inner and H.text_w(" ".join(head), 84) <= inner and H.text_w(g["detail"][0], 46, False) <= inner, gid
    t_e = at(S, ph["eyebrow"], a - 0.4); t_h = [at(S, ph["head"][0], t_e)]; t_h.append(at(S, ph["head"][1], t_h[0]))
    t_d = at(S, ph["detail"], t_h[0])
    xs, acc = [], ""
    for p in head: xs.append(round(cx + (H.text_w(acc + " ", 84) if acc else 0), 1)); acc = (acc + " " + p).strip()
    chip = None
    if lab:
        cw_ = round(H.text_w(lab, 46, False) + 80); chip = dict(x=round(px + pw / 2 - cw_ / 2), y=py + phh + 20, s=lab, w=cw_)
    ext = pathlib.Path(g["photo"]).suffix.lower()
    s = dict(id=f"{S}_{gid}", dur=round(b - a, 3), push=g.get("push", 1.06), drift=g.get("drift", -8), canvas=[W, PH],
             photo=dict(x=px, y=py, w=pw, h=phh, src="assets/photo" + ext), chip=chip, card=card,
             eyebrow=dict(x=cx, y=cy + 28, s=eb, t=rel(t_e)),
             head=[dict(x=x_, y=cy + 108, s=p, t=rel(t)) for p, t, x_ in zip(head, t_h, xs)],
             detail=dict(x=cx + 2, y=cy + 226, s=g["detail"][0], t=rel(t_d)), sweep=None)
    k = g["count"]; s["count"] = dict(value=int(k["value"]), frm=k.get("from", 0), dur=k.get("dur", 0.55), w=H.text_w(k["value"], 84), rest=head[0][len(k["value"]):])
    assert cy + card_h <= 1066
    return (TPL, s, [(g["photo"], "photo" + ext)]), (a, b)
JOBS = {"A_G04": ("A", "G04"), "A_G05": ("A", "G05"), "C_G15": ("C", "G15"), "D_G28b": ("D", "G28b")}
if __name__ == "__main__":
    which = [x for x in sys.argv[1:] if not x.startswith("--")] or list(JOBS)
    manp = HF / "manifest.json"; man = json.load(open(manp)) if manp.exists() else {}
    for k in which:
        (tpl, c, assets), (a, b) = cfg(*JOBS[k])
        d = H.make_scene(tpl, c, HF / "proj", assets); H.lint_check(d)
        if "--snap" in sys.argv: H.snapshot(d, [round(c["dur"] - 0.6, 2)])
        mov = HF / "renders" / f"{c['id']}.mov"; mov.parent.mkdir(parents=True, exist_ok=True)
        if "--render" in sys.argv: H.render(d, mov)
        man[k] = dict(id=c["id"], a=a, b=b, mov=str(mov), cfg=c)
        print(k, "a", a, "b", b, "dur", c["dur"], "eyebrow", c["eyebrow"]["t"], "head", [h["t"] for h in c["head"]], "detail", c["detail"]["t"])
    json.dump(man, open(manp, "w"), indent=1)
