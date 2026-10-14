#!/bin/zsh
# RO-08 round 3 delivery: the checked master (same bytes, stamps travel with it), sidecars, 540p review copy, reviews, recipe.
# The VLC copy in the project folder (Videos to Review/, Dan's 2026-10-08 rule) replaces the three round 2 files.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
W=/Volumes/Extreme/_edit_work/ro08; R=$W/round3; M="$R/RO-08 round 3 - full film.mp4"
D="$P/claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs"
T="Intermittent Fasting The Best Way To Get Abs | claude round 3 | 16x9 | RO-08"
mkdir -p "$D/recipe-RO-08"
cp "$M" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$M.$s" ] && cp "$M.$s" "$D/$T.mp4.$s"
done
cp "$R/RO08.srt" "$D/$T.srt"; cp "$R/RO08.chapters.txt" "$D/$T.chapters.txt"
cp "$R/RO-08 round 3 - full film.edit-sheet.json" "$D/$T.edit-sheet.json"
[ -f "$R/RO-08 audio AB (reference then ours).mp4" ] && cp "$R/RO-08 audio AB (reference then ours).mp4" "$D/$T audio AB (reference then ours).mp4"
[ -f "$R/logs/gate.log" ] && cp "$R/logs/gate.log" "$D/$T.deliver_gate.log"
cp "$R/RO-08 round 3 - full film - REVIEW 540p.mp4" "$D/$T REVIEW 540p.mp4"
cp "$R"/ROUND-3-REVIEW*.md "$D/" 2>/dev/null || true
setopt null_glob
cp "$W"/recipe/*.py "$W"/recipe/*.sh "$D/recipe-RO-08/"
cp "$R/plan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/hf/manifest.json" "$W"/round2/srt_fixes.json "$W"/round2/srt_words.json "$W/round2/motion/ledger.json" "$R/motion/A5-cut.mp4.json" "$D/recipe-RO-08/"
mkdir -p "$P/Videos to Review"
rm -f "$P/Videos to Review/Intermittent Fasting LFC R2 - "*.mp4
cp "$M" "$P/Videos to Review/Intermittent Fasting LFC R3 - full film.mp4"
ls -la "$D" | grep -v '\._' | grep "round 3"; ls -la "$P/Videos to Review" | grep "Intermittent"
