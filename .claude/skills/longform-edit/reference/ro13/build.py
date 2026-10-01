"""RO-13 builder. render_range(a, b, out): graded presenter (locked look) + every plan item, hard cuts, audio B chain.
usage: build.py range <t0> <t1> <out.mp4> [--placeholder-ai]"""
import sys, os, json, subprocess, hashlib, wave, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import frames as F, gfx as G, softblue as B
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as HC                      # HyperFrames compositor: lt, fact, l3, cycle (from_plan.py renders)
HF_KINDS = ("lt", "l3", "cycle")            # + scene "fact"; every other kind stays gfx.paint (softblue)
def hf_item(it): return it["kind"] in HF_KINDS or (it["kind"] == "scene" and it.get("scene") == "fact")
W = "/Volumes/Extreme/_edit_work/ro13"; FPS = 30000/1001; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = json.load(open(f"{W}/shots.json")); R = json.load(open(f"{W}/plan_resolved.json"))
MANIFEST = f"{W}/hf/manifest.json"
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
# Audio B (WV-01 round 3, Dan: "love the audio"): its source EQ + 0.9 dB low shelf at 150 Hz, no dereverb, then -0.9 dB.
# Audio B on C1707: RO-16's EQ failed the tone row here (3.5 kHz +3.9, 5.5 kHz -5.2; RO-12 trap 4), so the chain's own fit on
# this roll (FIT.mp4.voice_chain.json, from the first minute's untreated voice) + Dan's approved +0.9 dB shelf at 150 Hz.
EQ = json.load(open(f"{W}/FIT.mp4.voice_chain.json"))["eq"] + ",bass=g=0.9:f=150:width_type=q:width=0.7"
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)

SIZE = {"W2": 3552, "W4": 2800, "W4S": 2800, "T2": 2608}
def _bad(x, y):
    """A cut between framings x and y reads as a jump when the sizes are within 1.2x (W2/W2, W4S/T2)."""
    if x is None or y is None: return 0
    r = max(SIZE[x], SIZE[y]) / min(SIZE[x], SIZE[y])
    return 1 if r < 1.2 else 0

FULL = ("scene", "title", "clip", "ai")
_SEGS = None
def all_segments():
    """Every picture segment of the film (shot joins + side-card edges) with its framing, solved once by dynamic
    programming: a join is a jump when the two framings are within 1.2x in size (W2/W2, W4S/T2), unless a full-screen
    item covers one side. Side cards (3A list, cycle) take W4S (the W4 crop slid left inside the 4K frame, preferred) or
    W2 + wall stretch; the phone takes W2 / W4 (its own shift); everything else W2 / T2 (RO-16 round-2 review)."""
    global _SEGS
    if _SEGS is not None: return _SEGS
    N = S[-1]["out_f1"]
    cards = [(fr(it["t0"]), fr(it["t1"]), it) for it in R if it["kind"] in ("l3", "cycle", "phone") and it["t1"]]
    full = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL and it["t1"]]
    cuts = sorted(set([0, N]) | {s["out_f0"] for s in S} | {a for a, b, i in cards} | {b for a, b, i in cards})
    segs = []
    for a, b in zip(cuts, cuts[1:]):
        sh = next(s for s in S if s["out_f0"] <= a < s["out_f1"])
        card = next((c for c in cards if c[0] <= a < c[1]), None)
        opts = (("W2", "W4") if card[2]["kind"] == "phone" else ("W4S", "W2")) if card else ("W2", "T2")
        cov = any(x <= a and b <= y for x, y in full)
        segs.append(dict(o0=a, o1=b, src0=sh["src_f0"] + a - sh["out_f0"], shot=sh["id"], card=card[2]["id"] if card else None,
                         opts=opts, covered=cov, shifted=bool(card)))
    INF = 10**9; cost = [{o: (0 if (not s["card"] or o == s["opts"][0]) else 1) for o in s["opts"]} for s in segs[:1]]; back = [{}]
    for i in range(1, len(segs)):
        s, p = segs[i], segs[i - 1]; c, bk = {}, {}
        for o in s["opts"]:
            pref = 0 if (not s["card"] or o == s["opts"][0]) else 1
            best = min(((cost[-1][q] + (0 if (s["covered"] or p["covered"]) else 10 * _bad(q, o)), q) for q in p["opts"]))
            c[o] = best[0] + pref; bk[o] = best[1]
        cost.append(c); back.append(bk)
    o = min(cost[-1], key=cost[-1].get); out = [None] * len(segs)
    for i in range(len(segs) - 1, -1, -1):
        out[i] = o
        if i: o = back[i][o]
    for sg, fm in zip(segs, out): sg["framing"] = fm
    _SEGS = segs
    return segs

def jumps():
    """Joins the solver could not make a clear size change (should be empty)."""
    sg = all_segments()
    return [(round(b["o0"] / FPS, 2), a["framing"], b["framing"]) for a, b in zip(sg, sg[1:])
            if not (a["covered"] or b["covered"]) and _bad(a["framing"], b["framing"])]

def framing_at(g):
    return next(s for s in all_segments() if s["o0"] <= g < s["o1"])

def segments(f0, f1):
    """Picture segments on [f0,f1), cut from the solved film segments."""
    out = []
    for s in all_segments():
        a, b = max(s["o0"], f0), min(s["o1"], f1)
        if a < b: out.append(dict(s, o0=a, o1=b, src0=s["src0"] + a - s["o0"]))
    return out

def render_seg(sg):
    key = hashlib.sha1(json.dumps([sg["src0"], sg["o1"]-sg["o0"], sg["framing"], F.CROP[sg["framing"]], F.LUT]).encode()).hexdigest()[:12]
    out = f"{W}/cache/seg_{sg['src0']}_{key}.mp4"
    if not os.path.exists(out):
        os.makedirs(f"{W}/cache", exist_ok=True)
        ts = sg["src0"]/FPS
        run([FF, "-v", "error", "-y", "-ss", f"{max(0, ts-1):.4f}", "-i", F.SRC, "-ss", f"{min(1, ts):.4f}", "-frames:v", str(sg["o1"]-sg["o0"]),
             "-vf", F.vf(sg["framing"]).replace("format=rgb24", "format=yuv420p"), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast",
             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"])
        os.rename(out + ".tmp.mp4", out)
    return out

class ClipReader:
    def __init__(self, it, fps_src=None):
        s = it["src"]; self.n0 = fr(it["t0"]); self.n1 = fr(it["t1"]); n = self.n1 - self.n0
        self.parts = []; per = n // len(s)
        for k, sp in enumerate(s):                                        # several sources = hard cuts in order
            m = per if k < len(s)-1 else n - per*(len(s)-1)
            self.parts.append((sp, m))
        self.q = []; self.it = it
    def frames(self):
        for sp, m in self.parts:
            path = G.src_path(sp); st = G.src_start(sp)
            dur = float(subprocess.run([F.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                       capture_output=True, text=True).stdout)
            assert dur - st >= m/FPS - 0.02, f"{self.it['id']}: {os.path.basename(path)} too short ({dur-st:.2f}s for {m/FPS:.2f}s) -- never hold a clip"
            if self.it["kind"] == "phone":
                vf = "fps=30000/1001,format=rgb24"; size = None
            else:
                vf = "fps=30000/1001," + G.clip_vf(self.it.get("zoom", 1.0)); size = (1920, 1080)
            p = subprocess.Popen([FF, "-v", "error", "-ss", f"{st:.3f}", "-i", path, "-frames:v", str(m), "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
            if size is None:
                w, h = map(int, subprocess.run([F.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                                "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip().split(","))
                size = (w, h)
            for _ in range(m):
                b = p.stdout.read(size[0]*size[1]*3)
                assert len(b) == size[0]*size[1]*3, f"{self.it['id']} short read"
                yield Image.frombytes("RGB", size, b)
            p.stdout.close(); p.wait()

def ai_placeholder(it, i, n):
    ph = it.get("ph", "A"); im = Image.open(f"{W}/aiframes/{ph}-{'start' if i < n/2 else 'end'}.png").convert("RGB").resize((1920, 1080))
    B.disclosure(im, "AI-GENERATED", (1866, 54), 2.0, anchor="rt")   # new A frame: his head is top-left
    B.disclosure(im, "PLACEHOLDER: " + ("START frame" if i < n/2 else "END frame") + ", motion not generated yet", (960, 990), 2.0, anchor="mt")
    return im

def render_range(a, b, out, placeholder_ai=True):
    global HCOMP
    HCOMP = HC.Compositor(json.load(open(MANIFEST)))
    f0, f1 = fr(a), fr(b); segs = segments(f0, f1)
    base = f"{W}/tmp_base.mp4"; txt = base + ".txt"
    open(txt, "w").write("".join(f"file '{render_seg(s)}'\n" for s in segs))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", base])
    items = [it for it in R if it["t1"] and it["t0"] < b and it["t1"] > a]
    readers = {it["id"]: ClipReader(it).frames() for it in items if it["kind"] in ("clip", "phone")}
    dec = subprocess.Popen([FF, "-v", "error", "-i", base, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".v.mp4"], stdin=subprocess.PIPE)
    for g in range(f0, f1):
        buf = dec.stdout.read(1920*1080*3); assert len(buf) == 1920*1080*3, g
        t = g/FPS; im = Image.frombytes("RGB", (1920, 1080), buf)
        sg = next(s for s in segs if s["o0"] <= g < s["o1"])
        act = [it for it in items if fr(it["t0"]) <= g < fr(it["t1"])]
        clip = None
        for it in act:
            if it["id"] in readers: clip = next(readers[it["id"]])
            if it["kind"] == "ai": clip = ai_placeholder(it, g - fr(it["t0"]), fr(it["t1"]) - fr(it["t0"]))
        if sg["shifted"] and sg["framing"] == "W2" and not any(x["kind"] == "phone" for x in act):
            im = B.shift_presenter(im, **G.SHIFT["W2"])          # W2 has only 144 px of room: keep the wall stretch
        pil = [x for x in act if not hf_item(x)]
        if pil:
            span = [dict(x, t0=fr(x["t0"])/FPS, t1=fr(x["t1"])/FPS) for x in pil]
            im = G.paint(im, t, span, sg["framing"], clip) if not any(x["kind"] == "ai" for x in pil) else clip
        if HCOMP.active(g):
            im = Image.fromarray(HCOMP.apply(np.asarray(im), g))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    # ---- audio: lav on the shot timeline, audio B chain
    wv = wave.open(f"{W}/lav.wav"); L = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    N = int(round((f1-f0)/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    TAILFADE = {}   # round-2 review: a breath / lip-noise onset in the last 50 ms before the cut after "carbs." (src 936.82) and "benefits." (src 1072.88); faded, no timeline change   # review r1: a breath starts in the hook take's last 50 ms (src 233.21); fade it, no timeline change
    for s in S:
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 >= o1: continue
        si = int(round((s["src_f0"] + o0 - s["out_f0"])/FPS*SR)); n = int(round((o1-o0)/FPS*SR)); at = int(round((o0-f0)/FPS*SR))
        x = L[si:si+n].copy()
        cont_in = any(p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"] for p in S)    # a reframe cut: speech runs on
        cont_out = any(n["src_f0"] == s["src_f1"] and n["out_f0"] == s["out_f1"] for n in S)
        if o0 == s["out_f0"] and not cont_in: x[:r] *= np.linspace(0, 1, r)
        if o1 == s["out_f1"] and not cont_out:
            tf = int(TAILFADE.get(s["id"], 0.010)*SR); x[-tf:] *= np.linspace(1, 0, tf)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    # room tone at every join (+/-60 ms, 20 ms ramps) from a steady stretch of this roll (src 384.5-387.5, about -65 dB, std 0.8),
    # so a join never drops below the room (review r1: 60 ms at -75 dB where the air conditioning cycled)
    rt = L[int(384.5*SR):int(387.5*SR)].copy()
    for s in S:
        j = s["out_f0"]
        if not (f0 < j < f1) or any(p["src_f1"] == s["src_f0"] and p["out_f1"] == j for p in S): continue   # no fill on a reframe cut
        c = int(round((j-f0)/FPS*SR)); h = int(0.06*SR); rp = int(0.02*SR)
        a0, a1 = max(0, c-h-rp), min(N, c+h+rp); m = np.ones(a1-a0, np.float32); m[:rp] = np.linspace(0, 1, rp); m[-rp:] = np.linspace(1, 0, rp)
        # level-matched to the outgoing shot's last 150 ms of room (review r1 re-review: a -64 dB fill was under the chain's gate)
        ref = v[max(0, c-int(0.20*SR)):max(1, c-int(0.05*SR))]; tgt = float(np.sqrt(np.mean(ref*ref))) if len(ref) else 0.0
        g = min(tgt, 10**(-50/20)) / (float(np.sqrt(np.mean(rt*rt))) + 1e-9)     # never louder than -50 dBFS raw (room, not speech)
        v[a0:a1] += rt[:a1-a0]*m*g
    raw = out + ".untreated.wav"; o = wave.open(raw, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(v, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    # WV-01's extra -0.9 dB was only the A/B audition level match; the chain's own -14 LUFS target is the delivery level.
    run(["python3", VC, "--in", raw, "--video", out + ".v.mp4", "--frame-lock", out + ".v.mp4", "--out", out, "--no-dereverb", "--eq", EQ, "--work", out + ".work"])
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out + ".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
