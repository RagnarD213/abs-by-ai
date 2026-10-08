"""One graphics pass for any video: resolved plan + mapped word timings -> one config per HyperFrames template -> renders.

Usage:
    python3 from_plan.py --plan plan_resolved.json --words words_out.json --out OUT_DIR
                         [--shots shots.json] [--only G01,G02] [--render] [--force]

Reads every plan item of the four template kinds and ignores the rest (title, study, chart, recap, phone and clips stay
softblue.py / the video's own build):

  kind "lt"                  -> lower-third/   Motivation lower third
  kind "scene", scene "fact" -> before-card/   full-screen photo + glass fact card (opaque)
  kind "l3"                  -> side-list/     the 3A left card, items land on their words
  kind "cycle"               -> cycle/         4-step loop in the left-third card

Plan items carry t0 / t1 (the resolved in and out, film seconds) and the template copy. Every time inside a graphic is
given as a PHRASE Dan says ("seven months"), resolved here to the start of its first word in words_out.json, searched
from t0 - 1.0 s to t1. A number instead of a phrase is taken as film seconds; None means "the first word under the
graphic". So the rules hold by construction: every time is a word start, a lower third's point comes in parts where Dan
says each piece, items land on the word that starts them, counters count on the number's word.

Per kind (fields beyond id / kind / t0 / t1):
  lt:    topic, point, parts [[text, phrase], ...] (joined with spaces = point; default one part on the first word),
         bar {grow, shrink, land: phrase; grow_value, grow_unit, from_value, value, unit, ratio} (optional), drift
  fact:  photo, label (disclosure chip, optional), eyebrow [text, phrase], headline [[text, phrase], ...],
         count {value, from, dur} (optional; the number starting headline part 0), detail [text, phrase] (optional),
         sweep phrase (optional), push, drift
  l3:    heading, points [..] (max 4), reveal [phrase per point], drift
  cycle: title, hue red|teal, direction cw|ccw, boxes [TL, TR, BR, BL], reveal {TL: phrase, ...}, close phrase,
         pulse phrase, drift  (a flip scene: cycle_kind "flip", old_title, old_boxes, title_swap, flip {corner: phrase})

a / b of a card that moves Dan (l3, cycle) snap to a shot boundary within 0.7 s (--shots), so the reframe hides in a
cut. Fit is checked here before any render: the lower third and the fact card are single-line nowrap layouts.

Writes OUT/configs/<template>/<id>.json, OUT/renders/<id>.mov (+ <id>_mask.mov for a lower third), OUT/manifest.json
(what composite.py needs), OUT/BEATS.md + OUT/beats.json (the beat sheet for the review page). A scene whose config is
unchanged and whose .mov exists is not re-rendered (--force re-renders).
"""
import argparse, hashlib, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hfbuild as H                                  # noqa: E402
B = H.B
FPS = 30000 / 1001
TEMPLATE = {"lt": "lower-third", "fact": "before-card", "l3": "side-list", "cycle": "cycle"}
NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
       "nine": "9", "ten": "10", "twelve": "12", "fifteen": "15", "twenty": "20", "thirty": "30", "forty": "40",
       "fifty": "50", "hundred": "100", "ninety": "90", "first": "first", "percent": "%"}
SNAP = 0.7


def fr(t): return int(round(t * FPS))


def norm(s):
    s = re.sub(r"[^a-z0-9%]", "", s.lower())
    return NUM.get(s, s)


class Words:
    def __init__(self, path):
        self.w = [w for w in json.load(open(path)) if w.get("t0") is not None]
        self.tok = [norm(w["w"]) for w in self.w]

    def at(self, phrase, lo, hi, what):
        """Start of the first word of `phrase` inside [lo, hi]; number = film seconds; None = first word >= lo."""
        if isinstance(phrase, (int, float)): return float(phrase)
        if phrase is None:
            return next(w["t0"] for w in self.w if w["t0"] >= lo - 0.01)
        p = [norm(x) for x in re.split(r"[\s\-]+", phrase) if norm(x)]
        for i in range(len(self.tok)):
            if not (lo - 0.01 <= self.w[i]["t0"] <= hi): continue
            j, ok = i, True
            for q in p:
                while j < len(self.tok) and self.tok[j] == "": j += 1
                if j >= len(self.tok) or not (self.tok[j] == q or (len(q) > 3 and self.tok[j].startswith(q[:4]))): ok = False; break
                j += 1
            if ok: return self.w[i]["t0"]
        raise SystemExit(f"{what}: phrase {phrase!r} not found between {lo:.2f} and {hi:.2f}")

    def text(self, a, b):
        return " ".join(w["w"] for w in self.w if a <= w["t0"] < b)


def snap_edge(t, joins, what):
    j = min(joins, key=lambda x: abs(x - t)) if joins else None
    if j is not None and abs(j - t) <= SNAP: return round(j + 0.0005, 4)
    print(f"  note: {what} {t:.2f} has no shot boundary within {SNAP} s; the video's build must cut there", flush=True)
    return t


def fits(s, px, width, what, bold=True):
    w = H.text_w(s, px, bold)
    assert w <= width, f"{what}: {s!r} is {w:.0f} px, {width:.0f} px fit (shorten the copy)"


# ------------------------------------------------------------------ per template
def lt_cfg(it, W, beats):
    a, b = it["t0"], it["t1"]; at = lambda ph, what: W.at(ph, a - 1.0, b, f"{it['id']} {what}")
    parts = it.get("parts") or [[it["point"], None]]
    joined = " ".join(p for p, _ in parts)
    assert joined == it["point"], f"{it['id']}: parts join to {joined!r}, point is {it['point']!r}"
    ps = [[p, round(max(a, at(ph, p)), 3)] for p, ph in parts]
    assert all(x[1] <= y[1] for x, y in zip(ps, ps[1:])), f"{it['id']}: parts out of speech order {ps}"
    cfg = dict(id=it["id"], a=a, b=b, topic=it["topic"], parts=ps, drift=it.get("drift", -4))
    if it.get("topic_case") == "preserve": cfg["topic_case"] = "preserve"
    beats += [(a, "", "strip fades and rises, accent draws, topic " + it["topic"])]
    beats += [(t, W.text(t, t + 0.4), f"\"{p}\" rises") for p, t in ps]
    if it.get("bar"):
        bar = dict(it["bar"])
        for k in ("grow", "shrink", "land"): bar[k] = round(at(bar[k], "bar " + k), 3)
        cfg["bar"] = bar
        beats += [(bar["grow"], W.text(bar["grow"], bar["grow"] + 0.4), f"bar fills, counter 0 to {bar['grow_value']} {bar['grow_unit']}"),
                  (bar["shrink"], W.text(bar["shrink"], bar["shrink"] + 0.4), f"cyan bar retracts, counts {bar['from_value']} to {bar['value']} {bar['unit']}"),
                  (bar["land"], W.text(bar["land"], bar["land"] + 0.4), "short bar lands")]
    beats += [(b - 0.33, "", "strip fades and drops 10 px, gone on the out")]
    return cfg


def fact_cfg(it, W, beats):
    a, b = it["t0"], it["t1"]; at = lambda ph, what: round(max(a, W.at(ph, a - 1.0, b, f"{it['id']} {what}")), 3)
    U = 2.0; inner = (906 - 476 - 27 - 20) * U               # the glass card's text column
    eb = [it["eyebrow"][0], at(it["eyebrow"][1], "eyebrow")]
    head = [[p, at(ph, p)] for p, ph in it["headline"]]
    fits(eb[0], 64, inner, f"{it['id']} eyebrow")
    fits(" ".join(p for p, _ in head), 84, inner, f"{it['id']} headline")
    cfg = dict(id=it["id"], a=a, b=b, photo=it["photo"], eyebrow=eb, headline=head,
               push=it.get("push", 1.07), drift=it.get("drift", -8))
    if it.get("label"): cfg["label"] = it["label"]
    if it.get("count"): cfg["count"] = it["count"]
    if it.get("detail"):
        cfg["detail"] = [it["detail"][0], at(it["detail"][1], "detail")]
        fits(cfg["detail"][0], 46, inner, f"{it['id']} detail", bold=False)
    if it.get("sweep") is not None: cfg["sweep"] = at(it["sweep"], "sweep")
    beats += [(a, "", "photo rises in" + (" with its chip" if it.get("label") else "") + "; glass card rises"),
              (eb[1], W.text(eb[1], eb[1] + 0.4), f"\"{eb[0]}\" rises")]
    beats += [(t, W.text(t, t + 0.4), f"\"{p}\" rises" + (" and counts up" if it.get("count") and k == 0 else "")) for k, (p, t) in enumerate(head)]
    if cfg.get("detail"): beats += [(cfg["detail"][1], W.text(cfg["detail"][1], cfg["detail"][1] + 0.4), f"\"{cfg['detail'][0]}\" rises")]
    if cfg.get("sweep"): beats += [(cfg["sweep"], "", "one light sweep crosses the glass")]
    return cfg


def l3_cfg(it, W, beats):
    a, b = it["t0"], it["t1"]
    assert len(it["points"]) <= 4 and len(it["reveal"]) == len(it["points"]), f"{it['id']}: 1-4 points, one reveal each"
    rv = [round(max(a, W.at(ph, a - 1.0, b, f"{it['id']} item {k + 1}")), 3) for k, ph in enumerate(it["reveal"])]
    assert rv == sorted(rv) and rv[-1] < b - 0.6, f"{it['id']}: reveals {rv} out of order or too close to the out {b}"
    beats += [(a, "", "card rises, divider wipes, heading " + (it["heading"] if isinstance(it["heading"], str) else " / ".join(it["heading"])))]
    beats += [(t, W.text(t, t + 0.4), f"item {k + 1} lands: {p}") for k, (p, t) in enumerate(zip(it["points"], rv))]
    beats += [(b - 0.33, "", "card fades and drops, gone on the cut")]
    return dict(id=it["id"], a=a, b=b, heading=it["heading"], items=it["points"], reveal=rv, drift=it.get("drift", 0))


def cycle_cfg(it, W, beats):
    a, b = it["t0"], it["t1"]; at = lambda ph, what: round(max(a, W.at(ph, a - 1.0, b, f"{it['id']} {what}")), 3)
    kind = it.get("cycle_kind", "build")
    cfg = dict(id=it["id"], kind=kind, a=a, b=b, title=it["title"], hue=it["hue"], direction=it["direction"],
               boxes=it["boxes"], close=at(it["close"], "close"), pulse=at(it["pulse"], "pulse"), drift=it.get("drift", 0))
    fits(it["title"], 56, 740 - 60, f"{it['id']} title")
    for bx in it["boxes"]: fits(bx, 28, 278 - 24, f"{it['id']} box")
    beats += [(a, "", f"card rises, title \"{it['title']}\"")]
    if kind == "build":
        cfg["reveal"] = {k: at(v, "box " + k) for k, v in it["reveal"].items()}
        for k, t in sorted(cfg["reveal"].items(), key=lambda x: x[1]):
            beats += [(t, W.text(t, t + 0.4), f"box {k} lands: {it['boxes']['TL TR BR BL'.split().index(k)]}")]
    else:
        cfg.update(old_title=it["old_title"], old_boxes=it["old_boxes"], title_swap=at(it["title_swap"], "title swap"),
                   flip={k: at(v, "flip " + k) for k, v in it["flip"].items()})
        beats += [(cfg["title_swap"], W.text(cfg["title_swap"], cfg["title_swap"] + 0.4), f"title turns to \"{it['title']}\"")]
        for k, t in sorted(cfg["flip"].items(), key=lambda x: x[1]):
            beats += [(t, W.text(t, t + 0.4), f"box {k} flips")]
    beats += [(cfg["close"], W.text(cfg["close"], cfg["close"] + 0.4), "last arrow draws, loop closes"),
              (cfg["pulse"], W.text(cfg["pulse"], cfg["pulse"] + 0.4), "one pulse, then a light travels the loop"),
              (b - 0.33, "", "card fades and drops, gone on the cut")]
    return cfg


BUILD = {"lt": lt_cfg, "fact": fact_cfg, "l3": l3_cfg, "cycle": cycle_cfg}


def tkind(it):
    if it["kind"] == "scene": return "fact" if it.get("scene") == "fact" else None
    return it["kind"] if it["kind"] in ("lt", "l3", "cycle") else None


def render_scene(tk, cfg, out, force):
    tpl = TEMPLATE[tk]
    cdir = out / "configs" / tpl; cdir.mkdir(parents=True, exist_ok=True)
    rdir = out / "renders"; rdir.mkdir(parents=True, exist_ok=True)
    body = json.dumps([cfg], indent=1, sort_keys=True)
    sha = hashlib.sha256((body + (HERE / tpl / f"{tpl}.template.htm").read_text() + (HERE / tpl / "build.py").read_text()).encode()).hexdigest()[:16]
    cpath = cdir / f"{cfg['id']}.json"; stamp = rdir / f"{cfg['id']}.cfg.sha"
    movs = [rdir / f"{cfg['id']}.mov"] + ([rdir / f"{cfg['id']}_mask.mov"] if tk == "lt" else [])
    cpath.write_text(body)
    if not force and stamp.exists() and stamp.read_text() == sha and all(m.exists() for m in movs):
        print(cfg["id"], "unchanged, render kept", flush=True); return movs
    for m in movs:
        if m.exists(): m.unlink()
    r = subprocess.run([sys.executable, str(HERE / tpl / "build.py"), str(cpath), str(rdir), "--render"])
    assert r.returncode == 0 and all(m.exists() for m in movs), f"{cfg['id']}: {tpl} build failed"
    stamp.write_text(sha)
    return movs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--words", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--shots"); ap.add_argument("--only"); ap.add_argument("--render", action="store_true"); ap.add_argument("--force", action="store_true")
    A = ap.parse_args()
    out = pathlib.Path(A.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    W = Words(A.words)
    joins = [s["out_f0"] / FPS for s in json.load(open(A.shots))] if A.shots else []
    only = set(A.only.split(",")) if A.only else None
    manifest, allbeats = [], []
    for it in json.load(open(A.plan)):
        tk = tkind(it)
        if not tk or (only and it["id"] not in only): continue
        it = dict(it)
        if tk in ("l3", "cycle") and joins:
            it["t0"] = snap_edge(it["t0"], joins, it["id"] + " in"); it["t1"] = snap_edge(it["t1"], joins, it["id"] + " out")
        beats = []
        cfg = BUILD[tk](it, W, beats)
        rd = out / "renders"
        m = dict(id=it["id"], template=TEMPLATE[tk], a=cfg["a"], b=cfg["b"], mov=str(rd / f"{it['id']}.mov"),
                 kind={"fact": "opaque", "lt": "glass"}.get(tk, "overlay"))
        if tk == "lt": m.update(mask=str(rd / f"{it['id']}_mask.mov"), band=[760, 1080])
        if tk == "l3":
            x0, y0, x1, y1 = B.left_third_box(1920, 1080, it["heading"], it["points"])
            m.update(card_right=752, card=[round(x0), round(y0), round(x1), round(y1)])
        if tk == "cycle": m.update(card_right=776, card=[36, 42, 776, 530])
        if A.render: render_scene(tk, cfg, out, A.force)
        else:
            cdir = out / "configs" / TEMPLATE[tk]; cdir.mkdir(parents=True, exist_ok=True)
            (cdir / f"{cfg['id']}.json").write_text(json.dumps([cfg], indent=1, sort_keys=True))
        manifest.append(m)
        allbeats.append(dict(id=it["id"], template=TEMPLATE[tk], a=cfg["a"], b=cfg["b"],
                             rows=[dict(t=round(t, 2), word=w, beat=bt) for t, w, bt in sorted(beats, key=lambda x: x[0])]))
        print(f"{it['id']:5s} {TEMPLATE[tk]:12s} {cfg['a']:8.2f} - {cfg['b']:8.2f}", flush=True)
    if only and (out / "manifest.json").exists():                  # merge a partial run into the existing manifest
        old = {m["id"]: m for m in json.load(open(out / "manifest.json"))}; old.update({m["id"]: m for m in manifest})
        manifest = sorted(old.values(), key=lambda m: m["a"])
        ob = {b["id"]: b for b in json.load(open(out / "beats.json"))}; ob.update({b["id"]: b for b in allbeats})
        allbeats = sorted(ob.values(), key=lambda b: b["a"])
    json.dump(manifest, open(out / "manifest.json", "w"), indent=1)
    json.dump(allbeats, open(out / "beats.json", "w"), indent=1)
    md = ["# Beat sheet (HyperFrames templates, from_plan.py)", "",
          "Film times are the output timeline; every time is the start of the word Dan says.", ""]
    for bb in allbeats:
        md += [f"## {bb['id']} {bb['template']}, {bb['a']:.2f} to {bb['b']:.2f}", "", "| film s | word | beat |", "|---|---|---|"]
        md += [f"| {r['t']:.2f} | {r['word']} | {r['beat']} |" for r in bb["rows"]] + [""]
    (out / "BEATS.md").write_text("\n".join(md))
    print(len(manifest), "graphics;", out / "manifest.json", flush=True)


if __name__ == "__main__":
    main()
