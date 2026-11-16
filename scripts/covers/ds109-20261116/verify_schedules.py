from pathlib import Path
import sys,json
R=Path.cwd();sys.path.insert(0,str(R/'scripts/blotato'));from danrosefit_migration import api_key,fetch_schedules;from organic_short_queue import post_plan,account_id
v=json.load(open(R/'scripts/blotato/configs/ds109-hungry-or-bored.json'));items=fetch_schedules(api_key());rows=[]
for want in post_plan(v):
 hits=[z for z in items if account_id(z)==want['account']and z['scheduledAt'][:16]==want['when'][:16]and 'utm_content='+v['slug']in json.dumps(z)];assert len(hits)==1,(want['platform'],len(hits));z=hits[0];d=z['draft'];assert d['content']['text']==want['text'];assert d['target']==want['target'];media=d['content']['mediaUrls'];assert len(media)==1
 rows.append({'platform':want['platform'],'schedule_id':str(z['id']),'account':want['account'],'scheduledAt':z['scheduledAt'],'text':d['content']['text'],'target':d['target'],'saved_media_url':media[0],'original_upload_url':want['media'],'expected_asset':'tiktok'if want['platform']=='tiktok'else'video'})
proof={'verified':True,'scheduled':True,'queue_count':len(items),'local_release':'2027-01-14 18:00 America/Chicago','title':v['title'],'posts':rows};Path('/tmp/ds109-saved-schedules.json').write_text(json.dumps(proof,indent=2));print('FOUR_ACTUAL_SCHEDULES_READ_BACK',json.dumps({z['platform']:z['schedule_id']for z in rows}),flush=True)
