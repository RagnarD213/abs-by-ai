#!/bin/bash
# Everything after picture_1x1.mp4 exists: mux (approved audio copied), audio gate + A/B, the
# delivered-file transcript and alignment, the negative sheet, the gate plan, strips, the watch pass.
set -e
cd /Volumes/Extreme/_edit_work/ra01-sq
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
AG="$REPO/.claude/skills/_shared/audio/audio_gate.py"
SH="$REPO/.claude/skills/_shared/deliver"
K=1x1
python3 sq_mux.py
python3 "$AG" master_$K.mp4 --ab AB_ref-vs-ours.mp4 > logs/audiogate_$K.log 2>&1 || true
tail -5 logs/audiogate_$K.log
python3 s15_txmaster.py $K master_$K.mp4 > logs/tx_$K.log 2>&1; tail -2 logs/tx_$K.log
python3 s09_align.py master_$K.mp4 speech_$K.json > logs/align_$K.log 2>&1; tail -1 logs/align_$K.log
python3 s13_watch.py neg $K master_$K.mp4 > logs/neg_$K.log 2>&1; tail -1 logs/neg_$K.log
[ -f logs/negative_scan_$K.json ] || python3 s20_neg.py $K master_$K.mp4 0 '[{"status":"unresolved","note":"sheet not yet looked at"}]'
python3 s12_gateplan.py $K master_$K.mp4 | tail -2
python3 s34_strips.py $K master_$K.mp4 > logs/strips_$K.log 2>&1; tail -3 logs/strips_$K.log
rm -rf watchpass_$K
python3 "$SH/watch.py" master_$K.mp4 --plan recipe-square/gate_plan_$K.json --out watchpass_$K \
    --log watchpass_$K/watch_pass.json 2>&1 | tee logs/watch_$K.log | tail -8
echo SQ_FINISH_DONE
