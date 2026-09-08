#!/usr/bin/env python3
"""Ad 3 audio: lav voice chain -> centred stereo, ducked CC0 music bed, transition SFX,
two-pass loudnorm to -14 LUFS / -1.5 dBTP.

Source is already the RIGHT channel only, mono (base3.py). That is the fix that matters:
the roll carries two mics 7.81 ms apart with the far one polarity-inverted.

The VOICE chain is Ad 1 rev-5's, reused unchanged: C1593's lav measures within 0.47 dB
mean / 0.90 dB max of C1591's across ten speech bands, so a refit would be noise.
Music: Pixabay "Background Music" -- Pixabay Content Licence, commercial use, NO
attribution (a CC-BY track would oblige a credit inside a paid ad).
"""
import importlib.util, json, os, subprocess, sys
import numpy as np
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec=importlib.util.spec_from_file_location("sfxlib",f"{SK}/sfxlib.py")
sfxlib=importlib.util.module_from_spec(spec); spec.loader.exec_module(sfxlib)
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats3 as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
VIDEO=os.environ.get("VIN",f"{HERE}/nocap.mov")
OUT=os.environ.get("VOUT",f"{HERE}/nocap_audio.mov")
MUSIC="/Volumes/Extreme/_edit_work/ad1-8-14/rev5/music/acoustic_bg.mp3"
SR=sfxlib.SR
MUSIC_DB=-19.0; MUSIC_FADE=1.6; SFX_DB=-11.0; LEAD=0.06

CARDS =["whycard","brocard","before","goalimg","today","cta1","howcard","cta2"]
PANELS=["costcard","tailor","planbul","adapts","adaptmid"]
CHIPS =["lower3a","num1","num3","num4","toolate","gymq","notprice"]
N2B={n:getattr(B,n.upper()) for n in CARDS+PANELS+CHIPS}
CLIP_BEATS=[B.ROBOTCUT,B.SPACLIP,B.ROBOTSTORY,B.APPGEN,B.ASSESS,B.WORKOUT,B.DEMOS]
BULLET_PHRASES={
 "costcard":["on meal prep","quality food","or a home gym"],
 "planbul": ["any injuries you have","the equipment you actually own","how many days a week"],
 "adapts":  ["If it's too difficult","If it's too easy","Didn't sleep well"],
 "tailor":  ["and your lagging body parts","And it tailors your program"],
 "adaptmid":["If you can't get to the gym"]}

def np_bullets(name,a,b):
    out=[]
    for ph in BULLET_PHRASES.get(name,[]):
        try: out.append(B.at(ph,after=a-0.5))
        except KeyError: pass
    return [t for t in out if a<t<b]

def cues():
    c=[]
    for n in CARDS:
        a,b=N2B[n]; c+=[(a,"whoosh",0.80),(b,"whoosh_out",0.55)]
    for n in PANELS:
        a,b=N2B[n]; c+=[(a,"whoosh",0.85),(a,"sub",0.55),(b,"whoosh_out",0.60)]
    # (no transient on lower thirds -- see the density note in the module docstring)
    for (a,b) in CLIP_BEATS: c+=[(a,"whoosh",0.70),(b,"whoosh_out",0.45)]
    c.append((B.WHYCARD[0]-0.72,"riser",0.55))
    c.append((B.HOWCARD[0]-0.72,"riser",0.50))
    for n in PANELS:
        a,b=N2B[n]
        for t in np_bullets(n,a,b): c.append((t,"pop_soft",0.60))
    # the "200 POUNDS" number pop inside the before card
    c.append((B.BEFORE[0]+(B.BEFORE[1]-B.BEFORE[0])*0.46,"pop",0.55))
    c=sorted(t for t in c if 0<=t[0]<B.DUR)
    # Beats run back to back here, so an exit whoosh lands on the next card's entrance
    # and the pair reads as one muddy noise. Drop the exit when something enters <0.35s.
    ents=[t for t,n,_ in c if n in ("whoosh","whoosh_soft")]
    return [(t,n,g) for (t,n,g) in c
            if n!="whoosh_out" or not any(abs(t-e)<0.35 for e in ents)]

def dur_of(p):
    return float(subprocess.run([FFP,"-v","error","-show_entries","format=duration",
        "-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())

def build_sfx_bed(total,CUES):
    pack={k:sfxlib.__dict__[fn](**kw) for k,(fn,kw) in {
        "whoosh":("whoosh",dict(dur=0.42,f0=420,f1=4200,f2=900)),
        "whoosh_soft":("whoosh",dict(dur=0.34,f0=500,f1=2600,f2=800,q=1.0,seed=11)),
        "whoosh_out":("whoosh",dict(dur=0.36,f0=3200,f1=900,f2=320,q=1.1,seed=19)),
        "pop":("pop",dict(freq=920)),
        "pop_soft":("pop",dict(freq=700,dur=0.10,drop=0.40)),
        "riser":("riser",dict(dur=0.75)),
        "sub":("sub_drop",dict()),
    }.items()}
    bed=np.zeros(int(total*SR)+SR)
    for (t,name,gain) in CUES:
        y=pack[name]*gain; i=int(max(0.0,t-LEAD)*SR); bed[i:i+len(y)]+=y
    pk=np.abs(bed).max()
    if pk>0.9: bed*=0.9/pk
    sfxlib.save(f"{HERE}/sfxbed.wav",bed[:int(total*SR)])
    print(f"sfxbed.wav  {len(CUES)} cues, peak {pk:.2f}")

VOICE=("highpass=f=80,"
       "equalizer=f=320:t=q:w=1.1:g=-4.6,"
       "equalizer=f=170:t=q:w=1.0:g=-0.2,"
       "equalizer=f=1700:t=q:w=1.3:g=-2.0,"
       "equalizer=f=560:t=q:w=1.0:g=1.4,"
       "equalizer=f=2600:t=q:w=1.1:g=2.6,"
       "treble=g=4.6:f=3500:width_type=q:width=0.7,"
       "agate=threshold=0.010:ratio=1.6:range=0.5:attack=3:release=300:knee=8,"
       "acompressor=threshold=0.10:ratio=3:attack=10:release=200:makeup=1.7,"
       "pan=stereo|c0=c0|c1=c0")

def chain(total):
    return (f"[0:a]{VOICE},asplit=2[vmix][vkey];"
      f"[1:a]aloop=loop=3:size={int(140*44100)},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
      f"volume={MUSIC_DB}dB,afade=t=in:st=0:d=1.0,"
      f"afade=t=out:st={total-MUSIC_FADE:.3f}:d={MUSIC_FADE}[mus];"
      f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=9:attack=12:release=420:"
      f"makeup=1:level_sc=1[duck];"
      f"[2:a]volume={SFX_DB}dB[sfx];"
      f"[vmix][duck][sfx]amix=inputs=3:duration=first:normalize=0,aresample=48000[premix]")

def measure(fc):
    p=subprocess.run([FF,"-nostdin","-hide_banner","-nostats","-i",VIDEO,"-i",MUSIC,
        "-i",f"{HERE}/sfxbed.wav","-filter_complex",
        fc+";[premix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
        "-map","[a]","-f","null","-"],capture_output=True,text=True)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}")+1])

def main():
    total=dur_of(VIDEO); C=cues(); build_sfx_bed(total,C)
    fc=chain(total); m=measure(fc)
    print("measured:",{k:m[k] for k in ("input_i","input_tp","input_lra")})
    ln=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
        f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([FF,"-nostdin","-y","-v","error","-i",VIDEO,"-i",MUSIC,
        "-i",f"{HERE}/sfxbed.wav","-filter_complex",f"{fc};[premix]{ln}[aout]",
        "-map","0:v","-map","[aout]","-t",f"{B.DUR:.3f}","-c:v","copy",
        "-c:a","pcm_s16le",OUT],check=True)
    print(OUT,"done")

if __name__=="__main__":
    if "cues" in sys.argv:
        for t,n,g in cues(): print(f"  {t:7.2f}  {n:<12} {g}")
    else: main()
