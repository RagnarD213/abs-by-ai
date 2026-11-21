#!/bin/bash
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
cd /Users/danrrose/Projects/_edit_work/SL-36/round2
export PATH="$HOME/.local/node/bin:$HOME/.npm-global/bin:$PATH"
echo "gfx $(date)"; python3 recipe/batch.py gfx B C > logs/gfx2.log 2>&1
python3 recipe/batch.py plan A B > logs/plan2.log 2>&1
for S in A B C; do echo "proof $S $(date)"; python3 recipe/batch.py proof $S > logs/proof2_$S.log 2>&1; done
echo CHAIN_DONE
