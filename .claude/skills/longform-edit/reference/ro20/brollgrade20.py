"""RO-20 round 2 (Dan, 2026-10-11: "Color correct all B-roll used in this video and all videos going forward"): every clip of
Dan's own footage is graded to sit with the presenter under look D. Per clip: measure his skin (skin.py) on three frames, then a
skin-anchored curve lifts the skin median and its 90th percentile to the presenter's own (measured on the round 1 first minute),
with the highlights rolled off and the black point kept; saturation moves toward the presenter's when it is far off.
Writes round2/broll_grades.json {clip id: ffmpeg filter} (read by gfx.clip_vf) and round2/broll/<id>.jpg (presenter | before | after).
usage: brollgrade20.py [ids...]      then LOOK at every still: a number is not a look."""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import gfx as G, softblue as B
from measure import grab as _grab0
from skin import skin
def grab(path, t, vf=""):
    """BT.709 decode to RGB FIRST, then the grade (curves works in RGB: fed YUV it converts with the BT.601 default and tints the picture)"""
    f = "scale=960:540:in_color_matrix=bt709:in_range=tv,format=gbrp" + ("," + vf if vf else "") + ",format=rgb24"
    b = subprocess.run([G.FF, "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-vf", f, "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(540, 960, 3).astype(np.float32)/255
W = "/Volumes/Extreme/_edit_work/ro20"; OUT = f"{W}/round2/broll"; FM = f"{W}/round1/first-minute/DRAFT - RO-20 round 1 - first minute.mp4"
EXTRA = ["B0427", "B0429", "B0462", "B0032", "B0450"]          # the pickup pictures
OVER = json.load(open(f"{OUT}/overrides.json")) if os.path.exists(f"{OUT}/overrides.json") else {}     # {id: {"k": gain cap or fixed target, "sat": x}} after the look
def med(L, k): return float(np.median([x[k] for x in L]))
def presenter():
    L = [x for x in (skin(grab(FM, t)) for t in (3.0, 12.0, 33.0, 44.0, 49.0)) if x]
    return dict(y=med(L, "y"), y90=med(L, "y90"), s=med(L, "s"), h=med(L, "h"))
def dur(p): return float(subprocess.run([G.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def measure(path, vf=""):
    d = dur(path); L = [x for x in (skin(grab(path, d*f, vf)) for f in (0.2, 0.5, 0.8)) if x]
    return dict(y=med(L, "y"), y90=med(L, "y90"), s=med(L, "s"), h=med(L, "h"), p995=med(L, "p995"), n=med(L, "n")) if L else None
def curve(m, T, o):
    """One gain from BOTH skin readings: the median (his shaded side) and the 90th percentile (the sunlit side), each against the
    presenter's. In hard sun the median alone asks for far too much and flattens the lit skin (B0429, B0450: looked duller graded).
    Never darkens, never more than 2x (past that the clip is a swap, not a grade), and the highlights keep their own level."""
    k = o.get("k") or (min(T["y"]/m["y"], 2.2)*min(T["y90"]/m["y90"], 2.2))**0.5; k = min(max(k, 1.0), o.get("kmax", 2.0))
    if k < 1.10: return None, 1.0
    ym = m["y"]*k; y9 = min(m["y90"]*k, 0.82); top = min(0.985, max(m["p995"], m["y90"] + 0.08)); yt = max(top, min(0.975, y9 + 0.05))
    pts = [(0, 0), (round(m["y"]*0.25, 4), round(m["y"]*0.25*min(k, 1.2), 4)), (round(m["y"], 4), round(ym, 4)), (round(m["y90"], 4), round(y9, 4)), (round(top, 4), round(min(yt, 0.99), 4)), (1, 1)]
    assert all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(pts, pts[1:])), pts
    return "curves=all='" + " ".join(f"{x}/{y}" for x, y in pts) + "'", k
def grade(cid, T):
    p = G.lib_path(cid); m = measure(p)
    if not m: return None, None, "no skin found"
    o = OVER.get(cid, {})
    if o.get("skip"): return None, dict(before=m, after=m, gain=1.0, sat=1.0, note=o["skip"]), None
    c, k = curve(m, T, o); f = [c] if c else []
    sr = o.get("sat") or (T["s"]/m["s"] if T["s"]/m["s"] > 1.12 else 1.0); sr = min(max(sr, 1.0), 1.15)     # only ever a small lift for a washed clip
    if abs(sr - 1) > 0.02: f.append(f"eq=saturation={sr:.2f}")
    vf = ",".join(f) or None; a = measure(p, vf) if vf else m
    return vf, dict(before=m, after=a, gain=round(k, 2), sat=round(sr, 2)), None
def still(cid, vf, T, pres):
    p = G.lib_path(cid); t = dur(p)*0.5; w, h = 640, 360
    def fr(v): return Image.fromarray((grab(p, t, v)*255).astype("uint8")).resize((w, h))
    s = Image.new("RGB", (3*w, h + 26), (10, 14, 22)); s.paste(pres, (0, 26)); s.paste(fr(""), (w, 26)); s.paste(fr(vf or ""), (2*w, 26)); d = ImageDraw.Draw(s)
    for i, lab in enumerate(("presenter, look D", f"{cid} before", f"{cid} after" if vf else f"{cid} unchanged (already matches)")): d.text((i*w + 8, 6), lab, fill=(255, 255, 120))
    s.save(f"{OUT}/{cid}.jpg", quality=90)
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); T = presenter(); print("presenter skin under look D:", {k: round(v, 3) for k, v in T.items()})
    ids = sys.argv[1:] or sorted({s.split("@")[0] for it in json.load(open(f"{W}/plan_resolved.json")) if it["kind"] == "clip" and it.get("people") == "dan" for s in it.get("src", []) if not s.startswith("/")} | set(EXTRA))
    pres = Image.fromarray((grab(FM, 12.0)*255).astype("uint8")).resize((640, 360))
    GJ = json.load(open(f"{W}/round2/broll_grades.json")) if os.path.exists(f"{W}/round2/broll_grades.json") else {}; REP = json.load(open(f"{OUT}/report.json")) if os.path.exists(f"{OUT}/report.json") else {}
    for cid in ids:
        vf, rep, err = grade(cid, T)
        if err: print(f"{cid}: {err}"); REP[cid] = dict(error=err); GJ.pop(cid, None); still(cid, None, T, pres); continue
        if vf: GJ[cid] = vf
        else: GJ.pop(cid, None)
        REP[cid] = rep; b, a = rep["before"], rep["after"]; still(cid, vf, T, pres)
        print(f"{cid}: skinY {b['y']:.3f} -> {a['y']:.3f}  y90 {b['y90']:.3f} -> {a['y90']:.3f}  sat {b['s']:.2f} -> {a['s']:.2f}  hue {b['h']:.0f}  gain {rep['gain']} {'' if vf else '(unchanged)'}", flush=True)
    json.dump(GJ, open(f"{W}/round2/broll_grades.json", "w"), indent=1); json.dump(REP, open(f"{OUT}/report.json", "w"), indent=1)
