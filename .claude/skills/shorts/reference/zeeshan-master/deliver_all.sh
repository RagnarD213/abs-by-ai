#!/bin/zsh
# deliver + evidence for every SL-04 short: ./deliver_all.sh [IDS]
cd "${0:A:h}"
typeset -A NAME
NAME=(A short1_make-your-waist-look-smaller F short2_do-this-before-you-take-your-shirt-off C short3_raise-your-elbows-not-your-hands K short4_stop-swinging-your-curls H short5_how-to-do-bicep-curls)
for S in ${@:-A F C K H}; do ./deliver.sh $S $NAME[$S]; done
