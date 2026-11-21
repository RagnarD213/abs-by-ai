"""Shots: EDL pieces split at measured silences >= 0.70 s (tightened to ~0.42 s: 0.24 s tail + 0.18 s lead), then framing
alternated W2/T2 on every join so no presenter join is same-framing. Frame-locked on the 29.97 source.
Output: shots.json [{id, src_f0, src_f1, framing, t0, t1, piece}] on the output timeline."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro11"; FPS = 30000/1001; SR = 48000
wv = wave.open(f"{W}/lav.wav"); A = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
def frames_db(t0, t1, hop=0.01):
    ts = np.arange(t0, t1, hop); out = []
    for t in ts:
        x = A[int(t*SR):int((t+0.02)*SR)]; out.append(20*np.log10(np.sqrt(np.mean(x*x))+1e-9))
    return ts, np.array(out)
def silences(a, b, thr=-50.0, min_len=0.70):
    ts, db = frames_db(a, b); q = db < thr; res = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            s, e = ts[i], ts[j-1]+0.02
            if e-s >= min_len and s > a+0.3 and e < b-0.3: res.append((s, e))
            i = j
        else: i += 1
    return res
P = json.load(open(f"{W}/edl.json")); S = []
for p in P:
    cuts = [(p["in"], None)]
    for s, e in silences(p["in"], p["out"]): cuts[-1] = (cuts[-1][0], s+0.24); cuts.append((e-0.18, None))
    cuts[-1] = (cuts[-1][0], p["out"])
    for k, (a, b) in enumerate(cuts):
        S.append(dict(id=f"{p['id']}.{k}", piece=p["id"], src_f0=round(a*FPS), src_f1=round(b*FPS)))
# round-2 review: P01's card (W2 + shift) exited into s5d.0 at W2 with a 147-frame source jump (same size, head moved
# ~360 px). s5d.0 goes T2 so the exit is a W2 -> T2 cut; its own exit into s6a.0 (T2) is covered by the Step 6 card.
OVERRIDE = {"s5d.0": "T2"}
# pure reframe cuts (nothing removed): a shot longer than 18 s is split at sentence gaps (>= 0.22 s between words,
# preferring a full stop) about every 9-14 s, cut at the gap's quietest 40 ms (skill Step 5.4 rule 5)
WJ = json.load(open(f"{W}/words.json"))["words"]
def quietest(a, b):
    ts, db = frames_db(a, b, 0.01); k = int(np.argmin([db[i:i+4].mean() for i in range(max(1, len(db)-3))])); return ts[k] + 0.02
S2 = []
for sh in S:
    a, b = sh["src_f0"]/FPS, sh["src_f1"]/FPS
    if b - a <= 18.0: S2.append(sh); continue
    gaps = [(w1["end"], w2["start"], w1["word"].strip()[-1:]) for w1, w2 in zip(WJ, WJ[1:]) if a + 4 < w1["end"] and w2["start"] < b - 4 and w2["start"] - w1["end"] >= 0.22]
    cuts, last = [], a
    while b - last > 18.0:
        cand = [g for g in gaps if 9.0 <= g[0] - last <= 14.5 and b - g[1] >= 5.0]
        if not cand: cand = [g for g in gaps if 6.0 <= g[0] - last <= 17.0 and b - g[1] >= 4.0]
        if not cand: break
        g = max(cand, key=lambda g: (g[2] == ".", g[1] - g[0]))
        c = quietest(g[0], g[1]); cuts.append(c); last = c
    edges = [a] + cuts + [b]
    for k, (x, y) in enumerate(zip(edges, edges[1:])):
        S2.append(dict(id=f"{sh['id']}r{k}" if cuts else sh["id"], piece=sh["piece"], src_f0=round(x*FPS) if k else sh["src_f0"], src_f1=round(y*FPS) if k < len(edges)-2 else sh["src_f1"], reframe=bool(k)))
S = S2
t = 0
for i, s in enumerate(S):
    s["framing"] = OVERRIDE.get(s["id"], "W2" if i % 2 == 0 else "T2")
    n = s["src_f1"]-s["src_f0"]; s["out_f0"] = t; s["out_f1"] = t+n; t += n
json.dump(S, open(f"{W}/shots.json", "w"), indent=1)
print(len(S), "shots,", t, "frames =", round(t/FPS, 2), "s; shortest", round(min(s["src_f1"]-s["src_f0"] for s in S)/FPS, 2), "s")
for s in S:
    if (s["src_f1"]-s["src_f0"])/FPS < 2.0: print("short:", s["id"], round((s["src_f1"]-s["src_f0"])/FPS, 2))
