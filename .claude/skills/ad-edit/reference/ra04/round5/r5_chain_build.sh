#!/bin/bash
# RA-04 round 5: the full film from round5/r5_plan.py's beats.json and round5/r5_cards.py's cards. Captions, picture (full stage 1:
# the holds are re-indexed and the last one is shorter), the mix locked to the new picture (round 4's voice B chain and bed), mux.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SEG9=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_9x16; SEG16=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_16x9
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r5')"
echo "SLOT $(date +%T)"
set -x
if [ -z "$SKIP9" ]; then
python3 s07_captions.py 9x16 > logs/r5_s07_9.log 2>&1 || exit 4
SEG_DIR=$SEG9 SKIP1=${S1ONLY_9:-0} python3 s10_render04r4.py 9x16 > logs/r5_s10_9.log 2>&1 || exit 5
fi
env AUDIO_END=$(python3 -c "import json;print(json.load(open('beats.json'))['total'])") BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 OUT=mix_r5.wav EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=+3.78,equalizer=f=194:t=q:w=1.3:g=+3.01,equalizer=f=316:t=q:w=1.3:g=+1.70,equalizer=f=490:t=q:w=1.3:g=+0.33,equalizer=f=735:t=q:w=1.3:g=-1.02,equalizer=f=1755:t=q:w=1.3:g=-1.43,equalizer=f=2775:t=q:w=1.3:g=-3.04,equalizer=f=4387:t=q:w=1.3:g=-4.10,treble=g=+0.42:f=6500:width_type=q:width=0.6,equalizer=f=120:t=q:w=0.8:g=+3.0' python3 s08_audio.py > logs/r5_s08.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r5.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round5/master_9x16_r5.mp4 || exit 7
echo "R5_9x16_DONE $(date +%T)"
python3 s07_captions.py 16x9 > logs/r5_s07_16.log 2>&1 || exit 10
SEG_DIR=$SEG16 python3 s10_render04r4.py 16x9 > logs/r5_s10_16.log 2>&1 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r5.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round5/master_16x9_r5.mp4 || exit 12
echo "R5_BUILD_COMPLETE $(date +%T)"
