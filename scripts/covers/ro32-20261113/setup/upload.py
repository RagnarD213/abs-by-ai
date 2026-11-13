"""Upload approved RO-32 assets through shared Blotato client and verify remote SHA256."""
from pathlib import Path
import sys,json,hashlib,urllib.request,mimetypes
sys.path.insert(0,str(Path(__file__).parent));from exact_file_gate import check,digest,ROOT
sys.path.insert(0,str(ROOT/'scripts/blotato'));from danrosefit_migration import api_key,call
O=Path('/Users/danielrose/Projects/_edit_work/RO32-setup/publish');P=ROOT/"social media graphics/youtube/thumbnails/I'm 41. Here Are The 10 Exercises I Do Every Week"
FILES={'cover':P/"I'm 41. Here Are The 10 Exercises I Do Every Week - thumbnail FINAL.jpg",'instagram_cover':P/'ro32-instagram-cover-1080x1920.jpg','main':O/'ro32-main-1080p.mp4','instagram':O/'ro32-instagram-1080p.mp4','tiktok':O/'ro32-tiktok-cover-first.mp4'}
check();sp=O/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {}
for name in sys.argv[1:]:
 p=FILES[name];sha=digest(p);size=p.stat().st_size
 if name=='cover':assert sha=='a144e20a6ea4b003439516a61317b83b208aa82452b55b3156226ec0b06cf6e9'
 elif name=='instagram_cover':assert sha==json.loads((Path(__file__).parent/'instagram-cover.json').read_text())['sha256']
 elif name=='tiktok':assert json.loads((O/'tiktok-verification.json').read_text())['ok']
 else:
  v=json.loads((O/'upload-verification.json').read_text())[name];assert v['ok'] and v['sha256']==sha
 if state.get(name,{}).get('sha256')!=sha:
  up=call('POST','/media/uploads',api_key(),{'filename':'ro32-ten-exercises-'+name+p.suffix})
  req=urllib.request.Request(up['presignedUrl'],data=p.read_bytes(),method='PUT',headers={'Content-Type':mimetypes.guess_type(p.name)[0] or 'application/octet-stream'})
  with urllib.request.urlopen(req,timeout=300) as response:response.read()
  state[name]={'url':up['publicUrl'],'path':str(p),'sha256':sha,'bytes':size,'download_verified':False};sp.write_text(json.dumps(state,indent=2)+'\n')
 h=hashlib.sha256();count=0
 with urllib.request.urlopen(state[name]['url'],timeout=240) as response:
  for chunk in iter(lambda:response.read(1024*1024),b''):h.update(chunk);count+=len(chunk)
 assert h.hexdigest()==sha and count==size
 state[name]['download_verified']=True;sp.write_text(json.dumps(state,indent=2)+'\n');print(name,'uploaded, full download SHA256 verified',size,flush=True)
