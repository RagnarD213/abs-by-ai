from pathlib import Path
import subprocess,sys,json
O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3')
assert json.load(open(O/'asset-preflight-review.json'))['verdict']=='PASS'
with open(O/'logs/assemble.log','w') as f:subprocess.run([sys.executable,str(O/'recipe/assemble_render.py')],stdout=f,stderr=subprocess.STDOUT,check=True)
print('BOTH COMPLETE CANDIDATES READY',flush=True)
args=[sys.executable,str(O/'recipe/review_files.py'),str(O/'self-review-prompt.txt'),str(O/'self-review-answer.json')]+[str(next((O/'final').glob('[!._]*'+fmt+'*.mp4'))) for fmt in ['9x16','16x9']]+['/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg','/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4']
log=open(O/'logs/full-self-review.log','w');review=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT)
with open(O/'logs/exact-checks.log','w') as f:rc=subprocess.run([sys.executable,str(O/'recipe/after_assembly_render.py')],stdout=f,stderr=subprocess.STDOUT).returncode
rr=review.wait();log.close();print('EXACT CHECKS RC',rc,'SELF MEDIA REVIEW RC',rr,flush=True)
assert rc==0 and rr==0,'Inspect exact checks or media review logs'
print('EDITOR CANDIDATE EVIDENCE COMPLETE',flush=True)
