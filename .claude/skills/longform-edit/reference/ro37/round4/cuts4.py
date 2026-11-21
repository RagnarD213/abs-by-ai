"""Round 4: Dan's two pause cuts. 0:11 (24 frames, the hands-on-hips pause after "more than 20 years") and 2:44 (17 frames, the silence before
"on every rep"). Writes edl4.json and cuts4.json, the plan and graphics moved to the new timeline, the list graphic that spans the 2:44 cut, and the voice."""
import json, subprocess, sys
import numpy as np
W = "/Volumes/Expansion/_edit_work/RO-37"; R3 = f"{W}/round3"; R4 = f"{W}/round4"
sys.path.insert(0, f"{W}/round1/recipe")
import frames as F, build as B
FPS = F.FPS; FF = F.FF
E3 = json.load(open(f"{R3}/edl3.json")); sh3 = B.make_shots(E3)
H = next(s["out_f1"] for s in sh3 if s["id"] == "why.0" or s["id"].startswith("why")) if 0 else next(s["out_f0"] for s in sh3 if s["id"] == "why.0")
K = next(s["out_f0"] for s in sh3 if s["id"] == "rep.0")
print("join frames", H, H / FPS, K, K / FPS)
N1T, N1H, N2 = 2, 22, 17       # 2:44 was 21 frames; two blind listens called that join too tight, so it keeps about 0.37 s between the sentences
e = [dict(p) for p in E3]
def piece(i): return next(p for p in e if p["id"] == i)
piece("hook")["out"] = round(piece("hook")["out"] - N1T / FPS, 4)
why = piece("why"); why["in"] = (round(why["in"] * FPS) + N1H - 0.3) / FPS       # 0.3 of a frame early: same source frame, keeps the piece's frame count exact
rep = piece("rep"); rep["in"] = (round(rep["in"] * FPS) + N2) / FPS
for p, w in ((piece("hook"), "tail of the pause"), (why, "hands-on-hips pause cut"), (rep, "silence before 'on every rep' cut")): p["why"] += f" | round 4: {w}"
json.dump(e, open(f"{R4}/edl4.json", "w"), indent=1)
c1, n1 = (H - N1T) / FPS, (N1T + N1H) / FPS; c2, n2 = K / FPS, N2 / FPS
json.dump([[c1, n1], [c2, n2]], open(f"{R4}/cuts4.json", "w"))
def m(t):                                    # round 3 film seconds to round 4 (the cuts are before 4:47, so both timelines agree there)
    if t >= c2 + n2: return t - n1 - n2
    if t >= c2: return c2 - n1
    if t >= c1 + n1: return t - n1
    if t >= c1: return c1
    return t
new = B.make_shots(e)
print("end frames", sh3[-1]["out_f1"], new[-1]["out_f1"], "expected", sh3[-1]["out_f1"] - 41)
def nf_(sh, i): return sum(x["out_f1"] - x["out_f0"] for x in sh if x["id"].split(".")[0] == i)
for i in ("hook", "why", "rep"): print(i, nf_(sh3, i), nf_(new, i))
assert nf_(new, "hook") == nf_(sh3, "hook") - N1T and nf_(new, "why") == nf_(sh3, "why") - N1H and nf_(new, "rep") == nf_(sh3, "rep") - N2
assert new[-1]["out_f1"] == sh3[-1]["out_f1"] - 41
a = {s["id"]: s for s in sh3}
for s in new:
    o = a.get(s["id"])
    if o is None or o["framing"] != s["framing"] or abs(o["src0"] - s["src0"]) > 1e-3: print("  shot differs", s["id"], s["framing"], s["src0"], "was", o and (o["framing"], o["src0"]))
print("shots", len(sh3), len(new))
# the plan
P = json.load(open(f"{R3}/bg_plan3.json"))
for g in P["segments"]:
    g["t0"], g["t1"] = m(g["t0"]), m(g["t1"])
    if "line_times" in g: g["line_times"] = [m(t) for t in g["line_times"]]
json.dump(P, open(f"{R4}/bg_plan4_base.json", "w"), indent=1)
# the graphics; G11 spans the 2:44 cut, so its movie loses the same frames
G = json.load(open(f"{R3}/hf3/manifest3.json"))
for x in G:
    a0, b0 = x["a"], x["b"]; x["a"], x["b"] = m(a0), m(b0)
    if a0 < c2 and b0 > c2 + n2:
        print("spans cut:", x["id"], a0, b0, x["mov"])
        q = round((c2 - a0) * FPS); out = f"{R4}/hf4/{x['id']}.mov"
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", x["mov"], "-vf", f"select='not(between(n,{q},{q + N2 - 1}))',setpts=N/(30000/1001)/TB", "-r", "30000/1001",
                        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p12le", out], check=True)
        x["mov"] = out
    assert not (x["a"] == x["b"]), x
json.dump(G, open(f"{R4}/hf4/manifest4.json", "w"), indent=1)
# the voice: same frames out, 12 ms crossfades
sr = 48000; rd = subprocess.run([FF, "-v", "error", "-i", f"{R3}/voice_A_r3.wav", "-f", "f64le", "-ac", "2", "-ar", str(sr), "-"], capture_output=True).stdout
x = np.frombuffer(rd, np.float64).reshape(-1, 2); nf = int(.012 * sr); f = np.sin(np.linspace(0, np.pi / 2, nf))[:, None] ** 2
def cut(x, t, d):
    a = int(round(t * sr)); b = a + int(round(d * sr))
    j = x[a - nf // 2:a + nf - nf // 2] * (1 - f) + x[b - nf // 2:b + nf - nf // 2] * f
    return np.concatenate([x[:a - nf // 2], j, x[b + nf - nf // 2:]])
y = cut(cut(x, c2, n2), c1, n1)
subprocess.run([FF, "-v", "error", "-y", "-f", "f64le", "-ac", "2", "-ar", str(sr), "-i", "-", "-c:a", "pcm_s24le", f"{R4}/voice_A_r4.wav"], input=y.tobytes(), check=True)
print("voice", len(x) / sr, "->", len(y) / sr, "cuts", c1, n1, c2, n2)
