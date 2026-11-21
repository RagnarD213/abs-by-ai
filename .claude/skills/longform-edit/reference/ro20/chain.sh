#!/bin/zsh
# RO-20 round 1, unattended: lower thirds rendered part by part in film order (two workers: the machine cap), then that
# part's stills and a page refresh; then the moving context clip of every lower third (two workers), page refreshed as they land.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Extreme/_edit_work/ro20; cd $W
HF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py"
RS="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/review_server.py"
hf() { python3 "$HF" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf "$@" }
for L in a b c d e f g h; do
  A=$(python3 recipe/partids.py $L ltA); B=$(python3 recipe/partids.py $L ltB)
  hf --render --only "$A" > hf_${L}A.log 2>&1 &
  p1=$!
  if [ -n "$B" ]; then hf --render --only "$B" > hf_${L}B.log 2>&1 & p2=$!; wait $p2 || echo "HF FAILED part $L (B)" >> chain.log; fi
  wait $p1 || echo "HF FAILED part $L (A)" >> chain.log
  hf --only "$(python3 recipe/partids.py $L lt)" > hf_${L}M.log 2>&1 || echo "HF MANIFEST FAILED part $L" >> chain.log
  python3 recipe/stills20.py $(python3 recipe/partids.py $L all) > stills_$L.log 2>&1 || echo "STILLS FAILED part $L" >> chain.log
  python3 recipe/page20.py >> chain.log 2>&1; python3 "$RS" 8862 $W/round1 > /dev/null 2>&1
  echo "PART $L DONE $(date +%H:%M)" >> chain.log
done
echo "ALL STILLS DONE $(date +%H:%M)" >> chain.log
ctx() {  # one worker: every second lower third, eight per call
  LT=($(python3 -c "
import json,sys; x=[r['id'] for r in json.load(open('plan_resolved.json')) if r['kind']=='lt']; print(' '.join(x[int(sys.argv[1])::2]))" $1))
  i=1
  while [ $i -le ${#LT[@]} ]; do
    B=(${LT[@]:$((i-1)):8}); [ ${#B[@]} -eq 0 ] && break      # an empty batch would call round1.py with no ids = every item (it hung at the end of the RO-20 run)
    python3 recipe/round1.py context $B >> context_w$1.log 2>&1 || echo "CONTEXT FAILED worker $1 near ${LT[$i]}" >> chain.log
    i=$((i+8)); echo "CONTEXT worker $1: $((i-1)) of ${#LT[@]} $(date +%H:%M)" >> chain.log
    [ $1 = 0 ] && { python3 recipe/page20.py >> chain.log 2>&1; python3 "$RS" 8862 $W/round1 > /dev/null 2>&1 }
  done
}
ctx 0 & c0=$!; ctx 1 & c1=$!; wait $c0; wait $c1
python3 recipe/page20.py >> chain.log 2>&1; python3 "$RS" 8862 $W/round1 > /dev/null 2>&1
echo "CHAIN COMPLETE $(date +%H:%M)" >> chain.log
