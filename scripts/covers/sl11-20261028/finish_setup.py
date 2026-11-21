"""Save complete SL-11 packaging and join the existing shared release waiting list."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import json,hashlib,shutil,sys
P=Path(__file__).resolve().parents[3];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';S=B/'setup';sys.path.insert(0,str(P/'scripts/blotato'))
from organic_short_queue import post_plan
from cover_guard import assert_video_cover
from ad_guard import assert_organic
from danrosefit_migration import api_key,fetch_schedules
dump=lambda p,v:Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
u=json.loads((S/'uploads.json').read_text());assert len(u)==12 and all(r['verified'] for r in u.values())
draft=json.loads((S/'voice-draft.json').read_text());plan=json.loads((S/'release-plan.json').read_text());picks=json.loads((B/'picks.json').read_text())
ct=ZoneInfo('America/Chicago');titles={'a':'How To Do A Standing Stomach Vacuum','b':'Stop Holding Your Breath During Stomach Vacuums','c':'Start With One 20-Second Vacuum Every Morning'}
slugs={'a':'sl11-a-standing-stomach-vacuum','b':'sl11-b-stop-holding-your-breath','c':'sl11-c-one-20-second-vacuum-every-morning'}
waitpath=P/'scripts/blotato/video_waitlist.json';wait=json.loads(waitpath.read_text());fbpath=P/'scripts/blotato/fb_reel_covers.json';fb=json.loads(fbpath.read_text())
livepath=Path.home()/'.absbyai/fb-reel-covers/fb_reel_covers.json';live=json.loads(livepath.read_text());livecovers=livepath.parent/'covers';livecovers.mkdir(exist_ok=True)
queue=fetch_schedules(api_key());(S/'queue-at-install.json').write_text(json.dumps(queue,indent=2));assert not any('utm_content=sl11-' in json.dumps(q) for q in queue),'Existing SL11 schedules require reconciliation'
configs=[]
for k,slot in zip('abc',plan['slots']):
 slug=slugs[k];data=draft[k];when=datetime.strptime(slot,'%Y-%m-%d %H:%M').replace(tzinfo=ct).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
 assert all(q.get('scheduledAt','')[:16]!=when[:16] for q in queue)
 for e in wait:
  if e.get('queued') or e.get('release_hold') or e['config'].endswith(slug+'.json'):continue
  old=json.loads((P/e['config']).read_text());assert old['main'][:16]!=when[:16],f'Slot taken by {e["config"]}'
 assert len(data['pinned_comment'])<180 and data['pinned_comment'].endswith('?')
 close='Subscribe to the channel and go to sixpackabs.com for all the newest videos.';tags='#StomachVacuum #AbWorkout #CoreTraining #Shorts'
 def link(platform):return f'https://absbyai.com/?utm_source={platform}&utm_medium=short&utm_campaign=stomach-vacuum&utm_content={slug}'
 captions={pl:'\n\n'.join([data['hook'],data['body'],close,link(pl),tags]) for pl in ['facebook','instagram','tiktok']}
 v={'content_type':'organic','source':str(Path(u[k+'-master']['path']).relative_to(P)),'slug':slug,'campaign':'stomach-vacuum','title':titles[k],'main':when,'keyword':'ABS','ai_generated':False,'hook':data['hook'],'body':data['body'],'close':close,'tags':tags,'pinned_comment':data['pinned_comment'],'instagram_first_comment':'Abs By AI: '+link('instagram'),'caption_overrides':captions,'youtube_description':'\n\n'.join([data['hook'],data['youtube_body'],close,link('youtube'),tags]),'kitchen':False,'gym':False,'parent_config':plan['parent_config'],'film_approval_sha256':u[k+'-master']['sha256'],'approved_cover_round':4,'setup_note':'Exact R4 real-screenshot cover approved October29. Original master bytes unchanged. TikTok separate cover-first copy preserves picture units and exact audio. Shared waiting list after RO-02; no native YouTube upload.'}
 for field,name in [('video_url','master'),('tiktok_video_url','tiktok'),('instagram_cover_url','instagram'),('youtube_cover_url','youtube')]:v[field]=u[k+'-'+name]['url']
 assert not any(x in json.dumps(v,ensure_ascii=False) for x in ['\u2014','\u2013'])
 assert_organic(v,texts=[v['title'],v['hook'],v['body'],v['close'],v['youtube_description']],sources=[v['source']])
 cover=Path(next(r['installed_jpeg'] for r in picks['files'] if r['short']==k and r['platform']=='youtube'));record={'job':'SL-11','slug':slug,'match':data['hook'],'cover':str(cover),'w':1080,'h':1920,'approved':'Dan approved exact Round4 design1 for all three Shorts on 2026-10-29','sha256':sha(cover),'when':when}
 fb=[r for r in fb if r.get('slug')!=slug];assert not any(r['match']==data['hook'] for r in fb);fb.append(record)
 target=livecovers/(slug+'-approved.jpg');shutil.copy2(cover,target);live=[r for r in live if r.get('slug')!=slug];live.append({**record,'cover':str(target)})
 config=f'scripts/blotato/configs/{slug}.json';dump(P/config,v);configs.append(config)
 if not any(e['config']==config for e in wait):wait.append({'config':config,'kind':'short','job':'SL-11','label':titles[k],'added':'2026-10-29','parent_config':plan['parent_config'],'after':plan['parent_config'],'kitchen':False,'gym':False,'filming_set':'poolside','planned':slot,'note':'R3 film and exact R4 real-screenshot cover approved. Twelve uploaded assets for three Shorts hash-checked. Wait for four spaces in shared top-up; after RO-02 public release.'})
dump(fbpath,fb);dump(livepath,live)
for config in configs:
 v=json.loads((P/config).read_text())
 for post in post_plan(v):assert_video_cover({'post':{'content':{'platform':post['platform'],'text':post['text'],'mediaUrls':[post['media']]},'target':post['target']}})
ours=sorted([e for e in wait if e['config'] in configs],key=lambda e:json.loads((P/e['config']).read_text())['main']);wait=[e for e in wait if e['config'] not in configs]
for entry in ours:
 when=json.loads((P/entry['config']).read_text())['main'];pos=next((i for i,e in enumerate(wait) if json.loads((P/e['config']).read_text())['main']>when),len(wait));wait.insert(pos,entry)
dump(waitpath,wait)
dump(S/'ready-configs.json',{'configs':configs,'preflight':'PASS: all12 platform targets, covers decoded, approved FB covers source/live hashes match','queue_count':len(queue),'free':200-len(queue),'waiting_entries':len([e for e in wait if not e.get('queued') and not e.get('release_hold')]),'status':'HOLD: shared queue capacity and earlier videos','planned_slots':plan['slots']});print('Three complete configs, 12 platform preflights PASS, shared waitlist saved')
