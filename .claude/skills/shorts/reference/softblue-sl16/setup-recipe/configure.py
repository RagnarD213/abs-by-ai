#!/usr/bin/env python3
"""SL-16: four Blotato configs (FOOD), Facebook cover registry rows (repo + live installer), shared-waitlist entries
tied to RO-08 (after + parent_config), cover preflight on every planned post. Dates per Dan 2026-10-27 (recommended set)."""
from pathlib import Path
import json,sys,hashlib,shutil,datetime
from zoneinfo import ZoneInfo
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');S=P/'Short-form video content';R=S/'covers/review/sl16-20261027';C=S/'covers/approved-sl16';O=Path('/Volumes/Extreme/_edit_work/sl16-publish');sys.path.insert(0,str(P/'scripts/blotato'))
from danrosefit_migration import api_key,fetch_schedules
from organic_short_queue import post_plan
from cover_guard import assert_video_cover
m=json.loads((S/'fasting-SHORTS-final-manifest.json').read_text())['shorts'];cap=json.loads((R/'captions.json').read_text());up=json.loads((O/'uploads.json').read_text());picks=json.loads((C/'picks.json').read_text())['covers']
DATES={1:'2026-12-15',2:'2026-12-04',3:'2026-12-07',4:'2027-01-12'}
TITLE={1:'How To Start Fasting: Just Skip Breakfast',2:'Why Carbs Destroy Your Productivity',3:'Never Break Your Fast With Alcohol',4:'Why You Need A Simple Nutrition Plan'}
SLUG={1:'just-skip-breakfast',2:'why-carbs-destroy-your-productivity',3:'never-break-your-fast-with-alcohol',4:'why-you-need-a-simple-nutrition-plan'}
PARENT='scripts/blotato/configs/ro08-intermittent-fasting.json'
assert len(up)==16 and all(x.get('remote_hash_verified') for x in up.values())
items=fetch_schedules(api_key());(O/'live-before-configs.json').write_text(json.dumps(items,indent=1))
regadd=[];liveadd=[];entries=[];rows=[];lc=Path.home()/'.absbyai/fb-reel-covers/covers';lc.mkdir(parents=True,exist_ok=True)
for v in m:
 n=v['n'];k=f's{n}';src=S/v['file'];s=cap[k];slug=f'sl16-short{n}';cp=f'scripts/blotato/configs/{slug}-{SLUG[n]}.json';when=DATES[n]+'T15:00:00.000Z'
 assert datetime.datetime.fromisoformat(when.replace('Z','+00:00')).astimezone(ZoneInfo('America/Chicago')).hour==9
 assert not any(x['scheduledAt'][:16]==when[:16] for x in items if 'utm_medium=short' in json.dumps(x) or 'Shorts' in json.dumps(x)),('slot taken',when)
 assert not any(f'utm_content={slug}' in json.dumps(x) for x in items)
 url=lambda pl:f'https://absbyai.com/?utm_source={pl}&utm_medium=short&utm_campaign=intermittent-fasting&utm_content={slug}'
 tags=' '.join(s['tags']);lede='\n\n'.join(s[t] for t in ['hook','body','close'])
 yt=lede+'\n\nTry Abs By AI:\n'+url('youtube')+'\n\nFull video on this channel: Intermittent Fasting: The Best Way To Get Abs\n\nSome footage in this video is AI-generated and labeled on screen.'
 if n==4:yt+='\n\nPhoto of Mike Tyson: Glenn Francis, www.PacificProDigital.com (CC BY-SA 4.0)'
 yt+='\n\n'+tags.replace(' #AbsByAI','')+' #Shorts'
 credit='\n\nPhoto of Mike Tyson: Glenn Francis, www.PacificProDigital.com (CC BY-SA 4.0)' if n==4 else ''
 c={'content_type':'organic','source':str(src.relative_to(P)),'slug':slug,'campaign':'intermittent-fasting','title':TITLE[n],
  'video_url':up[k+'-master']['url'],'tiktok_video_url':up[k+'-tiktok']['url'],'instagram_cover_url':up[k+'-instagram']['url'],'youtube_cover_url':up[k+'-youtube']['url'],
  'main':when,'keyword':'FOOD','ai_generated':True,'hook':s['hook'],'body':s['body'],'close':s['close'],'tags':tags,'youtube_description':yt,'pinned_comment':s['pinned_comment'],
  'instagram_first_comment':'Try Abs By AI: '+url('instagram'),
  'caption_overrides':{'facebook':lede+'\n\nTry Abs By AI:\n'+url('facebook')+credit+'\n\n'+tags,'instagram':lede+"\n\nComment FOOD and I'll send you the Abs By AI link."+credit+'\n\n'+tags,'tiktok':lede+'\n\nAbs By AI, link in bio.\n'+url('tiktok')+credit+'\n\n'+tags},
  'parent_config':PARENT,'approved_cover':picks[src.stem]['pick'],'approval_date':'2026-10-27',
  'media_sha256':{f:up[k+'-'+u]['sha256'] for f,u in [('master','master'),('tiktok','tiktok'),('ig','instagram'),('yt','youtube')]}}
 assert not any(ch in json.dumps(c,ensure_ascii=False) for ch in ['—','–']);assert len(c['pinned_comment'])<180
 dest=P/cp;assert not dest.exists() or json.loads(dest.read_text())==c,str(dest);dest.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
 fbrel=f'scripts/blotato/fb_covers/{slug}-approved.png';fb=P/fbrel;fb.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(picks[src.stem]['instagram'],fb)
 assert hashlib.sha256(fb.read_bytes()).hexdigest()==up[k+'-instagram']['sha256'];lf=lc/fb.name;shutil.copy2(fb,lf)
 regadd.append({'job':f'SL-16 short {n}','when':when,'match':s['hook'],'cover':str(fb),'w':1080,'h':1920,'approved':f"{picks[src.stem]['pick']}, Dan 2026-10-27",'sha256':up[k+'-instagram']['sha256']});liveadd.append({**regadd[-1],'cover':str(lf)})
 entries.append({'config':cp,'kind':'short','job':f'SL-16 short {n}','label':TITLE[n],'added':'2026-10-27','parent_config':PARENT,'after':PARENT})
 rows.append({'short':n,'config':cp,'title':TITLE[n],'main':when,'planned_destinations':post_plan(c)})
rp=P/'scripts/blotato/fb_reel_covers.json';reg=json.loads(rp.read_text());reg.extend(z for z in regadd if not any(x['match']==z['match'] for x in reg));rp.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n')
lp=Path.home()/'.absbyai/fb-reel-covers/fb_reel_covers.json';lr=json.loads(lp.read_text());lr.extend(z for z in liveadd if not any(x['match']==z['match'] for x in lr));lp.write_text(json.dumps(lr,indent=2,ensure_ascii=False)+'\n')
wp=P/'scripts/blotato/video_waitlist.json';wl=json.loads(wp.read_text());wl.extend(z for z in entries if not any(x['config']==z['config'] for x in wl));wp.write_text(json.dumps(wl,indent=1,ensure_ascii=False)+'\n')
for row in rows:
 c=json.loads((P/row['config']).read_text())
 for p in post_plan(c):assert_video_cover({'post':{'accountId':p['account'],'content':{'platform':p['platform'],'text':p['text'],'mediaUrls':[p['media']]},'target':p['target']}})
(O/'prepared-post-plans.json').write_text(json.dumps({'queue_count':len(items),'free_slots':200-len(items),'state':'shared_waitlist','entries':entries,'rows':rows},indent=2,default=str));print('4 configs, 16 cover preflights passed, waitlist entries added. Queue:',len(items))
