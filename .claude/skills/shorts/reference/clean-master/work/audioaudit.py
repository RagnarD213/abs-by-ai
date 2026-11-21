#!/usr/bin/env python3
"""Why does one short sound worse than the others?

Dan: short 4 (A) "doesn't sound as good as the other ones", plus "double-check the audio on
all these shorts... I feel like we have room to improve."

Measure per short, on the DELIVERED file: integrated loudness and range, the noise floor
between words, the voice-band tilt, and crest factor. A short cut from a different part of a
23-minute take can differ in all of these even though loudnorm put them all at -14.
"""
import json, subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
rows = json.load(open('work/delivered.json'))
OUT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/'
print(f"{'#':2s} {'id':2s} {'LUFS':>7s} {'LRA':>5s} {'floor':>7s} {'p95':>7s} {'SNR':>6s} "
      f"{'crest':>6s} {'LF/HF tilt':>10s} {'sibilance':>9s}")
res={}
for r in rows:
    p = subprocess.run([FF,'-v','error','-i',OUT+r['name'],'-vn','-ac','1','-ar','48000',
                        '-f','s16le','-'],capture_output=True)
    x = np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
    # 20 ms frames
    n=len(x)//960
    fr=x[:n*960].reshape(n,960)
    rms=np.sqrt((fr**2).mean(1))
    db=20*np.log10(np.maximum(1e-7,rms))
    floor=np.percentile(db,10); p95=np.percentile(db,95)
    crest=20*np.log10(np.abs(x).max()/np.sqrt((x**2).mean()))
    # spectrum of the loud (speech) frames only
    loud=fr[db>np.percentile(db,70)]
    S=np.abs(np.fft.rfft(loud*np.hanning(960),axis=1)).mean(0)
    f=np.fft.rfftfreq(960,1/48000)
    band=lambda a,b: 20*np.log10(max(1e-9,S[(f>=a)&(f<b)].mean()))
    tilt=band(120,400)-band(2000,5000)
    sib=band(5000,9000)-band(300,3000)
    ln=subprocess.run([FF,'-hide_banner','-nostats','-i',OUT+r['name'],'-af','ebur128',
                       '-f','null','-'],capture_output=True,text=True).stderr
    I=float([l for l in ln.split('\n') if 'I:' in l and 'LUFS' in l][-1].split()[-2])
    LRA=float([l for l in ln.split('\n') if 'LRA:' in l and 'LU' in l][-1].split()[-2])
    res[r['id']]=dict(I=I,LRA=LRA,floor=floor,p95=p95,crest=crest,tilt=tilt,sib=sib)
    print(f"{r['n']:<2d} {r['id']:2s} {I:7.1f} {LRA:5.1f} {floor:7.1f} {p95:7.1f} "
          f"{p95-floor:6.1f} {crest:6.1f} {tilt:10.1f} {sib:9.1f}")
json.dump(res,open('work/audioaudit.json','w'),indent=1)
med={k:np.median([v[k] for v in res.values()]) for k in ('floor','tilt','sib','crest','LRA')}
print("\ndeviation from the batch median:")
for sid,v in res.items():
    d={k:v[k]-med[k] for k in med}
    flags=[f"{k} {d[k]:+.1f}" for k in med if abs(d[k])>1.5]
    print(f"  {sid}: {', '.join(flags) if flags else 'in line with the batch'}")
