#!/bin/zsh
cd /Users/danielrose/Projects/_edit_work/SL-21
L=round2/lipsync
for b in B1 B2; do python3 recipe/syncfix22.py $L/${b}_c.trim.mp4 $L/${b}_cl.mp4 $L/${b}_final4.mp4 --fps 25 --on-from 0.76 --on-exact --on-to 3.174 --search 5 2>/dev/null | tail -1; done
python3 recipe/undup.py $L/B1_c.trim.mp4 $L/B1_final4.mp4 clips/AIb1.mp4 2>/dev/null | tail -1
python3 recipe/undup.py $L/B2_c.trim.mp4 $L/B2_final4.mp4 clips/AIb2.mp4 2>/dev/null | tail -1
echo CLIPS_DONE
O="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content"
for S in D1 D2; do
  python3 recipe/batch.py render $S > logs_r2_render$S.txt 2>&1 || { echo RENDER_FAILED $S; tail -8 logs_r2_render$S.txt; exit 1; }
  python3 recipe/deliver.py copy $S > logs_r2_deliver$S.txt 2>&1 || { echo DELIVER_FAILED $S; tail -15 logs_r2_deliver$S.txt; exit 1; }
  recipe/runwatch.sh $S; tail -1 build/$S/gate/watch_run.log
  grep -v -i "warn" logs_r2_deliver$S.txt | grep -E "AUDIO GATE|caption text" | cut -c1-200
  N=$(cd recipe && python3 -c "import plans;print(plans.NAME['$S'])")
  python3 recipe/samecheck.py "$O/$N.mp4" "$O/whattocut REVIEW/round1/whattocut-short2_you-dont-deserve-a-vacation-until-youre-ripped.mp4" 2.48 5.95 2>/dev/null | tail -1 > round2/samecheck_$S.txt
  echo READY $S
done
echo ALL_READY
