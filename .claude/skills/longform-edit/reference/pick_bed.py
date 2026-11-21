#!/usr/bin/env python3
"""Choose the music bed by MEASUREMENT, not by taste (the /ad-edit rule), scored against
the REFERENCE CUT'S OWN BED rather than an abstract ideal.

Two criteria:
  1. SPECTRAL SHAPE -- his bed, sampled in his speech gaps (found from his word
     timings), is what a bed under this voice is supposed to look like. A bed with
     midrange energy where the voice lives is exactly what makes a mix sound amateur.
  2. FLATNESS -- energy must not swing over the 7 minutes it has to cover, or the
     sidechain pumps and the bed starts drawing attention to itself.

All seven candidates are Pixabay Content Licence: commercial use, no attribution, so
nothing has to be credited in perpetuity.
"""
import glob, json, subprocess
import numpy as np
FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
REF = "/Volumes/Extreme/_edit_work/abwheel/ref_muhammad/muhammad_organic.mp4"
WH  = "/Volumes/Extreme/_edit_work/abwheel/ref_muhammad/m.whisper.json"
SR  = 44100
BANDS = [(60,150),(150,400),(400,1000),(1000,3000),(3000,8000)]

def load(p, ss=None, t=None):
    cmd=[FF,"-v","error"]
    if ss is not None: cmd+=["-ss",str(ss)]
    if t is not None: cmd+=["-t",str(t)]
    cmd+=["-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,dtype=np.float32).astype(float)

def shape(a, n=1<<14):
    acc=np.zeros(n//2+1); k=0
    for i in range(0,max(1,len(a)-n),n):
        acc+=np.abs(np.fft.rfft(a[i:i+n]*np.hanning(n))); k+=1
    acc/=max(k,1); fr=np.fft.rfftfreq(n,1/SR)
    v=np.array([20*np.log10(acc[(fr>=lo)&(fr<hi)].mean()+1e-12) for lo,hi in BANDS])
    return v-v.max()

# his bed, from the gaps between his words
W=[w for s in json.load(open(WH))["segments"] for w in s.get("words",[])]
gaps=[(a["end"]+0.20, min(b["start"]-0.12, a["end"]+1.5))
      for a,b in zip(W,W[1:]) if b["start"]-a["end"]>=0.9 and a["end"]>4]
gaps=[g for g in gaps if g[1]-g[0]>=0.5][:24]
seg=np.concatenate([load(REF,a,b-a) for a,b in gaps])
HIS=shape(seg, 1<<13)
print("bed sampled from", len(gaps), "speech gaps in the reference cut")
print(f"{'track':<18}{'dur':>7}{'shape err':>11}{'flatness':>10}{'score':>8}   band profile")
best=None
for p in sorted(glob.glob("music/*.mp3")):
    a=load(p); dur=len(a)/SR
    s=shape(a); err=float(np.abs(s-HIS).mean())
    h=SR*4
    e=20*np.log10(np.sqrt((a[:len(a)//h*h].reshape(-1,h)**2).mean(1))+1e-9)
    flat=float(e.std()); score=err+flat*1.5
    print(f"{p[6:-4]:<18}{dur:6.0f}s{err:10.1f}{flat:9.1f}{score:8.1f}   "+" ".join(f"{x:5.1f}" for x in s))
    if best is None or score<best[0]: best=(score,p,dur)
print("\nreference bed:        "+" ".join(f"{x:5.1f}" for x in HIS))
need=433.57
print(f"\nPICK: {best[1]}  ({best[2]:.0f}s, needs {need:.0f}s -> "
      f"{'loop x%d'%int(np.ceil(need/best[2])) if best[2]<need else 'long enough'})")
