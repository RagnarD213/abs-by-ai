"""Assemble the private review only after final check and independent records exist."""
import sys,subprocess,json,time
from pathlib import Path
O=Path(__file__).resolve().parents[1]
while True:
 try:
  gates=json.load(open(O/'final-gate-results.json'));report=json.load(open(O/'INDEPENDENT_REVIEW.json'))
  if len(gates)==2 and all(any(x['aspect']==g['aspect'] and x['sha256']==g['sha256'] for x in report['masters']) for g in gates):break
 except (FileNotFoundError,json.JSONDecodeError,KeyError):pass
 time.sleep(10)
for name in ['r4_final_status.py','r4_package.py','r4_page.py']:
 q=subprocess.run([sys.executable,str(O/'recipe'/name)])
 if q.returncode:raise SystemExit((name,q.returncode))
print('PRIVATE REVIEW PACKAGED; PLAYER TEST REMAINS',flush=True)
