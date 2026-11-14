#!/usr/bin/env python3
"""Authorized client smoke test. All five state directories and ownership statuses are private fixtures.
No media, production jobs, real claims, running editors or dispatcher settings are changed.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
SHARED=HERE.parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--client',required=True);p.add_argument('--physical-host',required=True)
    a=p.parse_args();root=Path(tempfile.mkdtemp(prefix='priority-client-'+a.client+'-'))
    cfg=json.loads((HERE/'hosts.json').read_text())
    statuses={h:dict(host=h,reachable=True,editcap=dict(cap=cfg['hosts'][h]['slots'],in_use=[],waiting=[],edits={}),
                    drives=[dict(drive='internal',free_gb=500)],job=dict(folders=[])) for h in cfg['hosts']}
    (root/'statuses.json').write_text(json.dumps(statuses));(root/'hosts.json').write_text(json.dumps(cfg))
    env=dict(os.environ,EDIT_PRIORITY_DIR=str(root/'policy'),EDIT_STORAGE_DIR=str(root/'storage'),
             EDITROUTE_DIR=str(root/'route'),EDITCAP_DIR=str(root/'cap'),GATE_DIR=str(root/'rq'),
             EDITROUTE_FIXTURE_STATUS=str(root/'statuses.json'),EDITROUTE_HOSTS=str(root/'hosts.json'),
             EDITROUTE_HOST='m6',EDITCAP_MAX='2',EDITCAP_FAIRNESS='1',GATE_FAIRNESS='1',GATE_BORROWING='1',
             EDIT_PRIORITY_FIXTURE='1',GATE_BUDGET='6',GATE_MEM='20,0',GATE_UNMANAGED='0',GATE_HEADROOM_S='0',GATE_SETTLE='0',
             GATE_POOLS='heavy=1:1,light=1:1,quick=1:1')
    for k in ('GATE_HELD','GATE_OFF'):env.pop(k,None)
    events=[]
    def run(file,*args,code=0):
        cmd=[sys.executable,str(file)]+list(args);t=time.monotonic()
        r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=20)
        events.append(dict(argv=cmd,code=r.returncode,seconds=round(time.monotonic()-t,3),output=r.stdout[-1800:]))
        if r.returncode!=code:raise RuntimeError(str((cmd,r.returncode,r.stdout,r.stderr)))
        return r
    cap=SHARED/'editcap/editcap.py';control=HERE/'priority.py';rq=SHARED/'renderq/renderq.py'
    for job in ('DS-901','DS-902'):run(cap,'acquire',job,'--title','Disposable fixture')
    run(cap,'acquire','DS-903',code=3);run(control,'set','DS-904');run(cap,'acquire','DS-904','--priority',code=3)
    run(cap,'release','DS-901');reg=json.loads((root/'cap/registry.json').read_text())
    assert reg['edits']['DS-904']['state']=='promoted' and reg['edits']['DS-903']['state']=='waiting'
    run(cap,'release','DS-904');run(cap,'release','DS-902');run(cap,'release','DS-903')
    for job in ('DS-911','DS-912'):run(cap,'acquire',job)
    # One real sleeping step is a running checkpoint. Reserve while it is alive.
    worker=subprocess.Popen([sys.executable,str(rq),'run','--group','DS-911','--',sys.executable,'-c',
                            'import time;time.sleep(.8)'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    deadline=time.monotonic()+5
    while not any(json.loads(f.read_text()).get('group')=='DS-911' for f in (root/'rq/slots').glob('*.json')):
        if time.monotonic()>deadline:raise RuntimeError('fixture holder did not start')
        time.sleep(.02)
    run(control,'reserve','DS-913','--milestone','checked-preview','--minutes','2','--owner-pid',str(os.getpid()))
    reg=json.loads((root/'cap/registry.json').read_text());assert reg['edits']['DS-911']['state']=='active'
    assert reg['edits']['DS-912']['state']=='parked'
    run(cap,'acquire','DS-913');worker.communicate(timeout=5);assert worker.returncode==0
    # M2 uses another queue and remains eligible while the M6 reservation is active.
    other=dict(env,EDITROUTE_HOST='m2',GATE_DIR=str(root/'m2-rq'),EDITCAP_DIR=str(root/'m2-cap'),GATE_BUDGET='8')
    r=subprocess.run([sys.executable,str(rq),'run','--group','DS-921','--',sys.executable,'-c','print("M2_PROGRESS")'],env=other,capture_output=True,text=True,timeout=10)
    assert r.returncode==0 and 'M2_PROGRESS' in r.stdout
    run(rq,'run','--group','DS-913','--',sys.executable,'-c','print("CHECKED_FIXTURE_READY")')
    run(control,'milestone','DS-913','checked-preview');run(cap,'release','DS-913','--review')
    for job in ('DS-911','DS-912'):run(cap,'acquire',job)
    reg=json.loads((root/'cap/registry.json').read_text());assert all(reg['edits'][j]['state']=='active' for j in ('DS-911','DS-912'))
    for mode in ('cancel','crash','expiry'):
        run(control,'reserve','DS-913','--owner-pid',str(os.getpid()))
        if mode=='cancel':run(control,'release','DS-913','--reason','fixture cancellation')
        else:
            x=json.loads((root/'policy/priority.json').read_text())
            if mode=='crash':x['reservation']['owner_start']='stale reused owner PID'
            else:x['reservation']['expires']=time.time()-1
            (root/'policy/priority.json').write_text(json.dumps(x))
        run(cap,'acquire','DS-911');run(cap,'acquire','DS-912')
    result=dict(client=a.client,physical_host=a.physical_host,fixture=str(root),ordinary_priority='PASS',
                dedicated_m6='PASS',running_checkpoint='PASS',saved_owners_restored='PASS',
                independent_m2_policy='PASS',milestone_cancel_expiry_crash='PASS',events=events)
    (root/'receipt.json').write_text(json.dumps(result,indent=1))
    print(json.dumps({k:v for k,v in result.items() if k!='events'},indent=1))
    return 0

if __name__=='__main__':raise SystemExit(main())
