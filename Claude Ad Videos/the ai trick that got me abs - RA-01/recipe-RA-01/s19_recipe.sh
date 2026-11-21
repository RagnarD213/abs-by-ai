#!/bin/bash
# Refresh recipe-RA-01/ from the work dir: every script and JSON needed to rebuild both files.
set -e
cd /Volumes/Extreme/_edit_work/ra01
R=recipe-RA-01
mkdir -p $R
for f in ra01lib.py capwait.sh s0*.py s1*.py s2*.py s3*.py s4*.py s02_tx.sh s19_recipe.sh s23_finalize.sh \
         s24_gate.sh s26_all.sh s3*.sh s4*.sh capwait4.sh face_src_r3.json \
         edl_spec.json env.json cut.json beats.json framing.json grade.json expo.json eyeline.json \
         lighting.json sharpness.json macro_slice.json words_aligned.json hard_splices.json \
         timeline_9x16.json timeline_16x9.json mix.wav.voice_chain.json; do
  [ -e "$f" ] && cp -p "$f" "$R/" || true
done
rm -rf $R/tx $R/music
mkdir -p $R/tx && cp -p tx/*.json tx/*.py $R/tx/ 2>/dev/null || true
mkdir -p $R/music && cp -p music/Realizer.mp3 $R/music/ 2>/dev/null || true
# round 3: the bed asset the mix is actually built from (s42_bed.py rebuilds it from the mp3)
cp -p music/Realizer_r3bed.wav $R/music/ 2>/dev/null || true
[ -f r2/grade/proof.jpg ] && cp -p r2/grade/proof.jpg $R/grade_proof.jpg
ls $R | wc -l
echo "recipe refreshed -> $R"
