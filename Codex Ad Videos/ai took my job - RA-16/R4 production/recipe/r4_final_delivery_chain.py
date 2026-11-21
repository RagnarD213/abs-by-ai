"""Finish checks, then package the independently reviewed private films."""
import sys,subprocess,time,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]
while True:
 try:
  ready=(O/'CAPTION_REPAIR_READY.json').exists()
  watched=all(json.load(open(O/'watch'/a/'watch_pass.json')).get('inspected') is True for a in ['9x16','16x9'])
  if ready:break
 except (FileNotFoundError,json.JSONDecodeError):pass
 time.sleep(10)
q=subprocess.run([sys.executable,'-u',str(O/'recipe/r4_final_gates.py')])
if q.returncode:raise SystemExit(q.returncode)
q=subprocess.run([sys.executable,'-u',str(O/'recipe/r4_close_review.py')])
raise SystemExit(q.returncode)
