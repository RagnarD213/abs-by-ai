#!/bin/bash
# Everything after the two pictures exist: mux, gate, transcribe, align, evidence.
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
K=$1
python3 s14_deliver.py mux $K
if [ "$K" = "9x16" ]; then
  python3 "$AG" master_$K.mp4 --ab AB_ref-vs-ours.mp4 > logs/audiogate_$K.log 2>&1 || true
else
  python3 "$AG" master_$K.mp4 > logs/audiogate_$K.log 2>&1 || true
fi
tail -4 logs/audiogate_$K.log
python3 s15_txmaster.py $K master_$K.mp4 > logs/tx_$K.log 2>&1
tail -2 logs/tx_$K.log
python3 s09_align.py master_$K.mp4 speech_$K.json > logs/align_$K.log 2>&1
tail -2 logs/align_$K.log
python3 s13_watch.py neg $K master_$K.mp4 > logs/neg_$K.log 2>&1
tail -1 logs/neg_$K.log
echo "FINALIZE_$K DONE"
