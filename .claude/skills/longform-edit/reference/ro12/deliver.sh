#!/bin/zsh
# RO-12 delivery: copy the gated FINAL (stamps travel with it, same bytes) + sidecars into the project delivery folder, make the
# 540p phone review copy, copy notes and the recipe.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; FF="$P/Media/video_edit/bin/ffmpeg"
W=/Volumes/Extreme/_edit_work/ro12; D="$P/claude edited long form content/09 - Top 5 Zepbound Tips"
T="Top 5 Zepbound Tips"
mkdir -p "$D/recipe-RO12"
cp "$W/out/FINAL.mp4" "$D/$T | claude | 16x9 | RO-12.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json; do
  [ -f "$W/out/FINAL.mp4.$s" ] && cp "$W/out/FINAL.mp4.$s" "$D/$T | claude | 16x9 | RO-12.mp4.$s"
done
cp "$W/out/RO12.srt" "$D/$T.srt"; cp "$W/out/RO12.chapters.txt" "$D/$T - chapters.txt"
cp "$W/out/AB_muhammad-vs-ours.mp4" "$D/$T - audio AB (Muhammad then ours).mp4"
nice -n 20 "$FF" -v error -y -i "$W/out/FINAL.mp4" -vf "scale=960:540:flags=lanczos" -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k \
  -movflags +faststart "$D/$T - REVIEW 540p.mp4"
cp "$W/notes-RO12.md" "$D/notes-RO12.md"
cp "$W"/ROUND-*-REVIEW.md "$D/" 2>/dev/null || true
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO12/"
cp "$W/out/plan.json" "$W/out/timeline.json" "$D/recipe-RO12/"
ls -la "$D"
