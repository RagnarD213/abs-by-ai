#!/bin/bash
# RA-04 round 4 b: after the 9:16 watch-pass judge. The home card re-timed to B0464's clean stretch (7.30 s, round4/r4_home.py) with a new
# NEAR hold for "to do instead", and the CTA hold's calmer track (r4_track.py). Same mix (mix_r4.wav: same cut, same 1765 frames).
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4b')"
echo "SLOT $(date +%T)"
set -x
python3 s06_inserts04.py home > logs/r4b_s06_9.log 2>&1 || exit 3
python3 s07_captions.py 9x16 > logs/r4b_s07_9.log 2>&1 || exit 4
python3 s10_render04r4.py 9x16 > logs/r4b_s10_9.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_9x16_r4b.mp4 || exit 7
echo "R4B_9x16_DONE $(date +%T)"
python3 s06_inserts16_04.py home > logs/r4b_s06_16.log 2>&1 || exit 9
python3 s07_captions.py 16x9 > logs/r4b_s07_16.log 2>&1 || exit 10
python3 s10_render04r4.py 16x9 > logs/r4b_s10_16.log 2>&1 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_16x9_r4b.mp4 || exit 12
echo "R4B_CHAIN_COMPLETE $(date +%T)"
