#!/bin/zsh
# RO-21 round 3 delivery (00-RULES section 4): master, .srt, chapters, stamps, gate log, reviews, audio A/B, 540p review copy and the
# recipe into "claude edited long form content/24 - <title>/"; full-quality copy into Videos to Review.
set -e
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; B=/Volumes/Expansion/_edit_work/RO-21; R=$B/round3/final
D="$P/claude edited long form content/24 - What Every Body Fat Percentage Looks Like (On Me)"; T="What Every Body Fat Percentage Looks Like (On Me) | claude round 3 | 16x9 | RO-21"
mkdir -p "$D/recipe-RO-21-r3"
cp "$R/RO21_MASTER.mp4" "$D/$T.mp4"
for s in audio_gate.json deliver_gate.json audio_untreated.json voice_chain.json; do [ -f "$R/RO21_MASTER.mp4.$s" ] && cp "$R/RO21_MASTER.mp4.$s" "$D/$T.mp4.$s"; done
cp "$R/RO21.srt" "$D/$T.srt"; cp "$B/round3/chapters.txt" "$D/$T.chapters.txt"; cp "$R/logs/gate5.log" "$D/$T.deliver_gate.log"
cp "$R/RO-21 audio AB vs reference.mp4" "$D/$T | audio AB (reference then ours).mp4"
cp "$R/RO-21 round 3 - full film - REVIEW 540p.mp4" "$D/$T | REVIEW 540p.mp4"
cp "$R/ROUND-3-REVIEW.md" "$R/ROUND-3-REVIEW-2.md" "$R/negative_events_scan.json" "$R/plan.json" "$R/logs/findings.json" "$D/recipe-RO-21-r3/" 2>/dev/null || true
cp "$B"/recipe/*.py "$B"/recipe/*.sh "$B/round3/bg_plan.json" "$B/round3/film_manifest.json" "$B/round3/decisions_r2.json" "$D/recipe-RO-21-r3/"
cp "$B/round3/om/NOTES.md" "$D/recipe-RO-21-r3/other-man-NOTES.md"; cp "$B/round3/om/SHA256.txt" "$D/recipe-RO-21-r3/other-man-SHA256.txt"
cp "$R/RO21_MASTER.mp4" "$P/Videos to Review/Body Fat % LFC R3 - full film.mp4"
ls "$D" | head -20; echo DELIVER_DONE
