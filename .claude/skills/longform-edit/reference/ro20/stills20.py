"""RO-20 round 1 stills: every graphic and clip on its real graded frame + the speech before / during / after.
Differences from stills.py: a lower third that sits over a clip is drawn over THAT clip's frame (not over the presenter the
clip hides); a clip with two or three sources shows all of them side by side; rows merge into stills.json by id, so the
page can fill in part by part. usage: stills20.py [IDS...]"""
import sys, json, os, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/recipe")
import numpy as np
from PIL import Image
import frames as F, gfx as G, build as Bd
W = "/Volumes/Extreme/_edit_work/ro20"; OUT = f"{W}/round1/stills"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{W}/plan_resolved.json")); WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))}
HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST))); SEGS = Bd.all_segments()
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b)
def graded(g):
    sg = next(s for s in SEGS if s["o0"] <= g < s["o1"])
    return F.frame_src(sg["src0"] + g - sg["o0"], sg["shot"], sg["framing"]), sg
def clip_frame(it, k, off):
    """frame of source k of a clip item, `off` seconds after that source's own start"""
    if it.get("frames"):
        return Bd.ai_placeholder(it, 0 if k == 0 else 1, 2) if os.path.exists(it["frames"][0]) else Image.new("RGB", (1920, 1080), (20, 30, 44))
    sp = it["src"][k]; vf = G.clip_vf(1.0, G.src_path(sp) if not sp.startswith("/") else sp)
    if not os.path.exists(G.src_path(sp)): return Image.new("RGB", (1920, 1080), (60, 20, 20))
    if it.get("grade"):
        gk = it["grade"][k] if isinstance(it["grade"], list) else it["grade"]
        vf = vf.replace(",format=rgb24", f",format=gbrp16le,{F.GR[gk][F.LOOK]},format=rgb24")
    p = subprocess.run([G.FF, "-v", "error", "-ss", f"{G.src_start(sp) + max(0.0, off):.3f}", "-i", G.src_path(sp), "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    im = Image.frombytes("RGB", (1920, 1080), p)
    if it.get("label") and not it.get("label_in_picture"): G.ai_chip(im)
    return im
def under(t):
    """the clip on screen at film time t, with (source index, seconds into that source), or None"""
    for c in R:
        if c["kind"] == "clip" and c["t0"] <= t < c["t1"]:
            n = len(c.get("src", [1])); per = (c["t1"] - c["t0"]) / n; k = min(n - 1, int((t - c["t0"]) / per))
            return c, k, t - c["t0"] - k * per
    return None
only = set(sys.argv[1:]); rows = []
for it in R:
    if only and it["id"] not in only: continue
    t1 = it["t1"]
    if it["id"] in BEATS:
        land = [r["t"] for r in BEATS[it["id"]]["rows"] if not any(k in r["beat"] for k in ("fades", "gone", "sweep", "pulse"))]
        t = max(land) + 0.9
    else: t = (it["t0"] + t1) / 2
    t = min(t, t1 - 0.4); g = Bd.fr(t); sg = next(s for s in SEGS if s["o0"] <= g < s["o1"]); over = None
    if it["kind"] == "clip":
        n = len(it.get("src", [1])); per = (t1 - it["t0"]) / n
        if it.get("frames"): im = clip_frame(it, 0, 0)
        elif n == 1: im = clip_frame(it, 0, min(1.0, (t - it["t0"]) * 0.5))
        else:
            im = Image.new("RGB", (1920, 1080), (13, 22, 38)); w = 1920 // n; h = int(w * 9 / 16)
            for k in range(n): im.paste(clip_frame(it, k, min(0.8, per * 0.4)).resize((w - 8, h - 4), Image.LANCZOS), (k * w + 4, (1080 - h) // 2))
    else:
        u = under(t)
        if u: im = clip_frame(u[0], u[1], u[2]); over = u[0]["id"]
        else: im, sg = graded(g)
        im = Image.fromarray(HC.apply(np.asarray(im), g))
    im.save(f"{OUT}/{it['id']}.jpg", quality=86)
    rows.append(dict(id=it["id"], kind=it["kind"], t0=it["t0"], t1=it["t1"], still_t=round(t, 2), framing=sg["framing"], roll=sg["roll"], over=over,
                     before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1 + 5),
                     copy={k: it[k] for k in ("topic", "point", "label") if k in it}, nsrc=len(it.get("src", [])),
                     src=[os.path.basename(s.split("@")[0]) + "@" + (s.split("@") + ["0"])[1] for s in it.get("src", [])], note=it.get("note"), pending=it.get("pending", False)))
    print(it["id"], flush=True)
p = f"{W}/round1/stills.json"; old = {r["id"]: r for r in json.load(open(p))} if os.path.exists(p) else {}
old.update({r["id"]: r for r in rows}); ids = {r["id"] for r in R}
json.dump(sorted([r for r in old.values() if r["id"] in ids], key=lambda r: (r["t0"], r["kind"] != "clip")), open(p, "w"), indent=1)
