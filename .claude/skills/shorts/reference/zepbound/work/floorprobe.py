#!/usr/bin/env python3
"""The TRUE noise floor and the reverb tail, in both rooms.

The p12-frame measure still contains speech tails. Find the longest genuine silences and
measure those, and separately measure how fast the room decays after a word stops - a live
kitchen with granite and tile rings, and that ring is part of "doesn't sound clean".
"""
import json, subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PROJ="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
def load(f,af,t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def env(x,hop=240):
    n=len(x)//hop
    return 20*np.log10(np.maximum(1e-9,np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))))
def report(lab,x):
    e=env(x)
    # longest runs at least 12 dB under the median -> real silence
    thr=np.percentile(e,50)-12
    q=e<thr
    runs=[]; i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)*0.005>=0.30: runs.append((i,j))
            i=j
        else: i+=1
    if not runs:
        print(f"{lab}: no silence >=0.3s found"); return
    runs.sort(key=lambda r:-(r[1]-r[0]))
    seg=np.concatenate([x[a*240:b*240] for a,b in runs[:12]])
    N=2048
    n=(len(seg)-N)//N
    if n<2: print(f"{lab}: not enough silence"); return
    S=(np.abs(np.fft.rfft(seg[:n*N].reshape(n,N)*np.hanning(N),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(N,1/48000)
    band=lambda a,b:10*np.log10(max(1e-14,S[(f>=a)&(f<b)].mean()))
    tot=20*np.log10(max(1e-9,np.sqrt((seg**2).mean())))
    # reverb: median decay slope over the 250ms after a speech offset
    offs=[a for a,b in runs if a>60]
    dec=[]
    for a in offs[:40]:
        w=e[a-4:a+50]
        if len(w)<54: continue
        pk=w[:4].max()
        tail=w[6:50]
        below=np.where(tail<pk-20)[0]
        if len(below): dec.append(below[0]*0.005)
    print(f"{lab}")
    print(f"   true silence: {sum(b-a for a,b in runs)*0.005:.1f}s found, level {tot:6.1f} dBFS")
    print(f"   floor bands  20-80 {band(20,80):6.1f} | 80-250 {band(80,250):6.1f} | "
          f"250-1k {band(250,1000):6.1f} | 1k-4k {band(1000,4000):6.1f} | 4k-16k {band(4000,16000):6.1f}")
    if dec: print(f"   -20 dB decay after a word: {np.median(dec)*1000:.0f} ms")
report("OUR source, right channel",
       load(f"{PROJ}/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4",'pan=mono|c0=c1',200,300))
report("OUR delivered short 1",
       load('out/b_the-3-supplements-that-matter.mp4','anull',0,40))
report("MUHAMMAD ad (indoor, same rig)",
       load(f"{PROJ}/Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4",'anull',5,225))
