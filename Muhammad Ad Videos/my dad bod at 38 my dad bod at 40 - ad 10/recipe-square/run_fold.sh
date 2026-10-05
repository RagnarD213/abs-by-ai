#!/bin/zsh
source $HOME/abs-review/as06-ad10/recipe-square/env.sh
FORMAT=ad1x1 zsh "$K/kit_fold.sh" $Q "$SQV" "round 6 judges (fresh Opus 5.5 sessions over six rounds)"
echo FOLDFULL DONE
FORMAT=ad1x1 zsh "$K/kit_fold.sh" $Q/cut_audit "$SQC" "round 6 judges (fresh Opus 5.5 sessions over six rounds)"
echo FOLDCUT DONE
