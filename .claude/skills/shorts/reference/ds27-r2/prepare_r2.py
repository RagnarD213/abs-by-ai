from pathlib import Path
import json,hashlib,shutil,sys,os
import numpy as np
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
W=Path(__file__).resolve().parents[1];P=W.parent/'round1'
owner='01a19c79-c752-7650-93fe-698ca23fdc69'
j=json.loads((W/'round-controller.json').read_text())
assert j['productionOwner']==owner and j['phase']=='complete'
decision=json.loads((W/'decisions.json').read_text())
e=W/'execution.json'
if e.exists():
 d=json.loads(e.read_text());assert d['revision_id']==decision['owner_message_id']
 assert d['status']!='delivered','Already delivered; do not execute revision again'
else:
 checks=[]
 for a in j['plan']['approvedFiles']:
  h=hashlib.sha256(Path(a['path']).read_bytes()).hexdigest();assert h==a['sha256'],a['path'];checks.append(a)
 e.write_text(json.dumps(dict(revision_id=decision['owner_message_id'],round_key='DS-27:R2',owner=owner,status='in_progress',checkpoint='approved locks verified; R2 preparation',approved_manifest=checks,approved_decisions_sha256=hashlib.sha256((W/'decisions.json').read_bytes()).hexdigest(),new_spend_usd=0),indent=2))
for d in ['recipe','build','review','evidence','hf','measurements']:(W/d).mkdir(exist_ok=True)
for n in ['source.json','edl.json','grades.json','broll-plan.json','media-plates.json','asset-events.json','captions.ass','words_out.json','plan_resolved.json','graphics-sheet.json']:
 if not (W/n).exists():shutil.copy2(P/n,W/n)
if not (W/'untreated-cut.wav').exists():shutil.copy2(P/'untreated-cut.wav',W/'untreated-cut.wav')
shutil.copy2(P/'hf/manifest.json',W/'hf/manifest.json')
shutil.copy2(P/'measurements/head-samples.json',W/'measurements/head-samples.json')
sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import landing as L
shots=json.loads((P/'shots.json').read_text());rows=json.loads((P/'measurements/head-samples.json').read_text());stats=[]
# Keep the approved two-size editing grammar. Remove excessive empty headroom in FAR.
# All near shots retain their approved width. Source-calibrate the vertical anchor per hold.
for s in shots:
 if s['kind']=='equipment':continue
 if s['id']=='T09':s['n1']=1581 # continuous FAR into shorter approved AI clip
 if s['id']=='T10':s['src']+=(1656-s['n0'])/(30000/1001);s['n0']=1656
 if s['id']=='T10':
  anchor=json.load(open(W/'measurements/T10-R2-anchor.json'));s['anchor_head_x']=anchor['head_x'];s['anchor_hair_y']=anchor['hair_y']
 cw,ch=(1350,2400) if s['kind']=='wide' else (1120,1990)
 v=[r for r in rows if r['valid'] and s['src']<=r['t']<s['src']+(s['n1']-s['n0'])/(30000/1001)]
 assert v
 cy=int((min(r['hair_y'] for r in v)-.04*ch)//2*2)
 nr=[s['n0']];xr=[s['anchor_head_x']]
 for r in v:
  n=s['n0']+round((r['t']-s['src'])*(30000/1001))
  if s['n0']<n<s['n1']:nr.append(n);xr.append(r['head_x'])
 dn,centres,heads,info=L.vertical_dense(nr,xr,[s],cw,30000/1001);left=centres-cw/2
 assert min(left)>=0 and max(left)<=2160-cw
 s['crop']=[cw,ch,cy];s['tracking']=[[int(n),round(float(x),3)] for n,x in zip(dn,left)]
 stats.append(dict(id=s['id'],stats=L.motion_stats(dn,heads,centres,[s],cw,30000/1001),pixel_space='native 2160x3840 source',minimum_sampled_clearance=min((r['hair_y']-cy)/ch*1920 for r in v)))
(W/'shots.json').write_text(json.dumps(shots,indent=2));(W/'motion-stats.json').write_text(json.dumps(stats,indent=2))
events=json.loads((P/'asset-events.json').read_text())
for a in events:
 if a['id']=='A0157':a.update(a=1581,b=1656) # 75 frames, source 0 through 2.47 s, avoiding source-end clipped hair
(W/'asset-events.json').write_text(json.dumps(events,indent=2))
chunks=json.loads((P/'caption-chunks.json').read_text());origin=1467/(30000/1001)
old=[c for c in chunks if c[-1]['t1']<=origin+.02]
local=json.loads((P/'caption-overrides/Daily-workouts-context.json').read_text())['chunks']
new=[[dict(w=v['w'],t0=v['t0']+origin,t1=v['t1']+origin) for v in c] for c in local]
chunks=old+new
for a,b in zip(chunks,chunks[1:]):assert a[0]['t0']<b[0]['t0']
(W/'caption-chunks.json').write_text(json.dumps(chunks,indent=2))
(W/'words_out.json').write_text(json.dumps([v for c in chunks for v in c],indent=2))
print('R2 PREPARED: immutable approval packet retained; tighter FAR; shorter AI; corrected caption tail',flush=True)
