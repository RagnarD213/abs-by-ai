#!/bin/zsh
# R6: key the rest of the scripted take (R2 method), around the full-screen BMI table.
# S1F roll 1400.15 + 1.0 s at FULL height (laptop kept): the 0.5 s move from small to full size never shows a cut edge
# S2 roll 1409.40 + 14.10 s (after the R2 cache, which ends at 1409.55), crop row 3490
# S3 roll 1444.30 + 5.40 s (subscribe close), crop row 3490
set -e
cd /Volumes/Expansion/_edit_work/ds40/r6/key
for SEG in "S1F 1400.15 1.00 3840 1920" "S2 1409.40 14.10 3490 1745" "S3 1444.30 5.40 3490 1745"; do
  set -- ${=SEG}; S=$1; T0=$2; DUR=$3; YB=$4; RW=$5
  if [[ ! -f ../cache_$S/.done ]]; then
    Y_BOTTOM=$YB python3 stage1_key.py $T0 $DUR ../cache1_$S | tail -1
    N=$(ls ../cache1_$S/f*.npy | wc -l | tr -d ' ')
    ROWS=$RW python3 srcprep.py $T0 $N ../src_$S.npy
    if [[ $RW == 1920 ]]; then ln -sf ../r4fix/plate_out.npy ../plate_out.npy.1920; fi
    MINF=10 python3 stage15_temporal.py ../cache1_$S ../src_$S.npy ../cache_$S | tail -1
    touch ../cache_$S/.done
    echo SEG $S DONE $N
  fi
done
echo KEY DONE
