"""Shots: EDL pieces split at measured silences >= 0.70 s (tightened to ~0.42 s: 0.24 s tail + 0.18 s lead), then pure
reframe cuts in any shot over 18 s at sentence gaps. Multi-roll: every shot carries its roll. The 'set' piece (the live
20-second hold) is never tightened or split. Framing is solved in build.py. Output: shots.json on the output timeline."""
import json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl as E
W = E.W; FPS = E.FPS; SR = E.SR
NOSPLIT = {"set1", "set2", "set3"}
# pure reframe cuts inside the repeated hold (source seconds): each set changes size once, at a different moment; set 2 opens on its lead-in and goes near as the hold starts (35.08), not while he is still standing up
SETCUT = {"set1": [45.08], "set2": [35.08, 43.58], "set3": [46.58]}
# pauses kept on purpose: breath 31.49 is him showing the short nose breath; types 6.51 would leave a 1.2 s shot
KEEP = {("rest2", 31.49)}      # him showing the short nose breath (RO-02 kept it too)
def frames_db(roll, t0, t1, hop=0.01):
    A = E.lav(roll); ts = np.arange(t0, t1, hop)
    return ts, np.array([20*np.log10(np.sqrt(np.mean(A[int(t*SR):int((t+0.02)*SR)]**2))+1e-9) for t in ts])
def silences(roll, a, b, min_len=0.70):
    ts, db = frames_db(roll, a, b); q = db < E.thr(roll); res = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            s, e = ts[i], ts[j-1]+0.02
            if e-s >= min_len and s > a+0.3 and e < b-0.3: res.append((s, e))
            i = j
        else: i += 1
    return res
def quietest(roll, a, b):
    ts, db = frames_db(roll, a, b, 0.01); k = int(np.argmin([db[i:i+4].mean() for i in range(max(1, len(db)-3))])); return ts[k]+0.02
P = json.load(open(f"{W}/edl.json")); S = []; CUT = []
for p in P:
    cuts = [(p["in"], None)]
    if p["id"] not in NOSPLIT:
        for s, e in silences(p["roll"], p["in"], p["out"]):
            if (p["id"], round(float(s), 2)) in KEEP: continue
            cuts[-1] = (cuts[-1][0], s+0.24); cuts.append((e-0.18, None)); CUT.append((p["id"], round(float(s), 2), round(float(e), 2)))
    cuts[-1] = (cuts[-1][0], p["out"])
    for k, (a, b) in enumerate(cuts):
        S.append(dict(id=f"{p['id']}.{k}", piece=p["id"], roll=p["roll"], src_f0=round(a*FPS), src_f1=round(b*FPS)))
S2 = []
for sh in S:
    a, b = sh["src_f0"]/FPS, sh["src_f1"]/FPS
    if b-a <= 18.0 or sh["piece"] in NOSPLIT: S2.append(sh); continue
    WJ = json.load(open(f"{E.SHOOT}/{sh['roll']}.roll/words.json"))["words"]
    gaps = [(w1["end"], w2["start"], w1["word"].strip()[-1:]) for w1, w2 in zip(WJ, WJ[1:]) if a+4 < w1["end"] and w2["start"] < b-4 and w2["start"]-w1["end"] >= 0.22]
    cuts, last = [], a
    while b-last > 18.0:
        cand = [g for g in gaps if 9.0 <= g[0]-last <= 14.5 and b-g[1] >= 5.0]
        if not cand: cand = [g for g in gaps if 6.0 <= g[0]-last <= 17.0 and b-g[1] >= 4.0]
        if not cand: break
        g = max(cand, key=lambda g: (g[2] == ".", g[1]-g[0]))
        c = quietest(sh["roll"], g[0], g[1]); cuts.append(c); last = c
    edges = [a]+cuts+[b]
    for k, (x, y) in enumerate(zip(edges, edges[1:])):
        S2.append(dict(id=f"{sh['id']}r{k}" if cuts else sh["id"], piece=sh["piece"], roll=sh["roll"], src_f0=round(x*FPS) if k else sh["src_f0"],
                       src_f1=round(y*FPS) if k < len(edges)-2 else sh["src_f1"], reframe=bool(k)))
S3 = []
for sh in S2:
    cs = SETCUT.get(sh["piece"])
    if not cs: S3.append(sh); continue
    edges = [sh["src_f0"]]+[round(c*FPS) for c in cs]+[sh["src_f1"]]
    for k, (x, y) in enumerate(zip(edges, edges[1:])): S3.append(dict(id=f"{sh['piece']}.{k}", piece=sh["piece"], roll=sh["roll"], src_f0=x, src_f1=y, reframe=bool(k)))
S = S3; t = 0
for s in S:
    n = s["src_f1"]-s["src_f0"]; s["out_f0"] = t; s["out_f1"] = t+n; t += n
json.dump(S, open(f"{W}/shots.json", "w"), indent=1); json.dump(CUT, open(f"{W}/pauses_cut.json", "w"))
print(len(S), "shots,", t, "frames =", round(t/FPS, 2), "s =", f"{int(t/FPS//60)}:{t/FPS%60:04.1f}", "; pauses tightened", len(CUT), "; shortest", round(min(s["src_f1"]-s["src_f0"] for s in S)/FPS, 2))
for s in S:
    d = (s["src_f1"]-s["src_f0"])/FPS
    if d < 2.0 or d > 18.5: print("check:", s["id"], round(d, 2))
print("pauses:", CUT)
