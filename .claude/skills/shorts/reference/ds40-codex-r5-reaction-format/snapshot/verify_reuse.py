import sys,os,json,hashlib,numpy as np
from pathlib import Path
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
sys.path.insert(0,str(W/'recipe'));from common import frames
old=Path('/Volumes/Expansion/_edit_work/ds40/r2');src=np.load(old/'src_u8.npy',mmap_mode='r');rows=[]
with renderq.slot('Bill Maher R5 verify approved R2 source identity',pool='quick'):
 for i,f in enumerate(frames(1400.2322,nframes=279,scale=(1080,1920))):
  x=(np.clip(f[:1745],0,1)*255+.5).astype(np.uint8);d=np.abs(x.astype(np.int16)-src[i].astype(np.int16));rows.append({'i':i,'mean':float(d.mean()),'max':int(d.max())})
rec={'cache':str(old/'cache_r2'),'source':str(old/'src_u8.npy'),'frames':len(rows),'all_exact':all(x['max']==0 for x in rows),'rows':rows}
(W/'approved-prefix-source-identity.json').write_text(json.dumps(rec,indent=2));print(json.dumps({k:v for k,v in rec.items() if k!='rows'}),flush=True)
