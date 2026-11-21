import time,subprocess,sys,os,json
from pathlib import Path
O=Path(__file__).resolve().parents[1];W=Path('/Volumes/Extreme/_edit_work/ra16')
for _ in range(1440):
 if 'REPAIRED CANDIDATE EVIDENCE READY' in (O/'logs/resumed-check-chain.log').read_text():break
 time.sleep(10)
else:raise SystemExit('Evidence wait expired after four hours')
with open(O/'logs/editor-full-motion.txt','w') as log:
 q=subprocess.run([sys.executable,str(W/'recipe/round3_asset_review.py'),str(O/'editor-motion-prompt.txt')]+[str(O/'review'/f'AI Took Job AD R4 - {a} - REVIEW.mp4') for a in ['9x16','16x9']],stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,GM='gemini-3.1-pro-preview'))
print('EDITOR SUPPORTING MOTION REVIEW COMPLETE',q.returncode,flush=True)
raise SystemExit(q.returncode)
