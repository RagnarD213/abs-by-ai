from pathlib import Path
import subprocess,json,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro24-20261030';B=P/'social media graphics/youtube/thumbnails/Reacting To Celebrity Ozempic Transformations/_build-2026-10-30';S=Path('/Volumes/Extreme/_edit_work/RO-24/setup')
ref=P/'photos/finalized social media photos/_cutouts/studio-blue-222_CUTOUT.png'
def run(k):
 out=B/'assets'/('background-C.png' if k=='C-background' else f'ai-{k}.png')
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompt-{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 if k!='C-background':cmd+=['--image',str(ref)]
 with open(S/f'generate-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True);return dict(image=k,exit_code=rc,file=str(out),exists=out.exists())
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:r=list(ex.map(run,['A','B','C-background','D','E']))
(S/'image-generation-complete.json').write_text(json.dumps(r,indent=2)+'\n')
