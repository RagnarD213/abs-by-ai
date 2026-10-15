#!/bin/zsh
# clipcheck proof on RO-08's round 2 takes (README, "Motion takes"). Measure only: no stamps on the takes.
# usage: run_proof.sh [OUT]   (evidence folder, default a temp folder)
cd "${0:A:h}"
M=/Volumes/Extreme/_edit_work/ro08/round2/motion
O=${1:-${TMPDIR:-/tmp}/clipcheck-proof-ro08}; mkdir -p $O
CC=../../clipcheck.py
run() { echo "== $1 ${3:-whole}  (expect $2)"; python3 $CC $M/$1-t1.mp4 --spec spec_$1.json ${3:+--frames=$3} --out $O --no-stamp 2>&1 | grep -E "^  (PASS|FAIL)|^VERDICT" | cut -c1-260; }
run A5 FAIL                 # Dan: "all the donuts just disappear, vaporize, and go nowhere"
run A5 PASS 0:24            # round 3 shot one: he bites the donut, box full (shipped)
run A5 PASS 84:143          # round 3 shot two after the glaze-smear patch window (shipped)
run A5 "FAIL?" 74:143         # shot two as cut: the last of the glaze fades in the box over frames 74-78 (patched in the edit)
run A6 PASS                 # no note; shipped
run A7 PASS                 # no note; shipped
run A8 PASS                 # no note; shipped (camera pushes in, junk burns)
run A3 "FAIL?"               # Dan: "The water jumps up in the air for no reason"
