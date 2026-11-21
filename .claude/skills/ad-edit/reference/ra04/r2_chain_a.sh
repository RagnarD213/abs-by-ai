#!/bin/bash
# RA-04 round 2: picture with the fixed flow_b (B0049 from 28.0 s), then voice B locked to it, then the mux.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 s10_render04.py 9x16 > logs/r2_render.log 2>&1 || exit 5
env BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 OUT=mix_r2.wav EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+3.78,equalizer=f=194:t=q:w=1.3:g=+3.01,equalizer=f=316:t=q:w=1.3:g=+1.70,equalizer=f=490:t=q:w=1.3:g=+0.33,equalizer=f=735:t=q:w=1.3:g=-1.02,equalizer=f=1755:t=q:w=1.3:g=-1.43,equalizer=f=2775:t=q:w=1.3:g=-3.04,equalizer=f=4387:t=q:w=1.3:g=-4.10,treble=g=+0.42:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+3.0' python3 s08_audio.py > logs/r2_s08.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r2.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round2/draft_r2_9x16.mp4 || exit 7
echo R2_CHAIN_A_COMPLETE
