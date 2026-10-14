#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra05
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
R=round1; mkdir -p $R/stills
T=31.6983
"$FF" -nostdin -y -v error -t $T -i picture_9x16.mp4 -t $T -i mix.wav -map 0:v -map 1:a -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -af "afade=t=out:st=31.4:d=0.3" -c:a aac -b:a 256k -movflags +faststart "$R/DRAFT - RA-05 round 1 - first 30 seconds.mp4" || exit 8
"$FF" -nostdin -y -v error -i "$R/DRAFT - RA-05 round 1 - first 30 seconds.mp4" -vf scale=540:960 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 128k -movflags +faststart "$R/DRAFT - RA-05 round 1 - first 30 seconds - REVIEW 540p.mp4" || exit 9
"$FF" -nostdin -y -v error -ss 0.6 -i draft_9x16.mp4 -frames:v 1 -vf scale=540:960 $R/stills/first30.jpg
python3 page05.py --media || exit 10
echo CHAIN_D_COMPLETE
