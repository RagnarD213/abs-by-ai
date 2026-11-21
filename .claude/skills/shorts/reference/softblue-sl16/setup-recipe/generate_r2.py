from pathlib import Path
import subprocess,json,concurrent.futures,time
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=P/'Short-form video content/covers/review/sl16-20261027'
jobs=json.loads((R/'assets/jobs_r2.json').read_text())
def run(j):
 p=Path(j['out'])
 if p.exists():return 'exists '+p.stem
 args=[str(P/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',j['prompt'],'--out',j['out']]
 for r in j['ref']:args+=['--image',r]
 start=time.time();log=R/'assets'/f"{j['key']}-{j['which']}.log"
 with log.open('w') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
 msg=f"{p.stem} exit {r.returncode}, {round(time.time()-start)}s";print(msg,flush=True);return msg
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(run,jobs))
(R/'generation-results-r2.json').write_text(json.dumps(results,indent=1));print('Batch complete',len(list((R/'assets/gen').glob('*.png'))),flush=True)
