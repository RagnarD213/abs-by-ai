from pathlib import Path
import json,subprocess,sys
R=Path('/Volumes/Extreme/_edit_work/SL-11/round2');ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
for row in json.loads((R/'intro-manifest.json').read_text()):
 if len(sys.argv)>1 and row['id'] not in sys.argv[1:]:continue
 d=R/'build'/row['id'];w=json.loads((d/'gate/logs/watch_pass.json').read_text());assert w['inspected'] and w['open_defects']==0
 with open(d/'gate/check.log','w') as log:rc=subprocess.run(['python3',str(ROOT/'.claude/skills/_shared/deliver/gate.py'),row['file'],'--format','short','--plan',str(d/'gate/plan.json'),'--json',str(d/'gate/result.json')],stdout=log,stderr=subprocess.STDOUT).returncode
 print('GATE',row['id'],rc,flush=True)
 if (d/'gate/result.json').exists():
  j=json.loads((d/'gate/result.json').read_text());print(j.get('verdict'),[z for z in j.get('rows',[]) if not z.get('ok') and not z.get('na_reason')],flush=True)
