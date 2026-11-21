"""Read-only verification of the three approved Vacuum waiting-list packages."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
import hashlib,io,json,subprocess,sys,urllib.request
from PIL import Image
P=Path(__file__).resolve().parents[3];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';S=B/'setup'
sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,fetch_schedules
from organic_short_queue import post_plan
from cover_guard import assert_video_cover
from ad_guard import assert_organic
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
picks=json.loads((B/'picks.json').read_text());assert picks['round']==4
wait=json.loads((P/'scripts/blotato/video_waitlist.json').read_text());uploads=json.loads((S/'uploads.json').read_text())
fb=json.loads((P/'scripts/blotato/fb_reel_covers.json').read_text());livefb=json.loads((Path.home()/'.absbyai/fb-reel-covers/fb_reel_covers.json').read_text())
preserved=json.loads((S/'preservation-checks.json').read_text());tk=json.loads((S/'tiktok-verification.json').read_text())
names=['sl11-a-standing-stomach-vacuum','sl11-b-stop-holding-your-breath','sl11-c-one-20-second-vacuum-every-morning']
dates=['2027-01-16 09:00','2027-01-16 18:00','2027-01-18 18:00'];ct=ZoneInfo('America/Chicago');parent='scripts/blotato/configs/ro02-the-vacuum.json'
items=fetch_schedules(api_key());parent_config=json.loads((P/parent).read_text());parent_posts=[q for q in items if str(q.get('accountId') or q.get('draft',{}).get('accountId'))=='46963' and 'utm_content=ro02-the-vacuum' in json.dumps(q)]
assert len(parent_posts)==1 and parent_posts[0]['scheduledAt']==parent_config['main']=='2027-01-15T15:00:00.000Z'
assert not any('utm_content=sl11-' in json.dumps(q) for q in items)
jobs=json.loads((P/'Handoffs/video-editing/jobs.json').read_text())['jobs'];assert len({j['id'] for j in jobs})==len(jobs);assert next(j for j in jobs if j['id']=='SL-11')['state']=='finalized'
records=[]
for k,slug,local in zip('abc',names,dates):
 config=f'scripts/blotato/configs/{slug}.json';v=json.loads((P/config).read_text());entries=[e for e in wait if e['config']==config];assert len(entries)==1;e=entries[0]
 assert e['planned']==local and e['parent_config']==e['after']==parent and not e.get('queued') and not e.get('release_hold')
 utc=datetime.strptime(local,'%Y-%m-%d %H:%M').replace(tzinfo=ct).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z');assert v['main']==utc
 assert v['content_type']=='organic' and v['ai_generated'] is False and v['approved_cover_round']==4
 assert sha(P/v['source'])==v['film_approval_sha256']==picks['movie_sha256'][k]==uploads[k+'-master']['sha256']
 assert tk[k]['ok'] and tk[k]['audio_identical'] and preserved[k]['all_original_picture_VCL_units_identical'] and preserved[k]['audio_stream_hash_identical']
 assert sha(tk[k]['path'])==tk[k]['sha256']==uploads[k+'-tiktok']['sha256']
 for r in [r for r in picks['files'] if r['short']==k]:
  assert sha(r['installed_png'])==r['sha256'] and sha(r['installed_jpeg'])==r['jpeg_sha256']
 ig=next(r for r in picks['files'] if r['short']==k and r['platform']=='instagram');yt=next(r for r in picks['files'] if r['short']==k and r['platform']=='youtube')
 assert uploads[k+'-instagram']['sha256']==ig['sha256'] and uploads[k+'-youtube']['sha256']==yt['jpeg_sha256']
 for field,label in [('video_url','master'),('tiktok_video_url','tiktok'),('instagram_cover_url','instagram'),('youtube_cover_url','youtube')]:assert v[field]==uploads[k+'-'+label]['url']
 for registry in [fb,livefb]:
  hit=[r for r in registry if r.get('slug')==slug];assert len(hit)==1 and hit[0]['match']==v['hook'] and sha(hit[0]['cover'])==yt['jpeg_sha256']
 for post in post_plan(v):assert_video_cover({'post':{'content':{'platform':post['platform'],'text':post['text'],'mediaUrls':[post['media']]},'target':post['target']}})
 assert_organic(v,texts=[v['title'],v['hook'],v['body'],v['youtube_description']],sources=[v['source']])
 assert len(v['pinned_comment'])<180 and v['pinned_comment'].endswith('?')
 assert not any((q.get('scheduledAt') or '')[:16]==utc[:16] for q in items)
 records.append({'short':k.upper(),'slug':slug,'config':config,'planned_central':local,'planned_utc':utc,'waiting_entries':1,'approved_cover_round':4,'instagram_sha256':ig['sha256'],'youtube_sha256':yt['jpeg_sha256'],'master_sha256':v['film_approval_sha256'],'all_platform_preflights':'PASS','video_and_sound_unchanged':True})
def remote_check(item):
 name,r=item
 with urllib.request.urlopen(r['url'],timeout=240) as response:data=response.read()
 assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],name
 if name.endswith(('instagram','youtube')):
  with Image.open(io.BytesIO(data)) as im:assert im.size==(1080,1920);im.verify()
  if name.endswith('youtube'):assert len(data)<2_000_000
 print('Remote exact bytes PASS:',name,flush=True)
 return {'asset':name,'sha256':r['sha256'],'bytes':r['bytes']}
with ThreadPoolExecutor(max_workers=3) as pool:remote=list(pool.map(remote_check,uploads.items()))
result={'status':'PASS','checked_at':datetime.now(timezone.utc).isoformat(),'shorts':records,'remote_assets':remote,'live_schedules':len(items),'sl11_schedules':0,'parent_schedule':parent_posts[0]['id'],'parent_main':parent_config['main'],'queue_state':'waiting, not scheduled','git_head':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()}
(S/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: three waiting entries, exact planned dates, all approved covers, 12 remote hashes and unchanged masters/audio')
