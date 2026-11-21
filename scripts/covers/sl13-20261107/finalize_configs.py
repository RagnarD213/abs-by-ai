from pathlib import Path
import json,sys,hashlib,datetime,subprocess
root=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107');sys.path.insert(0,str(root/'scripts/blotato'));import video_topup as t,release_phases as rp
from danrosefit_migration import api_key,fetch_schedules
from organic_short_queue import post_plan
from ad_guard import assert_organic
from cover_guard import assert_video_cover
meta=json.loads((w/'packaging/metadata.json').read_text());picks=list(json.loads((root/'Short-form video content/covers/approved-sl13/picks.json').read_text())['covers'].values());media=json.loads((w/'approved-media-check.json').read_text());uploads=json.loads((w/'uploads.json').read_text());assert len(uploads)==12 and all(x.get('remote_hash_verified') for x in uploads.values())
wp=root/'scripts/blotato/video_waitlist.json';wl=json.loads(wp.read_text());(w/'waitlist-pre-final.json').write_text(json.dumps(wl,indent=2));items=fetch_schedules(api_key());(w/'live-schedules-pre-final.json').write_text(json.dumps(items,indent=2));assert not any('sl13-short' in json.dumps(x) for x in items)
parent='scripts/blotato/configs/ro11-calories-dont-matter.json';pv=json.loads((root/parent).read_text());pt=[x for x in items if t.acct(x)=='46963' and 'utm_content='+pv['slug'] in json.dumps(x)];assert len(pt)==1 and pt[0]['scheduledAt']==pv['main'];pday=t.local_day(pv['main'])
taken=set()
for x in items:
 dt=x.get('scheduledAt')
 if dt and t.acct(x) in t.ACCOUNTS:taken.add((t.local_day(dt),t.local_hhmm(dt)))
for e in wl:
 if e.get('job')=='SL-13':continue
 cp=root/e['config']
 if e.get('kind')=='short' and cp.is_file():
  cv=json.loads(cp.read_text())
  if cv.get('main'):taken.add((t.local_day(cv['main']),t.local_hhmm(cv['main'])))
owned=[];configs=[];plans=[]
for m,p,film in zip(meta,picks,media):
 k=p['short'];day,hhmm=rp.next_short_slot(pday,taken,{},m['slug']);taken.add((day,hhmm));when=t.utc(day,hhmm)
 v={a:b for a,b in m.items() if a not in ('writer','validation','ai_disclosure','source','approved_media_sha256')}
 v.update(content_type='organic',source='Short-form video content/Calories Dont Matter - SL-13/Finalized R2/'+Path(film['file']).name,main=when,keyword='FOOD',kitchen=False,gym=False,parent_config=parent,film_approval_sha256=film['sha256'],approved_cover=p['pick'],setup_note='Dan approved exact R2 master and both selected cover layouts. Master unchanged; TikTok cover-first copy preserves original audio. Shared waitlist after parent release. No organic YouTube holding upload.')
 for target,kind in [('video_url','master'),('tiktok_video_url','tiktok'),('instagram_cover_url','instagram'),('youtube_cover_url','youtube')]:v[target]=uploads[k+'-'+kind]['url']
 assert_organic(v,texts=[v['title'],v['hook'],v['body'],v['close'],v['youtube_description']],sources=[v['source']])
 for ppost in post_plan(v):
  assert_video_cover({'post':{'accountId':ppost['account'],'content':{'platform':ppost['platform'],'text':ppost['text'],'mediaUrls':[ppost['media']]},'target':ppost['target']}})
  assert 'free preview' not in ppost['text'].lower() and 'free ai' not in ppost['text'].lower();assert not any(d in ppost['text'] for d in ['—','–'])
  plans.append(dict(short=k,platform=ppost['platform'],account=ppost['account'],when=when,cover_preflight=True))
 cp='scripts/blotato/configs/'+m['slug']+'.json';(root/cp).write_text(json.dumps(v,indent=2)+'\n');configs.append(cp)
 owned.append({'config':cp,'kind':'short','job':'SL-13','label':m['title'],'added':'2026-11-08','parent_config':parent,'after':parent,'kitchen':False,'gym':False,'filming_set':'studio, with existing real stock cutaways','planned':str(day)+' '+hhmm,'note':'All media and exact selected covers approved and backed up. Four uploaded platform assets per Short SHA256 verified. Keep after parent; shared daily top-up only.'})
 assert datetime.date.fromisoformat(str(day))>pday
(w/'owned-waitlist-rows.json').write_text(json.dumps(owned,indent=2));(w/'planned-platforms.json').write_text(json.dumps(plans,indent=2));(w/'config-paths.json').write_text(json.dumps(configs,indent=2))
if len(items)+4<=200:raise SystemExit('Queue capacity changed: configs prepared; run maintained helper before waitlist placement.')
# Keep the existing list order, preserving every unrelated entry exactly.
existing=[e for e in wl if e.get('job')=='SL-13'];assert not existing or {e['config'] for e in existing}==set(configs)
newwl=[e for e in wl if e.get('job')!='SL-13']+owned;tmp=wp.with_suffix('.tmp');tmp.write_text(json.dumps(newwl,indent=1)+'\n');tmp.replace(wp)
check=json.loads(wp.read_text());assert [e for e in check if e.get('job')!='SL-13']==[e for e in wl if e.get('job')!='SL-13']
assert len([e for e in check if e.get('job')=='SL-13'])==3
(w/'waitlist-placement.json').write_text(json.dumps({'date':'2026-11-08','queue_count':len(items),'parent_schedule':pt[0]['id'],'parent_main':pv['main'],'entries':owned,'configs':configs,'platform_preflight':plans,'unrelated_entries_preserved':True,'state':'waitlisted, not scheduled'},indent=2))
print('3 complete configs,12 platform preflights,3 unique shared-waitlist rows read back; queue',len(items),'of200')
for e in owned:print(e['label'],e['planned'],'America/Chicago')
