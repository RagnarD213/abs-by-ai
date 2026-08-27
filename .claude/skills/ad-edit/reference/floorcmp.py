#!/usr/bin/env python3
"""Noise floor per span: a plane/HVAC raises the QUIET frames, especially 20-200 Hz."""
import sys, wave, json
import numpy as np
w=wave.open(sys.argv[1]); sr=w.getframerate()
a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
print(f"{'label':<16}{'floor dB':>10}{'LF floor':>10}{'MF floor':>10}{'nQuiet':>8}")
for lbl,s0,s1 in json.loads(sys.argv[2]):
    seg=a[int(s0*sr):int(s1*sr)]
    N=2048; fr=np.array([seg[i:i+N] for i in range(0,len(seg)-N,512)])
    rms=np.sqrt((fr**2).mean(1)+1e-15)
    q=fr[rms<=np.percentile(rms,20)]
    if len(q)<2: print(f"{lbl:<16} too short"); continue
    S=np.abs(np.fft.rfft(q*np.hanning(N),axis=1)).mean(0)+1e-12
    f=np.fft.rfftfreq(N,1/sr)
    fl=20*np.log10(np.sqrt((q**2).mean()))
    lf=20*np.log10(S[(f>20)&(f<200)].mean())
    mf=20*np.log10(S[(f>500)&(f<2000)].mean())
    print(f"{lbl:<16}{fl:10.1f}{lf:10.1f}{mf:10.1f}{len(q):8d}")
