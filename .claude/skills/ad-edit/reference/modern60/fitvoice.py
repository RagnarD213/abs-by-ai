#!/usr/bin/env python3
"""Measure a candidate voice chain against the reference voice, band by band.

Averaged over several windows across BOTH videos -- a single 4 s window over-fits.
"""
import subprocess,wave,numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BANDS=[(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),(2000,3200),(3200,5000),(5000,8000),(8000,10500)]
OURS=[(31.0,4),(35.0,4),(42.0,4),(51.5,3),(61.0,3)]
HIS =[(29.0,4),(33.0,3),(36.5,4),(51.5,3),(56.0,3)]
def grab(src,af,wins,out):
    parts=[]
    for i,(ss,d) in enumerate(wins):
        subprocess.run([FF,"-nostdin","-y","-v","error","-ss",str(ss),"-t",str(d),"-i",src,
                        "-af",af,"-ac","1","-ar","22050","-c:a","pcm_s16le","-f","wav",f"_w{i}.wav"],check=True)
        parts.append(f"_w{i}.wav")
    data=b""
    for p in parts:
        w=wave.open(p); data+=w.readframes(w.getnframes())
    o=wave.open(out,"wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(22050)
    o.writeframes(data); o.close()
def spec(p):
    w=wave.open(p);a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
    N=2048;fr=np.array([a[i:i+N]*np.hanning(N) for i in range(0,len(a)-N,512)])
    S=np.abs(np.fft.rfft(fr,axis=1));f=np.fft.rfftfreq(N,1/22050)
    rms=np.sqrt((fr**2).mean(1));keep=rms>np.percentile(rms,55)
    m=S[keep].mean(0)+1e-12
    return f,20*np.log10(m/m.sum()*len(m))
grab("reference/muhammad_a.mp4","pan=mono|c0=0.5*c0+0.5*c1",HIS,"_ref.wav")
F,H=spec("_ref.wav")
def test(chain,label,quiet=False):
    grab("tight60.mov",chain,OURS,"_fit.wav")
    _,o=spec("_fit.wav")
    errs=[o[(F>=lo)&(F<hi)].mean()-H[(F>=lo)&(F<hi)].mean() for lo,hi in BANDS]
    if not quiet:
        print(f"{label:40s} mean|err| {np.mean(np.abs(errs)):.2f} dB  max {np.max(np.abs(errs)):.2f}")
        print("      " + " ".join(f"{e:+5.1f}" for e in errs))
    return np.mean(np.abs(errs))
