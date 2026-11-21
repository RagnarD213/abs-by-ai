#!/bin/bash
# ROUND 3, part C: hold 4's 9:16 centre corrected (962 -> 950) so the face box AND framing:centering
# both hold. 16:9 is untouched -- its crops did not change and the mix is unchanged (the picture's
# frame count is identical, so voice_chain's --frame-lock output is the same file), so master_16x9
# and its audio stamp stay valid and the two files still carry the same audio.
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"

echo "== picture 9x16"
python3 s10_render.py 9x16 2>&1 | tee logs/r3c_render_9x16.log | tail -3
python3 s14_deliver.py mux 9x16 2>&1 | tail -2
python3 "$AG" master_9x16.mp4 --ab AB_ref-vs-ours.mp4 > logs/r3c_audiogate_9x16.log 2>&1 || true
tail -4 logs/r3c_audiogate_9x16.log
python3 s15_txmaster.py 9x16 master_9x16.mp4 > logs/r3c_tx.log 2>&1; tail -1 logs/r3c_tx.log
python3 s09_align.py master_9x16.mp4 speech_9x16.json > logs/r3c_align.log 2>&1; tail -1 logs/r3c_align.log
python3 s13_watch.py neg 9x16 master_9x16.mp4 > logs/r3c_neg.log 2>&1; tail -1 logs/r3c_neg.log
python3 s12_gateplan.py 9x16 master_9x16.mp4 | tail -1
python3 s34_strips.py 9x16 master_9x16.mp4 > logs/r3c_strips.log 2>&1; tail -2 logs/r3c_strips.log
rm -rf watchpass_9x16
python3 "$SH/watch.py" master_9x16.mp4 --plan recipe-RA-01/gate_plan_9x16.json --out watchpass_9x16 \
    --log watchpass_9x16/watch_pass.json 2>&1 | tee logs/r3c_watch.log | tail -6
python3 s43_r3verify.py 9x16 master_9x16.mp4 2>&1 | tee logs/r3c_verify9.log | tail -6
python3 s33_verify.py 9x16 master_9x16.mp4 > logs/r3c_v33.log 2>&1 || true; tail -3 logs/r3c_v33.log
python3 s48_tail.py master_9x16.mp4 round2/master_9x16.mp4 2>&1 | tee logs/r3c_tail.log | tail -6
python3 s47_sharpness.py master_9x16.mp4 > logs/r3c_sharp.log 2>&1; tail -3 logs/r3c_sharp.log
python3 s49_r3look.py > logs/r3c_look.log 2>&1; tail -2 logs/r3c_look.log
echo R3C_DONE
