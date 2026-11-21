from pathlib import Path
import json,subprocess,concurrent.futures,time
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers')
repo=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
(w/'sources').mkdir(exist_ok=True);(w/'logs').mkdir(exist_ok=True)
(w/'subscription-attempt.json').write_text(json.dumps({'google_project':'https://flow.google.com/project/215ff578-e91e-4e28-bf80-13d4af9e0be2','credits_before':20702,'model':'Nano Banana Pro','image_cost_credits':0,'watermarking':False,'first_submit':'1F','codex_model':'gpt-6.1-sol','codex_effort':'high','paid_api_spend':0},indent=2))
def run(j):
 k=j['id'];out=w/'sources'/f'{k}.png'
 if out.exists(): return (k,'exists')
 args=[str(repo/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',j['prompt'],'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 if not j.get('real_photo_slot'):args+=['--image',str(w/'identity-reference.jpg')]
 with (w/'logs'/f'{k}.log').open('w') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
 print(k,r.returncode,flush=True);return (k,r.returncode)
js=[j for j in json.loads((w/'generation-plan.json').read_text()) if j['source']=='codex']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,js))
(w/'generation-results.json').write_text(json.dumps(results));print('GENERATION_DONE',flush=True)
