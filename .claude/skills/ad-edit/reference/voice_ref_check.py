#!/usr/bin/env python3
"""THE AUDIO GATE: does this mix sound like Muhammad's ad? Measured, not argued.

Dan rejected the website video's audio (2026-09-02) as "the two-channel issue again". It was
NOT the comb filter -- L/R read +0.998 -- it was the FLOOR: the bed + compressor makeup + air
shelves lifted everything between the words ~9 dB above his, and every existing check
(LUFS, L/R corr, splices) passed. The raw lav measured BETTER than his ad on floor; the chain
destroyed it. So this gate compares a finished mix against the reference ad on the four
things a listener hears as "bad audio", and refuses to pass a mix that misses any of them.

  voice_ref_check.py <mix.mp4|.mov> [--ref <reference.mp4>] [--ab out.mp4]
      --ab writes a three-sentence A/B clip (his, then ours) for Dan to judge by ear.

Metrics (speech frames = top 40 % RMS, quiet frames = bottom 8 %, 2048-pt windows, 20-140 s):
  1 tonal balance   10-band speech spectrum, mean |error| vs the reference   <= 1.2 dB, max <= 2.5
  2 floor           voice-over-floor per band (80-250 / 250-1k / 1-4k)        within 3 dB of his
  3 dryness         median level drop 64 ms after a word ends                 >= his - 1.5 dB
  4 image           L/R correlation                                            >= +0.97
"""
import re, subprocess, sys
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
REF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4"
args=sys.argv[1:]; mix=args[0]
if "--ref" in args: REF=args[args.index("--ref")+1]
AB=args[args.index("--ab")+1] if "--ab" in args else None
SR=48000; EDGES=[80,150,250,400,600,900,1400,2200,3500,5500,9000]
def load(path, ss=20, dur=120, ch=1):
    raw=subprocess.run([FF,"-v","error","-ss",str(ss),"-t",str(dur),"-i",path,"-ac",str(ch),"-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)
def analyse(a):
    N=2048; hop=1024
    fr=np.array([a[i:i+N] for i in range(0,len(a)-N,hop)])
    rms=np.sqrt((fr**2).mean(1)+1e-12); db=20*np.log10(rms+1e-12)
    sp=rms>np.percentile(rms,60); nz=rms<np.percentile(rms,8)
    win=np.hanning(N); f=np.fft.rfftfreq(N,1/SR)
    S=(np.abs(np.fft.rfft(fr[sp]*win,axis=1))**2).mean(0); Sn=(np.abs(np.fft.rfft(fr[nz]*win,axis=1))**2).mean(0)
    bands=np.array([10*np.log10(S[(f>=lo)&(f<hi)].mean()+1e-15) for lo,hi in zip(EDGES,EDGES[1:])]); bands-=bands.mean()
    floor=np.array([10*np.log10(S[(f>=lo)&(f<hi)].mean()/(Sn[(f>=lo)&(f<hi)].mean()+1e-15)) for lo,hi in ((80,250),(250,1000),(1000,4000))])
    drops=[db[i-1]-db[min(i+3,len(db)-1)] for i in range(1,len(db)-5) if sp[i-1] and not sp[i] and db[i-1]>np.percentile(db,50)]
    return bands,floor,(float(np.median(drops)) if drops else float("nan"))
ref=analyse(load(REF)); ours=analyse(load(mix))
st=load(mix,ch=2).reshape(-1,2); corr=float(np.corrcoef(st[:,0],st[:,1])[0,1])
fails=[]
def check(ok,msg):
    print(("  PASS  " if ok else "  FAIL  ")+msg)
    if not ok: fails.append(msg)
print(f"voice_ref_check  {mix.split('/')[-1]}  vs  {REF.split('/')[-1]}")
err=np.abs(ours[0]-ref[0])
print("  band      ref    mix   diff")
for lo,r,o in zip(EDGES,ref[0],ours[0]): print(f"  {lo:5d}Hz {r:6.1f} {o:6.1f} {o-r:+6.1f}")
check(err.mean()<=1.2 and err.max()<=2.5, f"tonal balance: mean |err| {err.mean():.2f} dB (<=1.2), max {err.max():.2f} (<=2.5)")
fd=ours[1]-ref[1]
print(f"  voice-over-floor 80-250/250-1k/1-4k: ref {ref[1].round(1)}  mix {ours[1].round(1)}  diff {fd.round(1)}")
check(bool((fd>=-3.0).all()), "floor between words within 3 dB of the reference (bed + gate + makeup all count)")
check(ours[2]>=ref[2]-1.5, f"dryness: level drop 64 ms after a word {ours[2]:.1f} dB vs ref {ref[2]:.1f} (>= ref-1.5)")
check(corr>=0.97, f"stereo image: L/R correlation {corr:+.3f} (>= +0.97)")
if AB:
    # three sentences his, three ours, from the same 12 s windows (20 s in), for Dan's ear
    cmd=[FF,"-nostdin","-y","-v","error","-ss","20","-t","12","-i",REF,"-ss","20","-t","12","-i",mix,
         "-filter_complex","[0:a]volume=0dB[a];[1:a]volume=0dB[b];[a][b]concat=n=2:v=0:a=1[out]",
         "-map","[out]","-c:a","aac","-b:a","192k",AB]
    subprocess.run(cmd,check=True); print("  A/B written:",AB)
print("\n"+("AUDIO GATE PASSED" if not fails else f"AUDIO GATE FAILED -- {len(fails)}"))
sys.exit(1 if fails else 0)
