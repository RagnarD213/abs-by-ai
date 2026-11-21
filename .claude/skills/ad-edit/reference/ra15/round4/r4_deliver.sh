#!/bin/bash
# RA-15 round 4: one master into the delivery folder, then every measurement on the exact file.  r3_deliver.sh 9x16|16x9
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
K=$1; D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/never pay a nutritionist again - RA-15"
M="$D/never pay a nutritionist again | claude | $K | RA-15.mp4"; SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
cp master_${K}_r4.mp4 "$M" || exit 1
python3 "$SH/audio/audio_gate.py" "$M" --untreated mix_bass_r3c.wav.audio_untreated.json --ab "$D/never pay a nutritionist again | AB audio ref-vs-ours $K | RA-15.mp4" > logs/agate_$K.log 2>&1
round4/r4_measure.sh $K "$M" > logs/r4_measure_$K.out 2>&1 || exit 3
python3 round4/s_chips15.py > /dev/null || exit 4
"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg" -nostdin -y -v error -i "$M" -vf "fps=1,scale=$([ $K = 9x16 ] && echo 216:384 || echo 320:180),tile=$([ $K = 9x16 ] && echo 13x4 || echo 6x9)" -frames:v 1 round4/check/final_${K}_sheet.jpg
echo "DELIVER_MEASURED $K $(shasum -a 256 "$M" | cut -c1-16)"
