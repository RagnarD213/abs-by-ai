#!/bin/zsh
# REV 6 chain after the punch + inserts: mix (benchmarked, staged if the graph livelocks -- lesson 117) -> the tan pass
# TWICE (A corrected, B identical pipeline with the correction off) -> audio4 (rev-2 chain + Dan's approved dereverb)
# on both -> captions on both -> deliver.sh on both -> the face A/B. Every stage prints a timestamp; the last line is
# REV6 DONE. Two masters, both gated on their own.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
export OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6
cd /Volumes/Extreme/_edit_work/website-video-828
A=website_video_16x9_A_tan-corrected.mp4; B=website_video_16x9_B_tan-as-is.mp4
DR="DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45 MUSIC_DB=-44 COMP=0"
echo "== 1 mix benchmark (20 s of the real graph)  $(date +%H:%M:%S)"
t0=$(date +%s); MIX_T=20 MIX_OUT=/tmp/rev6_mixbench.mov python3 layout.py mix; t1=$(date +%s); echo "   benchmark $((t1-t0)) s"; rm -f /tmp/rev6_mixbench.mov
if [ $((t1-t0)) -gt 120 ]; then echo "   slow -> MIX_STAGES=3"; export MIX_STAGES=3; fi
echo "== 2 mix  $(date +%H:%M:%S)"; python3 layout.py mix; echo "   nocap.mov $(date +%H:%M:%S)"
echo "== 2.5 face-landmark track on THIS mix + proof sheet  $(date +%H:%M:%S)"; python3 tanpass.py track 2>&1 | grep -v "warn\|Prototype" | tail -2; GAIN=0.90 python3 tanpass.py proof 2>&1 | grep tan_proof
echo "== 3 tan pass A (GAIN 0.90) and B (GAIN 1.00), same pipeline  $(date +%H:%M:%S)"
GAIN=0.90 python3 tanpass.py render nocap_A.mov > logs/rev6_tan_A.log 2>&1 &
pa=$!; GAIN=1.00 python3 tanpass.py render nocap_B.mov > logs/rev6_tan_B.log 2>&1; wait $pa
grep -h "corrected" logs/rev6_tan_A.log logs/rev6_tan_B.log | tail -2
echo "== 3.5 tan gate (patch/surround ratio, before vs A)  $(date +%H:%M:%S)"; python3 tanpass.py gate nocap.mov nocap_A.mov 2>&1 | grep -v warn | tail -5
echo "== 4 audio (rev-2 chain + approved dereverb), identical env on both  $(date +%H:%M:%S)"
env VIN=nocap_A.mov VOUT=nocap_audio_A.mov ${=DR} python3 audio4.py | grep -v "^  fit"
env VIN=nocap_B.mov VOUT=nocap_audio_B.mov ${=DR} python3 audio4.py | grep -v "^  fit"
echo "== 5 captions on both  $(date +%H:%M:%S)"
VIN=nocap_audio_A.mov VOUT=$A python3 captions.py
VIN=nocap_audio_B.mov VOUT=$B python3 captions.py burn
echo "== 6 gates on A  $(date +%H:%M:%S)"; ./deliver.sh $A
echo "== 6 gates on B  $(date +%H:%M:%S)"; ./deliver.sh $B
echo "== 7 face A/B  $(date +%H:%M:%S)"; python3 ab_face.py $A $B AB_tan_face.mp4 2>&1 | grep -v warn
echo "REV6 DONE  $(date +%H:%M:%S)"
