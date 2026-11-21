#!/bin/zsh
# DS-36 R1 key: the house key (DS-40 Claude R2 algorithm, DS-44/DS-43 0.75-cache stage scripts, unchanged maths) on pieces of
# C1730 with the DS-44 plate (same roll; this take measured screen/plate 0.998-1.018 in every quadrant at 545-715 s).
#   watchF  537.50 +17.20  Dan watching the Bill Maher clip (clip 355.4-370.85 = roll +182.812), full camera height (laptop kept)
#   S       572.40 +59.30  scripted take ("Bill Maher is right here" .. "all my newest videos")
#   O       646.40 +70.80  off-the-cuff take (the restart "Bill Maher is right" .. "all my latest videos")
# keyonce.py stamps each piece (recipe code + plate + times): a later round never re-keys a finished piece.  zsh run_key.sh watchF|S|O
set -e
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-36/r1; K=$W/key; cd $W/recipe
KO="$R/.claude/skills/_shared/chroma-key/keyonce.py"
NW=${RENDERQ_CORES:-4}; N15=$(( NW > 3 ? 3 : NW ))
ln -sf $K/plate_out_full.npy $K/s_full/plate_out.npy; ln -sf $K/plate_out.npy $K/s_cut/plate_out.npy
typeset -A SPEC; SPEC=(watchF "537.50 17.20 3840 2880 s_full" S "572.40 59.30 3490 2618 s_cut" O "646.40 70.80 3490 2618 s_cut")
P=$1; set -- ${=SPEC[$P]}; T0=$1; D=$2; YB=$3; ROWS=$4; PD=$5
python3 "$KO" $K/$P.done --inputs stage1_key.py keylib.py stage15_temporal.py srcprep.py $K/$PD/plate_out.npy \
  --params "$P $T0 $D $YB" --clear $K/c1_$P $K/c2_$P -- zsh -c "
    Y_BOTTOM=$YB WORKERS=$NW python3 stage1_key.py $T0 $D $K/c1_$P | tail -1 &&
    N=\$(ls $K/c1_$P | grep -c '^f.*npy\$') &&
    mkdir -p $K/w_$P && ln -sf $K/$PD/plate_out.npy $K/w_$P/plate_out.npy &&
    ROWS=$ROWS python3 srcprep.py $T0 \$N $K/w_$P/src.npy &&
    WORKERS=$N15 python3 stage15_temporal.py $K/c1_$P $K/w_$P/src.npy $K/c2_$P | tail -1 && rm -f $K/w_$P/src.npy"
echo "PIECE $P DONE $(ls $K/c2_$P | grep -c '^f.*npy$')"
