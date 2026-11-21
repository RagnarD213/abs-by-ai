#!/bin/zsh
# Robustness: the verdicts must not depend on where the grid falls. Grid spacing 32 and 48 px (default 40) on the takes with a
# known verdict. Writes temp specs (spec + "bounds": {"grid_px": N}) next to the evidence, not here.
cd "${0:A:h}"
M=/Volumes/Extreme/_edit_work/ro08/round2/motion
O=${1:-${TMPDIR:-/tmp}/clipcheck-proof-ro08}; mkdir -p $O
for gp in 32 48; do
  for spec in A5 A5:0:24 A5:84:143 A6 A7; do
    k=${spec%%:*}; fr=${spec#*:}; [[ $fr == $spec ]] && fr=""
    python3 -c "import json,sys; d=json.load(open('spec_$k.json')); d.setdefault('bounds',{})['grid_px']=$gp; json.dump(d,open('$O/spec_${k}_g$gp.json','w'))"
    echo "== grid $gp $k ${fr:-whole}"
    python3 ../../clipcheck.py $M/$k-t1.mp4 --spec $O/spec_${k}_g$gp.json ${fr:+--frames=$fr} --out $O --no-stamp 2>&1 | grep -E "^  FAIL|^VERDICT|biggest" | sed -E 's/.*(VERDICT [A-Z]+).*/\1/; s/^  (PASS|FAIL)  (vanish|appear) +[^;]*; (biggest cluster [0-9]+).*/  \1 \2 \3/'
  done
done
