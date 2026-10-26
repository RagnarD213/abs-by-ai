from pathlib import Path
import sys,json,os
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod complete speech and corrected caption metadata measurement',pool='heavy')
sys.path.insert(0,str(R/'.claude/skills'));from _shared.deliver import gate as G
for v in sys.argv[1:]:
 q=W/'qa'/v;vid=W/'review/media'/('dad-bod-r2-'+v+'.mp4')
 for name,plan,rows in [('full-speech-junk','full-speech-plan.json',{'junk:repeated_take','junk:dead_air'}),('corrected-caption-sync','plan.json',{'captions:sync'})]:
  p=q/(name+'.json')
  if p.exists():continue
  pr,pp,rr=G.run(str(vid),'short',str(q/plan),rows)
  rec=dict(video_sha256=G.C.sha256(str(vid)),gate_version=G.GATE_VERSION,scope='Supplemental raw shared-row measurements on exact complete film; not a delivery stamp.',plan=plan,rows=[dict(key=r.key,ok=r.ok,detail=r.detail,value=r.value) for r in rr])
  p.write_text(json.dumps(rec,indent=1));print(v,name,[(r.key,r.ok,r.detail) for r in rr],flush=True)
