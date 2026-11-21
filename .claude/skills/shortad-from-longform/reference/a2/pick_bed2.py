#!/usr/bin/env python3
"""Pick the bed against THIS reference's bed, on TEMPO first and spectral shape second.

His bed measures a 0.480 s beat (125 BPM) with the pulse carried in 6-14 kHz hats and a
30-150 Hz kick. Attempt 1 inherited a 99.6 BPM acoustic strummer chosen against an older,
different reference and Dan said it put him to sleep. Tempo is the first-class criterion.
"""
import glob, json, os, subprocess, sys
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SR=48000
BANDS=[(60,150),(150,400),(400,1000),(1000,3000),(3000,8000),(8000,14000)]
HIS_BEAT=0.480

def load(p, ss=None, t=None):
    c=[FF,'-v','error']
    if ss is not None: c+=['-ss',str(ss)]
    if t is not None: c+=['-t',str(t)]
    c+=['-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,dtype=np.float32).astype(float)

def shape(a,n=1<<13):
    acc=np.zeros(n//2+1); k=0
    for i in range(0,max(1,len(a)-n),n):
        acc+=np.abs(np.fft.rfft(a[i:i+n]*np.hanning(n))); k+=1
    acc/=max(k,1); fr=np.fft.rfftfreq(n,1/SR)
    v=np.array([20*np.log10(acc[(fr>=lo)&(fr<hi)].mean()+1e-12) for lo,hi in BANDS])
    return v-v.max()

def beat(a):
    N,H=1024,256; fps=SR/H
    fr=np.lib.stride_tricks.sliding_window_view(a,N)[::H]*np.hanning(N)
    S=np.abs(np.fft.rfft(fr,axis=1)); f=np.fft.rfftfreq(N,1/SR)
    best=None
    for lo,hi in ((30,150),(6000,14000)):
        b=S[:,(f>=lo)&(f<hi)].sum(1)
        d=np.maximum(0,np.diff(b)); d=(d-d.mean())/(d.std()+1e-9)
        ac=np.correlate(d,d,'full')[len(d)-1:]; ac/=ac[0]
        lags=np.arange(len(ac))/fps; band=(lags>0.28)&(lags<1.1)
        k=int(np.argmax(ac[band])); v=(float(lags[band][k]), float(ac[band][k]))
        if best is None or v[1]>best[1]: best=v
    return best

# --- his bed from the speech gaps of HIS mix
# His cut has NO usable speech gaps -- 776 words, only 2 gaps over 0.5 s and a longest of
# 0.64 s, because airtight pause removal is the whole point of his edit. So the bed is
# estimated by MIN-STATISTICS instead: the 8th percentile of magnitude per frequency bin
# over the whole file, which is what is left when the voice is not in that bin.
HISWAV='ref_audit/his.wav'
def minstat(a, n=1<<13):
    fr=np.array([a[i:i+n]*np.hanning(n) for i in range(0,len(a)-n,n//2)])
    S=np.abs(np.fft.rfft(fr,axis=1))
    m=np.percentile(S,8,axis=0)
    f=np.fft.rfftfreq(n,1/SR)
    v=np.array([20*np.log10(m[(f>=lo)&(f<hi)].mean()+1e-12) for lo,hi in BANDS])
    return v-v.max()
HIS=minstat(load(HISWAV))
print('his bed estimated by min-statistics over the whole mix (no usable speech gaps)')
print('his band profile:', ' '.join(f'{x:5.1f}' for x in HIS), f'  beat {HIS_BEAT:.3f}s = {60/HIS_BEAT:.0f} BPM')
print()
print(f'{"track":<20}{"dur":>6}{"beat":>7}{"BPM":>6}{"|dBPM|":>7}{"shape":>7}{"flat":>6}{"score":>7}   profile')
rows=[]
for p in sorted(glob.glob('music/*.mp3'))+sorted(glob.glob('/Volumes/Extreme/_edit_work/abwheel/r2/music/*.mp3')):
    a=load(p)
    if len(a)<SR*20: continue
    dur=len(a)/SR; s=minstat(a); err=float(np.abs(s-HIS).mean())
    bl,_=beat(a)
    # fold to the octave nearest his
    cands=[bl*k for k in (0.5,1,2)]
    bl=min(cands,key=lambda x: abs(60/x-60/HIS_BEAT))
    dbpm=abs(60/bl-60/HIS_BEAT)
    h=SR*4
    e=20*np.log10(np.sqrt((a[:len(a)//h*h].reshape(-1,h)**2).mean(1))+1e-9)
    flat=float(e.std())
    score=dbpm*0.35 + err + flat*1.2
    rows.append((score,p,dur,bl,dbpm,err,flat,s))
    print(f'{os.path.basename(p)[:20]:<20}{dur:5.0f}s{bl:7.3f}{60/bl:6.0f}{dbpm:7.1f}{err:7.1f}{flat:6.1f}{score:7.1f}   '
          +' '.join(f'{x:5.1f}' for x in s))
rows.sort()
print(f'\nPICK: {rows[0][1]}  ({rows[0][2]:.0f}s, {60/rows[0][3]:.0f} BPM) -> loop x{int(np.ceil(232.8/rows[0][2]))}')
for r in rows[1:4]: print(f'  runner-up: {os.path.basename(r[1])} ({60/r[3]:.0f} BPM, score {r[0]:.1f})')
