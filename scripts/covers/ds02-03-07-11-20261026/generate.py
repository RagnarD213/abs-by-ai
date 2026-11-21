import subprocess,json,concurrent.futures,time,sys
sys.path.insert(0,__file__.rsplit('/',1)[0]);from plan import P,R,jobs
from pathlib import Path
(R/'assets/gen').mkdir(parents=True,exist_ok=True);(R/'assets/prompts').mkdir(exist_ok=True)
only=set(sys.argv[1:])
def run(j):
 p=Path(j['out']);tag=f"{j['key']}-{j['which']}"
 if only and tag not in only:return 'skip '+tag
 if p.exists() and not only:return 'exists '+tag
 pf=R/'assets/prompts'/f'{tag}.txt';pf.write_text(j['prompt'])
 args=[str(P/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',str(pf),'--out',j['out']]
 for r in j['ref']:args+=['--image',r]
 t=time.time()
 with (R/'assets'/f'{tag}.log').open('w') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
 m=f"{tag} exit {r.returncode}, {round(time.time()-t)}s";print(m,flush=True);return m
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:res=list(ex.map(run,jobs()))
(R/'generation-results.json').write_text(json.dumps(res,indent=1));print('done',flush=True)
