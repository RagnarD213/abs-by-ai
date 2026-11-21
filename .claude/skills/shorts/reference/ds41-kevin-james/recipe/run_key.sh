#!/bin/zsh
# DS-41 R1 key: the house key (DS-40 Claude R2 algorithm, DS-44/DS-43 0.75-cache stage scripts, unchanged maths) on pieces of
# C1730 with the DS-44 plate (same roll; this part measured screen/plate 0.990-1.008 in every quadrant at 1600-1790 s).
#   watchA  1608.00 +7.00   Dan watching clip piece 1 (clip 41.40-47.76 = roll +1566.872), full camera height (laptop kept)
#   watchB  1624.92 +8.20   Dan watching clip piece 2 (clip 58.25-65.90, same first viewing), full camera height
#   The talk takes are keyed only where Dan is on screen (the math card and the cutaways hide about a third of each take):
#   Sa/Sb/Sc/Sd  scripted: reply over the panel; "So you did six days .. doesn't work."; "this is the reason why .. have a day";
#                "Remember, ripped guys .. nutrition tips."
#   Oa..Oe       off the cuff: reply over the panel; "So guys .. other six days,"; "So I would say .. track your calories,";
#                "you're eating 6,000 .. when you cheat."; the second "Subscribe to my channel .. tips."
#   Start times sit just under a frame boundary so key frame i and source frame i are the same roll frame (DS-43 lesson).
# keyonce.py stamps each piece (recipe code + plate + times): a later round never re-keys a finished piece.  zsh run_key.sh watchA|watchB|S|O
set -e
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-41/r1; K=$W/key; cd $W/recipe
KO="$R/.claude/skills/_shared/chroma-key/keyonce.py"
NW=${RENDERQ_CORES:-4}; N15=$(( NW > 3 ? 3 : NW ))
ln -sf $K/plate_out_full.npy $K/s_full/plate_out.npy; ln -sf $K/plate_out.npy $K/s_cut/plate_out.npy
typeset -A SPEC; SPEC=(watchA "1608.00 7.00 3840 2880 s_full" watchB "1624.92 8.20 3840 2880 s_full" Sa "1673.80 5.32 3490 2618 s_cut" Sb "1689.95 8.07 3490 2618 s_cut" Sc "1699.86 8.16 3490 2618 s_cut" Sd "1711.07 13.31 3490 2618 s_cut" Oa "1730.89 9.79 3490 2618 s_cut" Ob "1754.48 11.44 3490 2618 s_cut" Oc "1767.86 9.88 3490 2618 s_cut" Od "1784.78 11.24 3490 2618 s_cut" Oe "1800.66 3.48 3490 2618 s_cut" Of "1780.64 2.75 3490 2618 s_cut")
[[ -n "${SPEC[$1]}" ]] || { echo "PIECE $1 not in this recipe (takes are keyed as Sa-Sd / Oa-Oe)"; exit 0; }
P=$1; set -- ${=SPEC[$P]}; T0=$1; D=$2; YB=$3; ROWS=$4; PD=$5
python3 "$KO" $K/$P.done --inputs stage1_key.py keylib.py stage15_temporal.py srcprep.py $K/$PD/plate_out.npy \
  --params "$P $T0 $D $YB" --clear $K/c1_$P $K/c2_$P -- zsh -c "
    Y_BOTTOM=$YB WORKERS=$NW python3 stage1_key.py $T0 $D $K/c1_$P | tail -1 &&
    N=\$(ls $K/c1_$P | grep -c '^f.*npy\$') &&
    mkdir -p $K/w_$P && ln -sf $K/$PD/plate_out.npy $K/w_$P/plate_out.npy &&
    ROWS=$ROWS python3 srcprep.py $T0 \$N $K/w_$P/src.npy &&
    MIN_N=40 WORKERS=$N15 python3 stage15_temporal.py $K/c1_$P $K/w_$P/src.npy $K/c2_$P | tail -1 && rm -f $K/w_$P/src.npy"
echo "PIECE $P DONE $(ls $K/c2_$P | grep -c '^f.*npy$')"
