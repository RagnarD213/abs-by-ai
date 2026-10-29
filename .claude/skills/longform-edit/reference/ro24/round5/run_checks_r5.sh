#!/bin/bash
# RO-24 round 5 checks after chain_r5.sh: audio gate (with the untreated baseline), subtitles, context clips, negative-events
# frames, the gate plan, the watch pass. The judge and the delivery gate run after this.
set -uo pipefail
R5=/Volumes/Expansion/_edit_work/RO-24/round5; R="$R5/recipe"; P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; A="$P/.claude/skills/_shared"
M="$R5/final/RO24_R5_MASTER.mp4"
echo "== audio gate"; python3 "$A/audio/audio_gate.py" "$M" --untreated "$M.audio_untreated.json" --ab "$R5/final/RO24_R5_MASTER - audio AB.mp4" > "$R5/checks/audio_gate.log" 2>&1; tail -6 "$R5/checks/audio_gate.log"
echo "== srt"; python3 "$R/srt_r5.py" 2>&1 | tail -3
echo "== context"; python3 "$R/ctx_r5.py" 2>&1 | tail -3
echo "== negscan frames"; python3 "$R/negscan_frames_r5.py" 2>&1 | tail -2
echo "== gate plan"; python3 "$R/gateplan_r5.py" 2>&1 | tail -6
echo "== watch"; python3 "$A/deliver/watch.py" "$M" --plan "$R5/final/plan.json" 2>&1 | tail -6
echo "CHECKS COMPLETE"
