#!/bin/zsh
# DS-107 R1 key: the house key (DS-40 Claude R2 algorithm, DS-44/DS-41 0.75-cache stage scripts, unchanged maths) on the stretches of
# C1908 where Dan is on screen (key_subs.json; 6 frames of handles), this roll's own plate (plate.py: 85 frames over 82-252 s).
# Full portrait frame kept (no laptop on this roll): Y_BOTTOM 3840, cache 1620 x 2880. Starts sit just under a frame boundary so key
# frame i and source frame i are the same roll frame (DS-43 lesson). keyonce.py stamps each piece: no round re-keys a finished one.
#   zsh run_key.sh Ka|Kb|Kc|Kd|Ke|Kf
set -e
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
W=/Volumes/Extreme/_edit_work/DS-107/r1; K=$W/key; cd $W/recipe
KO="$R/.claude/skills/_shared/chroma-key/keyonce.py"
NW=${RENDERQ_CORES:-4}; N15=$(( NW > 3 ? 3 : NW ))
read T0 D <<< "$(python3 -c "import json;a,d=json.load(open('key_subs.json'))['$1'];print(a,d)")"
P=$1
python3 "$KO" $K/$P.done --inputs stage1_key.py keylib.py stage15_temporal.py srcprep.py $K/plate_out.npy \
  --params "$P $T0 $D 3840" --clear $K/c1_$P $K/c2_$P -- zsh -c "
    Y_BOTTOM=3840 WORKERS=$NW python3 stage1_key.py $T0 $D $K/c1_$P | tail -1 &&
    N=\$(ls $K/c1_$P | grep -c '^f.*npy\$') &&
    mkdir -p $K/w_$P && ln -sf $K/plate_out.npy $K/w_$P/plate_out.npy &&
    ROWS=2880 python3 srcprep.py $T0 \$N $K/w_$P/src.npy &&
    MIN_N=40 WORKERS=$N15 python3 stage15_temporal.py $K/c1_$P $K/w_$P/src.npy $K/c2_$P | tail -1 && rm -f $K/w_$P/src.npy"
echo "PIECE $P DONE $(ls $K/c2_$P | grep -c '^f.*npy$')"
