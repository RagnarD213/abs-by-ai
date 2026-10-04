"""RO-02 round-2 stills: every graphic and clip on its real graded frame at a representative moment, plus the speech
before / during / after. Template kinds (lt, fact, l3) come from the HyperFrames renders through composite.py (the path
the film render uses); the rest from gfx.paint. The opener gets three stills (both playing, first X, both X's) and the
anatomy card two (each muscle as it lands). usage: stills.py [IDS...]"""
import sys, json, os
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro02/recipe")
import numpy as np
from PIL import Image
import frames as F, gfx as G, build as Bd
W = "/Volumes/Extreme/_edit_work/ro02"; OUT = f"{W}/round2/stills"; os.makedirs(OUT, exist_ok=True)
R = Bd.R; WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))} if os.path.exists(f"{W}/hf/beats.json") else {}
HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST))) if os.path.exists(Bd.MANIFEST) else None
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
def graded(g):
    sg = Bd.framing_at(g); sh = Bd.shot_of(sg)
    return F.frame_src(sh, (sg["src0"]+g-sg["o0"])/Bd.FPS, sg["framing"], True, bool(sg["card"])), sg
def still(it, t, name, note=None):
    g = Bd.fr(t); im, sg = graded(g); t1 = it["t1"] or it["t0"]+3
    if Bd.hf_item(it): im = Image.fromarray(HC.apply(np.asarray(im), g))
    else:
        clip = of = ph = None
        if it["kind"] == "clip": clip = G.clip_frame(G.src_path(it["src"][0]), G.src_start(it["src"][0])+(t-it["t0"]), it.get("zoom", 1.0))
        if it["kind"] == "opener": of = {p: G._panel_img(f"{W}/aiframes/{p}-start.png") for p in "AB"}; ph = "PLACEHOLDER: START frames, motion not generated yet"
        im = G.paint(im, g/Bd.FPS, [dict(it, t0=Bd.fr(it["t0"])/Bd.FPS, t1=Bd.fr(t1)/Bd.FPS)], clip, of, ph)
    im.save(f"{OUT}/{name}.jpg", quality=90)
    return dict(id=name, item=it["id"], kind="fact" if (it["kind"] == "scene" and it.get("scene") == "fact") else ("recap" if it["kind"] == "scene" else it["kind"]),
                t0=it["t0"], t1=it["t1"], still_t=round(t, 2), framing=sg["framing"], template=Bd.hf_item(it), moving=Bd.hf_item(it) or it["kind"] in ("anat", "count"),
                before=speech(it["t0"]-5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1+5), state=note,
                copy={k: it[k] for k in ("topic", "point", "heading", "points", "headline", "eyebrow", "detail", "label", "items", "title", "labels", "rows") if k in it},
                src=it.get("src"), note=it.get("note"), beats=BEATS.get(it["id"], {}).get("rows"))
rows = []; only = set(sys.argv[1:])
for it in R:
    if only and it["id"] not in only: continue
    t1 = it["t1"] or it["t0"]+3
    if it["kind"] == "opener":
        xa, xb = it["x"]["A"], it["x"]["B"]
        rows += [still(it, 2.0, "O01-1", "both clips playing"), still(it, xa+0.7, "O01-2", "first X on, at 'Stop doing crunches'"), still(it, min(xb+0.8, t1-0.2), "O01-3", "both X's on, at 'stop doing sit ups'")]
    elif it["kind"] == "anat":
        s1, s2 = it["stage_t"]
        rows += [still(it, s1+1.5, "AN1-1", "the six pack lights on 'rectus abdominis'"), still(it, s2+1.5, "AN1-2", "the deep muscle lights on 'transverse abdominis'")]
    else:
        if it["id"] in BEATS:
            land = [r["t"] for r in BEATS[it["id"]]["rows"] if not any(k in r["beat"].split('"')[-1] for k in ("fades", "gone", "sweep", "pulse"))]
            t = max(land)+0.9
        elif it["kind"] in ("scene", "title"): t = min(t1-.15, it["t0"]+2.2)
        elif it["kind"] == "count": t = it["hold_t"]+7.4
        else: t = (it["t0"]+t1)/2
        rows.append(still(it, min(t, t1-0.4), it["id"]))
    print(it["id"], flush=True)
if not only: json.dump(rows, open(f"{W}/round2/stills.json", "w"), indent=1)
