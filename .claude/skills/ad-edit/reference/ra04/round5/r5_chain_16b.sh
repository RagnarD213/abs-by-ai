#!/bin/bash
# RA-04 round 5 b: the 16:9 after the caption fix (s07 16x9 already rebuilt): re-composite, remux, deliver, then every 16:9 gate input
# again on the new file (measure, audio gate with the untreated baseline, negative sheet; plan + watch run after the look).
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/top 3 tips for getting abs - RA-04"
M="$D/top 3 tips for getting abs | claude | 16x9 | RA-04.mp4"
python3 -c "import sys; sys.path.insert(0,'$SH'); import buildcap; buildcap.wait('RA-04 r5 16b')"
SEG_DIR=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_16x9 SKIP1=1 python3 s10_render04r4.py 16x9 > logs/r5_recomp_16b.log 2>&1 || { echo RECOMP FAIL; exit 5; }
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r5.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round5/master_16x9_r5.mp4 || exit 7
cp round5/master_16x9_r5.mp4 "$M"
./round5/r5_measure.sh 16x9 "$M" > logs/r5_measure_16x9b.log 2>&1 || { echo MEASURE FAIL; exit 1; }
python3 "$SH/audio/audio_gate.py" "$M" --untreated mix_r5.wav.audio_untreated.json --ab "$D/top 3 tips for getting abs | AB audio ref-vs-ours 16x9 | RA-04.mp4" > logs/r5_audio_gate_16x9b.log 2>&1; echo "audio gate exit $?"
"$FF" -nostdin -v error -y -i "$M" -vf "fps=1,scale=-2:300,tile=10x6" -frames:v 1 /private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/neg_16x9b.jpg
nice -n 10 "$FF" -nostdin -v error -y -i "$M" -vf "scale=960:540:flags=lanczos" -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 160k -movflags +faststart "$D/top 3 tips for getting abs | REVIEW 540p 16x9 | RA-04.mp4"
echo "R5_16B_COMPLETE $(date +%T)"
