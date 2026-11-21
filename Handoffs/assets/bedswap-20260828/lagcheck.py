import numpy as np, wave, sys
SR=44100
def rd(p,t0,dur,mono=True):
    w=wave.open(p,'rb'); sr=w.getframerate(); ch=w.getnchannels(); w.setpos(int(t0*sr))
    a=np.frombuffer(w.readframes(int(dur*sr)),dtype=np.int16).astype(np.float64)/32768.
    if ch>1: a=a.reshape(-1,ch).mean(axis=1)
    return a
def best_lag(a,b,maxms=60):
    m=int(SR*maxms/1000); best=None
    for L in range(-m,m+1):
        if L<0: x,y=a[-L:],b[:len(b)+L]
        else:   x,y=a[:len(a)-L],b[L:]
        c=float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12))
        if best is None or c>best[1]: best=(L,c)
    return best
A,B,t0,d = sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
L,c = best_lag(rd(A,t0,d), rd(B,t0,d))
print(f"{A}  vs  {B}  @{t0}s: lag {L:+5d} samples = {L/SR*1000:+7.3f} ms   corr {c:.4f}")
