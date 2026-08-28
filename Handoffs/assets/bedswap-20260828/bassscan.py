import numpy as np, wave, sys
w=wave.open(sys.argv[1],'rb'); sr=w.getframerate()
a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768.
H=int(sr*0.25); n=len(a)//H
f=np.fft.rfftfreq(H,1/sr); m=(f>=20)&(f<120)
win=np.hanning(H)
vals=np.empty(n)
for i in range(n):
    S=np.abs(np.fft.rfft(a[i*H:(i+1)*H]*win))
    vals[i]=20*np.log10(np.sqrt(np.mean(S[m]**2))+1e-9)
thr=float(sys.argv[2]) if len(sys.argv)>2 else 36.0
hot=vals>thr
# group into runs, allow 1s gaps
runs=[]; cur=None
for i,h in enumerate(hot):
    t=i*0.25
    if h:
        if cur is None: cur=[t,t]
        else: cur[1]=t
    elif cur is not None and t-cur[1]>1.0:
        runs.append(cur); cur=None
if cur: runs.append(cur)
print(f"threshold {thr} dB in 20-120 Hz; {hot.sum()} of {n} frames hot ({hot.sum()*0.25:.1f}s)")
for s,e in runs:
    seg=vals[int(s/0.25):int(e/0.25)+1]
    print(f"  {s:8.2f} - {e:8.2f}s  ({e-s+0.25:6.2f}s)  peak {seg.max():5.1f} dB  n_hot {(seg>thr).sum()}")
