"""RO-06 round-1 stills: every graphic and clip on its real graded frame + the speech before / during / after.
usage: stills.py [IDS...]"""
import sys, json, os, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro07/recipe")
import numpy as np
from PIL import Image
import frames as F, gfx as G, build as Bd
W = "/Volumes/Extreme/_edit_work/ro07"; OUT = f"{W}/round1/stills"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json")); WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))}
HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST)))
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
def graded(g):
    sg = next(s for s in Bd.all_segments() if s["o0"] <= g < s["o1"])
    return F.frame_src(sg["src0"] + g - sg["o0"], sg["shot"], sg["framing"]), sg
rows = []; only = set(sys.argv[1:])
for it in R:
    if only and it["id"] not in only: continue
    t1 = it["t1"]
    if it["id"] in BEATS:
        land = [r["t"] for r in BEATS[it["id"]]["rows"] if not any(k in r["beat"] for k in ("fades", "gone", "sweep", "pulse"))]
        t = max(land) + 0.9
    elif it["kind"] == "scene": t = min(t1 - .15, it["t0"] + 2.6)
    else: t = (it["t0"] + t1) / 2
    t = min(t, t1 - 0.4); g = Bd.fr(t)
    im, sg = graded(g)
    if it["kind"] == "clip":
      if it.get("frames") or not os.path.exists(G.src_path(it["src"][0])):
        im = Bd.ai_placeholder(it, 0, 2) if it.get("frames") and os.path.exists(it["frames"][0]) else Image.new("RGB", (1920, 1080), (20, 30, 44))
      else:
        sp = it["src"][0]; vf = G.clip_vf(1.0)
        if it.get("grade"):
            gk = it["grade"][0] if isinstance(it["grade"], list) else it["grade"]
            vf = vf.replace(",format=rgb24", f",format=gbrp16le,{F.GR[gk][F.LOOK]},format=rgb24")
        p = subprocess.run([G.FF, "-v", "error", "-ss", f"{G.src_start(sp) + min(1.0, (t - it['t0']) * 0.5):.3f}", "-i", G.src_path(sp), "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        im = Image.frombytes("RGB", (1920, 1080), p)
      if it.get("label") and not it.get("label_in_picture") and not it.get("frames"): G.ai_chip(im)
    else:
        im = Image.fromarray(HC.apply(np.asarray(im), g))
    im.save(f"{OUT}/{it['id']}.jpg", quality=88)
    rows.append(dict(id=it["id"], kind="fact" if it["kind"] == "scene" else it["kind"], t0=it["t0"], t1=it["t1"], still_t=round(t, 2), framing=sg["framing"], roll=sg["roll"],
                     before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1 + 5),
                     copy={k: it[k] for k in ("topic", "point", "heading", "points", "headline", "eyebrow", "detail", "label") if k in it},
                     src=[os.path.basename(s.split("@")[0]) + "@" + s.split("@")[1] for s in it.get("src", [])], note=it.get("note"), pending=it.get("pending", False)))
    print(it["id"], flush=True)
if not only: json.dump(rows, open(f"{W}/round1/stills.json", "w"), indent=1)
