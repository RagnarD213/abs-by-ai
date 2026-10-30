from pathlib import Path
import json,subprocess,os,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');C=P/'scripts/covers/ro30-20261029/r2';B=P/'social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles/_build-2026-10-30-r2';S=Path('/Volumes/Extreme/_edit_work/RO-30/setup/r2')
refs=[P/'photos/finalized social media photos/_cutouts/studio-blue-222_CUTOUT.png',Path('/Volumes/Extreme/_edit_work/RO-30/setup/sources/heavier-torso-reference.png')]
def run(k):
 out=B/'assets'/f'AI-Dan-fat-gain-{k}.png';assert not out.exists(),out
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--prompt-file',str(C/f'prompt-{k}.txt'),'--out',str(out),'--model','gpt-6.1-sol','--effort','high']
 for p in refs:cmd+=['--image',str(p)]
 with open(S/f'generate-{k}.log','w') as log:rc=subprocess.run(cmd,cwd=P,stdout=log,stderr=subprocess.STDOUT).returncode
 print(k,rc,out.exists(),flush=True);return dict(design=k,exit_code=rc,file=str(out),exists=out.exists())
with concurrent.futures.ThreadPoolExecutor(max_workers=min(3,int(os.environ.get('RENDERQ_CORES','4')))) as ex:res=list(ex.map(run,['1','2','3']))
(S/'generation-complete.json').write_text(json.dumps(res,indent=2)+'\n')
