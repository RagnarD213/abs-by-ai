from pathlib import Path
import subprocess,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro21-20261031/r2';B=P/'social media graphics/youtube/thumbnails/What Every Body Fat Percentage Looks Like/_build-2026-10-31';S=Path('/Volumes/Expansion/_edit_work/ro21-publish')
def run(k):
 out=B/'r2/assets'/f'{k}.png'
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompts/{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high','--image',str(B/'assets/identity-reference.jpg')]
 with open(S/f'generate-r2-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,['R1','R2','R4']))
