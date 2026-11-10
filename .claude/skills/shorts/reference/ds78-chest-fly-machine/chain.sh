#!/bin/bash
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
cd /Users/danielrose/Projects/_edit_work/DS-78/round1
python3 recipe/build.py F > evidence/build4.log 2>&1
tail -1 evidence/build4.log
bash checks.sh
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py" "review/How To Do Chest Flies On SFC R1 - 1080p.mp4" --reference-mix audio/voice-selected.wav --verbatim > evidence/voice-preservation-gate.log 2>&1
tail -1 evidence/voice-preservation-gate.log
shasum -a 256 "review/How To Do Chest Flies On SFC R1 - 1080p.mp4"
echo CHAIN_DONE
