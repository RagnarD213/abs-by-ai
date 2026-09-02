#!/usr/bin/env python3
"""HARD AUDIO GATE - measures the DELIVERED file against Dan's reference ad.

⚠ WHY THIS EXISTS. On 2026-09-02 Dan rejected a batch whose audio passed every check the
pipeline had: right-channel-only (verified +0.9912 correlation), tone fitted to 0.35 dB,
-14 LUFS, no clipping, no silent seconds, floor cleaner than the reference. All true, and the
audio was still wrong - because NOTHING IN THE PIPELINE MEASURED THE ROOM. Early decay time
was 85 ms against the reference's 40 ms, and reverb is inside the words, so no gate that looks
at levels, spectra or gaps can see it.

Three numbers, all on the finished file, all against `Muhammad Ad Videos/…16x9.mp4`:
  EDT             ms to fall 20 dB after a speech offset.   FAIL over 55 ms (his 40).
  shape           octave-band speech difference, dB RMS.    FAIL over 1.00 dB.
  floor-to-voice  dB between speech and the gaps.           FAIL under his minus 3 dB.
"""
import json, subprocess, sys
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
REF=f"{P}/Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4"
# Same seven bands the corrector uses (finishaudio.py). 9-14 kHz is deliberately excluded: it
# sits ~47 dB below the peak band, and including it destabilised the corrective fit.
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]
MAX_EDT, MAX_SHAPE, FLOOR_MARGIN = 55.0, 1.00, 3.0
def pull(f,spans):
    o=[]
    for t,d in spans:
        p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
        o.append(np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.)
    return np.concatenate(o)
def frames(x,N=512,hop=128):
    n=(len(x)-N)//hop
    idx=np.arange(N)[None,:]+(np.arange(n)*hop)[:,None]
    return x[idx]
def edt(x):
    fr=frames(x); e=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
    p90=np.percentile(e,90); o=[]
    for i in range(1,len(e)-40):
        if e[i]>p90-4 and e[i+3]<e[i]-4:
            s=e[i:i+40]; b=np.nonzero(s<s[0]-20)[0]
            if len(b): o.append(b[0]*128/48000*1000)
    return float(np.median(o)) if o else float('nan')
def ftv(x):
    fr=frames(x); e=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
    S=np.abs(np.fft.rfft(fr*np.hanning(512),axis=1))**2
    f=np.fft.rfftfreq(512,1/48000); m=(f>=250)&(f<1000)
    return float(10*np.log10(S[e>np.percentile(e,88)][:,m].mean())-10*np.log10(S[e<np.percentile(e,12)][:,m].mean()))
def shape(x):
    idx=np.arange(960)[None,:]+(np.arange((len(x)-960)//480)*480)[:,None]
    fr=x[idx]; rms=np.sqrt((fr**2).mean(1)); loud=fr[rms>np.percentile(rms,75)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    v=np.array([10*np.log10(max(1e-14,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])
    return v-v.max()
r=pull(REF,[(10,60),(90,60),(160,50)])
R_EDT,R_FTV,R_SH = edt(r), ftv(r), shape(r)
print(f"reference: EDT {R_EDT:.0f} ms   floor-to-voice {R_FTV:.1f} dB\n")
segs=json.loads(subprocess.check_output(['node','-e',
  "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"]).decode())
only=[a.upper() for a in sys.argv[1:]]
bad=0
print(f"{'id':3s} {'EDT ms':>7s} {'shape dB':>9s} {'floor':>7s}   verdict")
for sid,slug in segs:
    if only and sid not in only: continue
    f=f"out/{sid.lower()}_{slug}.mp4"
    x=pull(f,[(1,120)])
    E,F=edt(x),ftv(x)
    S=float(np.sqrt((((R_SH-shape(x))-(R_SH-shape(x)).mean())**2).mean()))
    ok = E<=MAX_EDT and S<=MAX_SHAPE and F>=R_FTV-FLOOR_MARGIN
    bad += not ok
    why=[]
    if E>MAX_EDT: why.append(f"EDT {E:.0f}>{MAX_EDT:.0f} (ROOMY)")
    if S>MAX_SHAPE: why.append(f"shape {S:.2f}>{MAX_SHAPE:.2f}")
    if F<R_FTV-FLOOR_MARGIN: why.append(f"floor {F:.1f}<{R_FTV-FLOOR_MARGIN:.1f}")
    print(f"{sid:3s} {E:7.0f} {S:9.2f} {F:7.1f}   {'OK' if ok else '✗ '+', '.join(why)}")
print(f"\nAUDIO GATE {'PASS' if not bad else f'{bad} FAILURE(S)'}")
sys.exit(1 if bad else 0)
