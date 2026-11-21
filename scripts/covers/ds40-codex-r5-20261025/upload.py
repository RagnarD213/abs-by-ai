"""Install only Dan's approved cover R3 and exact Codex R5 master.
Upload state is written after byte-for-byte remote verification, allowing resume.
"""
from pathlib import Path
import sys,json,hashlib,urllib.request
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,call
O=Path('/Volumes/Extreme/_edit_work/ds40-codex-r5-publish')
C=P/'Short-form video content/covers/approved-ds40-codex-r5'
files={'master':P/'Short-form video content/Fat 90 Year Old - DS-40/Codex R5 setup/Bill Maher Fat 90-Year-Old - Codex R5.mp4',
       'instagram':C/'bill-maher-fat-90-year-old-instagram.png',
       'youtube':C/'bill-maher-fat-90-year-old-youtube.jpg'}
sha=lambda data:hashlib.sha256(data).hexdigest()
assert sha(files['master'].read_bytes())=='3808e604f218ad7281865ea74b3cbcf1a740a1bc595d060f1bcb34b8a3f4f720'
app=json.loads((C/'APPROVAL.json').read_text())
for key,ext in [('instagram','png'),('youtube','jpg')]:assert sha(files[key].read_bytes())==app['files'][f'{key}_{ext}']['sha256']
if '--tiktok-only' in sys.argv:
    assert json.loads((O/'tiktok-verification.json').read_text())['ok']
    assert json.loads((O/'audio-payload-identity.json').read_text())['identical']
    files={'tiktok':O/'bill-maher-fat-90-year-old-tiktok.mp4'}
sp=O/'uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key()
for name,p in files.items():
    data=p.read_bytes();digest=sha(data)
    if state.get(name,{}).get('sha256')==digest and state[name].get('remote_hash_verified'):
        print('Already uploaded and hash verified:',name,flush=True);continue
    result=call('POST','/media/uploads',key,{'filename':'ds40-bill-maher-fat-90-year-old-'+name+p.suffix})
    ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
    urllib.request.urlopen(urllib.request.Request(result['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=180).read()
    back=urllib.request.urlopen(result['publicUrl'],timeout=180).read();assert sha(back)==digest,name+' remote bytes differ'
    state[name]={'url':result['publicUrl'],'sha256':digest,'bytes':len(data),'path':str(p),'remote_hash_verified':True}
    sp.write_text(json.dumps(state,indent=2)+'\n');print('Uploaded and remote SHA-256 verified:',name,len(data),flush=True)
