"""RO-06 builder (from the RO-10 recipe, made multi-roll). render_range(a, b, out): graded presenter (per-roll grade, W/T
framing alternated on every join; W under the side list) + every plan item, hard cuts, shared voice chain.
usage: build.py range <t0> <t1> <out.mp4> | build.py segs"""
import sys, os, json, subprocess, hashlib, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import frames as F, gfx as G, softblue as B
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as HC
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = json.load(open(f"{W}/shots.json")); R = json.load(open(f"{W}/plan_resolved.json"))
MANIFEST = f"{W}/hf/manifest.json"
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)
def hf_item(it): return it["kind"] in ("lt", "l3") or (it["kind"] == "scene" and it.get("scene") == "fact")
FULL = ("scene", "clip")
OVERRIDE = {}
_SEGS = None
def cont(p, s): return p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"]      # a reframe cut: the same take runs on
def all_segments():
    """One picture segment per shot, framing solved for the whole film (dynamic programming, W or T each):
    a real join (different take or a removed pause) at the same framing with no full-screen cover is a jump (cost 10);
    a shot under the side list must be W (Dan stands right of the card only in the camera frame);
    a shot mostly under a lower third prefers T (in W the strip sits on the equipment at his feet);
    a reframe cut inside one take prefers to change framing (that is the point of it)."""
    global _SEGS
    if _SEGS is not None: return _SEGS
    cards = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "l3"]
    full = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL]
    lts = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "lt"]
    segs = []
    for s in S:
        n = s["out_f1"]-s["out_f0"]; under = sum(max(0, min(b, s["out_f1"])-max(a, s["out_f0"])) for a, b in lts)
        segs.append(dict(o0=s["out_f0"], o1=s["out_f1"], src0=s["src_f0"], shot=s["id"], roll=s["roll"],
                         forced=any(a < s["out_f1"] and s["out_f0"] < b for a, b in cards), lt=under > 0.45*n,
                         covered_in=any(a <= s["out_f0"] < b for a, b in full)))
    def own(sg, o):
        if sg["shot"] in OVERRIDE: return 0 if OVERRIDE[sg["shot"]] == o else 1000
        if sg["forced"]: return 0 if o == "W" else 1000
        return 1.0 if (sg["lt"] and o == "W") else 0.0
    def pair(k, q, o):
        if q != o: return 0.0
        if cont(S[k-1], S[k]): return 0.6
        return 0.0 if segs[k]["covered_in"] else 10.0
    cost = [{o: own(segs[0], o) + (0.2 if o == "T" else 0) for o in "WT"}]; back = [{}]      # open on the camera frame
    for k in range(1, len(segs)):
        c, bk = {}, {}
        for o in "WT":
            best = min((cost[-1][q] + pair(k, q, o), q) for q in "WT"); c[o] = best[0] + own(segs[k], o); bk[o] = best[1]
        cost.append(c); back.append(bk)
    o = min(cost[-1], key=cost[-1].get)
    for k in range(len(segs)-1, -1, -1):
        segs[k]["framing"] = o
        if k: o = back[k][o]
    _SEGS = segs; return segs
def jumps():
    sg = all_segments()
    return [(round(b["o0"]/FPS, 2), a["shot"], b["shot"], a["framing"]) for k, (a, b) in enumerate(zip(sg, sg[1:]))
            if a["framing"] == b["framing"] and not cont(S[k], S[k+1]) and not b["covered_in"]]
def segments(f0, f1):
    out = []
    for s in all_segments():
        a, b = max(s["o0"], f0), min(s["o1"], f1)
        if a < b: out.append(dict(s, o0=a, o1=b, src0=s["src0"] + a - s["o0"]))
    return out
def render_seg(sg):
    crop = F.crop_of(sg["shot"], sg["framing"]); roll, lf = F.roll_of(sg["src0"])
    vf = F.vf(roll, crop).replace("format=rgb24", "format=yuv420p")
    if sg["framing"] == "T": vf = vf.replace(",format=yuv420p", ",unsharp=5:5:0.5:5:5:0.0,format=yuv420p")   # 1.3-1.5x punch on a 1080p roll
    key = hashlib.sha1(json.dumps([sg["src0"], sg["o1"]-sg["o0"], vf]).encode()).hexdigest()[:12]
    out = f"{W}/cache/seg_{sg['src0']}_{key}.mp4"
    if not os.path.exists(out):
        os.makedirs(f"{W}/cache", exist_ok=True)
        ts = lf/FPS; ss_in = max(0, ts-1)
        run([FF, "-v", "error", "-y", "-ss", f"{ss_in:.4f}", "-i", F.ROLLS[roll]["path"], "-ss", f"{max(0, ts-ss_in-0.4/FPS):.4f}", "-frames:v", str(sg["o1"]-sg["o0"]),
             "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast",
             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"])
        os.rename(out + ".tmp.mp4", out)
    return out
def clip_frames(it):
    n = fr(it["t1"]) - fr(it["t0"]); s = it["src"]; per = n // len(s)
    for k, sp in enumerate(s):
        m = per if k < len(s)-1 else n - per*(len(s)-1)
        path = G.src_path(sp); st = G.src_start(sp)
        dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
        assert dur - st >= m/FPS - 0.02, f"{it['id']}: {os.path.basename(path)} too short ({dur-st:.2f}s for {m/FPS:.2f}s) -- never hold a clip"
        vf = "fps=30000/1001," + G.clip_vf(1.0)
        if it.get("grade"): vf = vf.replace(",format=rgb24", f",format=gbrp,{F.GR[it['grade']][F.LOOK]},format=rgb24")
        p = subprocess.Popen([FF, "-v", "error", "-ss", f"{st:.3f}", "-i", path, "-frames:v", str(m), "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for _ in range(m):
            b = p.stdout.read(1920*1080*3); assert len(b) == 1920*1080*3, f"{it['id']} short read"
            yield Image.frombytes("RGB", (1920, 1080), b)
        p.stdout.close(); p.wait()
def render_range(a, b, out, audio=True):
    HCOMP = HC.Compositor(json.load(open(MANIFEST)))
    f0, f1 = fr(a), fr(b); segs = segments(f0, f1)
    base = out + ".base.mp4"; txt = base + ".txt"
    open(txt, "w").write("".join(f"file '{render_seg(s)}'\n" for s in segs))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", base])
    items = [it for it in R if it["t0"] < b and it["t1"] > a]
    readers = {it["id"]: clip_frames(it) for it in items if it["kind"] == "clip"}
    dec = subprocess.Popen([FF, "-v", "error", "-i", base, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".v.mp4"], stdin=subprocess.PIPE)
    for g in range(f0, f1):
        buf = dec.stdout.read(1920*1080*3); assert len(buf) == 1920*1080*3, g
        im = Image.frombytes("RGB", (1920, 1080), buf)
        for it in items:
            if it["kind"] == "clip" and fr(it["t0"]) <= g < fr(it["t1"]):
                im = next(readers[it["id"]])
                if it.get("label"): G.ai_chip(im)
        if HCOMP.active(g): im = Image.fromarray(HCOMP.apply(np.asarray(im), g))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    if not audio: os.replace(out + ".v.mp4", out); return
    wv = wave.open(f"{W}/lav.wav"); wv.setpos(0); L = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    N = int(round((f1-f0)/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    for k, s in enumerate(S):
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 >= o1: continue
        si = int(round((s["src_f0"] + o0 - s["out_f0"])/FPS*SR)); n = int(round((o1-o0)/FPS*SR)); at = int(round((o0-f0)/FPS*SR))
        x = L[si:si+n].copy()
        cin = k > 0 and cont(S[k-1], s); cout = k < len(S)-1 and cont(s, S[k+1])
        if o0 == s["out_f0"] and not cin: x[:r] *= np.linspace(0, 1, r)
        if o1 == s["out_f1"] and not cout: x[-r:] *= np.linspace(1, 0, r)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    raw = out + ".untreated.wav"; o = wave.open(raw, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(v, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    eq = ["--eq", json.load(open(f"{W}/FIT.voice_chain.json"))["eq"]] if os.path.exists(f"{W}/FIT.voice_chain.json") else []
    run(["python3", VC, "--in", raw, "--video", out + ".v.mp4", "--frame-lock", out + ".v.mp4", "--out", out, "--work", out + ".work"] + eq)
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out + ".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)
if __name__ == "__main__":
    if sys.argv[1] == "segs":
        sg = all_segments(); print(len(sg), "segments; W", sum(s["framing"] == "W" for s in sg), "T", sum(s["framing"] == "T" for s in sg)); print("jumps:", jumps())
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
