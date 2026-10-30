from pathlib import Path
import sys,json,hashlib,urllib.request,mimetypes
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');OUT=Path('/Volumes/Extreme/_edit_work/RO-30/setup/install')
sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call
approval=json.loads((OUT/'approval.json').read_text())
FILES={'cover':Path(approval['cover']),'main':OUT/'ro30-main-1080p.mp4','instagram':OUT/'ro30-instagram-1080p.mp4','tiktok':OUT/'ro30-tiktok-cover-first.mp4'}
def digest_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):
   if not b:break
   h.update(b)
 return h.hexdigest()
def digest_url(url):
 h=hashlib.sha256();n=0
 with urllib.request.urlopen(url,timeout=240) as f:
  while True:
   b=f.read(1024*1024)
   if not b:break
   h.update(b);n+=len(b)
 return h.hexdigest(),n
sp=OUT/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {}
for name in sys.argv[1:]:
 p=FILES[name];sha=digest_file(p);size=p.stat().st_size
 if name=='cover':assert sha==approval['cover_sha256']
 elif name=='tiktok':assert json.loads((OUT/'tiktok-verification.json').read_text())['ok']
 else:assert json.loads((OUT/'upload-verification.json').read_text())[name]['ok']
 if state.get(name,{}).get('sha256')!=sha:
  record=call('POST','/media/uploads',api_key(),{'filename':'ro30-love-handles-'+name+p.suffix})
  data=p.read_bytes();req=urllib.request.Request(record['presignedUrl'],data=data,method='PUT',headers={'Content-Type':mimetypes.guess_type(p.name)[0] or 'application/octet-stream'})
  urllib.request.urlopen(req,timeout=300).read();del data
  state[name]={'url':record['publicUrl'],'path':str(p),'sha256':sha,'bytes':size,'download_verified':False};sp.write_text(json.dumps(state,indent=2)+'\n')
 digest,count=digest_url(state[name]['url']);assert digest==sha and count==size
 state[name]['download_verified']=True;sp.write_text(json.dumps(state,indent=2)+'\n')
 print(name,'uploaded and remote bytes hash-verified',size,flush=True)
