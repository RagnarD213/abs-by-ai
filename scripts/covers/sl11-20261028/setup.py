"""Install Dan's exact R4 picks and upload approved SL-11 media, without scheduling."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,urllib.request
P=Path(__file__).resolve().parents[3];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';S=B/'setup';S.mkdir(exist_ok=True)
W=Path('/Volumes/Expansion/_edit_work/sl11-publish');W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,call
import tiktok_cover as tc
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
dump=lambda p,v:Path(p).write_text(json.dumps(v,indent=2)+'\n')
final=json.loads((P/'Docs/SL11_FINALIZATION_RECEIPT_20261028.json').read_text());D=P/'Short-form video content/SL-11 The Vacuum'
files=final['drive_verification']['files'];masters={k:next(D/f['Name'] for f in files if f['Name'].endswith('.mp4') and f'Short {k.upper()} ' in f['Name']) for k in 'abc'}
for k,p in masters.items():assert sha(p)==next(f['Hashes']['sha256'] for f in files if f['Name']==p.name)
ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['approve','build','upload','backups']);args=ap.parse_args()
if args.phase=='approve':
 m=json.loads((B/'round4/manifest.json').read_text());assert json.loads((B/'round4/quality-checks.json').read_text())['status']=='PASS';picks=[]
 for r in m['outputs']:
  assert sha(P/r['path'])==r['sha256'];assert sha(P/r['jpeg_path'])==r['jpeg_sha256']
  dest=P/f"Short-form video content/covers/approved-sl11-{r['short']}";dest.mkdir(exist_ok=True)
  for field,suffix in [('path','.png'),('jpeg_path','.jpg')]:shutil.copy2(P/r[field],dest/f"sl11-{r['short']}-{r['platform']}-approved{suffix}")
  picks.append({**r,'installed_png':str(dest/f"sl11-{r['short']}-{r['platform']}-approved.png"),'installed_jpeg':str(dest/f"sl11-{r['short']}-{r['platform']}-approved.jpg")})
 dump(B/'picks.json',{'approved':'2026-10-29','quote':'These look good. Approve the revised covers for all three Shorts and complete the organic upload setup. Keep the approved videos and sound unchanged.','round':4,'files':picks,'movie_sha256':{k:sha(p) for k,p in masters.items()}})
 print('Exact R4 covers approved and installed, six PNG/JPEG pairs')
elif args.phase=='backups':
 remote=json.loads(subprocess.run([str(Path.home()/'bin/rclone'),'lsjson','gdrive_backup:Short-form video content/SL-11 The Vacuum','--hash'],capture_output=True,text=True,check=True).stdout)
 records=[]
 for f in files:
  local=D/f['Name'];backup=Path('/Volumes/Extreme/Short-form video content/SL-11 The Vacuum')/f['Name'];cloud=next(x for x in remote if x['Name']==f['Name']);digest=f['Hashes']['sha256']
  assert sha(local)==sha(backup)==cloud['Hashes']['sha256']==digest;assert local.stat().st_size==cloud['Size'];records.append({'name':f['Name'],'sha256':digest,'bytes':cloud['Size'],'drive_id':cloud['ID']})
 dump(S/'backups-verified.json',{'status':'PASS','files':records});print('Project, Extreme and fresh Drive metadata match:',len(records),'files')
elif args.phase=='build':
 picks=json.loads((B/'picks.json').read_text());ver={}
 def ah(p):
  r=subprocess.run([tc.FFMPEG,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True);return hashlib.sha256(r.stdout).hexdigest()
 for k,master in masters.items():
  cover=Path(next(r['installed_png'] for r in picks['files'] if r['short']==k and r['platform']=='instagram'));dest=W/f'sl11-{k}-tiktok-cover-first.mp4';r=tc.build(str(master),str(cover),str(dest));r.update(path=str(dest),sha256=sha(dest),master_sha256=sha(master),audio_identical=ah(master)==ah(dest));assert r['ok'] and r['audio_identical'];ver[k]=r;dump(S/'tiktok-verification.json',ver)
  tc.run([tc.FFMPEG,'-v','error','-y','-i',str(dest),'-frames:v','1',str(S/f'{k}-tiktok-frame-zero.png')]);print('Verified TikTok copy',k,flush=True)
elif args.phase=='upload':
 picks=json.loads((B/'picks.json').read_text());ver=json.loads((S/'tiktok-verification.json').read_text());statepath=S/'uploads.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
 for k,master in masters.items():
  ig=next(r for r in picks['files'] if r['short']==k and r['platform']=='instagram');yt=next(r for r in picks['files'] if r['short']==k and r['platform']=='youtube');assert ver[k]['ok'] and ver[k]['audio_identical']
  assets={'master':master,'tiktok':Path(ver[k]['path']),'instagram':Path(ig['installed_png']),'youtube':Path(yt['installed_jpeg'])}
  for name,p in assets.items():
   label=f'{k}-{name}';data=p.read_bytes();digest=sha(p);old=state.get(label,{})
   if old.get('sha256')==digest and old.get('verified'):
    assert hashlib.sha256(urllib.request.urlopen(old['url'],timeout=240).read()).hexdigest()==digest;print('Reverified',label,flush=True);continue
   r=call('POST','/media/uploads',api_key(),{'filename':f'sl11-{label}{p.suffix}'});ct={'.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'}[p.suffix]
   urllib.request.urlopen(urllib.request.Request(r['presignedUrl'],data=data,method='PUT',headers={'Content-Type':ct}),timeout=240).read();assert hashlib.sha256(urllib.request.urlopen(r['publicUrl'],timeout=240).read()).hexdigest()==digest
   state[label]={'url':r['publicUrl'],'path':str(p),'sha256':digest,'bytes':len(data),'verified':True};dump(statepath,state);print('Uploaded and verified',label,len(data),flush=True)
