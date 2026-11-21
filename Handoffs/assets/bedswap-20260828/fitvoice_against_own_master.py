#!/usr/bin/env python3
"""Fit the RAW cutdown's voice to V4's OWN processed voice.

Reference = V4 355-371.3 s (Dan talking, no music: the bass scan shows no beat
between 133.25 s and 371.50 s). Ours = the same words in the raw, at V4 - 0.040 s.
Compare on SPEECH frames only and normalise each spectrum by its own total, so the
fit is tone and not level.
"""
import subprocess, sys, wave
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BANDS=[(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),
       (2000,3200),(3200,5000),(5000,8000),(8000,10500)]
REF_W=[(356.0,4),(361.0,4),(365.5,4),(368.0,3.2)]           # V4 time
OUR_W=[(t-0.040,d) for t,d in REF_W]                        # raw time
def grab(src, af, wins, out):
    data=b""
    for i,(ss,d) in enumerate(wins):
        subprocess.run([FF,"-nostdin","-y","-v","error","-ss",str(ss),"-t",str(d),"-i",src,
            "-af",af,"-ac","1","-ar","22050","-c:a","pcm_s16le","-f","wav",f"/tmp/_v4w{i}.wav"],check=True)
        w=wave.open(f"/tmp/_v4w{i}.wav"); data+=w.readframes(w.getnframes())
    o=wave.open(out,"wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(22050)
    o.writeframes(data); o.close()
def spec(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
    N=2048
    fr=np.array([a[i:i+N]*np.hanning(N) for i in range(0,len(a)-N,512)])
    S=np.abs(np.fft.rfft(fr,axis=1)); f=np.fft.rfftfreq(N,1/22050)
    rms=np.sqrt((fr**2).mean(1)); keep=rms>np.percentile(rms,55)
    m=S[keep].mean(0)+1e-12
    return f,20*np.log10(m/m.sum()*len(m))
grab("wav/v4_44k.wav","anull",REF_W,"/tmp/_v4ref.wav")
F,H=spec("/tmp/_v4ref.wav")
def test(chain,label):
    grab("wav/raw44.wav", chain or "anull", OUR_W, "/tmp/_v4fit.wav")
    _,o=spec("/tmp/_v4fit.wav")
    errs=[o[(F>=lo)&(F<hi)].mean()-H[(F>=lo)&(F<hi)].mean() for lo,hi in BANDS]
    print(f"{label:44s} mean|err| {np.mean(np.abs(errs)):5.2f} dB  max {np.max(np.abs(errs)):5.2f}")
    print("      " + " ".join(f"{e:+5.1f}" for e in errs))
    return np.mean(np.abs(errs)),errs
print("bands: " + " ".join(f"{lo:>5}" for lo,_ in BANDS))
if len(sys.argv)>1:
    for c in sys.argv[1:]: test(c,c[:42])
else:
    test("","RAW (no EQ)")
