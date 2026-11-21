from pathlib import Path
import subprocess,sys,json
O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for n in ['preservation.py','native_checks.py']:
 print('STAGE',n,flush=True);subprocess.run([sys.executable,str(O/'recipe'/n)],check=True)
buildcap.wait('RA13 audio selftest')
with open(O/'logs/audio-selftest.log','w') as f:rc=subprocess.run(['zsh',str(R/'.claude/skills/_shared/audio/selftest.sh')],stdout=f,stderr=subprocess.STDOUT).returncode
(O/'audio-selftest.json').write_text(json.dumps(dict(returncode=rc,log=str(O/'logs/audio-selftest.log')),indent=2));print('AUDIO SELFTEST RETURN CODE',rc,flush=True)
for n,args in [('quality_pass.py',['9']),('quality_pass.py',['16']),('write_sheet.py',[])]:
 print('STAGE',n,args,flush=True);subprocess.run([sys.executable,str(O/'recipe'/n)]+args,check=True)
for fmt in ['9x16','16x9']:
 v=next((O/'final').glob('[!._]*'+fmt+'*.mp4.edit-sheet.json'));subprocess.run([sys.executable,str(R/'.claude/skills/_shared/edit-sheet/validate.py'),str(v),'--hash','--json',str(O/f'edit-sheet-validation-{fmt}.json')],check=True)
print('EXACT-FILE EVIDENCE READY FOR EDITOR DISPOSITIONS',flush=True)
