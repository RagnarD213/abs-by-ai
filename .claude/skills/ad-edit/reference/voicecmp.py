#!/usr/bin/env python3
"""Do two rolls' lav channels want the same EQ? Compare 10-band speech spectra.
An EQ match is only valid against the source you will actually ship (lesson 34)."""
import subprocess, sys
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
BANDS=[(80,160),(160,320),(320,530),(530,850),(850,1400),(1400,2200),
       (2200,3500),(3500,5500),(5500,8000),(8000,11000)]
def spec(path, wins, af="pan=mono|c0=c1"):
    out=[]
    for ss,d in wins:
        raw=subprocess.run([FF,"-v","error","-ss",str(ss),"-t",str(d),"-i",path,"-vn",
            "-af",af,"-ar","44100","-f","f32le","-"],capture_output=True).stdout
        a=np.frombuffer(raw,dtype=np.float32)
        if len(a)<8192: continue
        N=4096; fr=np.array([a[i:i+N] for i in range(0,len(a)-N,2048)])
        rms=np.sqrt((fr**2).mean(1)+1e-15); sp=fr[rms>np.percentile(rms,65)]
        S=np.abs(np.fft.rfft(sp*np.hanning(N),axis=1)).mean(0)+1e-12
        f=np.fft.rfftfreq(N,1/44100)
        out.append([20*np.log10(S[(f>=lo)&(f<hi)].mean()) for lo,hi in BANDS])
    m=np.array(out).mean(0); return m-m.mean()
A=spec(sys.argv[1],[(150,20),(220,20),(280,20)])
Bv=spec(sys.argv[2],[(150,20),(220,20),(280,20)])
print(f"{'band':>14}{'roll A':>9}{'roll B':>9}{'diff':>8}")
for (lo,hi),x,y in zip(BANDS,A,Bv):
    print(f"{lo:6d}-{hi:<6d}{x:9.1f}{y:9.1f}{y-x:8.1f}")
print(f"\nmean |diff| {np.abs(Bv-A).mean():.2f} dB   max {np.abs(Bv-A).max():.2f} dB")
