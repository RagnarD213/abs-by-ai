#!/bin/bash
# RO-21 round 1 first-minute draft: 0 to 62.0 s (ends after "...keep doing the earlier ones as you go."), warm grade, voice B.
set -euo pipefail
cd /Volumes/Expansion/_edit_work/RO-21/recipe; O=/Volumes/Expansion/_edit_work/RO-21/round1/fm
FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 facts_r1.py > /dev/null; python3 manifest_r1.py
G1=$(python3 -c "print(round(62.0*30000/1001))")
python3 assemble_r1.py $O/pic.mp4 --g0 0 --g1 $G1 --grade warm --stills 90,330,600,750,1100,1350,1500,1700
"$FF" -v error -y -i $O/pic.mp4 -ss 0 -i /Volumes/Expansion/_edit_work/RO-21/audio/film/film_voice_B.wav -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 256k -af "afade=t=out:st=61.45:d=0.3" -t 61.75 -movflags +faststart "$O/DRAFT - RO-21 round 1 - first minute.mp4"
"$FF" -v error -y -i "$O/DRAFT - RO-21 round 1 - first minute.mp4" -vf "scale=960:540:flags=lanczos" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k \
  -movflags +faststart "$O/DRAFT - RO-21 round 1 - first minute - REVIEW 540p.mp4"
echo FM DONE
