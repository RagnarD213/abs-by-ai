#!/usr/bin/env python3
"""Does Muhammad's audio carry a music bed under the voice, and how loud?

If it does, that is a structural difference no amount of denoising can close: under his voice
there is musical content, under ours there is room. Test for a steady beat in the speech gaps
(a periodic onset pattern), and measure the bed's level relative to his speech.
"""
import subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PROJ="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FILES={'Muhammad ad':f"{PROJ}/Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4",
       'Muhammad organic':f"{PROJ}/Muhammad Organic Videos/Daniel Organic Video -The $17 Ab Wheel Beats Every Crunch-v2 HD.mp4",
       'OUR delivered short 1':'out/b_the-3-supplements-that-matter.mp4'}
for lab,f in FILES.items():
    p=subprocess.run([FF,'-v','error','-ss','8','-i',f,'-t','120','-vn','-ac','1','-ar','48000',
                      '-f','s16le','-'],capture_output=True)
    x=np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
    if len(x)<48000*20: print(f"{lab}: too short"); continue
    # low-band energy envelope at 100 Hz frame rate; a music bed shows a periodic onset pattern
    hop=480
    n=len(x)//hop
    fr=x[:n*hop].reshape(n,hop)
    S=np.abs(np.fft.rfft(fr*np.hanning(hop),axis=1))
    fq=np.fft.rfftfreq(hop,1/48000)
    low=S[:,(fq>=40)&(fq<180)].mean(1)
    e=20*np.log10(np.maximum(1e-9,np.sqrt((fr**2).mean(1))))
    quiet=e<np.percentile(e,25)
    # autocorrelation of the low-band onset envelope during quiet frames
    env=low.copy(); env[~quiet]=np.nan
    env=np.where(np.isnan(env),np.nanmedian(env),env)
    env=env-env.mean()
    ac=np.correlate(env,env,'full')[len(env)-1:]
    ac/=max(1e-12,ac[0])
    lo,hi=int(0.30/0.01),int(1.20/0.01)     # 50-200 BPM
    k=lo+int(np.argmax(ac[lo:hi]))
    print(f"{lab}")
    print(f"   strongest periodicity in the quiet frames: {60/(k*0.01):5.1f} BPM, "
          f"autocorrelation {ac[k]:.3f}  -> {'A BEAT IS PRESENT' if ac[k]>0.25 else 'no steady beat'}")
    print(f"   level in quiet frames {np.percentile(e,15):6.1f} dB, speech p95 {np.percentile(e,95):6.1f} dB "
          f"-> bed sits {np.percentile(e,95)-np.percentile(e,15):.1f} dB under speech")
