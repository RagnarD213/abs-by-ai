#!/bin/bash
# usage: batch.sh "ID TAG SECS" ...   runs the takes in parallel, waits, prints MOTION_BATCH_DONE
cd /Volumes/Extreme/_edit_work/ra15
for t in "$@"; do set -- $t; ( python3 gen_motion15.py $1 $2 $3 ${4:-pair} > round2/motion/$2.log 2>&1; echo "$2 exit $?" ) & done
wait; echo MOTION_BATCH_DONE
