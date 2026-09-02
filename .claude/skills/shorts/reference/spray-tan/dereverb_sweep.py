#!/usr/bin/env python3
"""Sweep the dereverb parameters against the three numbers that decide it."""
import subprocess, sys
import numpy as np
sys.path.insert(0,'work')
from dereverb import dereverb
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/01 - My First Spray Tan/CUT_v1_graded_NO-GRAPHICS.mp4"
CH=open('work/voicechain.txt').read().strip()
SPANS=[(38,30),(300,30),(600,30),(1010,30)]
def pull(t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',SRC,'-t',str(d),'-vn','-af',CH,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def edt(x):
    N=512;hop=128;n=(len(x)-N)//hop
    idx=np.arange(N)[None,:]+(np.arange(n)*hop)[:,None]
    e=20*np.log10(np.sqrt((x[idx]**2).mean(1))+1e-9)
    p90=np.percentile(e,90);o=[]
    for i in range(1,n-40):
        if e[i]>p90-4 and e[i+3]<e[i]-4:
            s=e[i:i+40];b=np.nonzero(s<s[0]-20)[0]
            if len(b): o.append(b[0]*hop/48000*1000)
    return float(np.median(o)) if o else float('nan')
def hf_detail(x):   # proxy for musical noise / texture loss
    N=1024;hop=512;n=(len(x)-N)//hop
    idx=np.arange(N)[None,:]+(np.arange(n)*hop)[:,None]
    S=np.abs(np.fft.rfft(x[idx]*np.hanning(N),axis=1))
    f=np.fft.rfftfreq(N,1/48000); m=(f>3000)&(f<9000)
    return float(np.log10(S[:,m].mean()+1e-12))
refs=[pull(t,d) for t,d in SPANS]
base_edt=float(np.median([edt(r) for r in refs])); base_hf=float(np.mean([hf_detail(r) for r in refs]))
print(f"baseline  EDT {base_edt:5.0f} ms   target 40 (Muhammad)\n")
print(f"{'alpha':>6s} {'d1':>4s} {'floor':>6s} {'EDT ms':>7s} {'speech dB':>10s} {'HF keep':>8s}")
for alpha,d1,fl in [(0.45,22,-10),(0.62,22,-14),(0.62,16,-14),(0.75,16,-16),(0.85,14,-18),(0.95,12,-20)]:
    ys=[dereverb(r,alpha=alpha,d1_ms=d1,floor_db=fl) for r in refs]
    e=float(np.median([edt(y.astype(np.float64)) for y in ys]))
    lv=float(np.mean([20*np.log10((np.sqrt((y.astype(np.float64)**2).mean())+1e-12)/(np.sqrt((r**2).mean())+1e-12)) for r,y in zip(refs,ys)]))
    hf=float(np.mean([hf_detail(y.astype(np.float64)) for y in ys]))-base_hf
    print(f"{alpha:6.2f} {d1:4d} {fl:6.0f} {e:7.0f} {lv:10.2f} {hf:+8.3f}")
