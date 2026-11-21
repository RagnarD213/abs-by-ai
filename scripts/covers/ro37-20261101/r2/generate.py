from pathlib import Path
import subprocess,json,concurrent.futures,sys
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro37-20261101/r2';B=P/'social media graphics/youtube/thumbnails/First Time At The Gym/_build-2026-11-02-r2';S=Path('/Volumes/Expansion/_edit_work/RO-37/setup')
def run(k):
 out=B/'assets'/f'{k}.png'
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompts/{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 refs=[B/f'source-frames/{k}-2048.jpg'] if k[0]=='R' else [P/'social media graphics/youtube/thumbnails/First Time At The Gym/_build-2026-11-01/assets/identity-reference.jpg',B/'assets/gym-identity.jpg']
 for r in refs: cmd+=['--image',str(r)]
 with open(S/f'r2-generate-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True);return dict(image=k,exit_code=rc,file=str(out),exists=out.exists())
keys=sys.argv[1:] or ['T1','T2','R1','R2','R3','R4']
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:r=list(ex.map(run,keys))
print(json.dumps(r))
