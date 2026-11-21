"""edge check of edl.json on the lav: what is loud just before / after every piece in and out (thr = edl.THR)."""
import json, wave, sys, numpy as np
SR = 48000; THR = -43.0
wv = wave.open("/Volumes/Extreme/_edit_work/ro20/lav.wav"); A = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
def runs(t0, t1, thr=THR):
    ts = np.arange(t0, t1, 0.01); d = np.array([20*np.log10(np.sqrt(np.mean(A[int(t*SR):int((t+0.02)*SR)]**2))+1e-9) for t in ts]); q = d > thr; out = []; i = 0
    while i < len(q):
        j = i
        while j < len(q) and q[j] == q[i]: j += 1
        if q[i] and ts[j-1]-ts[i] >= 0.03: out.append((float(ts[i]), float(ts[j-1])+0.01, float(d[i:j].max())))
        i = j
    return out
P = json.load(open("/Volumes/Extreme/_edit_work/ro20/edl.json")); allp = "-a" in sys.argv
for p in P:
    a, b = p["in"], p["out"]
    ri = runs(a-0.6, a+0.5); ro = runs(b-0.5, b+0.6)
    pre = [r for r in ri if r[0] < a-0.005]; post = [r for r in ri if r[1] > a]
    lead = (post[0][0]-a) if post else 9
    fl = []
    if pre and pre[-1][1] > a-0.45: fl.append("IN: loud %.2f-%.2f (max %.0f) before in%s" % (pre[-1][0], pre[-1][1], pre[-1][2], " RUNS ACROSS" if pre[-1][1] > a else ""))
    if lead > 0.2 or lead < 0.03: fl.append("IN: lead %.2f" % lead)
    before = [r for r in ro if r[0] < b]; after = [r for r in ro if r[1] > b+0.005]
    tail = (b-before[-1][1]) if before else 9
    if before and before[-1][1] > b: fl.append("OUT: loud runs across out (%.2f-%.2f)" % (before[-1][0], before[-1][1]))
    elif tail > 0.3 or tail < 0.06: fl.append("OUT: tail room %.2f" % tail)
    nx = [r for r in after if r[0] >= b]
    if nx and nx[0][0] < b+0.25: fl.append("OUT: next loud starts %.2f after out (%.2f-%.2f max %.0f)" % (nx[0][0]-b, nx[0][0], nx[0][1], nx[0][2]))
    if fl or allp: print(f"{p['id']:8s} in {a:8.2f} out {b:8.2f} | " + " | ".join(fl))
