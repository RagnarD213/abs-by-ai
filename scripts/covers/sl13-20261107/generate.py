import concurrent.futures,json,subprocess,time,pathlib
w=pathlib.Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107')
plan=json.loads((w/'generation-plan.json').read_text())
root=pathlib.Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
def run(x):
 out=pathlib.Path(x['out'])
 if out.exists():return (x['id'],'exists')
 cmd=[str(root/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',x['prompt'],'--out',x['out']]
 if not x['real']:cmd+=['--image',str(w/'identity-reference.jpg')]
 t=time.time();r=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out.with_suffix('.log')).write_text(r.stdout)
 result={'id':x['id'],'exit':r.returncode,'seconds':round(time.time()-t),'exists':out.exists(),'output':r.stdout[-1800:]}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(run,plan))
(w/'generation-results.json').write_text(json.dumps(results,indent=2))
print('GENERATION_DONE',flush=True)
