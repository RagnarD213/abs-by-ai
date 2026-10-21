#!/bin/bash
# RO-24 round 1 rebuild after the independent check: wait for the re-keyed takes and the lower thirds, then ONE queued step runs
# the first minute, look stills, key comparisons, key numbers and every check.
W=/Volumes/Expansion/_edit_work/RO-24/round1; cd "$W"
deadline=$(( $(date +%s) + 4*3600 ))
while true; do
  ok=1
  for k in K1 K2 K3; do grep -q "KEY DONE" key/fm/$k.r4.log 2>/dev/null || ok=0; grep -q Traceback key/fm/$k.r4.log 2>/dev/null && { echo "KEY $k FAILED"; exit 1; }; done
  
  [ $ok = 1 ] && break
  [ $(date +%s) -gt $deadline ] && { echo "TIMEOUT waiting"; exit 1; }
  sleep 20
done
echo "INPUTS READY $(date +%H:%M)"
cat > "$W/recipe/_all_r1b.sh" <<'EOS'
#!/bin/bash
set -uo pipefail
R=/Volumes/Expansion/_edit_work/RO-24/round1/recipe
bash "$R/chain_fm.sh" && bash "$R/chain_fm2.sh" && bash "$R/post_fm.sh"
EOS
export GATE_GROUP=RO-24
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --priority --group RO-24 -- bash "$W/recipe/_all_r1b.sh" > "$W/checks/all_r1b.log" 2>&1
rc=$?; grep -E "DONE|FAIL|PASS|Traceback" "$W/checks/all_r1b.log" | tail -12; echo "ALL EXIT $rc"
