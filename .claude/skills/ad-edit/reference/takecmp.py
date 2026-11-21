#!/usr/bin/env python3
"""Compare candidate takes objectively: level, pace, internal dead air, LF noise (planes)."""
import sys, wave, json
import numpy as np
W = sys.argv[1]; SPANS = json.loads(sys.argv[2])
w = wave.open(W); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)/32768
wh = json.load(open(sys.argv[3])); WS=[x for s in wh['segments'] for x in s.get('words',[])]
print(f"{'label':<16}{'dur':>7}{'words':>7}{'wpm':>7}{'rms dB':>9}{'peak dB':>9}{'dead>0.25':>11}{'LF20-120':>10}{'HF tilt':>9}")
for lbl, s0, s1 in SPANS:
    seg = a[int(s0*sr):int(s1*sr)]
    nw = [x for x in WS if s0-0.01 <= x['start'] < s1]
    N=1024; fr=np.array([seg[i:i+N] for i in range(0,len(seg)-N,256)])
    rms=np.sqrt((fr**2).mean(1)+1e-15)
    voiced = rms > np.percentile(rms,60)
    lvl = 20*np.log10(rms[voiced].mean())
    pk  = 20*np.log10(max(np.abs(seg).max(),1e-9))
    # dead air inside the take
    hop=256/sr; quiet = rms < 10**(-40/20); runs=[];cur=0
    for q in quiet:
        if q: cur+=1
        else:
            if cur*hop>=0.25: runs.append(cur*hop)
            cur=0
    if cur*hop>=0.25: runs.append(cur*hop)
    S=np.abs(np.fft.rfft(fr*np.hanning(N),axis=1)).mean(0)+1e-12
    f=np.fft.rfftfreq(N,1/sr)
    lf = 20*np.log10(S[(f>20)&(f<120)].mean()/S[(f>300)&(f<3000)].mean())
    hf = 20*np.log10(S[(f>4000)&(f<9000)].mean()/S[(f>300)&(f<1500)].mean())
    dur=s1-s0
    print(f"{lbl:<16}{dur:7.2f}{len(nw):7d}{len(nw)/dur*60:7.0f}{lvl:9.1f}{pk:9.1f}"
          f"{sum(runs):11.2f}{lf:10.1f}{hf:9.1f}")
