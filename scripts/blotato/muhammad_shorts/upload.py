#!/usr/bin/env python3
"""Upload the eight Muhammad dedicated Shorts' media to Blotato (master, TikTok cover-first copy, both covers)
and hash-check every re-hosted file. State: /Volumes/Extreme/_edit_work/muhammad-shorts-publish/uploads.json"""
import hashlib,json,os,sys,urllib.request
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from danrosefit_migration import api_key,call
UP='/Volumes/Extreme/_edit_work/muhammad-shorts-publish';man=json.load(open(UP+'/manifest.json'))
sp=UP+'/uploads.json';st=json.load(open(sp)) if os.path.exists(sp) else {}
CT={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'};key=api_key()
sha=lambda b:hashlib.sha256(b).hexdigest()
for k,m in man.items():
    for f in ('video','tiktok','ig_cover','yt_cover'):
        if f'{k}:{f}' in st: continue
        data=open(m[f],'rb').read();ext=os.path.splitext(m[f])[1]
        r=call('POST','/media/uploads',key,{'filename':f'{k}-{f}{ext}'})
        urllib.request.urlopen(urllib.request.Request(r['presignedUrl'],data=data,method='PUT',headers={'Content-Type':CT[ext]})).read()
        back=urllib.request.urlopen(r['publicUrl']).read();assert sha(back)==sha(data),f'{k}:{f} re-hosted bytes differ'
        st[f'{k}:{f}']=dict(url=r['publicUrl'],sha256=sha(data),bytes=len(data));json.dump(st,open(sp,'w'),indent=1);print('uploaded',k,f,len(data),flush=True)
print('all uploaded and hash-checked:',len(st))
