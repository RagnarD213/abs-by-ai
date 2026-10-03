"""RO-02 builder, round 1 (cut + look only; graphics and clips join in round 2 from ../ro13/build.py's plan loop).
render_range(a, b, out): graded presenter on fixed F/N compositions that alternate at every join, hard cuts, lav on the
shot timeline through the shared voice chain. usage: build.py range <t0> <t1> <out.mp4>"""
import sys, os, json, subprocess, hashlib, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import frames as F, edl as E
W = E.W; FPS = E.FPS; FF = F.FF; SR = 48000
S = F.S
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
FORCE = {"set.0": "F"}                    # the live 20-second set: side-on, full torso and thighs
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)
def framings():
    """N/F alternating at every shot join (ratio 1.24, a clear size change). The opening size is whichever makes the
    forced shot (the live set, F) fall on its own turn, so no join is ever same-size."""
    k = next(i for i, x in enumerate(S) if x["id"] in FORCE); want = FORCE[S[k]["id"]]
    first = want if k % 2 == 0 else ("N" if want == "F" else "F")
    return {x["id"]: (first if i % 2 == 0 else ("N" if first == "F" else "F")) for i, x in enumerate(S)}
FR = framings()
def jumps():
    return [(S[i]["id"], FR[S[i]["id"]]) for i in range(1, len(S)) if FR[S[i]["id"]] == FR[S[i-1]["id"]]]
def render_seg(s, a, b):
    """source frames [a,b) of shot s, graded and framed; cached."""
    fm = FR[s["id"]]; key = hashlib.sha1(json.dumps([s["roll"], a, b, fm, F.crop(s, fm), F.lut(s)]).encode()).hexdigest()[:12]
    out = f"{W}/cache/seg_{s['roll']}_{a}_{key}.mp4"
    if not os.path.exists(out):
        os.makedirs(f"{W}/cache", exist_ok=True); ts = a/FPS - 0.4/FPS          # 0.4 frame early: never open on a repeated frame (RO-10 trap)
        run(["nice", "-n", "10", FF, "-v", "error", "-y", "-ss", f"{max(0, ts-1):.4f}", "-i", E.src(s["roll"]), "-ss", f"{min(1, ts):.4f}", "-frames:v", str(b-a),
             "-vf", F.vf(s, fm).replace("format=rgb24", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"), "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
             "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out+".tmp.mp4"])
        os.rename(out+".tmp.mp4", out)
    return out
def render_range(a, b, out, eq=None):
    f0, f1 = fr(a), fr(b); parts = []
    for s in S:
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 < o1: parts.append(render_seg(s, s["src_f0"]+o0-s["out_f0"], s["src_f0"]+o1-s["out_f0"]))
    txt = out+".txt"; open(txt, "w").write("".join(f"file '{p}'\n" for p in parts))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", out+".v.mp4"])
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
    cmd = ["python3", VC, "--in", raw, "--video", out+".v.mp4", "--frame-lock", out+".v.mp4", "--out", out, "--work", out+".work"]
    if eq: cmd += ["--eq", eq]
    run(cmd); print("built", out, f1-f0, "frames", flush=True)
if __name__ == "__main__":
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    if sys.argv[1] == "framings":
        print(" ".join(f"{k}:{v}" for k, v in FR.items())); print("same-size joins:", jumps())
