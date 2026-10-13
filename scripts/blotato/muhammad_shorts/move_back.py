#!/usr/bin/env python3
"""Move our other queued Shorts back behind the eight Muhammad dedicated Shorts (Dan, 2026-10-13).
Time-only change, in place (PATCH /schedules/{id} {"patch": {"scheduledTime": ...}}): ids, captions, media and covers
are untouched. All four platforms of a Short move together; order among the moved Shorts is kept.

    python3 scripts/blotato/muhammad_shorts/move_back.py            # dry run
    python3 scripts/blotato/muhammad_shorts/move_back.py --apply
"""
import json,os,sys,collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from danrosefit_migration import api_key,call,fetch_schedules
PLAN=[('sl04-short4','2026-11-03'),('sl05-short1','2026-11-05'),('sl05-short4','2026-11-07'),('sl05-short2','2026-11-10'),('sl05-short5','2026-11-12'),('sl05-short3','2026-11-14'),
      ('sl03-short1','2026-11-17'),('sl03-short4','2026-11-19'),('sl03-short5','2026-11-21'),('sl03-short2','2026-11-24'),('sl03-short3','2026-11-26'),('sl03-short6','2026-11-28')]
T=lambda d:d+'T15:00:00.000Z'   # 9 AM Central after Nov 1 (CST)
acct=lambda i:str(i.get('accountId') or i.get('draft',{}).get('accountId'))
def find(items,slug):return [i for i in items if f'utm_content={slug}"' in json.dumps(i).replace('\\n','"').replace('&','"') or f'utm_content={slug}\\n' in json.dumps(i) or json.dumps(i).count(f'utm_content={slug}')>0 and f'utm_content={slug}0' not in json.dumps(i)]
def main():
    apply='--apply' in sys.argv;key=api_key();items=fetch_schedules(key);moving={}
    for slug,day in PLAN:
        m=[i for i in find(items,slug) if 'utm_medium=short' in json.dumps(i)]
        assert len(m)==4 and len({acct(i) for i in m})==4,(slug,len(m))
        for i in m:moving[i['id']]=(slug,T(day),i)
    stay=collections.defaultdict(set)
    for i in items:
        if i['id'] not in moving:stay[acct(i)].add(i['scheduledAt'][:16])
    clash=[(s,t) for _,(s,t,i) in moving.items() if t[:16] in stay[acct(i)]]
    assert not clash,clash
    for sid,(slug,t,i) in sorted(moving.items(),key=lambda x:(x[1][1],x[0])):
        if i['scheduledAt'][:16]==t[:16]:print('  at target',slug,sid);continue
        print(f"  {'move' if apply else 'would move'} {slug:12} {i['draft']['content']['platform']:9} {sid} {i['scheduledAt'][:16]} -> {t[:16]}")
        if apply:call('PATCH',f'/schedules/{sid}',key,{'patch':{'scheduledTime':t}})
    if not apply:print('dry run');return 0
    after={i['id']:i for i in fetch_schedules(key)};bad=0
    for sid,(slug,t,i) in moving.items():
        a=after.get(sid);ok=bool(a) and a['scheduledAt'][:16]==t[:16] and a['draft']==i['draft'];bad+=0 if ok else 1
        if not ok:print('  FAIL',slug,sid,a and a['scheduledAt'])
    print(f'verified {len(moving)-bad} of {len(moving)} moves on a fresh pull; queue {len(after)}');return 1 if bad else 0
if __name__=='__main__':sys.exit(main())
