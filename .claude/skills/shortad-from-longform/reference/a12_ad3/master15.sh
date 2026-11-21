#!/bin/zsh
# Render 12 (2026-09-14): render 11 (Dan-approved colour + audio) with ONE change -- story clip v2, shot 3 (the bathroom
# mirror) regenerated without the breath-smoke/fogging-mirror artifact. Only chunk 0 (0-2845) contains the story beat
# (1944-2845); chunks 2845 and 5640 are render 11's own files (no input newer than picture_0.mp4 of render 11).
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert
while true; do n=$(for p in $(pgrep -f "whisper|ffmpeg|render|zbase|scan.py"); do lsof -a -p $p -d cwd -Fn 2>/dev/null | grep ^n | cut -c2-; done | grep -v ad3-vert | grep -E "_edit_work|Abs By AI" | sort -u | wc -l); [ $n -lt 2 ] && break; echo "waiting: $n other builds"; sleep 30; done
echo "master15 start $(date)"
python3 render3.py --from 0 --to 2845 --out picture_0_r12.mp4 > logs/render15_0.log 2>&1 || { echo CHUNK0 FAILED; tail -5 logs/render15_0.log; exit 1; }
printf "file 'picture_0_r12.mp4'\nfile 'picture_2845.mp4'\nfile 'picture_5640.mp4'\n" > cat15.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i cat15.txt -c copy picture_r12.mp4 || { echo CONCAT FAILED; exit 1; }
python3 zmux.py picture_r12.mp4 ad3_vertical_9x16_r12.mp4 > logs/mux15.log 2>&1 && cat logs/mux15.log || { echo MUX FAILED; tail logs/mux15.log; exit 1; }
echo "MASTER15 DONE $(date)"
