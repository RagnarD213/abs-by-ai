"""Install/upload only DS-84's exact approved D cover and Gemini R3 master."""
from pathlib import Path
import sys,json,hashlib,urllib.request,subprocess,argparse
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts/blotato'))
import tiktok_cover as tc
from danrosefit_migration import api_key,call
WORK=Path('/Volumes/Expansion/_edit_work/ds84-publish');WORK.mkdir(parents=True,exist_ok=True)
SAVE=ROOT/'Short-form video content/covers/approved-ds84';MASTER=ROOT/'Short-form video content/DS-84 How To Do Hamstring Curls/How To Do Hamstring Curls SFC R3 - complete Short.mp4';TIKTOK=WORK/'ds84-gemini-r3-D-tiktok-cover-first.mp4'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n')
def ah(p):
 r=subprocess.run([tc.FFMPEG,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True);return hashlib.sha256(r.stdout).hexdigest()
a=argparse.ArgumentParser();a.add_argument('phase',choices=['build','upload-main','upload']);args=a.parse_args()
app=json.loads((SAVE/'APPROVAL.json').read_text());assert app['variation']=='D';assert sha(MASTER)==app['master_sha256']=='de0e83f5e69bd000d83beb1f22ed0593510b670fe5db2bfe85e5983bca73d0c9'
files={}
for platform,ext,name in [('instagram','.png','instagram'),('youtube','.jpg','youtube')]:
 row=next(x for x in app['files'] if x['platform']==platform and x['path'].endswith(ext));p=Path(row['path']);assert sha(p)==row['sha256'];files[name]=p
if args.phase=='build':
 r=tc.build(str(MASTER.resolve()),str(files['instagram'].resolve()),str(TIKTOK.resolve()));r.update(path=str(TIKTOK),sha256=sha(TIKTOK),bytes=TIKTOK.stat().st_size,master_sha256=sha(MASTER),cover_sha256=sha(files['instagram']),audio_sha256_master=ah(MASTER),audio_sha256_tiktok=ah(TIKTOK));r['audio_payload_identical']=r['audio_sha256_master']==r['audio_sha256_tiktok'];assert r['ok'] and r['audio_payload_identical'];dump(SAVE/'tiktok-verification.json',r)
 tc.run([tc.FFMPEG,'-v','error','-y','-i',str(TIKTOK),'-frames:v','1',str(SAVE/'tiktok-frame-zero.png')]);print(json.dumps(r,indent=2),flush=True)
else:
 files.update(master=MASTER)
 if args.phase=='upload':
  ver=json.loads((SAVE/'tiktok-verification.json').read_text());assert ver['ok'] and ver['audio_payload_identical'] and sha(TIKTOK)==ver['sha256'];files.update(tiktok=TIKTOK)
 statepath=SAVE/'uploads.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
 for label,p in files.items():
  digest=sha(p);old=state.get(label,{})
  if old.get('sha256')==digest and old.get('verified'):
   print('Previously uploaded and hash verified',label,flush=True);continue
  data=p.read_bytes();ext=p.suffix;mime={'.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'}[ext]
  result=call('POST','/media/uploads',api_key(),{'filename':f'ds84-gemini-r3-D-{label}{ext}'})
  urllib.request.urlopen(urllib.request.Request(result['presignedUrl'],data=data,method='PUT',headers={'Content-Type':mime}),timeout=240).read()
  with urllib.request.urlopen(result['publicUrl'],timeout=240) as response:back=response.read()
  assert len(back)==len(data) and hashlib.sha256(back).hexdigest()==digest
  state[label]={'url':result['publicUrl'],'path':str(p),'sha256':digest,'bytes':len(data),'verified':True,'verification':'Full hosted file downloaded and SHA-256 compared with exact local approved asset'};dump(statepath,state);print('Uploaded/hash verified',label,len(data),flush=True)
