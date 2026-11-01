from pathlib import Path
import subprocess,json,concurrent.futures,sys
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro37-20261101';B=P/'social media graphics/youtube/thumbnails/First Time At The Gym/_build-2026-11-01';S=Path('/Volumes/Expansion/_edit_work/RO-37/setup')
ref=B/'assets/identity-reference.jpg'
def run(k):
 out=B/'assets'/('background-C.png' if k=='C-background' else f'ai-{k}.png')
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompts/{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 if k!='C-background':cmd+=['--image',str(ref)]
 with open(S/f'generate-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True);return dict(image=k,exit_code=rc,file=str(out),exists=out.exists())
keys=sys.argv[1:] or ['A','B','C-background','D','E']
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:r=list(ex.map(run,keys))
print(json.dumps(r))
