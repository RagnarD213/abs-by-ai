#!/usr/bin/env python3
"""What would make our voice sound like Muhammad's?

Dan's reference for good audio is Muhammad Arsalan's ab-wheel cut. Compare our source (the
clean master's RIGHT channel, mono - the lav, no comb) against his finished voice, and fit the
correction. Speech frames only, so a music bed under his voice does not skew the profile.
"""
import subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OURS="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"
MUH="/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4"
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000),(9000,14000)]
def pcm(f,t,d,af):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def prof(x):
    n=len(x)//960; fr=x[:n*960].reshape(n,960); rms=np.sqrt((fr**2).mean(1))
    db=20*np.log10(np.maximum(1e-7,rms))
    loud=fr[db>np.percentile(db,72)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS]), db
# sample Muhammad across several talking passages, avoiding his workout sets
m=np.concatenate([pcm(MUH,t,20.0,'anull') for t in (30,60,100,140,300,360)])
o=np.concatenate([pcm(OURS,t,20.0,'pan=mono|c0=c1') for t in (100,300,700,1000,1250,1350)])
pm,dbm=prof(m); po,dbo=prof(o)
pm=pm-pm.max(); po=po-po.max()
print(f"{'band':>14s} {'Muhammad':>9s} {'ours(R)':>9s} {'need':>7s}")
for (a,b),M,O in zip(BANDS,pm,po): print(f" {a:5d}-{b:5d}Hz {M:9.1f} {O:9.1f} {M-O:+7.1f}")
d=pm-po; d=d-d.mean()
print(f"\nshape difference: {float(np.sqrt((d**2).mean())):.2f} dB RMS")
g=np.clip(d*0.9,-6,6)
print("correction toward his voice:", np.round(g,1))
eq=','.join(f"equalizer=f={int(round((a*b)**0.5))}:width_type=o:width=1.0:g={gi:.1f}"
            for (a,b),gi in zip(BANDS,g))
open('work/muhfit.txt','w').write(eq)
print(f"\nnoise floor  Muhammad {np.percentile(dbm,10):6.1f} dB   ours {np.percentile(dbo,10):6.1f} dB")
print(f"speech p95   Muhammad {np.percentile(dbm,95):6.1f} dB   ours {np.percentile(dbo,95):6.1f} dB")
print(f"SNR          Muhammad {np.percentile(dbm,95)-np.percentile(dbm,10):6.1f} dB   "
      f"ours {np.percentile(dbo,95)-np.percentile(dbo,10):6.1f} dB")
