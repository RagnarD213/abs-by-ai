#!/usr/bin/env python3
"""What is the "weird under sound", and what does Muhammad's audio do that ours does not?

⚠ MY EARLIER COMPARISON WAS AGAINST THE WRONG THING. I matched only the SPEECH spectrum, and
I measured his "noise floor" on the ab-wheel organic cut - which carries a MUSIC BED, so what I
called his floor was his music. Dan's complaint is about what sits UNDER his voice, so measure
that directly: the spectrum inside speech gaps, and whether narrowband tones are present.
"""
import subprocess, sys
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PROJ="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
SRC={
 'OUR source (right ch, raw)': (f"{PROJ}/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4",'pan=mono|c0=c1',(200,1400)),
 'OUR delivered short 1':      ('out/b_the-3-supplements-that-matter.mp4','anull',(0,40)),
 "MUHAMMAD ad (indoor)":       (f"{PROJ}/Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4",'anull',(5,230)),
 "MUHAMMAD organic (outdoor)": (f"{PROJ}/Muhammad Organic Videos/Daniel Organic Video -The $17 Ab Wheel Beats Every Crunch-v2 HD.mp4",'anull',(5,410)),
}
def load(f,af,span,maxs=180):
    t0,t1=span; d=min(maxs,t1-t0)
    p=subprocess.run([FF,'-v','error','-ss',str(t0),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def analyse(lab,x):
    N=2048; hop=1024
    n=(len(x)-N)//hop
    idx=np.arange(N)[None,:]+(np.arange(n)*hop)[:,None]
    fr=x[idx]*np.hanning(N)
    S=np.abs(np.fft.rfft(fr,axis=1))
    f=np.fft.rfftfreq(N,1/48000)
    e=20*np.log10(np.maximum(1e-9,np.sqrt((x[idx]**2).mean(1))))
    # gaps = the quietest 12% of frames = what sits under the voice
    q=e<np.percentile(e,12)
    loud=e>np.percentile(e,80)
    P=lambda m:(S[m]**2).mean(0)
    ng,sg=P(q),P(loud)
    tot=lambda P_,a,b:10*np.log10(max(1e-14,P_[(f>=a)&(f<b)].mean()))
    print(f"\n{lab}")
    print(f"   frame level: p12 {np.percentile(e,12):6.1f} dB   p50 {np.percentile(e,50):6.1f}   p95 {np.percentile(e,95):6.1f}")
    print(f"   {'band':>13s} {'UNDER voice':>12s} {'speech':>8s}")
    for a,b in ((20,60),(60,120),(120,250),(250,500),(500,1000),(1000,2000),(2000,4000),(4000,8000),(8000,16000)):
        print(f"   {a:5d}-{b:5d} {tot(ng,a,b):12.1f} {tot(sg,a,b):8.1f}")
    # narrowband tones in the under-voice spectrum: peak vs local median
    nd=10*np.log10(np.maximum(1e-14,ng))
    sm=np.convolve(nd,np.ones(21)/21,'same')
    prom=nd-sm
    band=(f>20)&(f<16000)
    top=np.argsort(prom[band])[-6:][::-1]
    fb=f[band]
    print("   narrowband peaks under the voice: " +
          ', '.join(f"{fb[i]:.0f}Hz +{prom[band][i]:.1f}dB" for i in top if prom[band][i]>4) or "   none above +4 dB")
    return ng,sg,f
res={}
for lab,(f_,af,span) in SRC.items():
    res[lab]=analyse(lab,load(f_,af,span))
