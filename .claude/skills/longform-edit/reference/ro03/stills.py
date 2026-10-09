"""RO-03 round-1 stills: every graphic and clip on its real graded frame at its real time (the film's own compose path),
with the speech before / during / after. usage: stills.py"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import frames as F, gfx as G, build as Bd
W = "/Volumes/Extreme/_edit_work/ro03"; OUT = f"{W}/round1/stills"; os.makedirs(OUT, exist_ok=True)
R = Bd.R; WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]; MK = json.load(open(f"{W}/marks.json"))
BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))} if os.path.exists(f"{W}/hf/beats.json") else {}
HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST)))
def speech(a, b): return " ".join(w["w"] for w in WO if a <= w["t0"] < b and not w["piece"].startswith("set")) or "(no speech: the hold)"
def frame(t):
    g = Bd.fr(t); sg = Bd.framing_at(g); sh = Bd.shot_of(sg)
    im = F.frame_src(sh, (sg["src0"]+g-sg["o0"])/Bd.FPS, sg["framing"], True, False)
    act = [it for it in R if Bd.fr(it["t0"]) <= g < Bd.fr(it["t1"])]; clip = None
    for it in act:
        if it["kind"] == "clip": clip = G.clip_frame(G.src_path(it["src"][0]), G.src_start(it["src"][0])+(g-Bd.fr(it["t0"]))/Bd.FPS)
    pil = [dict(x, t0=Bd.fr(x["t0"])/Bd.FPS, t1=Bd.fr(x["t1"])/Bd.FPS) for x in act if not Bd.hf_item(x)]
    if pil: im = G.paint(im, g/Bd.FPS, pil, clip)
    if HC.active(g): im = Image.fromarray(HC.apply(np.asarray(im), g))
    return Bd.flash(im, g), sg
def row(sid, it, t, kind, shown, a=None, b=None, copy=None, moving=False, ctx=None):
    im, sg = frame(t); im.save(f"{OUT}/{sid}.jpg", quality=90); a = it["t0"] if a is None else a; b = it["t1"] if b is None else b
    print(sid, round(t, 2), sg["shot"], sg["framing"], flush=True)
    return dict(id=sid, item=it["id"], kind=kind, t0=a, t1=b, still_t=round(t, 2), framing=sg["framing"], shot=sg["shot"], state=shown, moving=moving, ctx=ctx,
                before=speech(a-5, a), during=speech(a, b), after=speech(b, b+5), copy=copy or {}, src=it.get("src"), note=it.get("note"), beats=BEATS.get(it["id"], {}).get("rows"))
I = {it["id"]: it for it in R}; H, Bp = MK["holds"], MK["beeps"]; rows = []
c0, t0, k0 = I["C00"], I["T00"], I["K00"]; tc = {k: t0[k] for k in ("eyebrow", "headline", "detail")}
rows.append(row("C00", c0, 1.4, "clip", "the opening shot, with the title chip", copy=tc, moving=True, ctx="first"))
rows.append(row("T00", t0, 4.4, "title", "the title chip stays through your intro line", copy=tc, moving=True, ctx="first"))
rows.append(row("K00-1", k0, H[0]-0.9, "work", "set 1, before the hold starts", a=k0["t0"], b=H[0], moving=True, ctx="first"))
rows.append(row("K00-2", k0, H[0]+12.6, "work", "set 1, holding: far framing first, near framing for the second half (this still)", a=H[0], b=Bp[0], moving=True, ctx="first"))
rows.append(row("K00-3", k0, Bp[0]+1.6, "work", "the rest countdown starts on the beep", a=Bp[0], b=H[1], moving=True, ctx="K00-rest1"))
rows.append(row("K00-4", k0, H[1]-2.6, "work", "last seconds of the rest: you start the timer and put the phone down", a=Bp[0], b=H[1], moving=True, ctx="K00-set2"))
rows.append(row("K00-5", k0, H[1]+10.0, "work", "set 2, holding (near framing first, far for the second half: this still)", a=H[1], b=Bp[1], moving=True, ctx="K00-set2"))
rows.append(row("K00-6", k0, H[2]+16.0, "work", "set 3, holding, near framing", a=H[2], b=Bp[2], moving=True, ctx="K00-end"))
rows.append(row("K00-7", k0, Bp[2]+0.7, "work", "after the last beep", a=Bp[2], b=k0["t1"], moving=True, ctx="K00-end"))
fl = MK["flashes"][0]/Bd.FPS
rows.append(row("FL1", dict(id="FL1", t0=fl-5/Bd.FPS, t1=fl+5/Bd.FPS, note="Muhammad's silent flash on the cut into each set (three in the film). Ten frames; this is its brightest frame."), fl-1/Bd.FPS, "flash", "brightest frame of the flash", moving=True, ctx="first"))
for gid in ("G01", "G02", "G03", "G04", "G05", "G06"):
    it = I[gid]; cf = json.load(open(f"{W}/hf/configs/lower-third/{gid}.json")); cf = cf[0] if isinstance(cf, list) else cf; land = max(p[1] for p in cf["parts"])+1.2
    rows.append(row(gid, it, min(land, it["t1"]-0.5), "lt", None, copy=dict(topic=it["topic"], point=it["point"]), moving=True, ctx="first" if gid == "G01" else gid))
rows.sort(key=lambda r: r["still_t"]); json.dump(rows, open(f"{W}/round1/stills.json", "w"), indent=1)
