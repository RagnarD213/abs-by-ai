from pathlib import Path
from datetime import datetime,date,timedelta,timezone
from zoneinfo import ZoneInfo
import sys,json,re
R=Path(__file__).resolve().parents[4];W=Path('/Volumes/Expansion/_edit_work/ds16-publish');sys.path.insert(0,str(R/'scripts/blotato'));import release_phases as rp
ct=ZoneInfo('America/Chicago');taken=set();reasons={}
def reserve(t,why):
 d=datetime.fromisoformat(t.replace('Z','+00:00')).astimezone(ct);x=(d.date(),d.strftime('%H:%M'));taken.add(x);reasons.setdefault(str(x),[]).append(why)
q=json.load(open(W/'queue-before.json'))
for x in q:reserve(x['scheduledAt'],'live')
for e in json.load(open(R/'scripts/blotato/video_waitlist.json')):
 p=R/e['config']
 if p.exists():
  v=json.load(open(p))
  if v.get('main'):reserve(v['main'],e['job'])
for line in (R/'Docs/SHORTS_RELEASE_CALENDAR.md').read_text().splitlines():
 cells=[c.strip() for c in line.split('|')]
 if len(cells)<7 or cells[4]=='OPEN':continue
 m=re.fullmatch(r'\w{3} (Oct|Nov|Dec|Jan|Feb) (\d+)',cells[1]);tm=re.fullmatch(r'(\d+) (AM|PM)',cells[3])
 if not m or not tm:continue
 mon={'Oct':10,'Nov':11,'Dec':12,'Jan':1,'Feb':2}[m[1]];day=date(2027 if mon<3 else 2026,mon,int(m[2]));hh=int(tm[1])%12+(12 if tm[2]=='PM' else 0);taken.add((day,f'{hh:02d}:00'))
# The approved Dec10 Fat Millionaire5PM exception occupies that day's evening Short slot.
if (date(2026,12,10),'17:00') in taken:taken.add((date(2026,12,10),'18:00'))
now=datetime.now(timezone.utc);start=now.astimezone(ct).date();d,t=rp.next_short_slot(start,taken,{'kitchen':False,'gym':False},'ds16-last-ten-pounds');local=datetime.combine(d,datetime.strptime(t,'%H:%M').time(),ct);out={'local':local.isoformat(),'main':local.astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'),'basis':'First dated-phase Short slot after today, preserving occupied live posts, all shared-waitlist configs, and every named dated-calendar reservation. Poolside, no kitchen or gym hold.','queue_count':len(q),'taken_slots':len(taken)}
(W/'slot.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
