#!/usr/bin/env python3
"""Wait without using an AI session, then run initial exact-file measurements once."""
import json,time,subprocess,sys,os
from pathlib import Path
O=Path(__file__).resolve().parents[1]
deadline=time.time()+43200
while time.time()<deadline:
 try:s=json.loads((O/'BUILD_STATE.json').read_text())
 except (OSError,ValueError):s={}
 if s.get('status')=='failed':raise SystemExit('Render failed. See BUILD_STATE.json and logs/render.log.')
 if s.get('status')=='complete-candidates-awaiting-QC':
  env=dict(os.environ,RA16_BUILD_WAIT_SINCE=(O/'build-wait-start.txt').read_text().strip())
  with open(O/'logs/initial-checks.log','w') as log:q=subprocess.run([sys.executable,str(O/'recipe/r4_gate.py')],env=env,stdout=log,stderr=subprocess.STDOUT)
  (O/'CHECK_STATE.json').write_text(json.dumps({'status':'initial-measurements-done-awaiting-editor-and-independent-review' if q.returncode==0 else 'initial-checks-script-failed','exit':q.returncode,'at':time.time()},indent=2))
  raise SystemExit(q.returncode)
 time.sleep(15)
raise SystemExit('Capacity wait exceeded 12 hours. No automatic retry.')
