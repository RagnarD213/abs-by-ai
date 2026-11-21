#!/bin/zsh
# RO-20 round 4 delivery for one video: the gated master (same bytes; stamps travel with it), SRT, chapters, edit sheet, audio A/B, notes, reviews,
# recipe, a 540p review copy, and the full-quality copy in Videos to Review for VLC.  usage: deliver_r4.sh v1 "18 - Why You Should Invest More In Your Health"
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; FF="$P/Media/video_edit/bin/ffmpeg"
V=$1; FOLDER=$2; W=/Volumes/Extreme/_edit_work/ro20; R=$W/round4/$V
JOB=$(cd $W/recipe && python3 -c "import json;print({'v1':'RO-20','v2':'RO-20B','v3':'RO-20C'}['$V'])")
TITLE=$(python3 -c "print({'v1':'Why You Should Invest More In Your Health','v2':'What To Cut To Afford Getting In Shape','v3':'What To Buy For Your Health At Every Income Level'}['$V'])")
NAME=${JOB//-/}; N=${V#v}
D="$P/claude edited long form content/$FOLDER"; T="$TITLE | claude round 4 | 16x9 | $JOB"
mkdir -p "$D/recipe-$JOB"
cp "$R/MASTER.mp4" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$R/MASTER.mp4.$s" ] && cp "$R/MASTER.mp4.$s" "$D/$T.mp4.$s"
done
cp "$R/$NAME.srt" "$D/$T.srt"; cp "$R/$NAME.chapters.txt" "$D/$T.chapters.txt"
[ -f "$R/MASTER.edit-sheet.json" ] && cp "$R/MASTER.edit-sheet.json" "$D/$T.edit-sheet.json"
[ -f "$R/audio AB (reference then ours).mp4" ] && cp "$R/audio AB (reference then ours).mp4" "$D/$T | audio AB (reference then ours).mp4"
[ -f "$R/logs/deliver_gate.log" ] && cp "$R/logs/deliver_gate.log" "$D/$T.deliver_gate.log"
nice -n 20 "$FF" -v error -y -i "$R/MASTER.mp4" -vf "scale=960:540:flags=lanczos" -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k -movflags +faststart "$D/$T | REVIEW 540p.mp4"
cp "$R/notes-$NAME-round4.md" "$D/"
cp "$R"/ROUND-4-REVIEW*.md "$D/" 2>/dev/null || true
cp "$R/plan.json" "$R/layout.json" "$R/logs/watch_pass.json" "$R/logs/findings.json" "$D/recipe-$JOB/" 2>/dev/null || true
cp "$W"/recipe/films_r4.py "$W"/recipe/finish_r4.py "$W"/recipe/build.py "$W"/recipe/frames.py "$W"/recipe/gfx.py "$W"/recipe/bed.py "$W"/recipe/chain_r4_*.sh "$W"/recipe/deliver_r4.sh "$W"/recipe/page6_20.py "$D/recipe-$JOB/"
cp "$W/plan_resolved.json" "$W/shots.json" "$W/edl.json" "$W/hf/manifest.json" "$W/round2/broll_grades.json" "$W/round4/srt_fixes.json" "$D/recipe-$JOB/"
mkdir -p "$P/Videos to Review"; cp "$R/MASTER.mp4" "$P/Videos to Review/Invest In Your Health LFC R4 - video $N full film.mp4"
ls -la "$D"
