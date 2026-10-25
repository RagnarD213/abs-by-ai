"""Upload approved DS-33 R5 and cover 3 R3; resume by verified local hashes."""
from pathlib import Path
import sys, json, hashlib, urllib.request
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,call
O=Path('/Volumes/Extreme/_edit_work/ds33-publish')
C=P/'Short-form video content/covers/approved-ds33'
files={'master':P/'Short-form video content/Ronaldo Ab Belt - DS-33/Ronaldo Ab Belt SFC R5 - complete Short.mp4',
       'tiktok':O/'ronaldo-ab-belt-tiktok.mp4',
       'instagram':C/'ronaldo-ab-belt-instagram.png',
       'youtube':C/'ronaldo-ab-belt-youtube.jpg'}
sha=lambda data:hashlib.sha256(data).hexdigest()
assert sha(files['master'].read_bytes())=='b78674a331cd51c6003614ea149dc89095fc1e2539406a0826a5a100f65e80d0'
approval=json.loads((C/'APPROVAL.json').read_text())
for k,ext in [('instagram','png'),('youtube','jpg')]:
    assert sha(files[k].read_bytes())==approval['files'][f'{k}_{ext}']['sha256']
assert json.loads((O/'tiktok-verification.json').read_text())['ok']
sp=O/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key()
for name,p in files.items():
    data=p.read_bytes();digest=sha(data)
    if state.get(name,{}).get('sha256')==digest:
        assert sha(urllib.request.urlopen(state[name]['url'],timeout=90).read())==digest
        print('verified existing',name,flush=True);continue
    result=call('POST','/media/uploads',key,{'filename':'ds33-ronaldo-ab-belt-'+name+p.suffix})
    ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
    urllib.request.urlopen(urllib.request.Request(result['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=120).read()
    back=urllib.request.urlopen(result['publicUrl'],timeout=120).read()
    assert sha(back)==digest,name+' remote bytes differ'
    state[name]={'url':result['publicUrl'],'sha256':digest,'bytes':len(data),'path':str(p)}
    sp.write_text(json.dumps(state,indent=2));print('uploaded and hash verified',name,len(data),flush=True)
