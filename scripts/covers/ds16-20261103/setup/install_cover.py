#!/usr/bin/env python3
"""Install Dan's unchanged X2 pick, preserving exact reviewed platform bytes."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,urllib.request
R=Path(__file__).resolve().parents[4]
V=R/'Short-form video content/covers/review/ds16-last-ten-pounds-20261103'
A=R/'Short-form video content/covers/approved-ds16';A.mkdir(parents=True,exist_ok=True)
D=R/'Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16/Approved covers';D.mkdir(parents=True,exist_ok=True)
E=Path('/Volumes/Extreme/Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16/Approved covers');E.mkdir(parents=True,exist_ok=True)
words='I like X2. Go ahead and install X2'
key=json.loads((V/'.blind-key.json').read_text())['labels']['X2']
k=re.search(r'letter (\w)',key['note']).group(1)
manifest=json.loads((V/'ds16/manifest.json').read_text())
rows={i['platform']:i for i in manifest['outputs'] if i['letter']==k}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(R/rows['youtube']['path']).startswith(key['sha'])
files={}
for platform,ext in [('instagram','.png'),('youtube','.jpg')]:
 row=rows[platform];src=R/(row['jpeg_path'] if ext=='.jpg' else row['path']);digest=row['jpeg_sha256'] if ext=='.jpg' else row['sha256'];assert sha(src)==digest
 name=f'{platform.title()}_ds-16_last-ten-pounds_cover-X2{ext}'
 for folder in [A,D,E]:
  dest=folder/name
  if dest.exists():assert sha(dest)==digest,'Existing approved cover differs; do not replace it silently.'
  else:shutil.copy2(src,dest)
  assert sha(dest)==digest
 files[platform]={'path':str(A/name),'sha256':digest,'bytes':src.stat().st_size,'delivery_path':str(D/name),'external_path':str(E/name),'copies_hash_verified':True}
record={'job':'DS-16','title':'How To Lose The Last Ten Pounds Of Fat','picked_by':'Dan','date':'2026-11-03','words':words,'pick':'X2','unchanged_from_review':True,'review_url':'http://127.0.0.1:9646/','files':files,'master_status':'HQ export pending; no master uploaded or scheduled'}
for folder in [A,D,E]:(folder/'picks.json').write_text(json.dumps(record,indent=2)+'\n')
# Log the blind pick exactly once.
log=Path.home()/'.absbyai-image-picks.jsonl'
existing=[json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
if not any(i.get('dan_words')==words and i.get('video')=='How To Lose The Last Ten Pounds Of Fat (DS-16)' for i in existing):
 subprocess.run(['python3',str(R/'.claude/skills/_shared/blind-image/blind.py'),'pick',str(V),'--chose','X2','--words',words],check=True)
# Cover uploads prepare the selected assets; they never create a post.
sys.path.insert(0,str(R/'scripts/blotato'))
from danrosefit_migration import api_key,call
statepath=A/'uploads.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
for platform,rec in files.items():
 p=Path(rec['path']);data=p.read_bytes();digest=rec['sha256']
 if state.get(platform,{}).get('sha256')==digest:
  assert hashlib.sha256(urllib.request.urlopen(state[platform]['url'],timeout=90).read()).hexdigest()==digest
  continue
 response=call('POST','/media/uploads',api_key(),{'filename':'ds16-last-ten-pounds-cover-X2-'+platform+p.suffix})
 req=urllib.request.Request(response['presignedUrl'],data=data,method='PUT',headers={'Content-Type':'image/png' if p.suffix=='.png' else 'image/jpeg'})
 urllib.request.urlopen(req,timeout=90).read();download=urllib.request.urlopen(response['publicUrl'],timeout=90).read();assert hashlib.sha256(download).hexdigest()==digest
 state[platform]={'url':response['publicUrl'],'path':str(p),'sha256':digest,'bytes':len(data),'remote_hash_verified':True};statepath.write_text(json.dumps(state,indent=2)+'\n');print('Uploaded and hash-verified selected',platform,'cover',flush=True)
# Register this unique caption hook with the existing Facebook cover installer.
hook="Here's how to lose the last 10 pounds of fat before you see your abs."
repo=R/'scripts/blotato/fb_reel_covers.json';live=Path.home()/'.absbyai/fb-reel-covers';livepic=live/'covers/ds16-last-ten-pounds-X2.jpg';livepic.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(files['youtube']['path'],livepic);assert sha(livepic)==files['youtube']['sha256']
for registry,path in [(repo,files['youtube']['path']),(live/'fb_reel_covers.json',str(livepic))]:
 data=json.loads(registry.read_text());matches=[x for x in data if x.get('job')=='DS-16' or x.get('match')==hook]
 assert len(matches)<=1,'Duplicate Facebook registry rows need reconciliation.'
 row={'job':'DS-16','match':hook,'cover':path,'w':1080,'h':1920,'cover_pick':'X2','note':'Approved unchanged2026-11-03. HQ export pending; no schedule yet.'}
 if matches:
  old=matches[0];row={**old,**row};data[data.index(old)]=row
 else:data.append(row)
 registry.write_text(json.dumps(data,indent=1)+'\n');read=json.loads(registry.read_text());saved=next(x for x in read if x.get('job')=='DS-16');assert sha(saved['cover'])==files['youtube']['sha256']
record.update(uploads=state,facebook={'repo_registry':str(repo),'live_registry':str(live/'fb_reel_covers.json'),'match':hook,'live_cover':str(livepic),'hash_verified':True},tiktok='Selected cover ready; frame-zero derivative awaits HQ master')
for folder in [A,D,E]:
 (folder/'picks.json').write_text(json.dumps(record,indent=2)+'\n');shutil.copy2(statepath,folder/'uploads.json') if folder!=A else None
print('Approved X2 package and Facebook installer verified; HQ still pending.',flush=True)
