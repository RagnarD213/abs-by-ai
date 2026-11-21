#!/bin/zsh
# gate every delivered SL-05 short: r2/gate_all.sh TAG [IDS]
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
G=.claude/skills/_shared/deliver/gate.py; B=/Volumes/Extreme/_edit_work/sl05/build; D="Short-form video content"
typeset -A N; N=(S1 short1_deadlifts-cause-more-injuries S2 short2_safer-lifts-build-more-muscle S3 short3_deadlifts-build-a-powerlifter-body S4 short4_two-back-exercises-instead-of-deadlifts S5 short5_train-legs-without-deadlifts)
TAG=$1; shift; (( $# )) || set -- S1 S2 S3 S4 S5
for S in "$@"; do
  nice python3 $G "$D/stop-deadlifting-$N[$S].mp4" --format short --plan $B/gate/$S/plan.json > $B/gate/$S/gate_out_$TAG.txt 2>&1
  echo "== $S"; grep -E "FAIL|NOT MEASURED|UNCONFIG|NEEDS HUMAN|passed,|DELIVERY GATE" $B/gate/$S/gate_out_$TAG.txt
done
echo GATES_DONE
