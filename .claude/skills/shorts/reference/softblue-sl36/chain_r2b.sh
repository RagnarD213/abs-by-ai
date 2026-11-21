#!/bin/bash
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
cd /Users/danrrose/Projects/_edit_work/SL-36/round2
export PATH="$HOME/.local/node/bin:$HOME/.npm-global/bin:$PATH"
python3 recipe/batch.py gfx B > logs/gfx3.log 2>&1; python3 recipe/batch.py plan B > logs/plan3.log 2>&1
for S in A B C; do echo "render $S $(date)"; python3 recipe/batch.py render $S > logs/render_$S.log 2>&1; done
echo "end $(date)"
echo CHAIN_DONE
