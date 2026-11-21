from pathlib import Path
import json,hashlib,sys,subprocess,urllib.request,io,concurrent.futures
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/DS-109');S=W/'setup';P=S/'publish';P.mkdir(exist_ok=True);A=R/'Short-form video content/covers/approved-ds109';pick=json.load(open(A/'picks.json'));MASTER=W/'r4/review/media/hormozi-not-hungry-bored-r4.mp4';TT=P/'DS109-approved-B-cover-first-tiktok.mp4';sys.path.insert(0,str(R/'scripts/blotato'));from danrosefit_migration import api_key,call
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def files():return {'video':MASTER,'instagram':Path(pick['files']['instagram']['path']),'youtube':Path(pick['files']['youtube']['path']),'tiktok':TT}
def packets(p,stream):
 out=subprocess.check_output([str(R/'Media/video_edit/bin/ffprobe'),'-v','error','-select_streams',stream,'-show_packets','-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',str(p)],text=True);return [z['data_hash']for z in json.loads(out)['packets']]
def build():
 import tiktok_cover
 assert sha(MASTER)==pick['film_sha256'];proof=P/'tiktok-verification.json'
 if TT.exists()and proof.exists():
  q=json.load(open(proof));assert q['tiktok_sha256']==sha(TT)and q['cover_sha256']==pick['files']['instagram']['sha256'];print('TIKTOK_APPROVED_COPY_REUSED',flush=True);return
 q=tiktok_cover.build(str(MASTER),pick['files']['instagram']['path'],str(TT));assert q['ok'],q
 a,b=packets(MASTER,'a:0'),packets(TT,'a:0');assert a==b
 av,bv=packets(MASTER,'v:0'),packets(TT,'v:0');assert av==bv[1:];assert len(bv)==len(av)+1
 subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-i',str(TT),'-frames:v','1',str(P/'tiktok-actual-frame0.png')],check=True)
 q.update(master_sha256=sha(MASTER),tiktok_sha256=sha(TT),cover_sha256=pick['files']['instagram']['sha256'],audio_packet_payloads_identical=True,video_packet_payloads_after_cover_identical=True,video_packets_compared=len(av),audio_packets_compared=len(a));proof.write_text(json.dumps(q,indent=2));print('TIKTOK_APPROVED_COPY_VERIFIED',json.dumps(q),flush=True)
def upload_one(z):
 k,p=z;digest=sha(p);sp=P/('upload-'+k+'.json')
 if sp.exists():
  rec=json.load(open(sp));assert rec['sha256']==digest;back=urllib.request.urlopen(rec['url'],timeout=180).read();assert hashlib.sha256(back).hexdigest()==digest;print('REUSED_HASH_VERIFIED',k,flush=True);return k,rec
 q=call('POST','/media/uploads',api_key(),{'filename':'ds109-hormozi-approved-B-'+k+p.suffix});ct='video/mp4'if p.suffix=='.mp4'else('image/png'if p.suffix=='.png'else'image/jpeg');urllib.request.urlopen(urllib.request.Request(q['presignedUrl'],data=p.read_bytes(),method='PUT',headers={'Content-Type':ct}),timeout=240).read();back=urllib.request.urlopen(q['publicUrl'],timeout=240).read();assert len(back)==p.stat().st_size and hashlib.sha256(back).hexdigest()==digest
 if p.suffix!='.mp4':
  from PIL import Image
  im=Image.open(io.BytesIO(back));assert im.size==(1080,1920);im.verify()
  if k=='youtube':assert len(back)<2000000
 if k=='tiktok':(P/'uploaded-tiktok-download.mp4').write_bytes(back)
 rec={'path':str(p),'url':q['publicUrl'],'sha256':digest,'bytes':len(back),'full_download_verified':True};sp.write_text(json.dumps(rec,indent=2));print('UPLOADED_FULL_HASH_VERIFIED',k,len(back),flush=True);return k,rec
if sys.argv[1]=='build':build()
elif sys.argv[1]=='upload-base':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(upload_one,[(k,p)for k,p in files().items()if k!='tiktok']))
elif sys.argv[1]=='upload-tiktok':
 upload_one(('tiktok',TT));state={k:json.load(open(P/('upload-'+k+'.json')))for k in files()};(P/'uploads.json').write_text(json.dumps(state,indent=2));(A/'uploads.json').write_text(json.dumps(state,indent=2));print('ALL_FOUR_UPLOADS_VERIFIED',flush=True)
