#!/bin/bash
# RA-04 round 4: the full film. 9:16 picture (land-then-hold track, dan08 + brokenarm from round 3), voice B (round 2's fitted EQ +
# the 120 Hz bass lift, Realizer bed -32) locked to it, mux; then the 16:9 from the same edit: graphics, cards, captions, picture, mux
# with the same mix (same 1765 frames).
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4')"
echo "SLOT $(date +%T)"
set -x
python3 s07_captions.py 9x16 > logs/r4_s07_9.log 2>&1 || exit 4
python3 s10_render04r4.py 9x16 > logs/r4_s10_9.log 2>&1 || exit 5
env BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 OUT=mix_r4.wav EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+3.78,equalizer=f=194:t=q:w=1.3:g=+3.01,equalizer=f=316:t=q:w=1.3:g=+1.70,equalizer=f=490:t=q:w=1.3:g=+0.33,equalizer=f=735:t=q:w=1.3:g=-1.02,equalizer=f=1755:t=q:w=1.3:g=-1.43,equalizer=f=2775:t=q:w=1.3:g=-3.04,equalizer=f=4387:t=q:w=1.3:g=-4.10,treble=g=+0.42:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+3.0' python3 s08_audio.py > logs/r4_s08.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_9x16_r4.mp4 || exit 7
echo "R4_9x16_DONE $(date +%T)"
python3 gfx16_04.py > logs/r4_gfx16.log 2>&1 || exit 8
python3 s06_inserts16_04.py > logs/r4_s06_16.log 2>&1 || exit 9
python3 s07_captions.py 16x9 > logs/r4_s07_16.log 2>&1 || exit 10
python3 s10_render04r4.py 16x9 > logs/r4_s10_16.log 2>&1 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_16x9_r4.mp4 || exit 12
echo "R4_CHAIN_COMPLETE $(date +%T)"
