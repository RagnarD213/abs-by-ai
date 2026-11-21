from pathlib import Path
import sys,subprocess,shutil,json
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('RA13 R3 whole-head anchor proof')
backup=O/'face-mesh-firstpass';backup.mkdir(exist_ok=True)
if not (backup/'framing.json').exists():
 shutil.copytree(O/'seg9',backup/'seg9',dirs_exist_ok=True);shutil.copy2(O/'framing.json',backup/'framing.json')
for n in ['head_measure.py','framing.py']:
 print('STAGE',n,flush=True);subprocess.run([sys.executable,str(O/'recipe'/n)],check=True)
print('WHOLE HEAD CENTERING REFINED',flush=True)
