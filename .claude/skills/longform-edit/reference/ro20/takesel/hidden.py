"""hidden speech scan over the planned ranges: (a) word gaps >= 0.6 s that hold loud lav (a take Whisper dropped),
(b) words >= 0.9 s: their loud/quiet structure (a pause or a false start folded into the word)."""
import json, sys, wave, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/takesel")
from takeplan import RANGES
SR = 48000
wv = wave.open("/Volumes/Extreme/_edit_work/ro20/lav.wav"); A = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
W = json.load(open("/Volumes/Extreme/_edit_work/ro20/words.json"))["words"]
def db(t0, t1):
    ts = np.arange(t0, t1, 0.01); return ts, np.array([20*np.log10(np.sqrt(np.mean(A[int(t*SR):int((t+0.02)*SR)]**2))+1e-9) for t in ts])
def runs(t0, t1, thr=-40.0):
    ts, d = db(t0, t1); q = d > thr; out = []; i = 0
    while i < len(q):
        j = i
        while j < len(q) and q[j] == q[i]: j += 1
        out.append((round(float(ts[i]), 2), round(float(ts[j-1])+0.01, 2), bool(q[i]))); i = j
    return out
for r in RANGES:
    rid, a, b = r[0], r[1], r[2]
    ws = [w for w in W if w["start"] >= a-0.06 and w["end"] <= b+0.06]
    if not ws or abs(ws[0]["start"]-a) > 0.06 or abs(ws[-1]["end"]-b) > 0.06: print(f"!! {rid}: range edges do not sit on words: first {ws[0]['start'] if ws else None} last {ws[-1]['end'] if ws else None}")
    for w1, w2 in zip(ws, ws[1:]):
        g = w2["start"]-w1["end"]
        if g >= 0.6:
            rr = runs(w1["end"]+0.08, w2["start"]-0.05); loud = sum(y-x for x, y, l in rr if l)
            if loud >= 0.20: print(f"GAP  {rid}: {w1['word'].strip()} [{w1['end']:.2f}] .. [{w2['start']:.2f}] {w2['word'].strip()}  gap {g:.2f}s loud {loud:.2f}s  " + " ".join(f"{x:.2f}-{y:.2f}" for x, y, l in rr if l and y-x >= 0.05))
    for w in ws:
        d = w["end"]-w["start"]
        if d >= 0.9:
            rr = runs(w["start"], w["end"]); quiet = [(x, y) for x, y, l in rr if not l and y-x >= 0.15]
            print(f"LONG {rid}: {w['word'].strip()} {w['start']:.2f}-{w['end']:.2f} ({d:.2f}s) quiet inside: " + (" ".join(f"{x:.2f}-{y:.2f}" for x, y in quiet) or "none") + "  loud: " + " ".join(f"{x:.2f}-{y:.2f}" for x, y, l in rr if l and y-x >= 0.05))
