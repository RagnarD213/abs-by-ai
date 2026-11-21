#!/usr/bin/env python3
"""Lock the rev-4 voice chain and verify it against Muhammad's AD.

⚠ THE AD IS THE RIGHT REFERENCE. Rev 3 fitted the tone against his ab-wheel ORGANIC cut, which
is shot outdoors - so its low end carries wind and its own room, and matching it told us to add
+4 dB at 110 Hz. That boost raised our noise floor by 4.6 dB in the 80-250 band and doubled the
reverb tail (65 -> 120 ms). It is the single biggest cause of Dan's "weird under sound".

The ad is indoors on the same two-mic rig, so it is the like-for-like comparison.
"""
import subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PROJ="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OURS=f"{PROJ}/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4"
MUH=f"{PROJ}/Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4"
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000),(9000,14000)]
BASE=("pan=mono|c0=c1,"
      "highpass=f=75:p=2,"                                    # kill the rumble we were boosting
      "afftdn=nr=30:nf=-45:tn=1,"                             # broadband room tone
      "agate=threshold=0.030:ratio=6:range=0.15:attack=8:release=190:knee=8")
def load(f,af,t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def speech(x):
    idx=np.arange(960)[None,:]+(np.arange((len(x)-960)//480)*480)[:,None]
    fr=x[idx]; rms=np.sqrt((fr**2).mean(1))
    loud=fr[rms>np.percentile(rms,75)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-14,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])
m=np.concatenate([load(MUH,'anull',t,20) for t in (12,40,70,110,150,190)])
pm=speech(m); pm=pm-pm.max()
o=np.concatenate([load(OURS,BASE,t,20) for t in (120,320,700,1000,1250,1350)])
po=speech(o); po=po-po.max()
d=pm-po
print("speech shape, ours (cleaned, no tone EQ yet) vs HIS AD:")
for (a,b),M,O in zip(BANDS,pm,po): print(f"  {a:5d}-{b:5d}Hz  his {M:6.1f}  ours {O:6.1f}  need {M-O:+5.1f}")
g=np.clip((d-d.mean())*0.9,-6,6)
print(f"\nshape difference before tone EQ: {float(np.sqrt(((d-d.mean())**2).mean())):.2f} dB")
print("fitted correction:", np.round(g,1))
eq=','.join(f"equalizer=f={int(round((a*b)**0.5))}:width_type=o:width=1.0:g={gi:.1f}"
            for (a,b),gi in zip(BANDS,g))
chain=f"{BASE},{eq},deesser=i=0.35"
o2=speech(np.concatenate([load(OURS,chain,t,20) for t in (120,320,700,1000,1250,1350)]))
o2=o2-o2.max(); d2=pm-o2
print(f"shape difference AFTER: {float(np.sqrt(((d2-d2.mean())**2).mean())):.2f} dB")
open('work/voicechain.txt','w').write(chain)
print(f"\nwrote work/voicechain.txt ({len(chain)} chars)")
