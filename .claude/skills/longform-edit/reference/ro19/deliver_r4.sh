#!/bin/zsh
# RO-19 round 4 delivery (Dan, 2026-10-13: "Okay, everything looks good"): the checked master (same bytes, stamps travel with it), sidecars, 540p review copy,
# the independent review, the recipe. A NEW folder: "01 - My First Spray Tan" holds the August edit and is not touched.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
W=/Volumes/Extreme/_edit_work/ro19; R=$W/round4; F=$R/film; M="$F/RO-19 round 4 - full film.mp4"
D="$P/claude edited long form content/16 - My First Spray Tan (RO-19 re-edit)"
T="My First Spray Tan | claude round 4 | 16x9 | RO-19"
mkdir -p "$D/recipe-RO-19"
cp "$M" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json framing_proof.jpg; do
  [ -f "$M.$s" ] && cp "$M.$s" "$D/$T.mp4.$s"
done
cp "$F/RO19.srt" "$D/$T.srt"; cp "$F/RO19.chapters.txt" "$D/$T.chapters.txt"
cp "$F/RO-19 round 4 - full film.edit-sheet.json" "$D/$T.edit-sheet.json"
cp "$F/RO-19 audio AB (reference then ours).mp4" "$D/$T audio AB (reference then ours).mp4"
cp "$F/logs/gate.log" "$D/$T.deliver_gate.log"
cp "$R/review/full-film - REVIEW 540p.mp4" "$D/$T REVIEW 540p.mp4"
cp "$F/ROUND-4-REVIEW.md" "$F/scene_checklist.json" "$F/negative_events_scan.json" "$F/logs/cut_report_r4.json" "$F/logs/watch_pass.json" "$F/logs/findings.json" "$R/round4-hashes.sha256" "$D/"
setopt null_glob
cp "$W"/recipe/*19*.py "$W"/recipe/*r4*.py "$W"/recipe/*r4*.sh "$W"/recipe/edl.py "$W"/recipe/build.py "$W"/recipe/pairs.py "$W"/recipe/shots.py "$W"/recipe/words_src_out.py "$D/recipe-RO-19/"
cp "$F/plan.json" "$W/plan_resolved.json" "$W/edl.json" "$W/shots.json" "$W/words_out.json" "$W/word_patches.json" "$W/hf/manifest.r4.json" "$W/round3/srt_fixes.json" "$W/round4-plan/decisions.json" "$W/round4-plan/timeline_shift.json" "$W/round3-plan/timeline_shift.json" "$D/recipe-RO-19/" 2>/dev/null || true
shasum -a 256 "$D/$T.mp4"
ls -la "$D" | grep -v '\._' | awk '{print $5, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20}'
