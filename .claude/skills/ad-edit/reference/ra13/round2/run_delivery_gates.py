from pathlib import Path
import sys,subprocess,json
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Extreme/_edit_work/ra13/round2');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for fmt,name in [('9','ad9x16'),('16','ad16x9')]:
 d=O/f'checks{fmt}';w=json.load(open(d/'watch/logs/watch_pass.json'));assert w['inspected'] and w['open_defects']==0,'Native watch has unfinished/open issues'
 buildcap.wait('RA13 '+name+' full exact-file delivery gate')
 subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
 video=next((O/'final').glob('*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'))
 with open(d/'delivery-gate.log','w') as f:rc=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(video),'--format',name,'--plan',str(d/'plan.json'),'--json',str(d/'delivery-gate.json')],stdout=f,stderr=subprocess.STDOUT).returncode
 print('GATE COMPLETE',fmt,rc,flush=True)
print('BOTH FULL GATES COMPLETED',flush=True)
