#!/usr/bin/env python3
"""Upload the six SL-06 shorts' media to Blotato (master, TikTok cover-first copy, Instagram PNG, YouTube JPEG) and
hash-check every re-hosted file. Masters are re-hashed against the approved sha256 prefixes first.
State: /Volumes/Expansion/_edit_work/sl06-publish/uploads.json"""
import hashlib,json,os,sys,urllib.request
from pathlib import Path
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here))
from root import P
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,call
from build import COPY
APPROVED={'s1':'0ebf77cf','s2':'ad578fa5','s3':'56ed1071','s4':'0458bf1d','s5':'f11bfee8','s6':'e9b58ad3'}
OUT=Path('/Volumes/Expansion/_edit_work/sl06-publish');sp=OUT/'uploads.json';st=json.load(open(sp)) if sp.exists() else {}
picks=json.loads((P/'Short-form video content/covers/approved-sl06/picks.json').read_text())['covers']
CT={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'};key=api_key();sha=lambda b:hashlib.sha256(b).hexdigest()
for k in sys.argv[1:] or list(COPY):
 slug=COPY[k][1];files=dict(master=P/'Short-form video content'/f'{slug}.mp4',tiktok=OUT/f'{slug}_tiktok.mp4',ig=Path(picks[slug]['instagram']),yt=Path(picks[slug]['youtube']))
 data=files['master'].read_bytes();assert sha(data).startswith(APPROVED[k]),f'{k} master changed after approval'
 for f,p in files.items():
  if f'{k}:{f}' in st:continue
  data=p.read_bytes();ext=p.suffix
  r=call('POST','/media/uploads',key,{'filename':f'sl06-{k}-{f}{ext}'})
  urllib.request.urlopen(urllib.request.Request(r['presignedUrl'],data=data,method='PUT',headers={'Content-Type':CT[ext]})).read()
  back=urllib.request.urlopen(r['publicUrl']).read();assert sha(back)==sha(data),f'{k}:{f} re-hosted bytes differ'
  st[f'{k}:{f}']=dict(url=r['publicUrl'],sha256=sha(data),bytes=len(data),path=str(p));sp.write_text(json.dumps(st,indent=1));print('uploaded',k,f,len(data),flush=True)
print('uploaded and hash-checked:',len(st))
