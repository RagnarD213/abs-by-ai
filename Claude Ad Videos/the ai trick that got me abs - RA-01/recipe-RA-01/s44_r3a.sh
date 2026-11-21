#!/bin/bash
# ROUND 3, part A: the bed asset and the new 16:9 CTA pill (both cheap), plus a proof sheet of the
# pill on the frames it has to be clear of.
set -e
cd /Volumes/Extreme/_edit_work/ra01
mkdir -p r3 logs
python3 s42_bed.py 2>&1 | tee logs/r3_bed.log
python3 s11_cta.py 16x9 2>&1 | tee logs/r3_cta16.log
python3 s45_pillproof.py 2>&1 | tee logs/r3_pillproof.log
echo R3A_DONE
