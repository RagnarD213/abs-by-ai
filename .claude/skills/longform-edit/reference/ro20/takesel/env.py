"""print loud/quiet runs of the lav in a window. usage: env.py t0 t1 [thr] [more windows as t0:t1]"""
import sys, wave, numpy as np
SR = 48000
def runs(t0, t1, thr=-43.0):
    wv = wave.open("/Volumes/Extreme/_edit_work/ro20/lav/C1511.wav"); wv.setpos(int(t0*SR)); a = np.frombuffer(wv.readframes(int((t1-t0)*SR)), np.int16).astype(np.float32)/32768
    hop = 480; n = len(a)//hop - 1
    db = np.array([20*np.log10(np.sqrt(np.mean(a[i*hop:i*hop+960]**2))+1e-9) for i in range(n)])
    q = db > thr; out = []; i = 0
    while i < n:
        j = i
        while j < n and q[j] == q[i]: j += 1
        out.append((t0+i*0.01, t0+j*0.01, bool(q[i]), float(db[i:j].max()), float(np.median(db[i:j])))); i = j
    return out
if __name__ == "__main__":
    args = sys.argv[1:]; thr = -43.0; wins = []
    k = 0
    while k < len(args):
        if ":" in args[k]: a, b = args[k].split(":"); wins.append((float(a), float(b))); k += 1
        else:
            if k+1 < len(args) and ":" not in args[k+1] and len(wins) == 0 and k == 0: wins.append((float(args[0]), float(args[1]))); k += 2
            else: thr = float(args[k]); k += 1
    for t0, t1 in wins:
        print(f"--- {t0} to {t1} thr {thr}")
        for a, b, loud, mx, med in runs(t0, t1, thr):
            if loud and b-a >= 0.03: print(f"  SPEECH {a:8.2f}-{b:8.2f} {b-a:5.2f}s max {mx:5.1f}")
            elif not loud and b-a >= 0.15: print(f"     quiet {a:8.2f}-{b:8.2f} {b-a:5.2f}s med {med:5.1f}")
