#!/bin/bash
# RO-37 round 2, stage 2a (light slot): the mattes for every context window after the first minute ($14.25, under the
# $15 single-batch line)
set -e
cd /Volumes/Expansion/_edit_work/RO-37/round2/recipe
python3 matte.py run contexts --cap-usd 15 --threads 32
echo CHAIN2A_DONE
