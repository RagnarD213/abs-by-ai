#!/usr/bin/env python3
"""Close the loop on the raw insert's tonal seam.

Fitting the insert against its neighbour in the SOURCE gets most of the way, but the finished
short then gets a whole-short EQ and a limiter on top, which move it again. So measure the
seam that actually survives to the delivered file and fold it back into work/rawfit.txt.
"""
import subprocess, sys
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
F="out/e_stop-buying-a-big-supplement-stack.mp4"
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000)]
def prof(t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',F,'-t',str(d),'-vn','-ac','1',
                      '-ar','48000','-f','s16le','-'],capture_output=True)
    x=np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
    n=len(x)//960; fr=x[:n*960].reshape(n,960); rms=np.sqrt((fr**2).mean(1))
    loud=fr[rms>np.percentile(rms,65)]
    S=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    fq=np.fft.rfftfreq(960,1/48000)
    return np.array([10*np.log10(max(1e-12,S[(fq>=a)&(fq<b)].mean())) for a,b in BANDS])
seam = prof(5.5,38.0) - prof(0.3,4.0)
seam = seam - seam.mean()
print("residual seam per band:", np.round(seam,1), f"  RMS {float(np.sqrt((seam**2).mean())):.2f} dB")
af = open('work/rawfit.txt').read().strip()
import re
gains = [float(m) for m in re.findall(r'width=1\.0:g=(-?[\d.]+)', af)]
new = np.clip(np.array(gains) + seam*0.9, -10, 10)
print("rawfit gains", np.round(gains,1), "->", np.round(new,1))
parts = af.split(',')
k = 0
for i,p in enumerate(parts):
    if 'width=1.0:g=' in p:
        parts[i] = re.sub(r'g=-?[\d.]+', f'g={new[k]:.1f}', p); k += 1
open('work/rawfit.txt','w').write(','.join(parts))
print("updated work/rawfit.txt")
