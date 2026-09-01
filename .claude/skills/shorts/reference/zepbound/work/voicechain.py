#!/usr/bin/env python3
"""Build and TEST the voice chain that brings our lav toward Muhammad's character.

Measured need, relative to the 320-640 Hz body band: we are 3.8 dB short of weight, 3.8 dB
short of presence, 8.7 dB short of air and 12 dB short above 9 kHz. That darkness is what
"doesn't sound as good as Muhammad's" means.

We can afford it: our SNR is 30.2 dB against his 21.2, so lifting the top by ~9 dB lands our
noise floor at roughly his, not worse. Applied to the RIGHT CHANNEL ONLY, in mono - the left
input on this shoot records a room mic 7.58 ms late and summing them combs the voice.
"""
import subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OURS="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"
MUH="/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4"
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000),(9000,14000)]

# Refined once against the measured residual: after the first pass we were still 1.7 dB short
# of air, 2.7 dB short of the top octave and 2.3 dB heavy in the 1.25-2.5 kHz nasal band.
CHAIN = ("pan=mono|c0=c1,"
         "equalizer=f=110:width_type=o:width=1.4:g=4.0,"      # weight
         "equalizer=f=900:width_type=o:width=1.2:g=1.2,"      # lower presence
         "equalizer=f=1800:width_type=o:width=1.2:g=-2.0,"    # take out the nasal honk
         "equalizer=f=3500:width_type=o:width=1.2:g=3.0,"     # presence / intelligibility
         "highshelf=f=6000:g=9.0,"                            # air - the biggest single gap
         "equalizer=f=11000:width_type=o:width=1.0:g=5.0,"    # top octave
         "deesser=i=0.40")                                    # keep the added air off the S's

def pcm(f,t,d,af):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def prof(x):
    n=len(x)//960; fr=x[:n*960].reshape(n,960); rms=np.sqrt((fr**2).mean(1))
    db=20*np.log10(np.maximum(1e-7,rms)); loud=fr[db>np.percentile(db,72)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    p_=np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])
    sib=10*np.log10(max(1e-12,S[(f>=5500)&(f<9000)].mean()))-10*np.log10(max(1e-12,S[(f>=300)&(f<3000)].mean()))
    return p_, db, sib
m=np.concatenate([pcm(MUH,t,20.0,'anull') for t in (30,60,100,140,300,360)])
pm,dbm,sm=prof(m); pm=pm-pm.max()
for lab,af in (('ours, right channel, no chain','pan=mono|c0=c1'), ('ours, WITH the chain',CHAIN)):
    o=np.concatenate([pcm(OURS,t,20.0,af) for t in (100,300,700,1000,1250,1350)])
    po,dbo,so=prof(o); po=po-po.max()
    d=pm-po
    print(f"{lab}:")
    print(f"   shape vs Muhammad {float(np.sqrt(((d-d.mean())**2).mean())):.2f} dB RMS   "
          f"floor {np.percentile(dbo,10):6.1f} (his {np.percentile(dbm,10):.1f})   "
          f"SNR {np.percentile(dbo,95)-np.percentile(dbo,10):5.1f} (his {np.percentile(dbm,95)-np.percentile(dbm,10):.1f})   "
          f"sibilance {so:6.1f} (his {sm:.1f})")
    print(f"   per band need: {np.round(d-d.mean(),1)}")
open('work/voicechain.txt','w').write(CHAIN)
print("\nwrote work/voicechain.txt")
