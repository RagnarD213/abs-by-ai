"""RO-16 builder. render_range(a, b, out): graded presenter (locked look) + every plan item, hard cuts, audio B chain.
usage: build.py range <t0> <t1> <out.mp4> [--placeholder-ai]"""
import sys, os, json, subprocess, hashlib, wave, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import frames as F, gfx as G, softblue as B
W = "/Volumes/Extreme/_edit_work/ro16"; FPS = 30000/1001; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = json.load(open(f"{W}/shots.json")); R = json.load(open(f"{W}/plan_resolved.json"))
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
# Audio B (WV-01 round 3, Dan: "love the audio"): its source EQ + 0.9 dB low shelf at 150 Hz, no dereverb, then -0.9 dB.
EQ = ("highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+1.02,equalizer=f=194:t=q:w=1.3:g=+1.75,equalizer=f=316:t=q:w=1.3:g=+0.67,"
      "equalizer=f=490:t=q:w=1.3:g=-1.37,equalizer=f=735:t=q:w=1.3:g=-3.29,equalizer=f=1122:t=q:w=1.3:g=-2.00,"
      "equalizer=f=1755:t=q:w=1.3:g=-0.80,equalizer=f=2775:t=q:w=1.3:g=+0.99,equalizer=f=4387:t=q:w=1.3:g=+0.87,"
      "treble=g=+1.13:f=6500:width_type=q:width=0.6,bass=g=0.9:f=150:width_type=q:width=0.7")
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)

def segments(f0, f1):
    """Picture segments on [f0,f1): shot framing, or W2/W3 alternating (shifted) while a side card is up."""
    cards = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in ("l3", "phone")]
    cuts = set([f0, f1]) | {s["out_f0"] for s in S} | {a for a, b in cards} | {b for a, b in cards}
    cuts = sorted(c for c in cuts if f0 <= c <= f1)
    segs = []
    for a, b in zip(cuts, cuts[1:]):
        sh = next(s for s in S if s["out_f0"] <= a < s["out_f1"])
        card = next((c for c in cards if c[0] <= a < c[1]), None)
        if card:
            # W2 and W4 (1.27x) alternate at every join inside a card. Round-2 review: the card's LAST framing must differ in
            # size from the shot it cuts to when a join sits on the card's exit (W2 into a W2 shot read as a jump at P01's exit;
            # W3, only 1.14x, read as a jump inside G20), so the parity is chosen from the exit.
            k = sum(1 for s in S if card[0] < s["out_f0"] <= a)        # joins passed inside this card
            m = sum(1 for s in S if card[0] < s["out_f0"] < card[1])  # joins inside the card
            nxt = next((s for s in S if s["out_f0"] == card[1]), None)  # a shot that starts exactly at the card's exit
            flip = 1 if (nxt is not None and nxt["framing"] == "W2") else 0   # end on W4 before a W2 shot, on W2 before T2
            fm = "W2" if (k + m + flip) % 2 == 0 else "W4"
        else: fm = sh["framing"]
        segs.append(dict(o0=a, o1=b, src0=sh["src_f0"] + a - sh["out_f0"], framing=fm, shifted=bool(card)))
    return segs

def render_seg(sg):
    key = hashlib.sha1(json.dumps([sg["src0"], sg["o1"]-sg["o0"], sg["framing"], F.LUT]).encode()).hexdigest()[:12]
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
    ph = "A"; im = Image.open(f"{W}/aiframes/{ph}-{'start' if i < n/2 else 'end'}.png").convert("RGB").resize((1920, 1080))
    B.disclosure(im, "AI-GENERATED", (1866, 54), 2.0, anchor="rt")   # new A frame: his head is top-left
    B.disclosure(im, "PLACEHOLDER: " + ("START frame" if i < n/2 else "END frame") + ", motion not generated yet", (960, 990), 2.0, anchor="mt")
    return im

def render_range(a, b, out, placeholder_ai=True):
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
        if act:
            # items are painted with frame-exact spans
            span = [dict(x, t0=fr(x["t0"])/FPS, t1=fr(x["t1"])/FPS) for x in act]
            im = G.paint(im, t, span, sg["framing"], clip) if not any(x["kind"] == "ai" for x in act) else clip
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    # ---- audio: lav on the shot timeline, audio B chain
    wv = wave.open(f"{W}/lav.wav"); L = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    N = int(round((f1-f0)/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    TAILFADE = {"hook.0": 0.08, "s6d.0": 0.07}   # round-2 review: a breath / lip-noise onset in the last 50 ms before the cut after "carbs." (src 936.82); faded, no timeline change. Round 3: the "s8b.0" fade is gone (that burst was the start of the "s" of "benefits", not a lip noise; the piece now runs past the word)   # review r1: a breath starts in the hook take's last 50 ms (src 233.21); fade it, no timeline change
    for s in S:
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 >= o1: continue
        si = int(round((s["src_f0"] + o0 - s["out_f0"])/FPS*SR)); n = int(round((o1-o0)/FPS*SR)); at = int(round((o0-f0)/FPS*SR))
        x = L[si:si+n].copy()
        if o0 == s["out_f0"]: x[:r] *= np.linspace(0, 1, r)
        if o1 == s["out_f1"]:
            tf = int(TAILFADE.get(s["id"], 0.010)*SR); x[-tf:] *= np.linspace(1, 0, tf)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    # room tone at every join (+/-60 ms, 20 ms ramps) from a steady stretch of this roll (src 1082.0-1085.0, about -64 dB),
    # so a join never drops below the room (review r1: 60 ms at -75 dB where the air conditioning cycled)
    rt = L[int(1082.0*SR):int(1085.0*SR)].copy()
    for s in S:
        j = s["out_f0"]
        if not (f0 < j < f1): continue
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
