#!/bin/bash
# After both pictures exist: mux, audio gate, transcript, delivered-audio alignment, evidence sheets.
set -e
cd /Volumes/Extreme/_edit_work/ra01
bash s23_finalize.sh 9x16
bash s23_finalize.sh 16x9
echo ALL_FINALIZED
