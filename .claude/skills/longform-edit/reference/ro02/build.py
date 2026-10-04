"""RO-02 builder, round 2: graded presenter (colour A, hair-anchored F/N per shot) + every plan item, hard cuts, lav on
the shot timeline through the shared voice chain with the roll's fitted EQ (FIT.json).
render_range(a, b, out). usage: build.py range <t0> <t1> <out.mp4> | build.py framings"""
import sys, os, json, subprocess, hashlib, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import frames as F, edl as E, gfx as G, softblue as B
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as HC
HF_KINDS = ("lt", "l3", "cycle")
def hf_item(it): return it["kind"] in HF_KINDS or (it["kind"] == "scene" and it.get("scene") == "fact")
W = E.W; FPS = E.FPS; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = F.S; R = json.load(open(f"{W}/plan_resolved.json")) if os.path.exists(f"{W}/plan_resolved.json") else []
MANIFEST = f"{W}/hf/manifest.json"
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
EQ = json.load(open(f"{W}/FIT.json"))["eq"]
FORCE = {"set.0": "F"}                    # the live 20-second set: side-on, full torso and thighs
FULL = ("scene", "title", "clip", "opener")
CARDS = ("l3", "cycle", "anat")           # a left card: Dan's crop window slides left inside the 1080p frame
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)

_SEGS = None
def all_segments():
    """Every picture segment (shot joins + side-card edges), framing solved once by dynamic programming: two on-camera
    segments either side of a cut must differ in size (F / N, ratio 1.24), unless a full-screen item covers one side.
    Under a card F is preferred (more room for his hands); the live set is forced F."""
    global _SEGS
    if _SEGS is not None: return _SEGS
    N = S[-1]["out_f1"]
    cards = [(fr(it["t0"]), fr(it["t1"]), it) for it in R if it["kind"] in CARDS and it["t1"]]
    full = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL and it["t1"]]
    cuts = sorted(set([0, N]) | {s["out_f0"] for s in S} | {a for a, b, i in cards} | {b for a, b, i in cards})
    segs = []
    for a, b in zip(cuts, cuts[1:]):
        sh = next(s for s in S if s["out_f0"] <= a < s["out_f1"]); card = next((c for c in cards if c[0] <= a < c[1]), None)
        opts = (FORCE[sh["id"]],) if sh["id"] in FORCE else ("F", "N")
        segs.append(dict(o0=a, o1=b, src0=sh["src_f0"]+a-sh["out_f0"], shot=sh["id"], card=card[2]["id"] if card else None, opts=opts,
                         covered=any(x <= a and b <= y for x, y in full)))
    pref = lambda s, o: 1 if (s["card"] and o == "N") else 0
    cost = [{o: pref(segs[0], o) for o in segs[0]["opts"]}]; back = [{}]
    for i in range(1, len(segs)):
        s, p = segs[i], segs[i-1]; c, bk = {}, {}
        for o in s["opts"]:
            best = min((cost[-1][q] + (0 if (s["covered"] or p["covered"]) else 10*(q == o)), q) for q in p["opts"])
            c[o] = best[0]+pref(s, o); bk[o] = best[1]
        cost.append(c); back.append(bk)
    o = min(cost[-1], key=cost[-1].get)
    for i in range(len(segs)-1, -1, -1):
        segs[i]["framing"] = o
        if i: o = back[i][o]
    _SEGS = segs; return segs
def jumps():
    sg = all_segments()
    return [(round(b["o0"]/FPS, 2), a["framing"], b["framing"]) for a, b in zip(sg, sg[1:]) if not (a["covered"] or b["covered"]) and a["framing"] == b["framing"]]
def framing_at(g): return next(s for s in all_segments() if s["o0"] <= g < s["o1"])
def shot_of(sg): return next(s for s in S if s["id"] == sg["shot"])
def segments(f0, f1):
    out = []
    for s in all_segments():
        a, b = max(s["o0"], f0), min(s["o1"], f1)
        if a < b: out.append(dict(s, o0=a, o1=b, src0=s["src0"]+a-s["o0"]))
    return out
def render_seg(sg):
    s = shot_of(sg); fm = sg["framing"]; card = bool(sg["card"]); a = sg["src0"]; n = sg["o1"]-sg["o0"]
    key = hashlib.sha1(json.dumps([s["roll"], a, n, fm, F.crop(s, fm, card), F.lut(s)]).encode()).hexdigest()[:12]
    out = f"{W}/cache/seg_{s['roll']}_{a}_{key}.mp4"
    if not os.path.exists(out):
        os.makedirs(f"{W}/cache", exist_ok=True); ts = a/FPS - 0.4/FPS          # 0.4 frame early: never open on a repeated frame (RO-10 trap)
        run(["nice", "-n", "10", FF, "-v", "error", "-y", "-ss", f"{max(0, ts-1):.4f}", "-i", E.src(s["roll"]), "-ss", f"{min(1, ts):.4f}", "-frames:v", str(n),
             "-vf", F.vf(s, fm, True, card).replace("format=rgb24", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"), "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
             "-r", FPSS, "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out+".tmp.mp4"])
        os.rename(out+".tmp.mp4", out)
    return out

class ClipReader:
    def __init__(self, it): self.it = it; self.n = fr(it["t1"])-fr(it["t0"])
    def frames(self):
        sp = self.it["src"][0]; path = G.src_path(sp); st = G.src_start(sp)
        dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
        assert dur-st >= self.n/FPS-0.02, f"{self.it['id']}: {os.path.basename(path)} too short ({dur-st:.2f}s for {self.n/FPS:.2f}s): never hold a clip"
        p = subprocess.Popen([FF, "-v", "error", "-ss", f"{st:.3f}", "-i", path, "-frames:v", str(self.n), "-vf", "fps=30000/1001,"+G.clip_vf(self.it.get("zoom", 1.0)), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for _ in range(self.n):
            b = p.stdout.read(1920*1080*3); assert len(b) == 1920*1080*3, f"{self.it['id']} short read"
            yield Image.frombytes("RGB", (1920, 1080), b)
        p.stdout.close(); p.wait()

def opener_frames(t):
    """Until the motion is approved and generated: each panel alternates its START and END frame (0.8 s each)."""
    k = "start" if int(t/0.8) % 2 == 0 else "end"
    return {p: G._panel_img(f"{W}/aiframes/{p}-{k}.png") for p in ("A", "B")}, f"PLACEHOLDER: {k.upper()} frames, motion not generated yet"

def compose(im, g, items, readers, HCOMP):
    t = g/FPS; act = [it for it in items if fr(it["t0"]) <= g < fr(it["t1"])]; clip = None; of = note = None
    for it in act:
        if it["id"] in readers: clip = next(readers[it["id"]])
        if it["kind"] == "opener": of, note = opener_frames(t)
    pil = [dict(x, t0=fr(x["t0"])/FPS, t1=fr(x["t1"])/FPS) for x in act if not hf_item(x)]
    if pil: im = G.paint(im, t, pil, clip, of, note)
    if HCOMP is not None and HCOMP.active(g): im = Image.fromarray(HCOMP.apply(np.asarray(im), g))
    return im

def render_range(a, b, out):
    HCOMP = HC.Compositor(json.load(open(MANIFEST))) if os.path.exists(MANIFEST) else None
    f0, f1 = fr(a), fr(b); segs = segments(f0, f1)
    base = out+".base.mp4"; txt = base+".txt"
    open(txt, "w").write("".join(f"file '{render_seg(s)}'\n" for s in segs))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", base])
    items = [it for it in R if it["t1"] and it["t0"] < b and it["t1"] > a]
    readers = {it["id"]: ClipReader(it).frames() for it in items if it["kind"] == "clip"}
    for it in items:                                                   # a clip that began before the range: skip its earlier frames
        if it["id"] in readers:
            for _ in range(max(0, f0-fr(it["t0"]))): next(readers[it["id"]])
    dec = subprocess.Popen([FF, "-v", "error", "-i", base, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["nice", "-n", "10", FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out+".v.mp4"], stdin=subprocess.PIPE)
    for g in range(f0, f1):
        buf = dec.stdout.read(1920*1080*3); assert len(buf) == 1920*1080*3, g
        enc.stdin.write(compose(Image.frombytes("RGB", (1920, 1080), buf), g, items, readers, HCOMP).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    # ---- audio: each shot's own roll lav on the shot timeline (round 1's assembly, unchanged)
    N = int(round((f1-f0)/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    for s in S:
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 >= o1: continue
        L = E.lav(s["roll"]); si = int(round((s["src_f0"]+o0-s["out_f0"])/FPS*SR)); n = int(round((o1-o0)/FPS*SR)); at = int(round((o0-f0)/FPS*SR))
        x = L[si:si+n].copy()
        cont_in = any(p["roll"] == s["roll"] and p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"] for p in S)
        cont_out = any(q["roll"] == s["roll"] and q["src_f0"] == s["src_f1"] and q["out_f0"] == s["out_f1"] for q in S)
        if o0 == s["out_f0"] and not cont_in: x[:r] *= np.linspace(0, 1, r)
        if o1 == s["out_f1"] and not cont_out: x[-r:] *= np.linspace(1, 0, r)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    raw = out+".untreated.wav"; o = wave.open(raw, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(v, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    run(["python3", VC, "--in", raw, "--video", out+".v.mp4", "--frame-lock", out+".v.mp4", "--out", out, "--eq", EQ, "--work", out+".work"])
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out+".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    if sys.argv[1] == "framings":
        for s in all_segments(): print(f"{s['o0']/FPS:7.2f} {s['shot']:14s} {s['framing']} {'card '+s['card'] if s['card'] else ''}{' covered' if s['covered'] else ''}")
        print("same-size joins:", jumps())
