#!/usr/bin/env python3
"""DS-05 Why Having Abs Beats Being A Fat Millionaire (Muhammad, organic dedicated Short), setup 2026-10-16.
Dan picked cover F3 (scripts/covers/ds05-20261014). Steps, each skipped when already done:
  1. lock the covers: Instagram PNG, YouTube JPEG under 2 MB, into covers/approved-muhammad-batch/
  2. TikTok cover-first copy (the Instagram cover as frame 0), verified
  3. upload master, TikTok copy and both covers to Blotato, hash-check each re-hosted file
State shares the batch files: /Volumes/Extreme/_edit_work/muhammad-shorts-publish/{manifest,uploads}.json"""
import hashlib,io,json,os,shutil,subprocess,sys,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(HERE,'..'))
from PIL import Image
import tiktok_cover
from danrosefit_migration import api_key,call
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
UP='/Volumes/Extreme/_edit_work/muhammad-shorts-publish';K='ds-05';SLUG='ds-05_why-having-abs-beats-being-a-fat-millionaire';PICK='F3'
REV=os.path.join(ROOT,'Short-form video content/covers/review/ds05-20261014');APP=os.path.join(ROOT,'Short-form video content/covers/approved-muhammad-batch')
sha=lambda b:hashlib.sha256(b).hexdigest();fsha=lambda p:sha(open(p,'rb').read())
ig=os.path.join(APP,f'Instagram_{SLUG}_cover-{PICK}.png');yt=os.path.join(APP,f'YouTube_{SLUG}_cover-{PICK}.jpg')
shutil.copyfile(os.path.join(REV,'instagram',f'{SLUG}_cover-{PICK}.png'),ig)
b=io.BytesIO();Image.open(os.path.join(REV,'youtube',f'{SLUG}_cover-{PICK}.png')).convert('RGB').save(b,'JPEG',quality=92);assert b.tell()<2_000_000;open(yt,'wb').write(b.getvalue())
lock=os.path.join(ROOT,'Short-form video content/covers/review/muhammad-batch-20261013/finals-locked.json');L=json.load(open(lock))
L['locked']=[x for x in L['locked'] if x['short']!=K]+[dict(short=K,pick=PICK,dan_words='Go with F3, set it up (2026-10-16)',instagram=os.path.relpath(ig,ROOT),instagram_sha256=fsha(ig),youtube=os.path.relpath(yt,ROOT),youtube_sha256=fsha(yt))]
json.dump(L,open(lock,'w'),indent=1)
video=os.path.join(ROOT,f'Short-form video content/{SLUG}.mp4');tt=os.path.join(UP,f'{SLUG}_tiktok-coverfirst.mp4')
mp=os.path.join(UP,'manifest.json');man=json.load(open(mp))
if not os.path.exists(tt) or man.get(K,{}).get('pick')!=PICK:
    v=tiktok_cover.build(video,ig,tt);print('tiktok build',v)
    FP=os.path.join(ROOT,'Media/video_edit/bin/ffprobe')
    cnt=lambda f,s,e:int(subprocess.run([FP,'-v','error','-select_streams',s,'-count_packets','-show_entries','stream=nb_read_packets','-of','csv=p=0',f],capture_output=True,text=True).stdout.strip())
    ver=dict(frames_src=cnt(video,'v:0',0),frames_out=cnt(tt,'v:0',0),audio_pkts_src=cnt(video,'a:0',0),audio_pkts_out=cnt(tt,'a:0',0))
    ver['ok']=ver['frames_out']==ver['frames_src']+1 and ver['audio_pkts_out']==ver['audio_pkts_src'];assert ver['ok'],ver
    man[K]=dict(video=video,tiktok=tt,ig_cover=ig,yt_cover=yt,pick=PICK,verify=ver);json.dump(man,open(mp,'w'),indent=1);print('verified',ver)
sp=os.path.join(UP,'uploads.json');st=json.load(open(sp));key=api_key();CT={'.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg'}
for f in ('video','tiktok','ig_cover','yt_cover'):
    path=man[K][f];data=open(path,'rb').read()
    if st.get(f'{K}:{f}',{}).get('sha256')==sha(data):continue
    ext=os.path.splitext(path)[1];r=call('POST','/media/uploads',key,{'filename':f'{K}-{f}{ext}'})
    urllib.request.urlopen(urllib.request.Request(r['presignedUrl'],data=data,method='PUT',headers={'Content-Type':CT[ext]})).read()
    back=urllib.request.urlopen(r['publicUrl']).read();assert sha(back)==sha(data),f'{f} re-hosted bytes differ'
    st[f'{K}:{f}']=dict(url=r['publicUrl'],sha256=sha(data),bytes=len(data));json.dump(st,open(sp,'w'),indent=1);print('uploaded',f,len(data),flush=True)
print(json.dumps({f:st[f'{K}:{f}'] for f in ('video','tiktok','ig_cover','yt_cover')},indent=1))
