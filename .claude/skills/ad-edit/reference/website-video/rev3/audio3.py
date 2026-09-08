#!/usr/bin/env python3
"""REV 2 audio -- the voice chain fitted to Muhammad's ad (voicefit.py), a gentle downward
expander, NO compressor by default, a bed at -30 dB or lower (or none), centred stereo,
then the measured gain + alimiter finish from audio2.py (never loudnorm: it went DYNAMIC
on rev 1). The gate (reference/voice_ref_check.py) is the judge, not this script.

  VIN=<video-or-wav> VOUT=<out> [MUSIC_DB=-30|none] [COMP=0|1] python3 audio3.py

What rev 1 did wrong, measured (handoff §1): bed at -23 dB + a 3:1 compressor with makeup +
two air shelves lifted everything between the words 9.5 dB above his floor. The raw lav was
8 dB CLEANER than his ad. So: EQ fitted to HIS file, compressor off, bed quiet or absent.
"""
import json, os, re, subprocess, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
VIN=os.environ.get("VIN",f"{HERE}/nocap.mov")
VOUT=os.environ.get("VOUT",f"{HERE}/nocap_audio.mov")
MUSIC="/Volumes/Extreme/_edit_work/ad1-8-14/rev5/music/acoustic_bg.mp3"
_m=os.environ.get("MUSIC_DB","-30")
MUSIC_DB=None if _m.lower() in ("none","off","") else float(_m)
COMP=os.environ.get("COMP","0")=="1"
MUSIC_FADE=2.0
TARGET_I=float(os.environ.get("TARGET_I","-14"))

# voicefit.py iteration 2 (2026-09-02): tone error vs his ad mean 0.76 dB / max 1.06 on the
# gate's own metric. Later iterations reached 0.30 but only by alternating +4/-3/+1.5/-7 on
# neighbouring bands -- an over-fit comb, not a voice EQ. This curve is smooth: fill the thin
# 150-250 (+2.7), pull the 600-900 honk (-5.1) and the 1.4-2.2 k edge (-3.3), and put back
# the air the lav does not have (+7.9 above 6.5 k).
EQ=("highpass=f=70,"
    "equalizer=f=110:t=q:w=1.3:g=-1.80,"
    "equalizer=f=194:t=q:w=1.3:g=+2.66,"
    "equalizer=f=316:t=q:w=1.3:g=+0.31,"
    "equalizer=f=735:t=q:w=1.3:g=-5.07,"
    "equalizer=f=1122:t=q:w=1.3:g=-0.67,"
    "equalizer=f=1755:t=q:w=1.3:g=-3.33,"
    "equalizer=f=2775:t=q:w=1.3:g=+0.44,"
    "equalizer=f=4387:t=q:w=1.3:g=-0.39,"
    "treble=g=+7.87:f=6500:width_type=q:width=0.6")
# gentle downward expander for the room between words: the +7.9 dB air shelf lifts hiss up
# there, this takes ~9 dB back between words and leaves the words alone
EXPAND=os.environ.get("EXPAND","agate=threshold=0.012:ratio=1.8:range=0.35:attack=4:release=250:knee=6")
# at most 1.5:1 above -18 dB (handoff §1 step 2) -- OFF by default; his LRA is 3.5
COMPRESS="acompressor=threshold=0.126:ratio=1.5:attack=12:release=220:makeup=1.0"
VOICE=",".join(x for x in [EQ,EXPAND,(COMPRESS if COMP else ""),"pan=stereo|c0=c0|c1=c0"] if x)

def dur_of(p):
    return float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",p],
                                capture_output=True,text=True).stdout.strip())

def chain(total):
    if MUSIC_DB is None:
        return f"[0:a]{VOICE},aresample=48000[premix]"
    return (f"[0:a]{VOICE},asplit=2[vmix][vkey];"
      f"[1:a]aloop=loop=3:size={int(140*44100)},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
      f"volume={MUSIC_DB}dB,afade=t=in:st=0:d=1.5,afade=t=out:st={total-MUSIC_FADE:.3f}:d={MUSIC_FADE}[mus];"
      f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=6:attack=12:release=420:makeup=1:level_sc=1[duck];"
      f"[vmix][duck]amix=inputs=2:duration=first:normalize=0,aresample=48000[premix]")

def inputs():
    return ["-i",VIN]+(["-i",MUSIC] if MUSIC_DB is not None else [])

def premix(fc,extra):
    return subprocess.run([FF,"-nostdin","-v","error"]+inputs()+["-filter_complex",f"{fc};[premix]{extra}[a]",
        "-map","[a]","-ac","2","-ar","48000","-f","f32le","-"],capture_output=True).stdout

def ebur(fc,extra):
    p=subprocess.run([FF,"-nostdin","-nostats"]+inputs()+["-filter_complex",f"{fc};[premix]{extra},ebur128=peak=true[a]",
        "-map","[a]","-f","null","-"],capture_output=True,text=True).stderr
    g=lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)",p)[-1]); return g("I"),g("Peak"),g("LRA")

def main():
    total=dur_of(VIN); fc=chain(total)
    print(f"voice: {VOICE}\nbed: {MUSIC_DB} dB   comp: {COMP}")
    I0,TP0,LRA0=ebur(fc,"anull"); print(f"premix  I {I0:.2f}  TP {TP0:.2f}  LRA {LRA0:.2f}")
    gain=TARGET_I-I0
    LIM="alimiter=limit=0.71:attack=5:release=60:level=false"
    # limiter delay measured on the real programme by cross-correlation (audio2.py lesson)
    ref=np.frombuffer(premix(fc,f"volume={gain:.3f}dB"),dtype=np.float32).reshape(-1,2)[:,0]
    lim=np.frombuffer(premix(fc,f"volume={gain:.3f}dB,{LIM}"),dtype=np.float32).reshape(-1,2)[:,0]
    sr=48000; s=slice(20*sr,40*sr); x=ref[s]-ref[s].mean(); y=lim[s]-lim[s].mean()
    N=1<<int(np.ceil(np.log2(len(x)*2))); c=np.fft.irfft(np.fft.rfft(y,N)*np.conj(np.fft.rfft(x,N)),N)
    lags=np.concatenate([np.arange(0,600),np.arange(-600,0)]); cc=np.concatenate([c[:600],c[-600:]])
    delay=int(lags[int(np.argmax(cc))]); print(f"limiter delay {delay} samples")
    def fin(g):
        return f"volume={g:.3f}dB,{LIM}"+(f",atrim=start_sample={delay},asetpts=N/SR/TB,apad=whole_dur={total:.3f}" if delay>0 else "")
    I1,TP1,LRA1=ebur(fc,fin(gain)); print(f"gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    if abs(I1-TARGET_I)>0.3:
        gain+=(TARGET_I-I1); I1,TP1,LRA1=ebur(fc,fin(gain)); print(f"gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    is_wav=VOUT.lower().endswith(".wav")
    maps=(["-map","[aout]"] if is_wav else ["-map","0:v","-map","[aout]","-c:v","copy"])
    subprocess.run([FF,"-nostdin","-y","-v","error"]+inputs()+["-filter_complex",f"{fc};[premix]{fin(gain)}[aout]"]+maps+
        ["-t",f"{total:.3f}","-c:a","pcm_s16le",VOUT],check=True)
    print(VOUT,"done")

if __name__=="__main__": main()
