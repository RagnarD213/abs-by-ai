#!/usr/bin/env python3
"""Is this roll really two microphones hard-panned, and if so which channel wins?

Measures, per channel and for the naive L+R sum:
  inter-channel delay + polarity (cross-correlation)
  clipped samples, SNR (speech rms vs the quietest 5% of frames)
  comb ripple: the std-dev of the speech spectrum after removing its broad tilt --
  a comb filter shows up as regular ripple that no EQ curve can flatten.
usage: chan_analyse.py <video> [start] [dur]
"""
import subprocess, sys, wave
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
src = sys.argv[1]; ss = sys.argv[2] if len(sys.argv) > 2 else "200"; dur = sys.argv[3] if len(sys.argv) > 3 else "60"
subprocess.run([FF,"-nostdin","-v","error","-y","-ss",ss,"-t",dur,"-i",src,
    "-vn","-ac","2","-ar","48000","-c:a","pcm_s16le","/tmp/_ch.wav"],check=True)
w=wave.open("/tmp/_ch.wav"); n=w.getnframes(); sr=w.getframerate()
a=np.frombuffer(w.readframes(n),dtype=np.int16).reshape(-1,2).astype(np.float64)/32768
L,R=a[:,0],a[:,1]
print(f"{src.split('/')[-1]}  {ss}s +{dur}s  sr={sr}  channels=2")
# delay + polarity
# FFT cross-correlation: np.correlate("full") on 20s at 48kHz is O(n^2) and hangs.
seg=slice(0,min(len(L),sr*20))
x,y=L[seg]-L[seg].mean(),R[seg]-R[seg].mean()
N=1<<int(np.ceil(np.log2(len(x)*2)))
c=np.fft.irfft(np.fft.rfft(x,N)*np.conj(np.fft.rfft(y,N)),N)
c=np.concatenate([c[-(sr//10):],c[:sr//10]])          # +/-100 ms only
lags=np.arange(-(sr//10),sr//10)
k=int(np.argmax(np.abs(c))); lag=lags[k]; peak=c[k]
den=np.sqrt((x**2).sum()*(y**2).sum())
print(f"  peak cross-correlation {peak/den:+.3f} at lag {lag} samples = {lag/sr*1000:+.2f} ms"
      f"   -> {'POLARITY INVERTED' if peak<0 else 'in polarity'}")
print(f"  zero-lag correlation   {float((x*y).sum()/den):+.3f}")
def stats(sig,name):
    clipped=int((np.abs(sig)>=0.999).sum())
    N=1024; fr=np.array([sig[i:i+N] for i in range(0,len(sig)-N,512)])
    rms=np.sqrt((fr**2).mean(1)+1e-15)
    sp=rms>np.percentile(rms,70); nz=rms<np.percentile(rms,5)
    snr=20*np.log10(rms[sp].mean()/max(rms[nz].mean(),1e-9))
    S=np.abs(np.fft.rfft(fr[sp]*np.hanning(N),axis=1)).mean(0)+1e-12
    f=np.fft.rfftfreq(N,1/sr); band=(f>300)&(f<6000)
    db=20*np.log10(S[band]); sm=np.convolve(db,np.ones(9)/9,"same")
    ripple=float(np.std((db-sm)[5:-5]))
    print(f"  {name:14s} clipped {clipped:7d}   SNR {snr:5.1f} dB   comb ripple {ripple:.2f} dB   "
          f"peak {20*np.log10(max(np.abs(sig).max(),1e-9)):+.1f} dBFS")
    return snr,ripple,clipped
stats(L,"LEFT"); stats(R,"RIGHT"); stats((L+R)/2,"naive L+R sum")
