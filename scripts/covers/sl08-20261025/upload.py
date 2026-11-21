from pathlib import Path
import sys,json,hashlib,urllib.request,threading,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(P/'scripts/blotato'));from danrosefit_migration import api_key,call
D=P/'Short-form video content/Calories Not Losing Weight - Shorts R6';C=P/'Short-form video content/covers/approved-sl08';O=Path('/Volumes/Extreme/_edit_work/sl08-publish');sp=O/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key();lock=threading.Lock();files={}
m=json.loads((D/'finalization-manifest.json').read_text());picks=json.loads((C/'picks.json').read_text())['covers'];sha=lambda b:hashlib.sha256(b).hexdigest()
for i,v in enumerate(m['files'],1):
 p=Path(v['file']);assert sha(p.read_bytes())==v['sha256'];x=picks[p.stem]
 if '--tiktok' in sys.argv:
  verifies=json.loads((O/'tiktok-verification.json').read_text());row=next(z for z in verifies if z['short']==i);assert row['verification']['ok'] and row['audio_identical'];files[f's{i}-tiktok']=(Path(row['path']),row['sha256'])
 else:
  files[f's{i}-master']=(p,v['sha256']);files[f's{i}-instagram']=(Path(x['instagram']),x['instagram_sha256']);files[f's{i}-youtube']=(Path(x['youtube']),x['youtube_sha256'])
def save():
 tmp=sp.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2));tmp.replace(sp)
def upload(item):
 name,(p,digest)=item;data=p.read_bytes();assert sha(data)==digest
 with lock:old=state.get(name,{}).copy()
 if old.get('sha256')==digest and old.get('remote_hash_verified'):print('Already verified',name,flush=True);return
 if old.get('sha256')!=digest or not old.get('presignedUrl'):
  r=call('POST','/media/uploads',key,{'filename':'sl08-calories-'+name+p.suffix});old={'path':str(p),'sha256':digest,'bytes':len(data),'url':r['publicUrl'],'presignedUrl':r['presignedUrl']}
  with lock:state[name]=old;save()
 ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
 urllib.request.urlopen(urllib.request.Request(old['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=240).read()
 with urllib.request.urlopen(old['url'],timeout=240) as r:back=r.read()
 assert sha(back)==digest,(name,'download hash mismatch')
 old.pop('presignedUrl',None);old['remote_hash_verified']=True
 with lock:state[name]=old;save()
 print('Uploaded, downloaded and SHA-256 verified',name,len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(upload,files.items()))
print('Upload batch complete',len(files),flush=True)
