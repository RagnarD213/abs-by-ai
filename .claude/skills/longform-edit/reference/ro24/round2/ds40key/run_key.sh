#!/bin/bash
# one key range end to end, inside a processing box around Dan: box -> stage 1 (4K key) -> source prep -> stage 1.5 (approved
# finishing pass, unchanged; RIM from the environment, 4 for this roll) -> plate.   run_key.sh NAME F0 N [PLATE] [X0 X1]
set -euo pipefail
cd /Volumes/Expansion/_edit_work/RO-24/round2/recipe/ds40key
K=/Volumes/Expansion/_edit_work/RO-24/round2/key; NAME=$1; F0=$2; N=$3; PL=${4:-plate}
mkdir -p $K/$NAME
if [ $# -ge 6 ]; then X0=$5; X1=$6; else read X0 X1 < <(python3 box16.py $F0 $N); fi; echo "$NAME box $X0 $X1 plate $PL RIM ${RIM:-2}"
WORKERS=${WORKERS:-5} python3 stage1_16.py $F0 $N $K/$NAME/c1 $X0 $X1 $PL 2>&1 | tail -1
python3 srcprep16.py $F0 $N $K/$NAME/src_u8.npy $X0 $X1 | tail -1
ln -sf $K/${PL}_out.npy $K/$NAME/plate_out.npy
WORKERS=${WORKERS:-5} python3 stage15_temporal.py $K/$NAME/c1 $K/$NAME/src_u8.npy $K/$NAME/c15 2>&1 | tail -1
python3 write16.py $K/$NAME/c15 $F0 $K/$NAME.mkv $X0 | tail -1
rm -rf $K/$NAME/c1 $K/$NAME/src_u8.npy
echo "KEY RANGE DONE $NAME"
