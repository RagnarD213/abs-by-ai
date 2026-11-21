"""Read RO-32 schedules and hash-download their saved media/cover URLs."""
from pathlib import Path
import sys,json,hashlib,urllib.request,datetime
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call,fetch_schedules
from longform_queue import posts,acct_of
O=Path('/Users/danielrose/Projects/_edit_work/RO32-setup/publish');v=json.loads((ROOT/'scripts/blotato/configs/ro32-ten-exercises.json').read_text());uploads=json.loads((O/'uploads.json').read_text());items=fetch_schedules(api_key());marker='utm_content='+v['slug'];ours=[i for i in items if marker in json.dumps(i)];assert len(ours)==4,len(ours)
cache={}
def remote(url,expected):
 if url not in cache:
  h=hashlib.sha256();n=0
  with urllib.request.urlopen(url,timeout=240) as r:
   for chunk in iter(lambda:r.read(1024*1024),b''):h.update(chunk);n+=len(chunk)
  cache[url]={'sha256':h.hexdigest(),'bytes':n}
 assert cache[url]['sha256']==expected['sha256'] and cache[url]['bytes']==expected['bytes'];return cache[url]
records=[]
for account,platform,when,target,text,media in posts(v):
 found=[i for i in ours if acct_of(i)==account];assert len(found)==1;item=found[0];draft=item['draft'];assert item['scheduledAt']==when,(platform,item['scheduledAt'],when);assert draft['content']['text']==text
 for k,value in target.items():assert draft['target'].get(k)==value,(platform,k,draft['target'].get(k),value)
 actualmedia=draft['content']['mediaUrls'];assert len(actualmedia)==1
 asset='instagram' if platform=='instagram' else 'tiktok' if platform=='tiktok' else 'main';verified=remote(actualmedia[0],uploads[asset]);cover=None
 if platform in ('youtube','instagram'):
  key='thumbnailUrl' if platform=='youtube' else 'coverImageUrl';cov='cover' if platform=='youtube' else 'instagram_cover';cover={'url':draft['target'][key],**remote(draft['target'][key],uploads[cov])}
 record={'platform':platform,'account_id':account,'schedule_id':str(item['id']),'scheduled_utc':when,'scheduled_chicago':datetime.datetime.fromisoformat(when.replace('Z','+00:00')).astimezone(__import__('zoneinfo').ZoneInfo('America/Chicago')).isoformat(),'caption':text,'target':draft['target'],'media_url':actualmedia[0],'media_verification':verified,'cover':cover,'youtube_public_required_before_social_release':platform!='youtube','readback_verified':True};records.append(record);print(platform,item['id'],when,'payload and full media download verified',flush=True)
# Only save relevant account fields; never credentials.
account_note='Schedule account IDs verified against existing shared queue configuration. Optional account-list endpoint returned401 in prior attempt; no profile lookup claimed.'
result={'account_identity_note':account_note,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queue_count':len(items),'ro32_count':len(ours),'schedules':records,'waitlisted':False,'native_youtube_upload':False,'new_per_video_routine':False,'tag_application':'Saved in config; Blotato target has no native keyword-tags field. Apply after release.','caption_application':'English SRT filed; native track waits for public YouTube ID.','future_public_tile_verification':'Actual tiles checked after release, not claimed now.'}
(Path(__file__).parent/'schedule-readback.json').write_text(json.dumps(result,indent=2)+'\n');(O/'queue-after-private.json').write_text(json.dumps(items,indent=2)+'\n')
