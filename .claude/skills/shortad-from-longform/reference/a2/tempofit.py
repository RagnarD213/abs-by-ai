#!/usr/bin/env python3
"""Rank candidate beds by how closely their tempo and spectral tilt match the bed under
Muhammad's mix. Attempt 1 reused a bed picked by spectral shape against a DIFFERENT, older
reference; Dan's verdict was 'it kind of puts me to sleep'. A bed choice never transfers."""
import glob, subprocess, sys, wave, os
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"

def mono(path, t=60):
    p='/tmp/_tf.wav'
    subprocess.run([FF,'-v','error','-y','-t',str(t),'-i',path,'-ac','1','-ar','48000',
                    '-c:a','pcm_s16le',p],check=True)
    w=wave.open(p); return np.frombuffer(w.readframes(10**9),dtype='<i2').astype(np.float32)/32768

def analyse(m, SR=48000):
    N,H=1024,256; fps=SR/H
    fr=np.lib.stride_tricks.sliding_window_view(m,N)[::H]*np.hanning(N)
    S=np.abs(np.fft.rfft(fr,axis=1)); f=np.fft.rfftfreq(N,1/SR)
    out={}
    for lo,hi,tag in ((28,150,'low'),(6000,14000,'hi')):
        b=S[:,(f>=lo)&(f<hi)].sum(1)
        d=np.maximum(0,np.diff(b)); d=(d-d.mean())/(d.std()+1e-9)
        ac=np.correlate(d,d,'full')[len(d)-1:]; ac/=ac[0]
        lags=np.arange(len(ac))/fps; band=(lags>0.28)&(lags<1.1)
        k=int(np.argmax(ac[band])); out[tag]=(float(lags[band][k]), float(ac[band][k]))
    # onset density: transients per second
    e=S.sum(1); d=np.maximum(0,np.diff(e)); thr=np.percentile(d,97)
    on=(d>thr).sum()/(len(d)/fps)
    tilt=20*np.log10(S[:,(f>=30)&(f<=120)].mean()/S[:,(f>=500)&(f<=4000)].mean())
    return out, on, float(tilt)

if __name__=='__main__':
    print(f'{"track":34s} {"beat(low)":>10s} {"BPM":>7s} {"beat(hi)":>9s} {"BPM":>7s} {"onset/s":>8s} {"tilt dB":>8s}')
    for p in sys.argv[1:]:
        try: m=mono(p)
        except Exception as e: print(p,'ERR',e); continue
        o,on,tilt=analyse(m)
        print(f'{os.path.basename(p)[:34]:34s} {o["low"][0]:10.3f} {60/o["low"][0]:7.1f} '
              f'{o["hi"][0]:9.3f} {60/o["hi"][0]:7.1f} {on:8.2f} {tilt:8.1f}')
