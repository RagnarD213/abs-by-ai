#!/bin/zsh
# RO-03 round 2 delivery: the gated master (same bytes, stamps travel with it), sidecars, 540p review copy, notes, recipe,
# the VLC copy in Videos to Review. Absolute paths.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; FF="$P/Media/video_edit/bin/ffmpeg"
W=/Volumes/Extreme/_edit_work/ro03; R=$W/round2
D="$P/claude edited long form content/13 - The Vacuum Workout Only"
T="The Vacuum Workout Only | claude round 2 | 16x9 | RO-03"
mkdir -p "$D/recipe-RO-03"
cp "$R/RO03_MASTER.mp4" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json; do
  [ -f "$R/RO03_MASTER.mp4.$s" ] && cp "$R/RO03_MASTER.mp4.$s" "$D/$T.mp4.$s"
done
cp "$R/RO03.srt" "$D/$T.srt"; cp "$R/RO03.chapters.txt" "$D/$T.chapters.txt"
cp "$R/RO03_MASTER.edit-sheet.json" "$D/$T.edit-sheet.json"
cp "$R/RO-03 audio AB (reference then ours).mp4" "$D/$T audio AB (reference then ours).mp4"
[ -f "$R/logs/deliver_gate.log" ] && cp "$R/logs/deliver_gate.log" "$D/$T.deliver_gate.log"
cp "$R/logs/audio_gate.log" "$D/$T.audio_gate.whole-film.log"; cp "$R/logs/audio_gate_speech_only.log" "$D/$T.audio_gate.speech-only.log"
[ -f "$R/RO-03 round 2 - full film - REVIEW 540p.mp4" ] || nice -n 20 "$FF" -nostdin -v error -y -i "$R/RO03_MASTER.mp4" -vf "scale=960:540:flags=lanczos" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k \
  -movflags +faststart "$R/RO-03 round 2 - full film - REVIEW 540p.mp4"
cp "$R/RO-03 round 2 - full film - REVIEW 540p.mp4" "$D/$T REVIEW 540p.mp4"
cp "$R/notes-RO03.md" "$D/notes-RO03.md"
cp "$R"/ROUND-*-REVIEW.md "$D/" 2>/dev/null || true
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO-03/"
cp "$R/plan.json" "$R/srt_words.json" "$R/negative_events_scan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/marks.json" "$W/FIT.json" "$W/hf/manifest.json" "$W/hf/BEATS.md" "$W/round2-plan/decisions.json" "$D/recipe-RO-03/"
mkdir -p "$P/Videos to Review"
cp "$R/RO03_MASTER.mp4" "$P/Videos to Review/Vacuum Workout Only LFC R2 - full film.mp4"
find "$P/Videos to Review" -maxdepth 1 \( -name "Vacuum Workout Only LFC R1*" -o -name "Vacuum Workout Only LFC - 8-14 vs 8-28*" \) -print -delete
ls -la "$D"
