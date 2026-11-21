from pathlib import Path
import sys,json,hashlib,urllib.request,threading,concurrent.futures
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(P/'scripts/blotato'));from danrosefit_migration import api_key,call
S=P/'Short-form video content';C=S/'covers/approved-sl16';O=Path('/Volumes/Extreme/_edit_work/sl16-publish');sp=O/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key();lock=threading.Lock();files={}
m=json.loads((S/'fasting-SHORTS-final-manifest.json').read_text())['shorts'];picks=json.loads((C/'picks.json').read_text())['covers'];tt={r['short']:r for r in json.loads((O/'tiktok-verification.json').read_text())};sha=lambda b:hashlib.sha256(b).hexdigest()
for v in m:
 n=v['n'];p=S/v['file'];x=picks[p.stem]
 files[f's{n}-master']=(p,v['sha256']);files[f's{n}-instagram']=(Path(x['instagram']),x['instagram_sha256']);files[f's{n}-youtube']=(Path(x['youtube']),x['youtube_sha256']);files[f's{n}-tiktok']=(Path(tt[n]['path']),tt[n]['sha256'])
def save():
 tmp=sp.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2));tmp.replace(sp)
def upload(item):
 name,(p,digest)=item;data=p.read_bytes();assert sha(data)==digest
 with lock:old=state.get(name,{}).copy()
 if old.get('sha256')==digest and old.get('remote_hash_verified'):print('Already verified',name,flush=True);return
 r=call('POST','/media/uploads',key,{'filename':'sl16-fasting-'+name+p.suffix});old={'path':str(p),'sha256':digest,'bytes':len(data),'url':r['publicUrl'],'presignedUrl':r['presignedUrl']}
 ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
 urllib.request.urlopen(urllib.request.Request(old['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=300).read()
 with urllib.request.urlopen(old['url'],timeout=300) as rr:back=rr.read()
 assert sha(back)==digest,(name,'download hash mismatch')
 old.pop('presignedUrl',None);old['remote_hash_verified']=True
 with lock:state[name]=old;save()
 print('verified',name,len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(upload,files.items()))
print('Upload batch complete',len(files),flush=True)
