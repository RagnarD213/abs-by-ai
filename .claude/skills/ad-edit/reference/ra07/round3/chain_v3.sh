#!/bin/bash
# RA-07 round 3: mux -> first-30 identity -> audio gate -> composite checks -> plan -> watch (v3 picture)
set -e
cd /Volumes/Extreme/_edit_work/ra07
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FP="${FF%ffmpeg}ffprobe"
S="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
M="round3/deliver/fire your trainer | claude | 9x16 | RA-07.mp4"
until grep -q "wrote round3/work_v3/picture_9x16.mp4" round3/assemble_v3.log; do sleep 5; done
rm -f "$M".*.json; rm -rf round3/deliver/watch round3/deliver/logs/watch_pass.json round3/deliver/logs/findings.json
"$FF" -nostdin -y -v error -i round3/work_v3/picture_9x16.mp4 -i round3/mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart "$M"
"$FP" -v error -count_frames -show_entries stream=codec_name,nb_read_frames -of compact "$M"
shasum -a 256 "$M" | cut -c1-16
"$FF" -v error -i round3/work_v3/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round3/v3.md5
"$FF" -v error -i round2/work/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round3/r2.md5
cmp -s round3/v3.md5 round3/r2.md5 && echo "FIRST30 IDENTICAL" || echo "FIRST30 DIFFERS"
python3 "$S/audio/audio_gate.py" "$M" --ab "round3/deliver/fire your trainer | AB audio ref-vs-ours 9x16 | RA-07.mp4" --untreated mix_bass.wav.audio_untreated.json 2>&1 | tail -2
PLAN=beats_r3_dan.json PIC=round3/work_v3/picture_9x16.mp4 python3 s88r3_checks.py 2>&1 | tail -1
"$FF" -nostdin -y -v error -i "$M" -vf "fps=40/52.686,scale=216:384,tile=10x4" -frames:v 1 round3/neg_v3.jpg
echo CHAIN_A_DONE
