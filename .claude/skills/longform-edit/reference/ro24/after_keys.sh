#!/bin/bash
# wait for K1-K3 and both lower thirds, then run chain_fm.sh as one queued step (prints why it stopped)
W=/Volumes/Expansion/_edit_work/RO-24/round1; cd "$W"
deadline=$(( $(date +%s) + 3*3600 ))
while true; do
  ok=1
  for k in K1 K2 K3; do grep -q "KEY DONE" key/fm/$k.log 2>/dev/null || ok=0; grep -q Traceback key/fm/$k.log 2>/dev/null && { echo "KEY $k FAILED"; exit 1; }; done
  [ -s hf/renders/G01.mov ] && [ -s hf/renders/G02.mov ] && [ -s hf/renders/G02_mask.mov ] && ! pgrep -f "from_plan.py --plan $W" >/dev/null || ok=0
  grep -q Traceback hf/render.log && { echo "HF FAILED"; exit 1; }
  [ $ok = 1 ] && break
  [ $(date +%s) -gt $deadline ] && { echo "TIMEOUT waiting for keys"; exit 1; }
  sleep 20
done
echo "INPUTS READY $(date +%H:%M)"
export GATE_GROUP=RO-24
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --group RO-24 -- bash "$W/recipe/chain_fm.sh" > "$W/checks/chain_fm.log" 2>&1
rc=$?; tail -3 "$W/checks/chain_fm.log"; echo "CHAIN EXIT $rc"
