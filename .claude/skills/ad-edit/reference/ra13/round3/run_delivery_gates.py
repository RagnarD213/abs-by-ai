from pathlib import Path
import sys,subprocess,json
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for fmt,name in [('9','ad9x16'),('16','ad16x9')]:
 if len(sys.argv)>1 and fmt not in sys.argv[1:]:continue
 d=O/f'checks{fmt}';w=json.load(open(d/'watch-final/logs/watch_pass.json'));assert w['inspected'] and w['open_defects']==0,'Native watch has unfinished/open issues'
 buildcap.wait('RA13 '+name+' full exact-file delivery gate')
 subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
 video=next((O/'final').glob('[!._]*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'))
 man=json.load(open(O/f'hf-manifest{fmt}.json'))
 for m in man:m['template']='analysis-card' if m['id']=='A1' else 'cta'
 (d/'hf-manifest.json').write_text(json.dumps(man,indent=1))
 code="import sys;sys.path.insert(0,sys.argv[1]);import checks;checks.C.WH=(1080,1920) if sys.argv[2]=='9' else (1920,1080);sys.argv=[sys.argv[0]]+sys.argv[3:];checks.main()"
 with open(d/'hyperframes.log','w') as f:subprocess.run([sys.executable,'-c',code,str(R/'.claude/skills/_shared/hyperframes'),fmt,str(d/'hf-manifest.json'),'--film',str(video),'--out',str(d/'hyperframes')],stdout=f,stderr=subprocess.STDOUT)
 with open(d/'delivery-gate.log','w') as f:rc=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(video),'--format',name,'--plan',str(d/'plan.json'),'--json',str(d/'delivery-gate.json')],stdout=f,stderr=subprocess.STDOUT).returncode
 print('GATE COMPLETE',fmt,rc,flush=True)
print('REQUESTED FULL GATES COMPLETED',flush=True)
