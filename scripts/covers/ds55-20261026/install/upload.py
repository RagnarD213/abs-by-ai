"""Upload exact approved DS55 bytes and verify each public download."""
from pathlib import Path
import argparse, hashlib, json, sys, urllib.request
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call
parser=argparse.ArgumentParser()
parser.add_argument('kind',choices=['approved','tiktok'])
args=parser.parse_args()
OUT=Path('/Volumes/Expansion/_edit_work/ds55-publish')
OUT.mkdir(parents=True,exist_ok=True)
COVERS=ROOT/'Short-form video content/covers/approved-ds55'
approval=json.loads((COVERS/'APPROVAL.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
if args.kind=='approved':
    files={k:(Path(v['path']),v['sha256']) for k,v in approval['files'].items()}
    # Creative approval is not a synthetic technical PASS. Preserve raw gate failures.
    gate=json.loads((ROOT/'Short-form video content/Five Minute Exercises - DS-55/full-delivery-gate.json').read_text())
    assert gate['gate_version']=='2.6.2'
    files['master']=(ROOT/'Short-form video content/Five Minute Exercises - DS-55/Five Minute Exercises SFC R5 - complete Short.mp4',approval['movie_sha256'])
else:
    v=json.loads((OUT/'tiktok-verification.json').read_text())
    assert v['ok'] and v['audio_identical']
    files={'tiktok':(Path(v['path']),v['sha256'])}
state_path=OUT/'uploads.json'
state=json.loads(state_path.read_text()) if state_path.exists() else {}
for name,(path,digest) in files.items():
    data=path.read_bytes();assert sha(data)==digest
    if state.get(name,{}).get('sha256')==digest:
        assert sha(urllib.request.urlopen(state[name]['url'],timeout=180).read())==digest
        print('Existing upload reverified:',name,flush=True);continue
    record=call('POST','/media/uploads',api_key(),{'filename':'ds55-five-minute-exercises-'+name+path.suffix})
    request=urllib.request.Request(record['presignedUrl'],data=data,method='PUT',headers={'Content-Type':{'.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'}[path.suffix]})
    urllib.request.urlopen(request,timeout=180).read()
    assert sha(urllib.request.urlopen(record['publicUrl'],timeout=180).read())==digest
    state[name]={'url':record['publicUrl'],'path':str(path),'sha256':digest,'bytes':len(data),'remote_hash_verified':True}
    state_path.write_text(json.dumps(state,indent=2)+'\n')
    print('Uploaded and download-verified:',name,len(data),flush=True)
