#!/usr/bin/env python3
"""Can we take PICTURE from the clean master and AUDIO from the delivered one?

The clean master carries the unrepaired two-mic recording; only FINAL_zepbound.mp4 got the
2026-08-23 single-mic repair. Both are the same picture edit, so if their audio is sample
aligned we can simply pull audio from FINAL and keep cutting picture from the clean file.

Also compares both against Muhammad's ab-wheel cut, which is Dan's reference for good audio.
"""
import subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BASE = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/"
CLEAN, FINAL = BASE+"CUT_v1_graded_NO-GRAPHICS.mp4", BASE+"FINAL_zepbound.mp4"
MUH = "/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4"

def pcm(f,t,d,af='anull'):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.

print("=== alignment: FINAL's audio vs the CLEAN master's right channel ===")
for t in (200.0, 700.0, 1000.0, 1300.0):
    a=pcm(FINAL,t,6.0); b=pcm(CLEAN,t,6.0,'pan=mono|c0=c1')
    n=min(len(a),len(b)); best=(-2,0)
    for lag in range(-4800,4801,4):
        x=a[max(0,lag):max(0,lag)+n-abs(lag)]; y=b[max(0,-lag):max(0,-lag)+n-abs(lag)]
        if len(x)<48000: continue
        d_=np.linalg.norm(x)*np.linalg.norm(y)
        if d_:
            c=float(np.dot(x,y)/d_)
            if c>best[0]: best=(c,lag)
    print(f"  t={t:7.1f}s  corr {best[0]:+.4f} at lag {best[1]/48:+.2f} ms")

print("\n=== voice character vs Muhammad's cut (Dan's reference) ===")
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]
def stats(x):
    n=len(x)//960; fr=x[:n*960].reshape(n,960); rms=np.sqrt((fr**2).mean(1))
    db=20*np.log10(np.maximum(1e-7,rms))
    loud=fr[db>np.percentile(db,70)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    prof=np.array([10*np.log10(max(1e-12,S[(f>=a)&(f<b)].mean())) for a,b in BANDS])
    # comb ripple: how jagged the spectrum is across neighbouring FFT bins in the voice band
    band=(f>=300)&(f<=4000)
    sm=np.convolve(10*np.log10(np.maximum(1e-12,S)),np.ones(9)/9,'same')
    ripple=float(np.std((10*np.log10(np.maximum(1e-12,S))-sm)[band]))
    return prof, float(np.percentile(db,10)), float(np.percentile(db,95)), ripple
for lab,f,t,af in (('CLEAN master, summed (what shipped)',CLEAN,1000.,'anull'),
                   ('CLEAN master, right channel only',CLEAN,1000.,'pan=mono|c0=c1'),
                   ('FINAL master (8/23 repair)',FINAL,1000.,'anull'),
                   ("Muhammad's ab-wheel cut",MUH,120.,'anull')):
    prof,floor,p95,rip = stats(pcm(f,t,30.0,af))
    print(f"  {lab:36s} floor {floor:6.1f}  p95 {p95:6.1f}  SNR {p95-floor:5.1f}  "
          f"comb ripple {rip:4.2f} dB")
