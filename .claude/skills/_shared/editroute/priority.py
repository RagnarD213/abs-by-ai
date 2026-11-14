#!/usr/bin/env python3
"""Job-wide priority and temporary dedicated-M6 control, consumed by the existing queues.

priority.py set JOB | reserve JOB [--milestone TEXT] [--minutes 120]
priority.py renew JOB | release JOB [--reason TEXT] | milestone JOB TEXT | status
Control records are durable; no process is killed or suspended. A reservation blocks NEW
M6 grants. Existing holders run to exit; editcap parks only after their last holder exits.
"""
import argparse
import contextlib
import fcntl
import json
import os
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = 1


def job_id(value):
    s = str(value or '').strip()
    if s.lower().startswith('work:'):
        s = s[5:]
    m = re.match(r'^([A-Za-z]{2,3})-?(\d{1,3}[A-Za-z]?)(?!\d)', s)
    if m and not s.upper().startswith('SHOOT-'):
        return m[1].upper() + '-' + m[2].upper()
    return s.upper()  # grouping only; output paths/arm identities are never rewritten


def state_dir():
    return Path(os.environ.get('EDIT_PRIORITY_DIR') or os.environ.get('EDITROUTE_DIR') or Path.home()/'.absbyai-editroute')


@contextlib.contextmanager
def locked():
    d = state_dir(); d.mkdir(parents=True, exist_ok=True)
    with (d/'priority.lock').open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield d


def read():
    p = state_dir()/'priority.json'
    try:
        x = json.loads(p.read_text())
        if not isinstance(x.get('jobs'), dict):
            raise ValueError('invalid priority record')
        return x
    except FileNotFoundError:
        return {'version': VERSION, 'jobs': {}, 'reservation': None, 'events': []}


def save(x):
    p = state_dir()/'priority.json'; p.parent.mkdir(parents=True, exist_ok=True)
    x['events'] = x.get('events', [])[-100:]
    tmp = p.with_name('priority.%s.tmp'%os.getpid())
    with tmp.open('w') as f:
        json.dump(x, f, indent=1); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, p)


def pid_identity(pid):
    try:
        r = subprocess.run(['ps','-p',str(int(pid)),'-o','lstart='],capture_output=True,text=True,timeout=2)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def snapshot(now=None):
    x = read(); r = x.get('reservation'); now = time.time() if now is None else now
    if r and (r['expires'] <= now or (r.get('owner_pid') and pid_identity(r['owner_pid']) != r.get('owner_start'))):
        x['reservation'] = None
    x['jobs'] = {j:v for j,v in x['jobs'].items() if v.get('expires',0)>now}
    return x


def current(host=None):
    if host is None:
        import hostcfg
        host = hostcfg.this_host()
    try:return snapshot().get('reservation') if host == 'm6' else None
    except (ValueError,OSError):return {'job':'_CONTROL_UNREADABLE_','milestone':'repair controls'} if host=='m6' else None


def urgent(job):
    try:return job_id(job) in snapshot()['jobs']
    except (ValueError,OSError):return False


def blocked(job, host=None):
    r = current(host)
    return bool(r and r['job'] != job_id(job))


def update(action, job, milestone='checked-preview', minutes=120, reason='', owner_pid=None):
    job = job_id(job)
    if minutes <= 0 or minutes > 24*60:
        raise ValueError('minutes must be >0 and <=1440')
    with locked():
        x = snapshot(); r = x.get('reservation'); now = time.time()
        if action in ('set','reserve','renew'):
            x['jobs'][job] = {'expires':now+minutes*60, 'set':now}
        if action == 'reserve':
            import hostcfg
            if hostcfg.this_host() != 'm6':
                raise ValueError('reserve must run on M6 after verifying existing ownership')
            if r and r['job'] != job:
                raise ValueError('M6 already reserved for '+r['job'])
            if owner_pid and not pid_identity(owner_pid):
                raise ValueError('owner PID is not alive')
            x['reservation'] = dict(job=job, milestone=milestone, since=now, expires=now+minutes*60,
                owner_pid=owner_pid, owner_start=pid_identity(owner_pid) if owner_pid else None,
                owner=os.environ.get('CODEX_THREAD_ID') or os.environ.get('CLAUDE_CODE_SESSION_ID') or 'cli')
        elif action == 'renew':
            if not r or r['job'] != job:
                raise ValueError('no live reservation for '+job)
            r['expires'] = now+minutes*60
        elif action in ('release','milestone'):
            if r and r['job'] == job and (action=='release' or milestone==r['milestone']):
                x['reservation'] = None
            if action == 'release' or not x.get('reservation'):
                x['jobs'].pop(job,None)
        x.setdefault('events',[]).append(dict(t=now,action=action,job=job,reason=reason,milestone=milestone))
        save(x)
        return x


def legacy_cap_waiters():
    path=Path(os.environ.get('EDITCAP_DIR') or '/tmp/absbyai-editcap')/'registry.json'
    try:reg=json.loads(path.read_text())
    except FileNotFoundError:return []
    old=[]
    for e in reg.get('edits',{}).values():
        pid=e.get('waiter_pid')
        if not pid or e.get('waiter_scheduler_version',0)>=5:continue
        identity=pid_identity(pid)
        if not identity or (e.get('waiter_start') and e['waiter_start']!=identity):continue
        r=subprocess.run(['ps','-p',str(pid),'-o','args='],capture_output=True,text=True,timeout=2)
        if r.returncode==0 and 'editcap.py' in r.stdout and ' wait ' in r.stdout and e['job'] in r.stdout:
            old.append(dict(job=e['job'],pid=pid,start=identity))
    return old


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['set','reserve','renew','release','milestone','status','activate','deactivate'])
    p.add_argument('job',nargs='?');p.add_argument('target',nargs='?')
    p.add_argument('--milestone',default='checked-preview');p.add_argument('--minutes',type=float,default=120)
    p.add_argument('--reason',default='');p.add_argument('--owner-pid',type=int)
    a=p.parse_args(argv)
    if os.environ.get('EDIT_PRIORITY_FIXTURE')=='1' and not all(os.environ.get(k) for k in ('GATE_DIR','EDITCAP_DIR','EDITROUTE_DIR','EDIT_PRIORITY_DIR','EDIT_STORAGE_DIR')):
        p.error('fixture mode requires all five isolated state directories')
    if a.action=='status':
        print(json.dumps(snapshot(),indent=1));return 0
    import sys
    sys.path.insert(0,str(HERE.parent/'renderq'))
    import renderq
    if a.action in ('activate','deactivate'):
        renderq._ensure()
        with renderq._mutex():
            states=renderq.slot_states();tickets=renderq._tickets()
            old=[s['info'] for s in states if s['held'] and s['info'].get('scheduler_version',0)<5]
            old += [t for t in tickets if t.get('scheduler_version',0)<5]
            old += legacy_cap_waiters()
            if old and a.action=='activate':
                print('WAIT: old render holders/tickets or whole-edit waiters must drain naturally before activating priority/fairness.');return 3
            enabled=a.action=='activate'
            renderq._write(renderq.DIR/'features.json',dict(fairness=enabled,borrowing=enabled,priority=enabled))
        cap_dir=Path(os.environ.get('EDITCAP_DIR') or '/tmp/absbyai-editcap');cap_dir.mkdir(parents=True,exist_ok=True)
        flag=cap_dir/'fairness.enabled'
        if enabled:flag.touch()
        elif flag.exists():flag.unlink()
        if not enabled:
            r=current()
            if r:update('release',r['job'],reason='scoped rollback')
        print('scheduler features '+('enabled' if enabled else 'disabled'));return 0
    if a.action in ('set','reserve') and not (renderq.feature('priority') or os.environ.get('EDIT_PRIORITY_FIXTURE')=='1'):
        print('WAIT: priority rollout has not reached its safe activation boundary. No reservation created.');return 3
    if a.action in ('set','reserve') and legacy_cap_waiters():
        print('WAIT: old whole-edit waiters are still alive. No priority control changed.');return 3
    if not a.job:p.error('JOB required')
    if a.action=='reserve':
        import resume
        owner=resume.locate(a.job)
        if owner['state']=='unresolved':print(owner['reason']);return 6
        if owner.get('host') and owner['host']!='m6':
            print('Existing edit belongs on '+owner['host']+'; inspect its stage and moving cost before requesting a move.');return 5
    x=update(a.action,a.job,a.target or a.milestone,a.minutes,a.reason,a.owner_pid)
    # Settling uses the same editcap lock as all ordinary admission. No extra scheduler.
    import sys
    sys.path.insert(0,str(HERE.parent/'editcap'))
    import editcap
    with editcap._locked():
        reg=editcap.settle(editcap._load(),*editcap._context())
        editcap._save(reg)
    print(json.dumps(x,indent=1));return 0


if __name__=='__main__':
    try: raise SystemExit(main())
    except (ValueError,OSError) as e: raise SystemExit(str(e))
