"""Upload only the approved RO-04 assets; persist each URL and verify remote bytes."""
from pathlib import Path
import sys,json,hashlib,urllib.request
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call
OUT=Path('/Volumes/Expansion/_edit_work/ro04-publish');OUT.mkdir(parents=True,exist_ok=True)
files={'master':ROOT/'Codex Content Videos/Arms Shoulders Workout Only - RO-04/Arms Shoulders Workout Only | codex | 16x9 | RO-04.mp4','cover':ROOT/'social media graphics/youtube/thumbnails/Arms Shoulders Workout Only/Arms Shoulders Workout Only - thumbnail FINAL.png'}
if '--tiktok-only' in sys.argv:
    verify=json.loads((OUT/'tiktok-verification.json').read_text());assert verify['ok'] and verify['audio_payload_identical']
    files={'tiktok':OUT/'Arms Shoulders Workout Only - TikTok cover first.mp4'}
statepath=OUT/'uploads.json';state=json.loads(statepath.read_text()) if statepath.exists() else {};key=api_key()
sha=lambda data:hashlib.sha256(data).hexdigest()
for name,p in files.items():
    data=p.read_bytes();digest=sha(data)
    if name=='master':assert digest=='140fd719899dc17d9d8d4217326a73dbdba6150fb1012c89eae7105518f8b7df'
    if name=='cover':assert digest=='548af7f873776f406634dd20195732f83935ecc8c41453fa73532c77fe3266d2'
    old=state.get(name,{})
    if old.get('sha256')==digest and old.get('remote_hash_verified'):
        print('Already uploaded and hash-verified:',name,flush=True);continue
    # Save the new media allocation immediately, so an uncertain transfer resumes it.
    if old.get('sha256')==digest and old.get('presignedUrl'):
        r=old
    else:
        r=call('POST','/media/uploads',key,{'filename':'ro04-arms-shoulders-workout-only-'+name+p.suffix})
        state[name]={'sha256':digest,'bytes':len(data),'path':str(p),'presignedUrl':r['presignedUrl'],'url':r['publicUrl']}
        statepath.write_text(json.dumps(state,indent=2))
    public=state[name]['url'];signed=state[name]['presignedUrl']
    ct='video/mp4' if p.suffix=='.mp4' else 'image/png'
    urllib.request.urlopen(urllib.request.Request(signed,data=data,method='PUT',headers={'Content-Type':ct}),timeout=240).read()
    back=urllib.request.urlopen(public,timeout=240).read();assert sha(back)==digest,name+' remote bytes differ'
    state[name].pop('presignedUrl',None);state[name]['remote_hash_verified']=True
    statepath.write_text(json.dumps(state,indent=2));print('Uploaded and SHA256 verified:',name,len(data),flush=True)
