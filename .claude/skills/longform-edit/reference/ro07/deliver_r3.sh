#!/bin/zsh
# RO-07 round 3 delivery: the checked master (same bytes, stamps travel with it), sidecars, 540p review copy, reviews, recipe.
# Also the VLC copy in the project folder (Videos to Review/, Dan's 2026-10-08 rule).
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
W=/Volumes/Extreme/_edit_work/ro07; R=$W/round3; M="$R/RO-07 round 3 - full film.mp4"
D="$P/claude edited long form content/14 - Why You MUST Work Out Every Day"
T="Why You MUST Work Out Every Day | claude round 3 | 16x9 | RO-07"
mkdir -p "$D/recipe-RO-07"
cp "$M" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$M.$s" ] && cp "$M.$s" "$D/$T.mp4.$s"
done
cp "$R/RO07.srt" "$D/$T.srt"; cp "$R/RO07.chapters.txt" "$D/$T.chapters.txt"
[ -f "$R/RO-07 round 3 - full film.edit-sheet.json" ] && cp "$R/RO-07 round 3 - full film.edit-sheet.json" "$D/$T.edit-sheet.json"
cp "$R/RO-07 audio AB (reference then ours).mp4" "$D/$T audio AB (reference then ours).mp4"
[ -f "$R/logs/gate.log" ] && cp "$R/logs/gate.log" "$D/$T.deliver_gate.log"
cp "$R/RO-07 round 3 - full film - REVIEW 540p.mp4" "$D/$T REVIEW 540p.mp4"
cp "$R"/ROUND-3-REVIEW*.md "$D/" 2>/dev/null || true
setopt null_glob
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO-07/"
cp "$R/plan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/hf/manifest.json" "$R/srt_fixes.json" "$R/srt_words.json" "$D/recipe-RO-07/"
mkdir -p "$P/Videos to Review"
cp "$M" "$P/Videos to Review/Work Out Every Day LFC R3 - full film.mp4"
ls -la "$D" | grep -v '\._'; ls -la "$P/Videos to Review" | grep "Work Out Every Day"
