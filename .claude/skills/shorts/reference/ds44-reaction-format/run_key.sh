#!/bin/zsh
# DS-44 R1 key: this take's plate, then the house key (stage 1 at 4K -> 0.75 cache, stage 1.5) on three pieces.
#   watch  C1730 2192.30 +22.00  Dan watching the Hormozi clip on the laptop (corner of the opening)
#   A      C1730 2268.00 +37.85  "This is a critical insight..." to "...at the rate you want."
#   B      C1730 2307.80 +8.40   "and if you need help stopping eating..." to the subscribe line
set -e
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-44/r1; cd $W/recipe
[ -f $W/key/plate_q.npy ] || python3 plate.py
python3 -c "
import numpy as np; from scipy import ndimage as ndi
q=np.load('$W/key/plate_q.npy'); z=(2880/q.shape[0],1620/q.shape[1])
p=np.stack([ndi.zoom(q[...,c],z,order=1) for c in range(3)],-1)[:2618].astype(np.float32); np.save('$W/key/plate_out.npy',p); print('plate_out',p.shape)"
for spec in "watch 2192.30 22.00" "A 2268.00 37.85" "B 2307.80 8.40" "A0 2256.90 2.30"; do
  set -- ${=spec}; P=$1; T0=$2; D=$3
  if [ ! -f $W/key/$P.done ]; then
    python3 stage1_key.py $T0 $D $W/key/c1_$P | tail -1
    N=$(ls $W/key/c1_$P | grep -c '^f.*npy$')
    [ -f $W/key/src_$P.npy ] || python3 srcprep.py $T0 $N $W/key/src_$P.npy
    MIN_N=40 WORKERS=3 python3 stage15_temporal.py $W/key/c1_$P $W/key/src_$P.npy $W/key/c2_$P $( [ -f $W/key/watch_$P.json ] && echo $W/key/watch_$P.json ) | tail -1
    echo "$T0 $N" > $W/key/$P.done; echo "PIECE $P DONE $N"
  fi
done
echo KEY ALL DONE
