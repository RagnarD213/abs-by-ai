import sys,subprocess
from pathlib import Path
O=Path(__file__).resolve().parents[1]
for name in ['r4_gate.py','r4_native_audit.py']:
 with open(O/'logs'/('resumed-'+name+'.log'),'w') as f:q=subprocess.run([sys.executable,str(O/'recipe'/name)],stdout=f,stderr=subprocess.STDOUT)
 if q.returncode:raise SystemExit(str((name,q.returncode)))
print('REPAIRED CANDIDATE EVIDENCE READY',flush=True)
