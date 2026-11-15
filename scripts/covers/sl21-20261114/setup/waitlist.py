from pathlib import Path
import json,fcntl,sys
ROOT=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');w=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts/blotato'));from danrosefit_migration import api_key,fetch_schedules
items=fetch_schedules(api_key());assert len(items)>196,'Queue now has room for a full Short; reassess before waitlisting'
assert not any('utm_content=sl21-short' in json.dumps(i) for i in items),'Existing SL21 schedule: resume rather than duplicate'
paths=json.loads((w/'config-paths.json').read_text());slots=json.loads((w/'slots.json').read_text())
parent='scripts/blotato/configs/ro20b-what-to-cut.json'
entries=[]
for path,slot in zip(paths,slots):
 v=json.loads((ROOT/path).read_text())
 entries.append({'config':path,'kind':'short','job':'SL-21','label':v['title'],'added':'2026-11-15','kitchen':True,'gym':False,'filming_set':'kitchen (Aug 3)','planned':slot['planned_central'],'after':parent,'parent_config':parent,'note':'All three films and exact covers approved. Setup complete: project/Extreme/public Drive backups and all uploaded bytes verified; TikTok native pictures/audio preserved, cover-first checked; four-platform preflight passed. Ready for shared top-up in order after parent. February 8/10/12 at 9AM Central plans, not live schedules. Receipt Docs/SL21_SETUP_RECEIPT_20261115.md.'})
p=ROOT/'scripts/blotato/video_waitlist.json'
with p.with_suffix('.json.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX);rows=json.loads(p.read_text())
 for e in entries:
  hits=[r for r in rows if r['config']==e['config']]
  assert len(hits)<=1
  if hits:assert not hits[0].get('queued');rows[rows.index(hits[0])]=e
  else:rows.append(e)
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(rows,indent=1,ensure_ascii=False)+'\n');tmp.replace(p)
saved=json.loads(p.read_text());readback=[e for e in saved if e['config'] in paths]
assert readback==entries
(w/'waitlist-entries.json').write_text(json.dumps(entries,indent=2))
(w/'waitlist-readback.json').write_text(json.dumps({'queue_count':len(items),'live_sl21_schedule_count':0,'status':'shared waitlist, no live schedules','entries':readback,'all_four_platform_targets_ready':True},indent=2))
print('Three unique entries read back from shared waitlist. Blotato',len(items),'/200; zero live SL21 schedules.',flush=True)
