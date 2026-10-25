import os,sys,subprocess,json
from pathlib import Path
W=Path(__file__).parent; R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); C=W/'recipe'; K=W/'key';K.mkdir(exist_ok=True)
name=sys.argv[1];p=next(x for x in json.loads((W/'plan.json').read_text())['pieces'] if x['id']==name); d=K/name;d.mkdir(exist_ok=True)
pl=d/'plate_out.npy'
if not pl.exists():pl.symlink_to(C/'plate_out.npy')
cmd=[sys.executable,str(R/'.claude/skills/_shared/chroma-key/keyonce.py'),str(d/'key.done'),'--inputs',str(C/'stage1_key.py'),str(C/'keylib.py'),str(C/'stage15_temporal.py'),str(C/'srcprep.py'),str(C/'common.py'),str(C/'plate_q.npy'),str(C/'plate_out.npy'),str(W/f'watch-{name}.json'),'--params',json.dumps(p,sort_keys=True),'--clear',str(d/'c1'),str(d/'c15'),'--',sys.executable,str(W/'key_stages.py'),name]
subprocess.run(cmd,check=True,cwd=C)
assert len(list((d/'c15').glob('f*.npy')))==p['n'],(name,'wrong frame count')
print('KEY_COMPLETE',name,flush=True)
if name=='response':
 subprocess.run([sys.executable,str(W/'pipeline_tail.py')],check=True,cwd=W)
