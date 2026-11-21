#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra06
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+3.43,equalizer=f=194:t=q:w=1.3:g=+2.82,equalizer=f=316:t=q:w=1.3:g=+0.97,equalizer=f=490:t=q:w=1.3:g=-0.16,equalizer=f=735:t=q:w=1.3:g=-1.03,equalizer=f=1755:t=q:w=1.3:g=-1.72,equalizer=f=2775:t=q:w=1.3:g=-3.57,equalizer=f=4387:t=q:w=1.3:g=-4.51,treble=g=+1.56:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+3.0' python3 s08_audio.py > logs/s08_a.log 2>&1 || exit 1
env BED=music/Realizer.mp3 BED_DB=-32 EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+3.43,equalizer=f=194:t=q:w=1.3:g=+2.82,equalizer=f=316:t=q:w=1.3:g=+0.97,equalizer=f=490:t=q:w=1.3:g=-0.16,equalizer=f=735:t=q:w=1.3:g=-1.03,equalizer=f=1755:t=q:w=1.3:g=-1.72,equalizer=f=2775:t=q:w=1.3:g=-3.57,equalizer=f=4387:t=q:w=1.3:g=-4.51,treble=g=+1.56:f=6500:width_type=q:width=0.6' OUT=mix_nobass.wav python3 s08_audio.py > logs/s08_b.log 2>&1 || exit 1
python3 s09_align.py > logs/s09_a.log 2>&1 || exit 2
python3 s04_track.py > logs/s04_a.log 2>&1 || exit 3
echo CHAIN_A_COMPLETE
