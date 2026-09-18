#!/bin/bash
# ROUND 3, part B: both pictures from the one build script, the mix with the fixed bed, the two
# masters, both gates and every piece of delivered evidence. One capwait job = one build.
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"
mkdir -p logs r3

echo "== bed asset (tuned)"
python3 s42_bed.py 2>&1 | tee logs/r3_bed.log

echo "== pictures"
python3 s10_render.py 9x16 2>&1 | tee logs/r3_render_9x16.log | tail -3
python3 s10_render.py 16x9 2>&1 | tee logs/r3_render_16x9.log | tail -3

echo "== mix (bed asset fixed; chain, loudness and L/R untouched)"
BED=music/Realizer_r3bed.wav BED_DB=-32 LOCK=picture_9x16.mp4 \
  python3 s08_audio.py 2>&1 | tee logs/r3_audio.log | tail -6

for K in 9x16 16x9; do
  echo "== master $K"
  python3 s14_deliver.py mux $K 2>&1 | tail -2
  if [ "$K" = "9x16" ]; then
    python3 "$AG" master_$K.mp4 --ab AB_ref-vs-ours.mp4 > logs/r3_audiogate_$K.log 2>&1 || true
  else
    python3 "$AG" master_$K.mp4 > logs/r3_audiogate_$K.log 2>&1 || true
  fi
  tail -6 logs/r3_audiogate_$K.log
  python3 s15_txmaster.py $K master_$K.mp4 > logs/r3_tx_$K.log 2>&1; tail -2 logs/r3_tx_$K.log
  python3 s09_align.py master_$K.mp4 speech_$K.json > logs/r3_align_$K.log 2>&1; tail -1 logs/r3_align_$K.log
  python3 s13_watch.py neg $K master_$K.mp4 > logs/r3_neg_$K.log 2>&1; tail -1 logs/r3_neg_$K.log
  python3 s12_gateplan.py $K master_$K.mp4 | tail -2
  python3 s34_strips.py $K master_$K.mp4 > logs/r3_strips_$K.log 2>&1; tail -3 logs/r3_strips_$K.log
done

echo "== hard-splice measurement on the round-3 picture (evidence only; the plan pins round 2's)"
python3 s25_hard.py master_9x16.mp4 2>&1 | tee logs/r3_hard.log | tail -6

for K in 9x16 16x9; do
  echo "== watch pass $K"
  rm -rf watchpass_$K
  python3 "$SH/watch.py" master_$K.mp4 --plan recipe-RA-01/gate_plan_$K.json --out watchpass_$K \
      --log watchpass_$K/watch_pass.json 2>&1 | tee logs/r3_watch_$K.log | tail -6
done

echo "== R3 proof measurements"
python3 s43_r3verify.py 9x16 master_9x16.mp4 2>&1 | tee logs/r3_verify9.log | tail -20
python3 s43_r3verify.py 16x9 master_16x9.mp4 2>&1 | tee logs/r3_verify16.log | tail -30
python3 s33_verify.py 9x16 master_9x16.mp4 > logs/r3_v33_9x16.log 2>&1 || true; tail -6 logs/r3_v33_9x16.log
python3 s33_verify.py 16x9 master_16x9.mp4 > logs/r3_v33_16x9.log 2>&1 || true; tail -6 logs/r3_v33_16x9.log
echo R3B_STAGE_DONE
python3 s48_tail.py master_9x16.mp4 round2/master_9x16.mp4 2>&1 | tee logs/r3_tail.log
python3 s47_sharpness.py master_9x16.mp4 2>&1 | tee logs/r3_sharp.log | tail -8
python3 s16_measure.py > logs/r3_measure.log 2>&1; tail -3 logs/r3_measure.log
python3 s31_measure_finalize.py 2>&1 | tail -6
echo R3B_ALL_DONE
