import time,subprocess,sys,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]
for _ in range(1440):
 log=(O/'logs/hair-repair2.log').read_text()
 if 'REPAIRED R4 CANDIDATES READY' in log:
  for name in ['r4_gate.py','r4_native_audit.py']:
   with open(O/'logs'/('resumed-'+name+'.log'),'w') as f:r=subprocess.run([sys.executable,str(O/'recipe'/name)],stdout=f,stderr=subprocess.STDOUT)
   if r.returncode:raise SystemExit(str((name,r.returncode)))
  print('REPAIRED CANDIDATE EVIDENCE READY',flush=True);break
 time.sleep(10)
else:raise SystemExit('Repair wait expired after four hours')
