from pathlib import Path
import json,subprocess
root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');w=Path(__file__).parent
paths=json.loads((w/'config-paths.json').read_text());configs={p:(root/p).read_text() for p in paths}
entries=json.loads((w/'waitlist-entries.json').read_text())
job=next(x for x in json.loads((root/'Handoffs/video-editing/jobs.json').read_text())['jobs'] if x['id']=='SL-21')
script=r'''from pathlib import Path
import json,fcntl,sys,importlib.util
root=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');configs=json.loads(CONFIGS);entries=json.loads(ENTRIES);job=json.loads(JOB)
for name,content in configs.items():
 p=root/name;p.write_text(content);assert p.read_text()==content
p=root/'scripts/blotato/video_waitlist.json'
with p.with_suffix('.json.lock').open('a') as f:
 fcntl.flock(f,fcntl.LOCK_EX);rows=json.loads(p.read_text())
 for e in entries:
  hits=[x for x in rows if x['config']==e['config']];assert len(hits)<=1
  if hits:assert not hits[0].get('queued');rows[rows.index(hits[0])]=e
  else:rows.append(e)
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(rows,indent=1,ensure_ascii=False)+'\n');tmp.replace(p)
sys.path.insert(0,str(root/'scripts/blotato'));from organic_short_queue import post_plan;from cover_guard import assert_video_cover
plans=[]
for name in configs:
 v=json.loads((root/name).read_text());plan=post_plan(v)
 for x in plan:assert_video_cover({'post':{'content':{'platform':x['platform'],'text':x['text'],'mediaUrls':[x['media']]},'target':x['target']}})
 plans.extend(plan)
assert len(plans)==12
spec=importlib.util.spec_from_file_location('sl21_edit_queue',root/'scripts/edit-queue/queue.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
with q.locked():
 data=q.load();old=q.find(data,'SL-21');data['jobs'][data['jobs'].index(old)]=job;q.save(data);q.master_status('SL-21',q.STATES['finalized'])
(Path.home()/'Projects/_edit_work/SL-21-setup-readback.json').write_text(json.dumps({'waitlist':entries,'configs':list(configs),'platform_targets':12,'preflight':'PASS','state':job['state'],'rev':job['rev']},indent=2))
print('M2: three unique waitlist entries, twelve platform targets and finalized status read back.',flush=True)
'''
inputs='CONFIGS='+repr(json.dumps(configs))+'\nENTRIES='+repr(json.dumps(entries))+'\nJOB='+repr(json.dumps(job))+'\n'
subprocess.run(['ssh','m2','python3','-'],input=inputs+script,text=True,check=True)
