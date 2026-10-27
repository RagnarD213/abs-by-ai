"""Upload only exact Dan-approved DS35 media, with resumable hash verification."""
from pathlib import Path
import argparse,json,hashlib,sys,urllib.request

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call

parser=argparse.ArgumentParser()
parser.add_argument('kind',choices=['covers','master','tiktok'])
args=parser.parse_args()
OUT=Path('/Volumes/Expansion/_edit_work/ds35-publish')
COVERS=ROOT/'Short-form video content/covers/approved-ds35'
APPROVAL=json.loads((COVERS/'APPROVAL.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
files={}
if args.kind=='covers':
    for k,row in APPROVAL['files'].items():files[k]=(Path(row['path']),row['sha256'])
elif args.kind=='master':
    p=ROOT/'Short-form video content/Dad Bod - DS-35/Dad Bod SFC R3 - off the cuff.mp4'
    gate=json.loads((OUT/'current-gate-2.6.2.json').read_text())
    assert gate['verdict']=='PASS' and gate['gate_version']=='2.6.2'
    files['master']=(p,APPROVAL['movie_sha256'])
else:
    v=json.loads((OUT/'tiktok-verification.json').read_text());assert v['ok'] and v['audio_identical']
    files['tiktok']=(Path(v['path']),v['sha256'])
state_path=OUT/'uploads.json'
state=json.loads(state_path.read_text()) if state_path.exists() else {}
for name,(path,digest) in files.items():
    data=path.read_bytes();assert sha(data)==digest
    existing=state.get(name)
    if existing and existing.get('sha256')==digest:
        back=urllib.request.urlopen(existing['url'],timeout=180).read()
        assert sha(back)==digest
        print('Existing upload reverified:',name,flush=True);continue
    record=call('POST','/media/uploads',api_key(),{'filename':'ds35-dad-bod-'+name+path.suffix})
    mime={'.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'}[path.suffix]
    request=urllib.request.Request(record['presignedUrl'],data=data,method='PUT',headers={'Content-Type':mime})
    urllib.request.urlopen(request,timeout=180).read()
    back=urllib.request.urlopen(record['publicUrl'],timeout=180).read();assert sha(back)==digest
    state[name]={'url':record['publicUrl'],'path':str(path),'sha256':digest,'bytes':len(data),'remote_hash_verified':True}
    state_path.write_text(json.dumps(state,indent=2)+'\n')
    print('Uploaded, downloaded and SHA-256 verified:',name,len(data),flush=True)
