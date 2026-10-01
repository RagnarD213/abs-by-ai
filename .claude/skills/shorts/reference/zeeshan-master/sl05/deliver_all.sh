#!/bin/zsh
# deliver + evidence for every SL-05 short: ./deliver_all.sh [IDS]
cd "${0:A:h}"
typeset -A NAME
NAME=(S1 short1_deadlifts-cause-more-injuries S2 short2_safer-lifts-build-more-muscle S3 short3_deadlifts-build-a-powerlifter-body S4 short4_two-back-exercises-instead-of-deadlifts S5 short5_train-legs-without-deadlifts)
(( $# )) || set -- S1 S2 S3 S4 S5
for S in "$@"; do ./deliver.sh $S $NAME[$S]; done
