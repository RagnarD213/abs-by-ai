import sys, numpy as np, json
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl07"); import pickup as K
def bands(x):
    # speech frames only (top 40% RMS), 1/3-octave-ish bands, dB relative to total
    n=2048; fr=np.lib.stride_tricks.sliding_window_view(x,n)[::1024]; r=np.sqrt((fr**2).mean(1)); fr=fr[r>np.percentile(r,60)]
    S=(np.abs(np.fft.rfft(fr*np.hanning(n),axis=1))**2).mean(0); f=np.fft.rfftfreq(n,1/48000)
    ed=[90,125,180,250,355,500,710,1000,1400,2000,2800,4000,5600,8000,11000]
    v=np.array([S[(f>=a)&(f<b)].sum() for a,b in zip(ed[:-1],ed[1:])]); return 10*np.log10(v/v.sum()), ed
S=sys.argv[1]; T=json.load(open(f"build/{S}/timeline.json")); h=T["head"]
film=K.rd(f"build/{S}/audio.wav", h+0.1, h+8).mean(1); fb,ed=bands(film)
print("band  "+" ".join("%5d"%e for e in ed[:-1]))
for name in sys.argv[2:]:
    x=K.rd(name).mean(1); b,_=bands(x); print("%-28s"%name[-28:], " ".join("%+5.1f"%v for v in b-fb), " meanabs %.1f"%np.abs(b-fb)[1:13].mean())
