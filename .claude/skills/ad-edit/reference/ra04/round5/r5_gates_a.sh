#!/bin/bash
# RA-04 round 5 gates, part A (on the DELIVERED files): measurements, chips, the audio gate with its A/B, and a negative-imagery
# contact sheet to LOOK at (s20_neg.py is recorded only after that look, then r5_gates_b.sh).
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/top 3 tips for getting abs - RA-04"
for a in 9x16 16x9; do
  M="$D/top 3 tips for getting abs | claude | $a | RA-04.mp4"
  ./round5/r5_measure.sh $a "$M" > logs/r5_measure_$a.log 2>&1 || { echo "MEASURE FAIL $a"; tail -5 logs/r5_measure_$a.log; exit 1; }
  python3 "$SH/audio/audio_gate.py" "$M" --ab "$D/top 3 tips for getting abs | AB audio ref-vs-ours $a | RA-04.mp4" > logs/r5_audio_gate_$a.log 2>&1; echo "audio gate $a exit $?"; grep -E "VERDICT|FAIL" logs/r5_audio_gate_$a.log | head -8
  "$FF" -nostdin -v error -y -i "$M" -vf "fps=1,scale=-2:300,tile=10x6" -frames:v 1 /private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/neg_$a.jpg
done
python3 round5/s_chips04.py > logs/r5_chips.log 2>&1 || { echo CHIPS FAIL; tail -5 logs/r5_chips.log; exit 2; }
grep -h "candidates" logs/junk_9x16.log logs/junk_16x9.log
echo GATES_A_COMPLETE
