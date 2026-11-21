#!/bin/zsh
# DS-43 R1 key: the house key (DS-40 Claude R2 algorithm, DS-44 0.75-cache stage scripts, unchanged maths) on three pieces of
# C1730, the DS-44 plate (same roll, minutes apart; this take measured screen/plate 0.997-1.005 in every quadrant).
#   watchF  1984.40 +20.60  Dan watching the Terry Crews clip, full camera height (laptop kept: corner + large watching layer)
#   S       2024.80 +60.00  scripted take ("Terry Crews is smart as fuck" .. "subscribe to my channel")
#   O       2098.90 +67.90  off-the-cuff take
# keyonce.py stamps each piece (recipe code + plate + times): a later round never re-keys a finished piece.
set -e
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-43/r1; K=$W/key; cd $W/recipe
KO="$R/.claude/skills/_shared/chroma-key/keyonce.py"
NW=${RENDERQ_CORES:-4}; N15=$(( NW > 3 ? 3 : NW ))
mkdir -p $K/s_full $K/s_cut
ln -sf $K/plate_out_full.npy $K/s_full/plate_out.npy; ln -sf $K/plate_out.npy $K/s_cut/plate_out.npy
for spec in "watchF 1984.40 20.60 3840 2880 s_full" "S 2024.80 60.00 3490 2618 s_cut" "O 2098.90 67.90 3490 2618 s_cut"; do
  set -- ${=spec}; P=$1; T0=$2; D=$3; YB=$4; ROWS=$5; PD=$6
  python3 "$KO" $K/$P.done --inputs stage1_key.py keylib.py stage15_temporal.py srcprep.py $K/$PD/plate_out.npy \
    --params "$P $T0 $D $YB" --clear $K/c1_$P $K/c2_$P -- zsh -c "
      Y_BOTTOM=$YB WORKERS=$NW python3 stage1_key.py $T0 $D $K/c1_$P | tail -1 &&
      N=\$(ls $K/c1_$P | grep -c '^f.*npy\$') &&
      mkdir -p $K/w_$P && ln -sf $K/$PD/plate_out.npy $K/w_$P/plate_out.npy &&
      ROWS=$ROWS python3 srcprep.py $T0 \$N $K/w_$P/src.npy &&
      WORKERS=$N15 python3 stage15_temporal.py $K/c1_$P $K/w_$P/src.npy $K/c2_$P | tail -1 && rm -f $K/w_$P/src.npy"
  echo "PIECE $P DONE $(ls $K/c2_$P | grep -c '^f.*npy$')"
done
echo KEY ALL DONE
