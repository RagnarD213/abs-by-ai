#!/bin/zsh
# RO-11 round 4 delivery: the gated master (same bytes, stamps travel with it), sidecars, 540p review copy, notes, recipe.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; FF="$P/Media/video_edit/bin/ffmpeg"
W=/Volumes/Extreme/_edit_work/ro11; R=$W/round4
D="$P/claude edited long form content/11 - When Calories Don't Matter For Fat Loss"
T="When Calories Don't Matter For Fat Loss | claude round 4 | 16x9 | RO-11"
mkdir -p "$D/recipe-RO-11"
cp "$R/RO11_MASTER.mp4" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$R/RO11_MASTER.mp4.$s" ] && cp "$R/RO11_MASTER.mp4.$s" "$D/$T.mp4.$s"
done
cp "$R/RO11.srt" "$D/$T.srt"; cp "$R/RO11.chapters.txt" "$D/$T.chapters.txt"
cp "$R/RO-11 audio AB (Muhammad then ours).mp4" "$D/$T | audio AB (Muhammad then ours).mp4"
[ -f "$R/logs/deliver_gate.log" ] && cp "$R/logs/deliver_gate.log" "$D/$T.deliver_gate.log"
nice -n 20 "$FF" -v error -y -i "$R/RO11_MASTER.mp4" -vf "scale=960:540:flags=lanczos" -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k \
  -movflags +faststart "$D/$T | REVIEW 540p.mp4"
cp "$R/notes-RO11.md" "$D/notes-RO11.md"
cp "$R"/ROUND-*-REVIEW.md "$D/" 2>/dev/null || true
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO-11/"
cp "$R/plan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/hf/manifest.json" "$W/hf/BEATS.md" "$D/recipe-RO-11/"
[ -f "$R/negative_events_scan.json" ] && cp "$R/negative_events_scan.json" "$D/recipe-RO-11/"
[ -f "$R/srt_fixes.json" ] && cp "$R/srt_fixes.json" "$D/recipe-RO-11/"
ls -la "$D"
