#!/usr/bin/env python3
"""DS37 approved master/cover uploads through the shared Blotato client."""
from pathlib import Path
import json,hashlib,sys,subprocess,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[4]
A=R/'Short-form video content/covers/approved-ds37'
WORK=Path('/Volumes/Expansion/_edit_work/DS-37-publish')
MASTER=R/'Short-form video content/Dr Mike Dial SFC R4/Dr Mike Dial SFC R4 - final off the cuff.mp4'
TT=WORK/'Dr Mike Dial SFC R4 - TikTok approved B cover-first.mp4'
sys.path.insert(0,str(R/'scripts/blotato'))
import tiktok_cover
from danrosefit_migration import api_key,call
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def media():
 picks=json.loads((A/'picks.json').read_text())
 return dict(video=MASTER,tiktok=TT,instagram=Path(picks['files']['instagram']['path']),youtube=Path(picks['files']['youtube']['path']))
def build():
 assert sha(MASTER)=='92431f246bc27b03e0dd4fbc408062aa1b6fa65d134ffed564f940adc390ad41'
 p=WORK/'tiktok-verification.json'
 if TT.exists() and p.exists():
  old=json.loads(p.read_text());assert old['tiktok_sha256']==sha(TT) and old['cover_sha256']==sha(media()['instagram']);return
 result=tiktok_cover.build(str(MASTER),str(media()['instagram']),str(TT));assert result['ok'],result
 fp=str(R/'Media/video_edit/bin/ffprobe')
 def payloads(path):
  data=json.loads(subprocess.run([fp,'-v','error','-select_streams','a:0','-show_packets','-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',str(path)],capture_output=True,text=True,check=True).stdout)
  return [x['data_hash'] for x in data['packets']]
 a,b=payloads(MASTER),payloads(TT);assert a==b
 first=WORK/'tiktok-actual-frame0.png'
 subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-i',str(TT),'-frames:v','1',str(first)],check=True)
 result.update(master_sha256=sha(MASTER),tiktok_sha256=sha(TT),cover_sha256=sha(media()['instagram']),audio_packet_payloads_identical=True,audio_packets_compared=len(a),frame0=str(first))
 p.write_text(json.dumps(result,indent=2));print('TikTok one-frame cover verified; all original audio packet payloads unchanged.',flush=True)
def upload_one(item):
 k,p=item;dest=WORK/f'upload-{k}.json';digest=sha(p)
 if dest.exists():
  rec=json.loads(dest.read_text());assert rec['sha256']==digest
  with urllib.request.urlopen(rec['url'],timeout=180) as q:back=q.read()
  assert hashlib.sha256(back).hexdigest()==digest;print('Reused verified',k,flush=True);return k,rec
 result=call('POST','/media/uploads',api_key(),{'filename':'ds37-dr-mike-dial-'+k+p.suffix})
 ct='video/mp4' if p.suffix=='.mp4' else 'image/jpeg'
 with urllib.request.urlopen(urllib.request.Request(result['presignedUrl'],data=p.read_bytes(),method='PUT',headers={'Content-Type':ct}),timeout=240) as q:q.read()
 with urllib.request.urlopen(result['publicUrl'],timeout=240) as q:data=q.read()
 assert len(data)==p.stat().st_size and hashlib.sha256(data).hexdigest()==digest
 if k=='tiktok':
  checked=WORK/'uploaded-tiktok-download.mp4';checked.write_bytes(data)
  first=WORK/'uploaded-tiktok-actual-frame0.png'
  subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-i',str(checked),'-frames:v','1',str(first)],check=True)
 if p.suffix!='.mp4':
  from PIL import Image
  import io
  im=Image.open(io.BytesIO(data));assert im.size==(1080,1920);im.verify()
  if k=='youtube':assert len(data)<2_000_000
 rec=dict(path=str(p),url=result['publicUrl'],sha256=digest,bytes=len(data),full_download_verified=True)
 dest.write_text(json.dumps(rec,indent=2));print('Uploaded and full-hash-verified',k,len(data),flush=True);return k,rec
def upload():
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=dict(pool.map(upload_one,media().items()))
 (A/'uploads.json').write_text(json.dumps(rows,indent=2));(WORK/'uploads.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':
 WORK.mkdir(exist_ok=True,parents=True)
 if sys.argv[1]=='build':build()
 elif sys.argv[1]=='upload':upload()
