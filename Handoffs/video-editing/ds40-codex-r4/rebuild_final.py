import os,time,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).parent
while True:
 try:os.kill(3202,0);time.sleep(3)
 except ProcessLookupError:break
C=W/'internal-candidate-c';C.mkdir(exist_ok=True)
for name in ['assembly.json','delivery-plan.json','caption-states.json','audio-gate.log','delivery-gate-initial.log','qa-preparation-complete.json']:
 if (W/name).exists():shutil.copy2(W/name,C/name)
for name in ['bill-maher-fat-90-year-old-r4.mp4','phone.mp4','frame-0588.jpg','bill-maher-fat-90-year-old-r4.mp4.deliver_gate.json']:
 q=W/'review/media'/name
 if q.exists():shutil.copy2(q,C/name)
if (W/'watch').exists():shutil.copytree(W/'watch',C/'watch',dirs_exist_ok=True);shutil.rmtree(W/'watch')
(W/'qa-preparation-complete.json').unlink(missing_ok=True)
subprocess.run([sys.executable,str(W/'assemble.py')],stdout=open(W/'assemble-final.log','w'),stderr=subprocess.STDOUT,check=True)
subprocess.run([sys.executable,str(W/'qa_prepare.py')],stdout=open(W/'qa-final.log','w'),stderr=subprocess.STDOUT,check=True)
