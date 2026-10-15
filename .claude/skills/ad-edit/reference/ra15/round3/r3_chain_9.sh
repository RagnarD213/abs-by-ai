#!/bin/bash
# RA-15 round 3: the 9:16 master. Captions, picture (land-then-hold track, salmon macro card), the approved V2 voice (mix_bass.wav's
# chain and EQ) frame-locked to the picture, mux with the audio exactly the picture's length.
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r3 9x16')"
echo "SLOT $(date +%T)"
set -x
python3 s07_captions.py 9x16 > logs/s07_r3.log 2>&1 || exit 4
python3 s10_render05.py 9x16 > logs/s10_r3.log 2>&1 || exit 5
EQ=$(python3 -c "import json;print(json.load(open('mix_bass.wav.voice_chain.json'))['eq'])")
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_bass_r3.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass_r3 \
   --eq "$EQ" --frame-lock picture_9x16.mp4 > logs/s08_r3.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_9x16_r3.mp4 || exit 7
echo "R3_CHAIN9_COMPLETE $(date +%T)"
