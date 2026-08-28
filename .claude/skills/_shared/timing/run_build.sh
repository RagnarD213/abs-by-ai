#!/bin/zsh
# Cold, single-tenant instrumented rebuild of the Ad 1 vertical master.
cd /Volumes/Extreme/_edit_work/_timing/build
mkdir -p seg out gfx cap logs
S="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/timing/stage.zsh"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"

"$S" 01_build_base   python3 build_base.py   > logs/01_build_base.log   2>&1 || echo "FAIL build_base"
"$S" 02_build_audio  python3 build_audio.py  > logs/02_build_audio.log  2>&1 || echo "FAIL build_audio"
"$S" 03_finish_audio python3 finish_audio.py > logs/03_finish_audio.log 2>&1 || echo "FAIL finish_audio"
"$S" 04_captions     python3 captions.py     > logs/04_captions.log     2>&1 || echo "FAIL captions"
"$S" 05_render       python3 render.py       > logs/05_render.log       2>&1 || echo "FAIL render"
"$S" 06_master_mux "$FF" -v error -y -i picture.mp4 -i captions.mov -i audio_final.wav \
   -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[v]" -map "[v]" -map 2:a \
   -r 30000/1001 -t 232.768 -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p \
   -af "alimiter=limit=0.79:attack=3:release=60:level=disabled" -c:a aac -b:a 256k \
   -movflags +faststart TIMING_master.mp4 > logs/06_mux.log 2>&1 || echo "FAIL mux"
"$S" 07_review_540p "$FF" -v error -y -i TIMING_master.mp4 -vf scale=540:-2 \
   -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 128k TIMING_review540.mp4 \
   > logs/07_review.log 2>&1 || echo "FAIL review"
echo BUILD_DONE
