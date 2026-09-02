#!/usr/bin/env python3
"""REV 2 voice fit -- iterate an EQ against Muhammad's ad using THE GATE'S OWN METRIC.

Rev 1's chain was copied from Ad 3 and adjusted by a roll-vs-roll comparison; it measured
1.70 dB mean tone error against his ad and, worse, buried the floor 9.5 dB (bed at -23 dB,
3:1 compressor with makeup, two air shelves). This script measures exactly what
reference/voice_ref_check.py measures (speech = top 40 % RMS frames, quiet = bottom 8 %,
10 bands, 20-140 s) on the lav of the TIGHT CUT (identical audio to the rev-2 render) and
solves the 10-band correction by iteration, because parametric bands interact.

  python3 voicefit.py fit                 # iterate the EQ, print the chain
  python3 voicefit.py test "<af chain>"   # measure one chain
"""
import subprocess, sys
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE="/Volumes/Extreme/_edit_work/website-video-828"
REF=f"{HERE}/audio/muhammad48.wav"
LAV=f"{HERE}/audio/tight_lav48.wav"
SR=48000; EDGES=[80,150,250,400,600,900,1400,2200,3500,5500,9000]
CENTRES=[int(round((lo*hi)**0.5)) for lo,hi in zip(EDGES,EDGES[1:])]   # geometric band centres

def load(path, af="anull", ss=20, dur=120, ch=1):
    raw=subprocess.run([FF,"-v","error","-ss",str(ss),"-t",str(dur),"-i",path,"-af",af,
                        "-ac",str(ch),"-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)

def analyse(a):
    """verbatim from voice_ref_check.py, plus a 4-9 kHz floor band for information"""
    N=2048; hop=1024
    fr=np.array([a[i:i+N] for i in range(0,len(a)-N,hop)])
    rms=np.sqrt((fr**2).mean(1)+1e-12); db=20*np.log10(rms+1e-12)
    sp=rms>np.percentile(rms,60); nz=rms<np.percentile(rms,8)
    win=np.hanning(N); f=np.fft.rfftfreq(N,1/SR)
    S=(np.abs(np.fft.rfft(fr[sp]*win,axis=1))**2).mean(0); Sn=(np.abs(np.fft.rfft(fr[nz]*win,axis=1))**2).mean(0)
    bands=np.array([10*np.log10(S[(f>=lo)&(f<hi)].mean()+1e-15) for lo,hi in zip(EDGES,EDGES[1:])]); bands-=bands.mean()
    floor=np.array([10*np.log10(S[(f>=lo)&(f<hi)].mean()/(Sn[(f>=lo)&(f<hi)].mean()+1e-15)) for lo,hi in ((80,250),(250,1000),(1000,4000),(4000,9000))])
    drops=[db[i-1]-db[min(i+3,len(db)-1)] for i in range(1,len(db)-5) if sp[i-1] and not sp[i] and db[i-1]>np.percentile(db,50)]
    return bands,floor,(float(np.median(drops)) if drops else float("nan"))

REFA=analyse(load(REF))

def report(label, af, src=LAV, quiet=False):
    b,fl,dry=analyse(load(src,af))
    err=b-REFA[0]; fd=fl-REFA[1]
    ok_tone=np.abs(err).mean()<=1.2 and np.abs(err).max()<=2.5
    ok_floor=bool((fd[:3]>=-3.0).all()); ok_dry=dry>=REFA[2]-1.5
    if not quiet:
        print(f"{label}")
        print("   tone err  "+" ".join(f"{e:+5.1f}" for e in err)+
              f"   mean {np.abs(err).mean():.2f}  max {np.abs(err).max():.2f}  {'PASS' if ok_tone else 'FAIL'}")
        print(f"   floor vs ref (80-250/250-1k/1-4k | 4-9k info) "+" ".join(f"{x:+5.1f}" for x in fd)+
              f"   {'PASS' if ok_floor else 'FAIL'}")
        print(f"   dryness {dry:.1f} vs ref {REFA[2]:.1f}  {'PASS' if ok_dry else 'FAIL'}")
    return err,fd,dry

def eq_chain(g, shelf=None, pre="", post=""):
    """g: 10 gains at the band centres. The top band is a shelf, not a bell."""
    parts=[pre] if pre else []
    for c,gain in zip(CENTRES[:-1],g[:-1]):
        if abs(gain)>=0.15: parts.append(f"equalizer=f={c}:t=q:w=1.3:g={gain:+.2f}")
    if abs(g[-1])>=0.15: parts.append(f"treble=g={g[-1]:+.2f}:f={shelf or 6500}:width_type=q:width=0.6")
    if post: parts.append(post)
    return ",".join(parts)

def fit(pre="highpass=f=70", post="", iters=6, damp=0.75):
    g=np.zeros(10)
    err,_,_=report("RAW lav", pre or "anull")
    for it in range(iters):
        g=g-damp*err
        chain=eq_chain(g,pre=pre,post=post)
        err,fd,dry=report(f"iter {it+1}: {chain}",chain)
    return g,chain

if __name__=="__main__":
    mode=sys.argv[1] if sys.argv[1:] else "fit"
    print("bands   "+" ".join(f"{c:5d}" for c in CENTRES))
    print("ref     "+" ".join(f"{x:5.1f}" for x in REFA[0])+f"   floor {REFA[1].round(1)}  dry {REFA[2]:.1f}\n")
    if mode=="fit":
        g,chain=fit()
        print("\nFITTED EQ gains:",[round(float(x),2) for x in g])
        print("CHAIN:",chain)
    elif mode=="test":
        for c in sys.argv[2:]: report(c,c)
