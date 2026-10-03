"""Concatenate the EDL's lav ranges (5 ms fades) into assembled_untreated.wav + a piece map on the assembled timeline."""
import json, wave, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl as E
W = E.W; SR = E.SR; FPS = E.FPS
P = json.load(open(f"{W}/edl.json")); out = []; t = 0.0; M = []; r = int(0.005*SR)
for p in P:
    f0 = round(p["in"]*FPS); f1 = round(p["out"]*FPS)
    x = E.lav(p["roll"])[int(round(f0/FPS*SR)):int(round(f1/FPS*SR))].copy(); x[:r] *= np.linspace(0, 1, r); x[-r:] *= np.linspace(1, 0, r)
    M.append(dict(id=p["id"], roll=p["roll"], src_f0=f0, src_f1=f1, t0=t, t1=t+len(x)/SR)); out.append(x); t += len(x)/SR
y = np.concatenate(out); o = wave.open(f"{W}/assembled_untreated.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
o.writeframes((np.clip(y, -1, 1)*32767).astype("<i2").tobytes()); o.close()
json.dump(M, open(f"{W}/piece_map.json", "w"), indent=1); print("assembled", round(t, 2), "s,", len(M), "pieces")
