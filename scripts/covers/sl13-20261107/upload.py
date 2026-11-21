from pathlib import Path
import sys,json,hashlib,urllib.request,threading,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107');sys.path.insert(0,str(P/'scripts/blotato'));from danrosefit_migration import api_key,call
sp=w/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key();lock=threading.Lock();files={};sha=lambda b:hashlib.sha256(b).hexdigest()
picks=json.loads((P/'Short-form video content/covers/approved-sl13/picks.json').read_text())['covers'];media=json.loads((w/'approved-media-check.json').read_text())
if '--tiktok' in sys.argv:
 for r in json.loads((w/'tiktok-verification.json').read_text()):
  assert r['verification']['ok'] and r['audio_identical'];files[r['short']+'-tiktok']=(Path(r['path']),r['sha256'])
else:
 for m,x in zip(media,picks.values()):
  k=x['short'];files[k+'-master']=(Path(m['file']),m['sha256'])
  for platform in ['instagram','youtube']:files[k+'-'+platform]=(Path(x[platform]),x[platform+'_sha256'])
def save():
 tmp=sp.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2));tmp.replace(sp)
def upload(item):
 name,(p,digest)=item;data=p.read_bytes();assert sha(data)==digest
 with lock:old=state.get(name,{}).copy()
 if old.get('sha256')==digest and old.get('remote_hash_verified'):print('Already verified',name,flush=True);return
 if old.get('sha256')!=digest or not old.get('presignedUrl'):
  r=call('POST','/media/uploads',key,{'filename':'sl13-calories-'+name+p.suffix});old={'path':str(p),'sha256':digest,'bytes':len(data),'url':r['publicUrl'],'presignedUrl':r['presignedUrl']}
  with lock:state[name]=old;save()
 ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
 urllib.request.urlopen(urllib.request.Request(old['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=300).read()
 with urllib.request.urlopen(old['url'],timeout=300) as r:back=r.read()
 assert len(back)==len(data) and sha(back)==digest,(name,'download mismatch')
 old.pop('presignedUrl',None);old['remote_hash_verified']=True
 with lock:state[name]=old;save()
 print('Uploaded/downloaded SHA256 verified',name,len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(upload,files.items()))
print('UPLOAD_BATCH_DONE',len(files),flush=True)
