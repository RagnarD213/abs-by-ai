#!/bin/zsh
# SL-06 r2: gate each short once its judge is recorded (inspected true), one at a time
cd /Volumes/Extreme/_edit_work/sl06
for S in "$@"; do
  until python3 -c "import json,sys; d=json.load(open('build/$S/gate/logs/watch_pass.json')); sys.exit(0 if d.get('inspected') else 1)" 2>/dev/null; do sleep 20; done
  while pgrep -f "deliver/gate.py" >/dev/null; do sleep 20; done
  ./rungate.sh $S > r5log/gate_$S.txt 2>&1; echo "GATE $S: $(grep 'DELIVERY GATE ' r5log/gate_$S.txt | tail -1)"
done
