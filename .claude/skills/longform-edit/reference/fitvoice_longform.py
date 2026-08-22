#!/usr/bin/env python3
"""Fit our lav against the reference edit's voice, band by band.

Same method as the modern-edit task: average several windows (a single 4 s window
over-fits), keep only frames above the 55th percentile of RMS so the comparison is
made on SPEECH and not on room tone, and normalise each spectrum by its own total
so the comparison is tone, not level.
usage: fitvoice.py ["<ffmpeg -af chain>"] ...
"""
import subprocess, sys, wave
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
REF = "/Volumes/Seagate 4TB/_edit_work/ad1-8-14/reference/muhammad_a.mp4"
OURS = "/Volumes/Seagate 4TB/_edit_work/spraytan/voice_raw.wav"
BANDS = [(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),
         (2000,3200),(3200,5000),(5000,8000),(8000,10500)]
HIS  = [(6.0,4),(14.0,4),(24.0,4),(38.0,4),(50.0,4)]
OUR  = [(60.0,5),(300.0,5),(600.0,5),(850.0,5),(1050.0,5)]

def grab(src, af, wins, out):
    data = b""
    for i,(ss,d) in enumerate(wins):
        subprocess.run([FF,"-nostdin","-y","-v","error","-ss",str(ss),"-t",str(d),"-i",src,
            "-af",af,"-ac","1","-ar","22050","-c:a","pcm_s16le","-f","wav",f"/tmp/_w{i}.wav"],check=True)
        w=wave.open(f"/tmp/_w{i}.wav"); data+=w.readframes(w.getnframes())
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

grab(REF,"pan=mono|c0=0.5*c0+0.5*c1",HIS,"/tmp/_ref.wav")
F,H = spec("/tmp/_ref.wav")

def test(chain,label):
    grab(OURS, chain or "anull", OUR, "/tmp/_fit.wav")
    _,o = spec("/tmp/_fit.wav")
    errs=[o[(F>=lo)&(F<hi)].mean()-H[(F>=lo)&(F<hi)].mean() for lo,hi in BANDS]
    print(f"{label:38s} mean|err| {np.mean(np.abs(errs)):5.2f} dB   max {np.max(np.abs(errs)):5.2f}")
    print("      " + " ".join(f"{e:+5.1f}" for e in errs))
    return np.mean(np.abs(errs)), errs

print("bands: " + " ".join(f"{lo//100 if lo>=1000 else lo:>5}" for lo,_ in BANDS))
if len(sys.argv)>1:
    for c in sys.argv[1:]: test(c, c[:36])
else:
    test("", "RAW right-channel lav (no EQ)")
