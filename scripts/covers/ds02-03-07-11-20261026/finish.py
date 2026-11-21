"""Finish one approved Short: file the approved cover pair, build the TikTok cover-first copy, upload master + TikTok copy +
both covers to Blotato storage (hash-checked downloads), and write the URLs into its config. Resumes by verified hashes.
  python3 finish.py ds03 SB   (cover variant from round2/)"""
from pathlib import Path
import sys,json,hashlib,shutil,urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parent));from plan import P,R,SHORTS
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,call
import tiktok_cover
from configs import C as CFG,SRC
O=Path('/Volumes/Expansion/_edit_work/ds-batch-a-publish');O.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
k,v=sys.argv[1],sys.argv[2];s=SHORTS[k];slug=CFG[k]['slug']
A=P/'Short-form video content/covers/approved-ds-batch-a';A.mkdir(exist_ok=True)
ig=A/f'{slug}-instagram.png';yt=A/f'{slug}-youtube.jpg'
shutil.copy2(R/'round2/instagram'/f"{s['slug']}_cover-{v}.png",ig);shutil.copy2(R/'round2/youtube'/f"{s['slug']}_cover-{v}.jpg",yt)
assert yt.stat().st_size<2_000_000
master=P/'Short-form video content'/SRC[k];tt=O/f'{slug}-tiktok.mp4'
ver=tiktok_cover.build(str(master),str(ig),str(tt));print('tiktok',json.dumps(ver)[:300],flush=True)
assert ver.get('ok',True)
(O/f'{slug}-tiktok-verification.json').write_text(json.dumps(ver,indent=1,default=str))
files={'master':master,'tiktok':tt,'instagram':ig,'youtube':yt}
sp=O/f'{slug}-uploads.json';state=json.loads(sp.read_text()) if sp.exists() else {};key=api_key()
for name,p in files.items():
 data=p.read_bytes();d=sha(data)
 if state.get(name,{}).get('sha256')==d:print('kept',name);continue
 r=call('POST','/media/uploads',key,{'filename':f'{slug}-{name}{p.suffix}'})
 ct={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}[p.suffix]
 urllib.request.urlopen(urllib.request.Request(r['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=300).read()
 assert sha(urllib.request.urlopen(r['publicUrl'],timeout=300).read())==d,name+' remote bytes differ'
 state[name]={'url':r['publicUrl'],'sha256':d,'bytes':len(data),'path':str(p)};sp.write_text(json.dumps(state,indent=2));print('uploaded',name,len(data),flush=True)
cp=P/'scripts/blotato/configs'/f'{slug}.json';c=json.loads(cp.read_text())
c.update(video_url=state['master']['url'],tiktok_video_url=state['tiktok']['url'],instagram_cover_url=state['instagram']['url'],youtube_cover_url=state['youtube']['url'])
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
(A/f'{slug}-APPROVAL.json').write_text(json.dumps({'cover':v,'instagram_png':{'path':str(ig),'sha256':sha(ig.read_bytes())},'youtube_jpg':{'path':str(yt),'sha256':sha(yt.read_bytes()),'bytes':yt.stat().st_size},'uploads':state},indent=1))
print('done',slug)
