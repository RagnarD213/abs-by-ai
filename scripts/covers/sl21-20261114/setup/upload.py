from pathlib import Path
import sys,json,hashlib,urllib.request,threading,concurrent.futures
ROOT=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');w=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts/blotato'));from danrosefit_migration import api_key,call
sp=w/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key();lock=threading.Lock()
sha=lambda b:hashlib.sha256(b).hexdigest();files={}
if '--tiktok' in sys.argv:
 for r in json.loads((w/'tiktok-verification.json').read_text()):
  assert r['ok'] and r['audio_payload_identical'];files[f'short{r["short"]}-tiktok']=(Path(r['path']),r['sha256'])
else:
 for r in json.loads((w/'approved-media.json').read_text()):
  k=f'short{r["short"]}';files[k+'-master']=(Path(r['stage_master']),r['master_sha256'])
  for pl,field in [('instagram','instagram'),('youtube','youtube_jpeg')]:
   c=r['covers'][field];files[k+'-'+pl]=(Path(c['file']),c['sha256'])
def save():
 tmp=sp.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2));tmp.replace(sp)
def upload(item):
 name,(p,digest)=item;data=p.read_bytes();assert sha(data)==digest
 with lock:old=state.get(name,{}).copy()
 if old.get('sha256')==digest and old.get('remote_hash_verified'):
  assert sha(urllib.request.urlopen(old['url'],timeout=300).read())==digest
  print('Existing upload reverified',name,flush=True);return
 if old.get('sha256')!=digest or not old.get('presignedUrl'):
  r=call('POST','/media/uploads',key,{'filename':'sl21-whattocut-'+name+p.suffix});old={'path':str(p),'sha256':digest,'bytes':len(data),'url':r['publicUrl'],'presignedUrl':r['presignedUrl']}
  with lock:state[name]=old;save()
 ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
 urllib.request.urlopen(urllib.request.Request(old['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=300).read()
 back=urllib.request.urlopen(old['url'],timeout=300).read();assert len(back)==len(data) and sha(back)==digest
 old.pop('presignedUrl',None);old['remote_hash_verified']=True
 with lock:state[name]=old;save()
 print('Uploaded and full-download SHA256 verified',name,len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(upload,files.items()))
print('UPLOAD_BATCH_DONE',len(files),flush=True)
