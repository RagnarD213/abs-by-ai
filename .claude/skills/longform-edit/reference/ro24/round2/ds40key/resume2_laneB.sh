#!/bin/bash
set -uo pipefail
cd /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key
export RIM=4 WORKERS=${WORKERS:-5}
bash run_key.sh R12 26770 2734 plateC || echo 'KEY FAILED R12'
bash run_key.sh R14 30325 287 plateC || echo 'KEY FAILED R14'
bash run_key.sh R16 31535 432 plateC || echo 'KEY FAILED R16'
echo 'RESUME2 LANE B DONE'
