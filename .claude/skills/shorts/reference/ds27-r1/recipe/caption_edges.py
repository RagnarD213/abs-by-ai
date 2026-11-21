from pathlib import Path
import json,sys,os
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];os.environ['GATE_GROUP']='DS-27';sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech
name='Daily-workouts-context';ws,method=speech.transcribe(str(W/'build'/(name+'.wav')),model='small.en');words=[dict(w=v['w'].strip(),t0=v['t'],t1=v['e']) for v in ws]
chunks=[];cur=[]
for w in words:
 if cur and (len(cur)>=3 or w['t0']-cur[-1]['t1']>.55):chunks.append(cur);cur=[]
 cur.append(w)
 if w['w'].endswith(('.',',','!','?')):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
D=W/'caption-overrides';D.mkdir(exist_ok=True);(D/(name+'.json')).write_text(json.dumps(dict(local_timeline=True,method=method,chunks=chunks),indent=2));print(' '.join(v['w'] for v in words),flush=True)
