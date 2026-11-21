#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 s03_edl.py | tail -3
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > logs/s08_c.log 2>&1 || exit 1
python3 s09_align.py | tail -2
python3 s05_plan04.py | tail -24 || exit 1
python3 gfx04.py > logs/gfx_c.log 2>&1 || exit 2
grep -E "^(flow|tour|LT|CTA)" logs/gfx_c.log
python3 s06_inserts04.py || exit 3
python3 s07_captions.py 9x16 > logs/s07_c.log 2>&1 || exit 4
cp cards_9x16/analysis.mp4 cards_9x16/analysis_blue_keep.mp4
ANALYSIS=olive python3 s06_inserts04.py analysis || exit 4
python3 s10_render04.py 9x16 || exit 5
env BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 python3 s08_audio.py > logs/s08_c2.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
R=round1; mkdir -p $R/stills
"$FF" -nostdin -y -v error -t 31.164 -i picture_9x16.mp4 -t 31.164 -i mix.wav -map 0:v -map 1:a -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -af "afade=t=out:st=30.86:d=0.3" -c:a aac -b:a 256k -movflags +faststart "$R/DRAFT - RA-04 round 1 - first 30 seconds.mp4" || exit 8
"$FF" -nostdin -y -v error -i "$R/DRAFT - RA-04 round 1 - first 30 seconds.mp4" -vf scale=540:960 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 128k -movflags +faststart "$R/DRAFT - RA-04 round 1 - first 30 seconds - REVIEW 540p.mp4" || exit 9
"$FF" -nostdin -y -v error -ss 1.5 -i draft_9x16.mp4 -frames:v 1 -vf scale=540:960 $R/stills/first30.jpg
"$FF" -nostdin -y -v error -ss 4.6 -i cards_9x16/analysis_blue_keep.mp4 -frames:v 1 -vf scale=540:960 $R/stills/analysis_blue.jpg
"$FF" -nostdin -y -v error -ss 4.6 -i cards_9x16/analysis_olive.mp4 -frames:v 1 -vf scale=540:960 $R/stills/analysis_olive.jpg
python3 page04.py --media || exit 10
echo CHAIN_C_COMPLETE
