"""RO-10 round-1 stills: every graphic and clip on its real graded frame, at a representative moment, plus the speech
before / during / after. Template kinds (lt, fact, l3, cycle) come from the HyperFrames renders through
hyperframes/composite.py (the same path the film render uses); the rest from gfx.paint (softblue).
usage: stills.py [IDS...]"""
import sys, json, os, io, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro10/recipe")
import numpy as np
from PIL import Image
import frames as F, gfx as G, softblue as B, build as Bd
W = "/Volumes/Extreme/_edit_work/ro10"; OUT = f"{W}/round1/stills"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json")); WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))}
HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST)))
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
def graded(g):
    sg = Bd.framing_at(g); ts = (sg["src0"] + g - sg["o0"]) / Bd.FPS
    im = F.frame_src(ts, sg["framing"])
    if sg["shifted"] and sg["framing"] == "W2" and not (sg["card"] or "").startswith("P"):
        im = B.shift_presenter(im, **G.SHIFT["W2"])
    return im, sg
rows = []; only = set(sys.argv[1:])
for it in R:
    if only and it["id"] not in only: continue
    t1 = it["t1"] or it["t0"] + 3
    if it["id"] in BEATS:                                        # after the last part / item lands (not the exit)
        land = [r["t"] for r in BEATS[it["id"]]["rows"] if not any(k in r["beat"] for k in ("fades", "gone", "sweep", "pulse"))]
        t = max(land) + 0.9
    elif it["kind"] in ("scene", "title"): t = min(t1 - .15, it["t0"] + 2.6)
    else: t = (it["t0"] + t1) / 2
    t = min(t, t1 - 0.4); g = Bd.fr(t)
    im, sg = graded(g)
    clip = None
    if it["kind"] in ("clip", "phone") and it.get("src"):
        src = G.src_path(it["src"][0])
        if it["kind"] == "clip":
            clip = G.clip_frame(src, G.src_start(it["src"][0]) + min(1.0, (t - it["t0"]) * 0.5), it.get("zoom", 1.0))
        else:
            p = subprocess.run([G.FF, "-v", "error", "-ss", "5", "-i", src, "-frames:v", "1", "-vf", "format=rgb24", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            clip = Image.open(io.BytesIO(p)).convert("RGB")
    if not Bd.hf_item(it):
        span = [dict(it, t0=Bd.fr(it["t0"]) / Bd.FPS, t1=Bd.fr(t1) / Bd.FPS)]
        im = G.paint(im, t, span, sg["framing"], clip)
    else:
        im = Image.fromarray(HC.apply(np.asarray(im), g))
    im.save(f"{OUT}/{it['id']}.jpg", quality=90)
    rows.append(dict(id=it["id"], kind=it["kind"] if not (it["kind"] == "scene" and it.get("scene") == "fact") else "fact",
                     t0=it["t0"], t1=it["t1"], still_t=round(t, 2), framing=sg["framing"], template=Bd.hf_item(it),
                     before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1 + 5),
                     copy={k: it[k] for k in ("topic", "point", "heading", "points", "headline", "eyebrow", "detail", "label", "items", "title", "boxes") if k in it},
                     src=it.get("src"), note=it.get("note"), beats=BEATS.get(it["id"], {}).get("rows")))
    print(it["id"], flush=True)
if not only: json.dump(rows, open(f"{W}/round1/stills.json", "w"), indent=1)
