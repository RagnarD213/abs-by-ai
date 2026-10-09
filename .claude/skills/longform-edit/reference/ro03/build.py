"""RO-03 builder (from RO-02 round 3; adds the flash into each set and the music bed): graded presenter (colour A, hair-anchored F/N per shot) + every plan item, hard cuts, lav on
the shot timeline through the shared voice chain with the roll's fitted EQ (FIT.json).
render_range(a, b, out). usage: build.py range <t0> <t1> <out.mp4> | build.py framings"""
import sys, os, json, subprocess, hashlib, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import frames as F, edl as E, gfx as G, softblue as B, bed as BD
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as HC
HF_KINDS = ("lt", "l3", "cycle")
def hf_item(it): return it["kind"] in HF_KINDS or (it["kind"] == "scene" and it.get("scene") == "fact")
W = E.W; FPS = E.FPS; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = F.S; R = json.load(open(f"{W}/plan_resolved.json")) if os.path.exists(f"{W}/plan_resolved.json") else []
MANIFEST = f"{W}/hf/manifest.json"
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
EQ = json.load(open(f"{W}/FIT.json"))["eq"]
TRIM = {"C1626": 1.2, "C1624": -1.7}       # dB, constant per roll: raw speech level read -17.1 (C1626), -14.1 (C1624), -15.6 (C1625), -15.3 (C1629)
FORCE = {"set1.0": "F", "set1.1": "N", "set2.0": "F", "set2.1": "N", "set2.2": "F", "set3.0": "F", "set3.1": "N"}   # the hold three times: each set changes size once (Muhammad punches in inside his sets)
FULL = ("scene", "title", "clip", "opener")
CARDS = ()           # a left card: Dan's crop window slides left inside the 1080p frame
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

MARKS = json.load(open(f"{W}/marks.json")) if os.path.exists(f"{W}/marks.json") else dict(flashes=[])
def bloom_frame(k, w=1920, h=1080):
    """Muhammad's silent bloom flash (RO-12 build.py, measured off his ab-wheel HD master): double pulse around the cut."""
    env = {-5: (0.30, 0.45), -4: (1.0, 3.0), -3: (0.15, 0.45), -2: (0.80, 0.65), -1: (0.95, 0.80), 0: (0.85, 0.75),
           1: (0.90, 0.90), 2: (0.50, 0.70), 3: (0.25, 0.55), 4: (0.10, 0.45)}
    if k not in env: return None
    a, rad = env[k]
    yy, xx = np.mgrid[0:h:4, 0:w:4].astype(np.float32)
    d = np.sqrt(((xx - w*1.02)/(w*rad))**2 + ((yy - h*0.45)/(h*rad*1.2))**2)
    core = np.clip(1.0 - d, 0, 1)**1.3; fringe = np.clip(1.35 - d, 0, 1)**2.0
    col = np.stack([0.75*fringe + core, 0.85*fringe + core, fringe + core], -1).clip(0, 1)*a
    return np.array(Image.fromarray((col*255).astype(np.uint8)).resize((w, h), Image.BILINEAR), np.float32)/255
def flash(im, g):
    for f0 in MARKS["flashes"]:
        b = bloom_frame(g - f0)
        if b is not None:
            x = np.asarray(im).astype(np.float32)/255; im = Image.fromarray(((1 - (1 - x)*(1 - b))*255).astype(np.uint8))
    return im

FILM_AUDIO = f"{W}/film_audio.wav"
TARGET = float(os.environ.get("RO03_TARGET", "-14.5"))   # the chain settles at +2.9 dB: speech alone reads -13.4 LUFS. Pushing the film to -14.0 took +5 dB and crushed the speech (spread 5.9 dB, tone max 2.58)
def film_audio():
    """The whole film's sound: each shot's own roll lav (constant per-roll trim) on the shot timeline, the bed, the shared chain."""
    N = int(round(S[-1]["out_f1"]/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    for s in S:
        L = E.lav(s["roll"]); si = int(round(s["src_f0"]/FPS*SR)); n = int(round((s["out_f1"]-s["out_f0"])/FPS*SR)); at = int(round(s["out_f0"]/FPS*SR))
        x = L[si:si+n].copy()*10**(TRIM.get(s["roll"], 0.0)/20)
        cont_in = any(p["roll"] == s["roll"] and p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"] for p in S)
        cont_out = any(q["roll"] == s["roll"] and q["src_f0"] == s["src_f1"] and q["out_f0"] == s["out_f1"] for q in S)
        if not cont_in: x[:r] *= np.linspace(0, 1, r)
        if not cont_out: x[-r:] *= np.linspace(1, 0, r)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    raw = f"{W}/film_untreated.wav"; o = wave.open(raw, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(v, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    if os.path.exists(f"{W}/bed_full.wav"): os.remove(f"{W}/bed_full.wav")
    BD.build()
    run(["python3", VC, "--in", raw, "--out", FILM_AUDIO, "--eq", EQ, "--tp", "-2.8", "--oversample", "4", "--work", f"{W}/tmp/film_audio.work", "--bed", f"{W}/bed_full.wav", "--bed-db", str(BD.BED_DB), "--target", str(TARGET)])

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

_OP = {}
def _opener_clip(p):
    """The approved AI motion (round 3): aiframes/A.mp4 (crunches) and B.mp4 (sit-ups), START to END then reversed, read
    once at panel size (850 x 478, the whole 16:9 frame)."""
    if p not in _OP:
        raw = subprocess.run([FF, "-v", "error", "-i", f"{W}/aiframes/{p}.mp4", "-vf", "scale=850:478:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        n = len(raw)//(850*478*3); _OP[p] = [Image.frombytes("RGB", (850, 478), raw[i*850*478*3:(i+1)*850*478*3]) for i in range(n)]
    return _OP[p]
def opener_frames(t):
    g = fr(t); out = {}
    for p in ("A", "B"):
        c = _opener_clip(p); assert g < len(c), f"opener clip {p} too short: never hold a clip"
        out[p] = c[g]
    return out, None

def compose(im, g, items, readers, HCOMP):
    t = g/FPS; act = [it for it in items if fr(it["t0"]) <= g < fr(it["t1"])]; clip = None; of = note = None
    for it in act:
        if it["id"] in readers: clip = next(readers[it["id"]])
        if it["kind"] == "opener": of, note = opener_frames(t)
    pil = [dict(x, t0=fr(x["t0"])/FPS, t1=fr(x["t1"])/FPS) for x in act if not hf_item(x)]
    if pil: im = G.paint(im, t, pil, clip, of, note)
    if HCOMP is not None and HCOMP.active(g): im = Image.fromarray(HCOMP.apply(np.asarray(im), g))
    return flash(im, g)

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
    # ---- audio: a slice of the FILM's finished mix (film_audio.wav, one pass of the shared chain over the whole film), so a
    # review clip sounds exactly like the film. The chain sets loudness per file; run per clip it made the speech louder.
    if not os.path.exists(FILM_AUDIO): film_audio()
    w = wave.open(FILM_AUDIO); w.setpos(int(round(f0/FPS*SR))); x = w.readframes(int(round((f1-f0)/FPS*SR))); w.close()
    sl = out+".slice.wav"; o = wave.open(sl, "w"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes(x); o.close()
    run([FF, "-v", "error", "-y", "-i", out+".v.mp4", "-i", sl, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{(f1-f0)/FPS:.3f}", out])
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out+".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "audio": film_audio()
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    if sys.argv[1] == "framings":
        for s in all_segments(): print(f"{s['o0']/FPS:7.2f} {s['shot']:14s} {s['framing']} {'card '+s['card'] if s['card'] else ''}{' covered' if s['covered'] else ''}")
        print("same-size joins:", jumps())
