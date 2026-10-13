#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 s05_plan04.py || exit 1
python3 gfx04.py || exit 2
python3 s06_inserts04.py || exit 3
python3 s07_captions.py 9x16 || exit 4
python3 s10_render04.py 9x16 || exit 5
env BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 python3 s08_audio.py || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
echo CHAIN_B_COMPLETE
