#!/bin/bash
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
cd /Users/danielrose/Projects/_edit_work/DS-78/round1
python3 recipe/check.py voice picture watch > evidence/check.log 2>&1
grep -E "AUDIO_GATE|CAPTIONS|HAIR|WATCH|PICTURE_DONE" evidence/check.log | cut -c1-400
echo CHAIN_DONE
