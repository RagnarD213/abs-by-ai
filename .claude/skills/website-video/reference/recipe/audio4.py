#!/usr/bin/env python3
"""REV 6 audio -- audio3.py (the rev-2 chain Dan approved by ear) with the two changes the rev-5 gate numbers ask for:
  1 DEREVERB before the EQ (the shared `_shared/audio/dereverb.py`, spray-tan params) -- audio3 never dereverbed and the
    room measured 77 ms against his 40 (the shorts-01 defect, 85 -> 29-40 ms with this exact stage)
  2 the downward expander is adjustable (EXPAND=... or EXPAND=none) -- agate 0.012/1.8 + 9 dB into the limiter put the
    speech spread at 5.6 dB against his 8.2
Everything else is audio3 verbatim: the fitted EQ, no compressor, bed at MUSIC_DB ducked, centred stereo, measured gain
+ alimiter (never loudnorm), limiter delay measured by cross-correlation.
  VIN=<video> VOUT=<out.mov|.wav> [DEREVERB=1|0] [DR_ALPHA=.62 DR_D1=20 DR_D2=150 DR_FLOOR=-24 DR_SMOOTH=.30]
      [EXPAND=<agate…>|none] [MUSIC_DB=-44|none] [T_MAX=<s>]  python3 audio4.py
"""
import json, os, re, subprocess, sys, wave
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
from dereverb import dereverb
try: import audio3_rev2chain as A3          # the real rev-2 chain (the skill's audio3.py is a shim to voice_chain)
except ImportError: import audio3 as A3
FF=A3.FF; FFP=A3.FFP
VIN=os.environ.get("VIN",f"{HERE}/nocap.mov"); VOUT=os.environ.get("VOUT",f"{HERE}/nocap_audio.mov")
T_MAX=os.environ.get("T_MAX")
DR=os.environ.get("DEREVERB","1")=="1"
DRP=dict(alpha=float(os.environ.get("DR_ALPHA",0.62)),d1_ms=float(os.environ.get("DR_D1",20)),d2_ms=float(os.environ.get("DR_D2",150)),
         floor_db=float(os.environ.get("DR_FLOOR",-24)),smooth=float(os.environ.get("DR_SMOOTH",0.30)))
_ex=os.environ.get("EXPAND",A3.EXPAND); EXPAND="" if _ex.lower() in ("none","off","") else _ex
VOICE=",".join(x for x in [A3.EQ,EXPAND,(A3.COMPRESS if A3.COMP else ""),"pan=stereo|c0=c0|c1=c0"] if x)
SR=48000
def pull(path):
    cmd=[FF,"-nostdin","-v","error","-i",path]+(["-t",T_MAX] if T_MAX else [])+["-map","0:a:0","-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,dtype=np.float32).copy()
def edt(x):
    fr=np.lib.stride_tricks.sliding_window_view(x,512)[::128]
    e=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9); p90=np.percentile(e,90); o=[]
    for i in range(1,len(e)-40):
        if e[i]>p90-4 and e[i+3]<e[i]-4:
            s=e[i:i+40]; b=np.nonzero(s<s[0]-20)[0]
            if len(b): o.append(b[0]*128/SR*1000)
    return float(np.median(o)) if o else float("nan")
def main():
    x=pull(VIN); total=len(x)/SR
    w0=x[20*SR:min(len(x),120*SR)]
    print(f"audio4  {os.path.basename(VIN)}  {total:.2f}s  raw EDT {edt(w0):.0f} ms")
    if DR:
        y=dereverb(x,sr=SR,**DRP); print(f"  dereverb {DRP} -> EDT {edt(y[20*SR:min(len(y),120*SR)]):.0f} ms")
    else: y=x
    lav=VOUT+".lav.wav"; wv=wave.open(lav,"w"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); wv.close()
    # ---- audio3's chain on the (dereverbed) lav; the picture is muxed back from VIN
    A3.VIN=lav; A3.VOICE=VOICE; A3.EXPAND=EXPAND
    print(f"  voice: {VOICE}\n  bed: {A3.MUSIC_DB} dB")
    fc=A3.chain(total)
    I0,TP0,LRA0=A3.ebur(fc,"anull"); print(f"  premix  I {I0:.2f}  TP {TP0:.2f}  LRA {LRA0:.2f}")
    gain=A3.TARGET_I-I0; LIM="alimiter=limit=0.71:attack=5:release=60:level=false"
    ref=np.frombuffer(A3.premix(fc,f"volume={gain:.3f}dB"),dtype=np.float32).reshape(-1,2)[:,0]
    lim=np.frombuffer(A3.premix(fc,f"volume={gain:.3f}dB,{LIM}"),dtype=np.float32).reshape(-1,2)[:,0]
    s=slice(20*SR,min(len(ref),40*SR)); xx=ref[s]-ref[s].mean(); yy=lim[s]-lim[s].mean()
    N=1<<int(np.ceil(np.log2(len(xx)*2))); c=np.fft.irfft(np.fft.rfft(yy,N)*np.conj(np.fft.rfft(xx,N)),N)
    lags=np.concatenate([np.arange(0,600),np.arange(-600,0)]); cc=np.concatenate([c[:600],c[-600:]])
    delay=int(lags[int(np.argmax(cc))]); print(f"  limiter delay {delay} samples")
    def fin(g): return f"volume={g:.3f}dB,{LIM}"+(f",atrim=start_sample={delay},asetpts=N/SR/TB,apad=whole_dur={total:.3f}" if delay>0 else "")
    I1,TP1,LRA1=A3.ebur(fc,fin(gain)); print(f"  gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    if abs(I1-A3.TARGET_I)>0.3:
        gain+=(A3.TARGET_I-I1); I1,TP1,LRA1=A3.ebur(fc,fin(gain)); print(f"  gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    is_wav=VOUT.lower().endswith(".wav")
    cmd=[FF,"-nostdin","-y","-v","error"]+A3.inputs()+([] if is_wav else ["-i",VIN])+["-filter_complex",f"{fc};[premix]{fin(gain)}[aout]"]
    cmd+=(["-map","[aout]"] if is_wav else ["-map",f"{len(A3.inputs())//2}:v","-map","[aout]","-c:v","copy"])
    cmd+=["-t",f"{total:.3f}","-c:a","pcm_s16le",VOUT]
    subprocess.run(cmd,check=True); os.remove(lav)
    json.dump(dict(vin=VIN,dereverb=DRP if DR else None,expand=EXPAND,voice=VOICE,bed_db=A3.MUSIC_DB,gain_db=round(gain,2),lufs=round(I1,2),tp=round(TP1,2),lra=round(LRA1,2),limiter_delay=delay),open(VOUT+".audio4.json","w"),indent=1)
    print(VOUT,"done")
if __name__=="__main__": main()
