#!/usr/bin/env python3
"""Website video audio: lav voice chain -> centred stereo, a QUIET ducked CC0 bed, NO
transition SFX (trust brief), two-pass loudnorm to -14 LUFS / -1.5 dBTP.

Source is already the lav only, mono (base.py). The VOICE chain is Ad 1 rev-5 / Ad 3's,
adjusted by the measured 10-band difference between this roll's lav and C1593's
(voicecmp below): this lav is ~2 dB lighter at 150-250 Hz, ~2 dB hotter at 1.4-3.5 kHz
and 4.3 dB lower above 5.5 kHz. So: the 320 Hz cut is eased 4.6 -> 2.6, the 2.6 kHz
boost eased 2.6 -> 0.6, and the air shelf gets an extra +3 dB above 5.5 kHz.
Music: Pixabay "acoustic_bg" -- flattest of the four cleared beds (level sd 2.35 dB),
Pixabay Content Licence, commercial use, NO attribution.
"""
import json, os, subprocess, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
VIDEO=os.environ.get("VIN",f"{HERE}/nocap.mov")
OUT=os.environ.get("VOUT",f"{HERE}/nocap_audio.mov")
MUSIC="/Volumes/Extreme/_edit_work/ad1-8-14/rev5/music/acoustic_bg.mp3"
MUSIC_DB=-23.0; MUSIC_FADE=2.0

VOICE=("highpass=f=80,"
       "equalizer=f=320:t=q:w=1.1:g=-2.6,"
       "equalizer=f=170:t=q:w=1.0:g=0.8,"
       "equalizer=f=1700:t=q:w=1.3:g=-2.4,"
       "equalizer=f=560:t=q:w=1.0:g=1.4,"
       "equalizer=f=2600:t=q:w=1.1:g=0.6,"
       "treble=g=4.6:f=3500:width_type=q:width=0.7,"
       "treble=g=3.0:f=6500:width_type=q:width=0.7,"
       "agate=threshold=0.010:ratio=1.6:range=0.5:attack=3:release=300:knee=8,"
       "acompressor=threshold=0.10:ratio=3:attack=10:release=200:makeup=1.7,"
       "pan=stereo|c0=c0|c1=c0")

def dur_of(p):
    return float(subprocess.run([FFP,"-v","error","-show_entries","format=duration",
        "-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())

def chain(total):
    return (f"[0:a]{VOICE},asplit=2[vmix][vkey];"
      f"[1:a]aloop=loop=3:size={int(140*44100)},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
      f"volume={MUSIC_DB}dB,afade=t=in:st=0:d=1.5,"
      f"afade=t=out:st={total-MUSIC_FADE:.3f}:d={MUSIC_FADE}[mus];"
      f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=8:attack=12:release=420:"
      f"makeup=1:level_sc=1[duck];"
      f"[vmix][duck]amix=inputs=2:duration=first:normalize=0,aresample=48000[premix]")

def measure(fc):
    p=subprocess.run([FF,"-nostdin","-hide_banner","-nostats","-i",VIDEO,"-i",MUSIC,
        "-filter_complex",fc+";[premix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
        "-map","[a]","-f","null","-"],capture_output=True,text=True)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}")+1])

def main():
    total=dur_of(VIDEO); fc=chain(total); m=measure(fc)
    print("measured:",{k:m[k] for k in ("input_i","input_tp","input_lra")})
    ln=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
        f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
    p=subprocess.run([FF,"-nostdin","-y","-hide_banner","-nostats","-i",VIDEO,"-i",MUSIC,
        "-filter_complex",f"{fc};[premix]{ln}[aout]",
        "-map","0:v","-map","[aout]","-t",f"{B.DUR:.3f}","-c:v","copy",
        "-c:a","pcm_s16le",OUT],capture_output=True,text=True,check=True)
    j=json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}")+1])
    print("loudnorm pass 2:",{k:j[k] for k in ("output_i","output_tp","normalization_type")})
    print(OUT,"done")

if __name__=="__main__": main()
