#!/bin/zsh
# DS-44 R2: the watching piece re-keyed at full camera height, laptop kept (Dan's 2026-10-22 standard reaction layout,
# DS-40 R4 option B). Same house key, same plate; only the bottom crop changes (Y_BOTTOM 3840, 2880 cache rows).
set -e
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
K=/Volumes/Expansion/_edit_work/DS-44/r1/key; cd /Volumes/Expansion/_edit_work/DS-44/r2/recipe
[ -f $K/plate_out_full.npy ] || python3 -c "
import numpy as np; from scipy import ndimage as ndi
q=np.load('$K/plate_q.npy'); z=(2880/q.shape[0],1620/q.shape[1])
p=np.stack([ndi.zoom(q[...,c],z,order=1) for c in range(3)],-1).astype(np.float32); np.save('$K/plate_out_full.npy',p); print('plate_out_full',p.shape)"
Y_BOTTOM=3840 python3 stage1_key.py 2192.30 22.00 $K/c1_watchF | tail -1
N=$(ls $K/c1_watchF | grep -c '^f.*npy$')
[ -f $K/src_watchF.npy ] || ROWS=2880 python3 srcprep.py 2192.30 $N $K/src_watchF.npy
mkdir -p $K/wF && ln -sf $K/plate_out_full.npy $K/wF/plate_out.npy && ln -sf $K/src_watchF.npy $K/wF/src.npy
WORKERS=3 python3 stage15_temporal.py $K/c1_watchF $K/wF/src.npy $K/c2_watchF | tail -1
echo "WATCHF DONE $(ls $K/c2_watchF | grep -c '^f.*npy$')"
