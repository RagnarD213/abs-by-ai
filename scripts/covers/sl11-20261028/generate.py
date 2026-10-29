from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,time
P=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent;R=P/'Short-form video content/covers/review/sl11-vacuum-20261028';S=R/'sources'
def run(item):
 key,letter=item;out=S/f'{key}-{letter}.png';log=S/f'{key}-{letter}-generation.log'
 if out.exists():return {'short':key,'letter':letter,'existing':True}
 cmd=[str(P/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',str(D/'prompts'/f'{key}-{letter}.txt'),'--out',str(out)]
 if letter!='C':cmd+=['--image',str(S/'identity-reference.jpg'),'--image',str(S/'film-A.jpg')]
 with log.open('w') as f:q=subprocess.run(cmd,cwd=P,stdout=f,stderr=subprocess.STDOUT)
 result={'short':key,'letter':letter,'exit':q.returncode,'exists':out.exists()};print(json.dumps(result),flush=True);return result
with ThreadPoolExecutor(max_workers=5) as pool:res=list(pool.map(run,[(s,k) for s in 'abc' for k in 'ABCDE']))
(R/'generation-results.json').write_text(json.dumps(res,indent=2))
