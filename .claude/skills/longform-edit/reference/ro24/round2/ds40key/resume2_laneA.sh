#!/bin/bash
set -uo pipefail
cd /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key
export RIM=4 WORKERS=${WORKERS:-5}
bash run_key.sh R07 24324 999 plateB || echo 'KEY FAILED R07'
bash run_key.sh R09 25421 638 plateC || echo 'KEY FAILED R09'
bash run_key.sh R11 26452 316 plateC || echo 'KEY FAILED R11'
bash run_key.sh R13 29983 237 plateC || echo 'KEY FAILED R13'
bash run_key.sh R15 30747 213 plateC || echo 'KEY FAILED R15'
echo 'RESUME2 LANE A DONE'
