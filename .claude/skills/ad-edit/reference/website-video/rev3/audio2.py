#!/usr/bin/env python3
"""Loudness finish WITHOUT loudnorm's silent dynamic fallback (the supplements-shorts /
ad-2 vertical trap): -19.35 LUFS in, TP -1.83 -> a linear +5.35 dB cannot meet -1.5 dBTP,
so loudnorm switched to DYNAMIC and compressed the bed against the voice. Here: pure gain
+ alimiter, delay measured and removed, then the result is MEASURED (ebur128)."""
import json, os, re, subprocess, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import audio as A, beats as B
FF=A.FF; VIDEO=A.VIDEO; OUT=A.OUT; MUSIC=A.MUSIC
total=A.dur_of(VIDEO); fc=A.chain(total)
def premix(extra):
    return subprocess.run([FF,"-nostdin","-v","error","-i",VIDEO,"-i",MUSIC,"-filter_complex",
        f"{fc};[premix]{extra}[a]","-map","[a]","-ac","2","-ar","48000","-f","f32le","-"],capture_output=True).stdout
def ebur(extra):
    p=subprocess.run([FF,"-nostdin","-nostats","-i",VIDEO,"-i",MUSIC,"-filter_complex",
        f"{fc};[premix]{extra},ebur128=peak=true[a]","-map","[a]","-f","null","-"],capture_output=True,text=True).stderr
    g=lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)",p)[-1]); return g("I"),g("Peak"),g("LRA")
I0,TP0,LRA0=ebur("anull"); print(f"premix  I {I0:.2f}  TP {TP0:.2f}  LRA {LRA0:.2f}")
gain=-14.0-I0
LIM="alimiter=limit=0.71:attack=5:release=60:level=false"
# measure the limiter delay on the real programme (never assume 219): xcorr of a 20 s window
ref=np.frombuffer(premix(f"volume={gain:.3f}dB"),dtype=np.float32).reshape(-1,2)[:,0]
lim=np.frombuffer(premix(f"volume={gain:.3f}dB,{LIM}"),dtype=np.float32).reshape(-1,2)[:,0]
sr=48000; s=slice(20*sr,40*sr); x=ref[s]-ref[s].mean(); y=lim[s]-lim[s].mean()
N=1<<int(np.ceil(np.log2(len(x)*2))); c=np.fft.irfft(np.fft.rfft(y,N)*np.conj(np.fft.rfft(x,N)),N)
lags=np.concatenate([np.arange(0,600),np.arange(-600,0)]); cc=np.concatenate([c[:600],c[-600:]])
delay=int(lags[int(np.argmax(cc))]); print(f"limiter delay {delay} samples")
chain=f"volume={gain:.3f}dB,{LIM}"+(f",atrim=start_sample={delay},asetpts=N/SR/TB,apad=whole_dur={total:.3f}" if delay>0 else "")
I1,TP1,LRA1=ebur(chain); print(f"gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
if abs(I1+14)>0.3:
    gain+=(-14.0-I1); chain=f"volume={gain:.3f}dB,{LIM}"+(f",atrim=start_sample={delay},asetpts=N/SR/TB,apad=whole_dur={total:.3f}" if delay>0 else "")
    I1,TP1,LRA1=ebur(chain); print(f"gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
subprocess.run([FF,"-nostdin","-y","-v","error","-i",VIDEO,"-i",MUSIC,"-filter_complex",f"{fc};[premix]{chain}[aout]",
    "-map","0:v","-map","[aout]","-t",f"{B.DUR:.3f}","-c:v","copy","-c:a","pcm_s16le",OUT],check=True)
print(OUT,"done")
