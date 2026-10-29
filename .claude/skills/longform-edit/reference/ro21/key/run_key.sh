#!/bin/bash
# RO-21: one key range end to end (RO-24 16:9 port of the house DS-40 R2 key, fast shared keylib/stage 1.5).
#   run_key.sh NAME F0 N [PLATE] [X0 X1]      RIM=4 (this set), WORKERS from the render queue allowance
set -euo pipefail
cd /Volumes/Expansion/_edit_work/RO-21/recipe/key
K=/Volumes/Expansion/_edit_work/RO-21/key; NAME=$1; F0=$2; N=$3; PL=${4:-plate}
mkdir -p $K/$NAME
if [ $# -ge 6 ]; then X0=$5; X1=$6; else read X0 X1 < <(python3 box16.py $F0 $N); fi; echo "$NAME box $X0 $X1 plate $PL RIM ${RIM:-4}"
export WORKERS=${RENDERQ_CORES:-4} RIM=${RIM:-4}
python3 stage1_16.py $F0 $N $K/$NAME/c1 $X0 $X1 $PL 2>&1 | tail -1
python3 srcprep16.py $F0 $N $K/$NAME/src_u8.npy $X0 $X1 | tail -1
ln -sf $K/${PL}_out.npy $K/$NAME/plate_out.npy
python3 stage15_temporal.py $K/$NAME/c1 $K/$NAME/src_u8.npy $K/$NAME/c15 2>&1 | tail -1
python3 write16.py $K/$NAME/c15 $F0 $K/$NAME.mkv $X0 | tail -1
rm -rf $K/$NAME/c1 $K/$NAME/src_u8.npy
echo "KEY RANGE DONE $NAME"
