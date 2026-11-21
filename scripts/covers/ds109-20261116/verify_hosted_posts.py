from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures,io
from PIL import Image
P=Path('/Volumes/Extreme/_edit_work/DS-109/setup/publish');q=json.load(open(P/'ds109-saved-schedules.json'));up=json.load(open(P/'uploads.json'))
def check(z):
 h=hashlib.sha256();size=0
 with urllib.request.urlopen(z['saved_media_url'],timeout=240)as r:
  while True:
   b=r.read(1024*1024)
   if not b:break
   size+=len(b);h.update(b)
 e=up[z['expected_asset']];assert size==e['bytes']and h.hexdigest()==e['sha256'],z['platform'];z.update(saved_media_sha256=h.hexdigest(),saved_media_bytes=size,full_saved_media_download_verified=True)
 field={'youtube':'thumbnailUrl','instagram':'coverImageUrl'}.get(z['platform'])
 if field:
  kind=z['platform'];data=urllib.request.urlopen(z['target'][field],timeout=90).read();assert hashlib.sha256(data).hexdigest()==up[kind]['sha256'];im=Image.open(io.BytesIO(data));assert im.size==(1080,1920);im.verify();z['saved_cover_sha256']=up[kind]['sha256'];z['saved_cover_download_verified']=True
 if z['platform']=='tiktok':assert z['target']['videoCoverTimestamp']==0
 print('SAVED_POST_MEDIA_FULL_SHA_VERIFIED',z['platform'],z['schedule_id'],size,flush=True);return z
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:q['posts']=list(pool.map(check,q['posts']))
q.update(all_four_saved_media_verified=True,public_tiles_verified=False,publication_pending=True);(P/'saved-post-verification.json').write_text(json.dumps(q,indent=2));print('ALL_FOUR_SAVED_POST_BYTES_AND_TARGETS_VERIFIED',flush=True)
