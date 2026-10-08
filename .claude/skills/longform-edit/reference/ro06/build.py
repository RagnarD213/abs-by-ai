"""RO-06 builder (from the RO-10 recipe, made multi-roll). render_range(a, b, out): graded presenter (per-roll grade, three
fixed sizes solved for the whole film, round 2: tight by default; W under the side list) + every plan item, hard cuts, shared voice chain.
usage: build.py range <t0> <t1> <out.mp4> | build.py voice <t0> <t1> <out.mp4> | build.py segs [seconds to list]"""
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
OVERRIDE = {"hook.0r0": "X", "hook.0r1": "W",          # round 2 (Dan): open tight, B-roll, then the wide that shows the equipment
            "hook.0r2+c": "T", "exc1.0": "X", "exc2.0r0": "T", "exc2.0r1": "X",   # first minute: tight on the punch lines, medium between
            "exc3.0r0": "W",                              # "the stuff in front of me right here": the wide, motivated
            "exc3.0r1b": "T"}                             # he leans and points at the equipment ("I still recommend this stuff"): too big a move for the tight
HOLD = 22.0                                              # one size never holds longer than this with nothing else changing
CLOSE = ("C1580", "C1581")                               # the camera frame is already tighter than Dan's tight shot
_SEGS = None
def cont(p, s): return p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"]      # a reframe cut: the same take runs on
def klass(shot):
    v = F.SF[shot["id"]]
    return "wide" if v["zt"] == 1.5 else ("close" if shot["roll"] in CLOSE else "medium")
def options(sg):
    """{size: own cost}. Wide rolls: X tight (the default), T medium, W the camera frame (the equipment at his feet: only
    when asked for, on an active shot, or under the side list). Medium rolls: their 1.3x T is already hair to shorts.
    Close rolls: the camera frame."""
    if sg["key"] in OVERRIDE: return {OVERRIDE[sg["key"]]: 0.0}
    if sg["forced"]: return {"W": 0.0}
    k, act = sg["klass"], sg["active"]
    if k == "wide":
        o = {"T": 1.0, "W": 0.0} if act else {"X": 0.0, "T": 0.5, "W": 1.5}
        if sg["lt"]: o["W"] += 3.0                                    # in W the strip sits on the equipment at his feet
        return o
    if k == "medium": return {"W": 0.0, "T": 3.0} if act else {"T": 0.0, "W": 0.8}
    return {"W": 0.0, "T": 3.0} if act else {"W": 0.0, "T": 0.8}
def size(sg, o): return 1920.0/F.crop_of(sg["shot"], o)[0]*F.SF[sg["shot"]]["xw_med"]     # how big he is on screen
def same_take(a, b): return a["shot"] == b["shot"] or cont(SBY[a["shot"]], SBY[b["shot"]])
def pair(a, qa, b, qb):
    if b["covered_in"]: return 0.0
    r = size(a, qa)/size(b, qb); near = 1/1.2 < r < 1.2
    if same_take(a, b): return 0.0 if qa == qb else (10.0 if near else 0.3)        # no cut needed inside one take
    return 10.0 if near else 0.0                                                    # a real join needs a real size change
SBY = {s["id"]: s for s in S}
def all_segments():
    """One picture segment per shot (a shot is split where a full-screen clip or card starts inside it, so the picture may
    come back at another size), framing solved for the whole film: dynamic programming over the sizes each shot allows,
    then no size holds over HOLD seconds, then every run of one take at one size shares ONE crop (no shift at a non-cut)."""
    global _SEGS
    if _SEGS is not None: return _SEGS
    cards = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "l3"]
    full = sorted((fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL)
    lts = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "lt"]
    segs = []
    for s in S:
        edges = [s["out_f0"]] + [a for a, b in full if s["out_f0"] < a < s["out_f1"]] + [s["out_f1"]]
        for j, (o0, o1) in enumerate(zip(edges, edges[1:])):
            n = o1-o0; under = sum(max(0, min(b, o1)-max(a, o0)) for a, b in lts)
            hid = sum(max(0, min(b, o1)-max(a, o0)) for a, b in full)
            segs.append(dict(o0=o0, o1=o1, src0=s["src_f0"] + o0 - s["out_f0"], shot=s["id"], roll=s["roll"],
                             key=s["id"] + ("" if j == 0 else "+c" + (str(j) if j > 1 else "")), klass=klass(s), active=F.SF[s["id"]]["active"],
                             forced=any(a < o1 and o0 < b for a, b in cards), lt=under > 0.45*max(1, n-hid),
                             covered_in=any(a <= o0 < b for a, b in full)))
    cost = [dict(options(segs[0]))]; back = [{}]
    for k in range(1, len(segs)):
        c, bk = {}, {}
        for o, own in options(segs[k]).items():
            best = min((cost[-1][q] + pair(segs[k-1], q, segs[k], o), q) for q in cost[-1]); c[o] = best[0] + own; bk[o] = best[1]
        cost.append(c); back.append(bk)
    o = min(cost[-1], key=cost[-1].get)
    for k in range(len(segs)-1, -1, -1):
        segs[k]["framing"] = o
        if k: o = back[k][o]
    def runs():
        out, cur = [], [0]
        for k in range(1, len(segs)):
            if same_take(segs[k-1], segs[k]) and segs[k-1]["framing"] == segs[k]["framing"]: cur.append(k)
            else: out.append(cur); cur = [k]
        return out + [cur]
    def longest(run):                                                 # the longest stretch of this run on screen with no cover
        a, b = segs[run[0]]["o0"], segs[run[-1]]["o1"]; best = (0, a, a); t = a
        for x, y in full + [(b, b)]:
            if y <= a or x > b: continue
            if x - t > best[0]: best = (x - t, t, x)
            t = max(t, y)
        return best
    for _ in range(200):                                              # the hold rule: flip a middle shot of a long run
        done = True
        for run in runs():
            n, x, y = longest(run)
            if n/FPS <= HOLD or len(run) < 2: continue
            mid = (x + y)/2; alt = {"X": "T", "T": "X"} if segs[run[0]]["klass"] == "wide" else {"T": "W", "W": "T"}
            for k in sorted(run, key=lambda k: abs((segs[k]["o0"] + segs[k]["o1"])/2 - mid)):
                q = alt.get(segs[k]["framing"]); sg = segs[k]
                if q is None or q not in options(sg) or options(sg)[q] >= 3 or sg["o1"] <= x or sg["o0"] >= y: continue
                if k and pair(segs[k-1], segs[k-1]["framing"], sg, q) >= 10: continue
                if k < len(segs)-1 and pair(sg, q, segs[k+1], segs[k+1]["framing"]) >= 10: continue
                sg["framing"] = q; done = False; break
        if done: break
    for run in runs():                                                # one crop per run
        cs = [F.crop_of(segs[k]["shot"], segs[k]["framing"]) for k in run]; w = [segs[k]["o1"] - segs[k]["o0"] for k in run]
        cw, ch = max(cs)[:2]; x0 = sum(c[2]*n for c, n in zip(cs, w))/sum(w); y0 = min(c[3] for c in cs)
        crop = (cw, ch, int(min(max(0, round(x0/2)*2), 1920-cw)), int(min(y0, 1080-ch)))
        for k in run: segs[k]["crop"] = crop; segs[k]["zoom"] = round(1920/cw, 3)
    _SEGS = segs; return segs
def jumps():
    sg = all_segments()
    return [(round(b["o0"]/FPS, 2), a["key"], b["key"], a["framing"], b["framing"]) for a, b in zip(sg, sg[1:])
            if not same_take(a, b) and pair(a, a["framing"], b, b["framing"]) >= 10]
def holds():
    sg = all_segments(); full = sorted((fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL); out = []; a = 0
    cuts = [s["o0"] for p, s in zip(sg, sg[1:]) if p["crop"] != s["crop"] or not same_take(p, s)] + [x for xy in full for x in xy] + [sg[-1]["o1"]]
    for c in sorted(set(cuts)):
        if not any(x <= a < y for x, y in full): out.append((round((c-a)/FPS, 1), round(a/FPS, 2)))
        a = c
    return sorted(out, reverse=True)[:8]
def segments(f0, f1):
    out = []
    for s in all_segments():
        a, b = max(s["o0"], f0), min(s["o1"], f1)
        if a < b: out.append(dict(s, o0=a, o1=b, src0=s["src0"] + a - s["o0"]))
    return out
SHARP = "unsharp=5:5:{a}:5:5:0.0"
def sharpen(zoom):                                       # a punch-in on a 1080p roll is an enlargement: restore edge contrast in step with it
    return None if zoom < 1.1 else SHARP.format(a=0.5 if zoom < 1.7 else TIGHT_SHARP)
TIGHT_SHARP = 0.9
def render_seg(sg):
    crop = sg["crop"]; roll, lf = F.roll_of(sg["src0"])
    vf = F.vf(roll, crop).replace("format=rgb24", "format=yuv420p")
    if sharpen(sg["zoom"]): vf = vf.replace(",format=yuv420p", f",{sharpen(sg['zoom'])},format=yuv420p")
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
def voice_shots():
    """Shots as the voice track is cut. A picture-only split (split_shot.py) is merged back, so adding a reframe cut never
    moves a sample of approved audio (each shot is placed by its own rounded sample position)."""
    out = []
    for s in S:
        if s.get("split_of") and out and cont(out[-1], s): out[-1] = dict(out[-1], src_f1=s["src_f1"], out_f1=s["out_f1"])
        else: out.append(dict(s))
    return out
def render_range(a, b, out, audio=True, picture=True):
    HCOMP = HC.Compositor(json.load(open(MANIFEST)))
    f0, f1 = fr(a), fr(b); segs = segments(f0, f1)
    if picture: render_picture(a, b, out, f0, f1, segs, HCOMP)
    items = [it for it in R if it["t0"] < b and it["t1"] > a]
    if not audio: os.replace(out + ".v.mp4", out); return
    render_voice(out, f0, f1)
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out + ".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)
def render_picture(a, b, out, f0, f1, segs, HCOMP):
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
def render_voice(out, f0, f1):
    S = voice_shots()
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
if __name__ == "__main__":
    if sys.argv[1] == "segs":
        sg = all_segments(); tot = sum(s["o1"]-s["o0"] for s in sg)
        print(len(sg), "segments;", {o: f"{sum(s['framing'] == o for s in sg)} shots, {100*sum(s['o1']-s['o0'] for s in sg if s['framing'] == o)/tot:.0f} % of the time" for o in "XTW"})
        print("jumps:", jumps()); print("longest holds (s, at):", holds())
        for s in sg:
            if s["o0"]/FPS < float(sys.argv[2] if len(sys.argv) > 2 else 80): print(f"  {s['o0']/FPS:7.2f} {s['key']:14s} {s['roll']} {s['klass']:6s} {s['framing']} {s['crop']} x{s['zoom']}{' lt' if s['lt'] else ''}{' covered' if s['covered_in'] else ''}{' ACTIVE' if s['active'] else ''}")
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    if sys.argv[1] == "voice": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], picture=False)   # picture kept, voice track rebuilt
