from pathlib import Path
import subprocess,os,json,concurrent.futures,time
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro30-20261029';B=P/'social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles/_build-2026-10-29';S=Path('/Volumes/Extreme/_edit_work/RO-30/setup')
ref=P/'photos/finalized social media photos/_cutouts/studio-blue-222_CUTOUT.png'
def run(k):
 out=B/'assets'/('background-C.png' if k=='C-background' else f'ai-{k}.png')
 assert not out.exists(),out
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompt-{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 if k!='C-background':cmd+=['--image',str(ref)]
 with open(S/f'generate-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True);return dict(image=k,exit_code=rc,file=str(out),exists=out.exists())
with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('RENDERQ_CORES','4'))) as ex:results=list(ex.map(run,['A','B','C-background','D']))
(S/'image-generation-complete.json').write_text(json.dumps(results,indent=2)+'\n')
