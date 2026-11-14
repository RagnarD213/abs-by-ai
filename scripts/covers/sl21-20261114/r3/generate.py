from pathlib import Path
import json,subprocess,concurrent.futures
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers/r3');repo=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');(w/'logs').mkdir(exist_ok=True)
(w/'subscription-attempt.json').write_text(json.dumps({'project':'https://flow.google.com/project/215ff578-e91e-4e28-bf80-13d4af9e0be2','first_submit':'A','credits_before':None,'paid_api_spend':0},indent=2))
def run(j):
 p=w/'sources'/(j['id']+'.png')
 if p.exists():return
 with (w/'logs'/(j['id']+'.log')).open('w') as f:
  r=subprocess.run([str(repo/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',j['prompt'],'--image',str(w.parent/'identity-reference.jpg'),'--out',str(p)],stdout=f,stderr=subprocess.STDOUT)
 print(j['id'],r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,[j for j in json.loads((w/'generation-plan.json').read_text()) if j['source']=='codex']))
print('GENERATION_DONE',flush=True)
