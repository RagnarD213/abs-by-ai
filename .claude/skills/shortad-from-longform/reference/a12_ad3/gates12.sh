#!/bin/zsh
# Render 12 gates (2026-09-14): render 11 + story v2 (shot 3 smoke artifact removed). Same checks as gates9.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert
AUD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
F=ad3_vertical_9x16.mp4
while true; do n=$(for p in $(pgrep -f "whisper|ffmpeg|render|zbase|scan.py"); do lsof -a -p $p -d cwd -Fn 2>/dev/null | grep ^n | cut -c2-; done | grep -v ad3-vert | grep -E "_edit_work" | sort -u | wc -l); [ $n -lt 2 ] && break; echo "waiting for a build slot: $n other builds"; sleep 30; done
echo "gates12 start $(date)"
rm -rf watch/strip watch/clip watch/sheets
python3 watch.py $F              > logs/watch12.log 2>&1    ; tail -12 logs/watch12.log
python3 zwatch_sheets.py         > logs/sheets12.log 2>&1   ; tail -2 logs/sheets12.log
python3 caption_sync_check.py $F > logs/capsync12.log 2>&1  ; tail -5 logs/capsync12.log
python3 zhairgate2.py $F         > logs/hairgate12.log 2>&1 ; tail -7 logs/hairgate12.log
python3 landing_check.py $F      > logs/landing12.log 2>&1  ; tail -4 logs/landing12.log
python3 "$AUD/audio_gate.py" $F --reference-mix ref/ad3_v6hd.mp4 --verbatim --ab AB_audio_his-vs-ours.mp4 > logs/audio12.log 2>&1 ; tail -8 logs/audio12.log
python3 qc.py $F --reference-cut ref/ad3_v6hd.mp4 > logs/qc12.log 2>&1 ; tail -26 logs/qc12.log
echo "GATES12 DONE $(date)"
