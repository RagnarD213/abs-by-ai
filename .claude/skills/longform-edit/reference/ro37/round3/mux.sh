#!/bin/bash
# mux.sh VIDEO.mp4 VOICE.wav VOICE_T0 OUT.mp4 : the voice from VOICE_T0 under the picture, then a 540p review copy
set -e
FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
"$FF" -nostdin -v error -y -i "$1" -ss "$3" -i "$2" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$4"
"$FF" -nostdin -v error -y -i "$4" -vf scale=960:540 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 160k -movflags +faststart "${4%.mp4} - REVIEW 540p.mp4"
