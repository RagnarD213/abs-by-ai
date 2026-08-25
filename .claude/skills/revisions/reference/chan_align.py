#!/usr/bin/env python3
"""Decide whether a delivered cut's two audio channels are the SAME mic or TWO mics,
and how much voice a mono fold-down loses.  Usage: chan_align.py video.mp4

Reads:
  same-mic residual  : best-fit delay+gain alignment of L against R.
                       < -12 dB => one mic (safe).  ~ -3 dB => two different mics.
  mono penalty       : rms of (L+R)/2 vs the louder channel, 300-3400 Hz voice band.
                       Negative numbers are voice you lose on every phone speaker.
  clipping           : samples at full scale per channel.
Needs the static ffmpeg on PATH (Media/video_edit/bin).
"""
import subprocess, sys, tempfile, os, wave
import numpy as np
from numpy.fft import rfft, irfft

def load(path):
    wav = os.path.join(tempfile.mkdtemp(), "s.wav")
    subprocess.run(["ffmpeg","-v","error","-i",path,"-vn","-ar","48000",
                    "-c:a","pcm_s16le",wav,"-y"], check=True)
    w = wave.open(wav,"rb"); sr = w.getframerate()
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768.
    if w.getnchannels() != 2: sys.exit("not stereo — nothing to compare")
    d = d.reshape(-1,2)
    return d[:,0].copy(), d[:,1].copy(), sr

def bp(x, lo, hi, sr):
    X = rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    X[(f<lo)|(f>hi)] = 0
    return irfft(X, n=len(x))

def db(x): return 20*np.log10(max(float(x),1e-12))

def align(a, b, sr, maxlag_ms=20):
    ml = int(maxlag_ms/1000*sr)
    A = a-a.mean(); B = b-b.mean(); N = len(A)
    cc = irfft(rfft(A,2*N)*np.conj(rfft(B,2*N)), 2*N)
    cc = np.concatenate([cc[-ml:], cc[:ml+1]])
    lags = np.arange(-ml, ml+1)
    i = int(np.argmax(np.abs(cc))); lag = int(lags[i])
    Bs = np.roll(B, lag)
    g = float(np.dot(A,Bs)/np.dot(Bs,Bs))
    r = A - g*Bs
    return lag/sr*1000, g, db(np.sqrt(np.mean(r**2))) - db(np.sqrt(np.mean(A**2)))

def main(path, probes=(16,47,78,110,168,228)):
    L,R,sr = load(path)
    dur = len(L)/sr
    print(f"duration {dur:.1f}s")
    for nm,ch in (("L",L),("R",R)):
        c = int(np.sum(np.abs(ch)>=0.999))
        print(f"  {nm} clipped samples {c:>8d}  ({c/len(ch)*100:.4f}%)  peak {db(np.max(np.abs(ch))):+.2f} dBFS")
    print("\nsame-mic test  (residual < -12 dB => ONE mic; ~ -3 dB => TWO different mics)")
    for t in probes:
        if t+4 > dur: continue
        s,e = int(t*sr), int((t+4)*sr)
        lag,g,res = align(L[s:e], R[s:e], sr)
        print(f"  t={t:4d}s  lag {lag:+6.2f} ms  gain {g:+.3f}"
              f"{'  (POLARITY INVERTED)' if g<0 else ''}  residual {res:+.1f} dB")
    print("\nmono fold-down penalty, 300-3400 Hz voice band")
    for t in probes:
        if t+5 > dur: continue
        s,e = int(t*sr), int((t+5)*sr)
        a = bp(L[s:e],300,3400,sr); b = bp(R[s:e],300,3400,sr)
        la, rb = db(np.sqrt(np.mean(a**2))), db(np.sqrt(np.mean(b**2)))
        su = db(np.sqrt(np.mean(((a+b)/2)**2)))
        print(f"  t={t:4d}s  L {la:+6.1f}  R {rb:+6.1f}  sum/2 {su:+6.1f}"
              f"   loss vs louder channel {su-max(la,rb):+.1f} dB")

if __name__ == "__main__":
    main(sys.argv[1])
