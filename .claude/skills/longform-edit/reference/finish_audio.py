#!/usr/bin/env python3
"""REV2 audio finish: voice chain + two-pass loudnorm, muxed onto the picture.

EQ is FITTED to this roll, not copied. The modern-edit ad chain cuts 320 Hz by
-4.6 dB for a chest bump; measured against the same reference voice, THIS roll is
9.4 dB LIGHT at 80-150 Hz and only boxy at 700-1200, so that curve would have made
it worse. Fitted over five 5-second windows spread across the programme:

    band      80  150  250  400  700  1k2  2k  3k2  5k  8k
    raw     -9.4 -5.2 -2.2 +0.9 +3.5 +0.6 +1.2 +0.4 -4.3 -5.5   mean 3.33 dB
    fitted  -1.9 +1.7 +1.2 +0.3 +0.4 -1.3 -0.8 -0.4 +0.5 +1.2   mean 0.97 dB

Dynamics and the dual-mono fold are taken from the modern-edit chain unchanged:
a gentle downward expander for lav hiss, light compression so the read sits
flatter, then pan the single mic to BOTH channels so the voice is centred instead
of living in one ear.
usage: finish_audio.py
"""
import json, subprocess
from pathlib import Path

B = Path("/Volumes/Seagate 4TB/_edit_work/spraytan")
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VOICE = B / "voice_raw.wav"
VIDEO = B / "roughcuts" / "CUT_v3_gfx.mp4"
OUT   = B / "roughcuts" / "FINAL_spraytan.mp4"

EQ_BODY = ("equalizer=f=115:t=q:w=0.7:g=6.5,"      # chest/warmth the lav loses
      "equalizer=f=210:t=q:w=1.0:g=2.8,"
      "equalizer=f=900:t=q:w=1.1:g=-3.4,"     # boxiness
      "equalizer=f=3800:t=q:w=1.2:g=-2.4,"    # keeps the shelf off the sibilants
      "treble=g=6.2:f=5200:width_type=q:width=0.7")   # the air a chest lav never has
# The gate is FIRMER than the ad chain's (0.016/2.2/0.30 vs 0.010/1.6/0.5) and it
# runs BEFORE the EQ. Reason: the fitted treble shelf is +6.2 dB above 5.2 kHz,
# which lifts lav hiss along with the air. At matched loudness the soft gate left
# the noise floor at -37.7 dBFS, 2.2 dB WORSE than what rev 1 shipped; the firmer
# one lands at -39.7 dBFS, i.e. parity, while the band fit is unchanged (0.99 vs
# 0.97 dB) and four 25-second windows re-transcribe at 100% word overlap against
# the ungated audio, so it is taking room tone and not word tails.
# `afftdn` was tried and rejected: nr=8 dropped the floor to -40.8 dBFS but pushed
# the band error 0.97 -> 1.73 dB, eating exactly the 5-10 kHz air the shelf exists
# to restore.
DYN = ("agate=threshold=0.016:ratio=2.2:range=0.30:attack=3:release=260:knee=8")
CMP = ("acompressor=threshold=0.10:ratio=3:attack=10:release=200:makeup=1.7")
# gate BEFORE eq, compressor after; then send the single mic to BOTH channels so
# the voice sits centred instead of living in one ear
CHAIN = f"highpass=f=65,{DYN},{EQ_BODY},{CMP},pan=stereo|c0=c0|c1=c0"

def measure():
    p = subprocess.run([FF,"-nostdin","-hide_banner","-nostats","-i",str(VOICE),
        "-af",f"{CHAIN},loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
        "-vn","-f","null","-"],capture_output=True,text=True)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}")+1])

m = measure()
print("measured:", {k: m[k] for k in ("input_i","input_tp","input_lra","input_thresh")})
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
      f"offset={m['target_offset']}:linear=true")
subprocess.run([FF,"-nostdin","-y","-v","error","-i",str(VIDEO),"-i",str(VOICE),
    "-filter_complex",f"[1:a]{CHAIN},{ln},aresample=48000[aout]",
    "-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","256k",
    "-movflags","+faststart",str(OUT)],check=True)
print("->", OUT)
