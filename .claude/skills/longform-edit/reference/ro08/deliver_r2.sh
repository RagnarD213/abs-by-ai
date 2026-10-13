#!/bin/zsh
# RO-08 round 2 delivery: the checked master (same bytes, stamps travel with it), sidecars, 540p review copy, reviews, recipe.
# Also the VLC copies in the project folder (Videos to Review/, Dan's 2026-10-08 rule); the round 1 copy is removed.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
W=/Volumes/Extreme/_edit_work/ro08; R=$W/round2; M="$R/RO-08 round 2 - full film.mp4"
D="$P/claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs"
T="Intermittent Fasting The Best Way To Get Abs | claude round 2 | 16x9 | RO-08"
mkdir -p "$D/recipe-RO-08"
cp "$M" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$M.$s" ] && cp "$M.$s" "$D/$T.mp4.$s"
done
cp "$R/RO08.srt" "$D/$T.srt"; cp "$R/RO08.chapters.txt" "$D/$T.chapters.txt"
[ -f "$R/RO-08 round 2 - full film.edit-sheet.json" ] && cp "$R/RO-08 round 2 - full film.edit-sheet.json" "$D/$T.edit-sheet.json"
[ -f "$R/RO-08 audio AB (reference then ours).mp4" ] && cp "$R/RO-08 audio AB (reference then ours).mp4" "$D/$T audio AB (reference then ours).mp4"
[ -f "$R/logs/gate.log" ] && cp "$R/logs/gate.log" "$D/$T.deliver_gate.log"
cp "$R/RO-08 round 2 - full film - REVIEW 540p.mp4" "$D/$T REVIEW 540p.mp4"
cp "$R"/ROUND-2-REVIEW*.md "$D/" 2>/dev/null || true
setopt null_glob
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO-08/"
cp "$R/plan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/hf/manifest.json" "$R"/srt_fixes.json "$R"/srt_words.json "$R/motion/ledger.json" "$D/recipe-RO-08/"
mkdir -p "$P/Videos to Review"
rm -f "$P/Videos to Review/Intermittent Fasting LFC R1 - first minute.mp4"
cp "$M" "$P/Videos to Review/Intermittent Fasting LFC R2 - full film (opener A time-lapse).mp4"
cp "$R/first-minute/DRAFT - RO-08 round 2 - first minute - opener A time-lapse.mp4" "$P/Videos to Review/Intermittent Fasting LFC R2 - first minute - opener A time-lapse.mp4"
cp "$R/first-minute/DRAFT - RO-08 round 2 - first minute - opener B split screen.mp4" "$P/Videos to Review/Intermittent Fasting LFC R2 - first minute - opener B split screen.mp4"
ls -la "$D" | grep -v '\._'; ls -la "$P/Videos to Review" | grep "Intermittent"
