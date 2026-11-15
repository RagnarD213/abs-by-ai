#!/usr/bin/env python3
"""Explicit named rounds, pulled by each Mac from one locked M2 ledger. Disabled on install."""
import argparse
import base64
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eq_common as eq
eq.unshadow()
sys.path.insert(0, str(Path(eq.ROOT)/'.claude/skills/_shared/editroute'))
import hostcfg

HOME = Path(os.environ.get('EDIT_BATCH_HOME') or Path.home()/'.absbyai-batch')
SHARED = Path(eq.ROOT)/'.claude/skills/_shared'
SOURCE_ROOTS = ['.claude/skills/_shared/'+n for n in ('editroute','editcap','renderq')] + ['scripts/edit-queue','scripts/edit-dashboard']
TERMINAL = {'delivered','delivered-unreviewed','needs-dan','blocked','taken-over'}
NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,95}$')
JOB = re.compile(r'^[A-Z]{2,8}-[A-Z0-9-]+$')
HEARTBEAT_S = 60
STALE_S = 600


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def write(path, doc):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    with tmp.open('w') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(str(path.parent), os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def checked_name(name):
    if not NAME.fullmatch(name): raise ValueError('invalid batch name')
    return name


def here():
    h = hostcfg.this_host()
    if h not in ('m2','m6'): raise RuntimeError('unknown Mac')
    return h


def remote(host, args, payload=None, timeout=25):
    hc = hostcfg.host(host)
    command = 'cd '+shlex.quote(hc['repo'])+' && python3 -B scripts/edit-queue/batch.py '+shlex.join(args)
    run = subprocess.run(['ssh','-oBatchMode=yes','-oConnectTimeout=3',hc.get('ssh',host),command],
                         input=json.dumps(payload) if payload is not None else None,
                         capture_output=True, text=True, timeout=timeout)
    if run.returncode: raise RuntimeError(host+': '+(run.stderr or run.stdout)[-1000:])
    return json.loads(run.stdout)


def rpc(op, **values):
    request = dict(op=op, **values)
    return handle(request) if here()=='m2' else remote('m2',['_rpc'],request)


@contextlib.contextmanager
def locked():
    HOME.mkdir(parents=True, exist_ok=True)
    with (HOME/'ledger.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def batches():
    return sorted(p.parent for p in HOME.glob('*/manifest.json'))


def control():
    return read(HOME/'control.json', {'enabled':False})


def key(job): return job['id']+'-R'+str(job['round'])


def load_batch(name):
    p = HOME/checked_name(name)
    return p, read(p/'manifest.json'), read(p/'state.json')


def snapshot():
    result = dict(control=control(), batches={})
    for p in batches():
        manifest=read(p/'manifest.json'); state=read(p/'state.json')
        if not manifest or not state: raise RuntimeError('incomplete ledger: '+p.name)
        result['batches'][p.name] = dict(manifest=manifest, **state)
    return result


def finish(row, outcome):
    status=outcome.get('status')
    if status not in TERMINAL: raise ValueError('invalid terminal outcome')
    if status in ('blocked','delivered-unreviewed') and not outcome.get('reason'):
        raise ValueError('outcome needs reason')
    if status=='blocked' and not outcome.get('next_action'): raise ValueError('blocked needs next action')
    if status=='needs-dan' and not (outcome.get('question') and outcome.get('link')):
        raise ValueError('needs Dan requires a question and review link')
    row.update(status=status, outcome=outcome, ended=time.time())
    row.pop('claim',None)


def handle(req):
    """The only ledger writer. Every mutation, including stop/claim, uses this single flock."""
    with locked():
        op=req['op']; now=time.time()
        if op=='snapshot': return snapshot()
        if op=='stop':
            c=control(); c.update(enabled=False,stopped=now);write(HOME/'control.json',c);return c
        if op=='preflight':
            c=control();c['preflight']=req['proof'];write(HOME/'control.json',c);return c
        if op=='enqueue':
            name=checked_name(req['batch']);p=HOME/name
            if (p/'manifest.json').exists():
                old=read(p/'manifest.json')
                if old['jobs']!=req['jobs']:raise ValueError('batch name already used with different jobs')
                return dict(registered=True,batch=name,duplicate=True)
            all_rows=[r for d in snapshot()['batches'].values() for r in d['jobs'].values()]
            for job in req['jobs']:
                for prior in all_rows:
                    if prior['id']==job['id'] and prior['status'] not in TERMINAL:
                        raise ValueError(job['id']+' has a nonterminal round; finish or take it over first')
                for sibling in req['jobs']:
                    if sibling is not job and sibling['id']==job['id']:
                        raise ValueError('only one round of a job per batch')
            p.mkdir(parents=True,exist_ok=True); rows={}
            for job in req['jobs']:
                data=base64.b64decode(req['briefs'][key(job)],validate=True)
                dest=p/'briefs'/(key(job)+'.md');dest.parent.mkdir(exist_ok=True)
                with dest.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
                if hashlib.sha256(dest.read_bytes()).hexdigest()!=job['brief_sha256']:
                    raise ValueError('brief readback failed')
                rows[key(job)]=dict(job,status='queued',queued_at=now,attempts=0,resumes=0,allowance_tries=0,not_before=0)
            write(p/'state.json',dict(enabled=False,jobs=rows,ticks={}))
            write(p/'manifest.json',dict(schema=1,batch=name,created=now,jobs=req['jobs']))
            return dict(registered=True,batch=name)
        if op=='tick':
            for p in batches():
                state=read(p/'state.json')
                last=state['ticks'].get(req['host'],now)
                elapsed=min(180,max(0,now-last))/60
                capacity=req.get('observation',{}).get('_capacity',{})
                for row in state['jobs'].values():
                    if row['status']=='queued' and row['placement'] in ('any',req['host']) and row['not_before']<=now and capacity.get('free',0)>0:
                        row['idle_slot_minutes']=row.get('idle_slot_minutes',0)+elapsed
                state['ticks'][req['host']]=now
                state.setdefault('observations',{})[req['host']]=req.get('observation',{})
                write(p/'state.json',state)
            return snapshot()
        if op=='start':
            p,manifest,state=load_batch(req['batch'])
            if not state:raise ValueError('unknown batch')
            proof=control().get('preflight',{})
            if not proof.get('passed') or proof.get('digest')!=req['digest']:
                raise ValueError('run preflight successfully before enabling')
            state['enabled']=True;write(p/'state.json',state)
            c=control();c.update(enabled=True,started=now);write(HOME/'control.json',c);return state
        if op=='claim':
            c=control()
            if not c.get('enabled') or not c.get('preflight',{}).get('passed') or req['digest']!=c.get('preflight',{}).get('digest'):return None
            live=[]
            for d in snapshot()['batches'].values():
                live.extend(r for r in d['jobs'].values() if r['status']=='claimed' and r['claim']['owner']==req['host'])
            unregistered=sum(r['id'] not in req['occupied'] for r in live)
            full=len(req['occupied'])+unregistered>=req['slots']
            choices=[]
            for p in batches():
                state=read(p/'state.json')
                if not state['enabled']:continue
                for k,r in state['jobs'].items():
                    if r['status']=='queued' and r['not_before']<=now and r['placement'] in ('any',req['host']):
                        if r['id'] in req.get('unavailable',[]):continue
                        choices.append(({'L':0,'M':1,'S':2}[r['size']],r['order'],r['queued_at'],p,k,r))
            if full:choices=[entry for entry in choices if entry[-1]['id'] in req['occupied']]
            if not choices:return None
            _,_,_,p,k,row=min(choices,key=lambda x:x[:3])
            state=read(p/'state.json');row=state['jobs'][k]
            brief=(p/'briefs'/(k+'.md')).read_bytes()
            if hashlib.sha256(brief).hexdigest()!=row['brief_sha256']:raise ValueError('stored brief changed')
            row.update(status='claimed',attempts=row['attempts']+1)
            row['claim']=dict(token=uuid.uuid4().hex,owner=req['host'],at=now,heartbeat=now,pid=None,birth=None,phase='starting')
            row['first_started']=row.get('first_started',now)
            write(p/'state.json',state)
            brief=(p/'briefs'/(k+'.md')).read_bytes()
            if hashlib.sha256(brief).hexdigest()!=row['brief_sha256']:raise ValueError('stored brief changed')
            return dict(batch=p.name,key=k,row=row,brief=base64.b64encode(brief).decode())
        if op=='takeover':
            found=[]
            for p in batches():
                state=read(p/'state.json')
                for k,r in state['jobs'].items():
                    if r['id']==req['job'] and r['status']!='taken-over':found.append((p,k,r))
            if not found:raise ValueError('no batch job found')
            p,k,row=max(found,key=lambda x:x[2]['queued_at'])
            if row['status']=='claimed':raise ValueError('live or unconfirmed claim; takeover refused until owner confirms exit')
            state=read(p/'state.json');row=state['jobs'][k]
            result=dict(row)
            finish(row,dict(status='taken-over',reason='explicit chat takeover',by=req['host']))
            write(p/'state.json',state);return result
        p,manifest,state=load_batch(req['batch'])
        row=state['jobs'][req['key']]
        claim=row.get('claim',{})
        if row['status']!='claimed' or claim.get('token')!=req['token']:
            # Idempotent replay from an offline owner's durable outbox.
            if op=='outcome' and row.get('outcome_token')==req['token']:return row
            raise ValueError('stale claim token')
        if req.get('host') and claim['owner']!=req['host']:raise ValueError('owner mismatch')
        if op=='heartbeat':
            claim.update(req.get('fields',{}));claim['heartbeat']=now
        elif op=='outcome':
            row['outcome_token']=req['token']; row.setdefault('timing',{})
            for field,value in req.get('timing',{}).items():row['timing'][field]=row['timing'].get(field,0)+value
            outcome=req['outcome']
            if outcome['status']=='paused-for-allowance':
                row['allowance_tries']+=1
                if row['allowance_tries']<3:
                    row.update(status='queued',not_before=now+req.get('backoff_s',7200),last_pause=now,
                               placement=claim['owner'],workdir=claim.get('workdir'),resume_phase=claim.get('phase'))
                    row.setdefault('allowance_pauses',[]).append(dict(at=now,until=row['not_before']))
                    row.pop('claim',None)
                else:finish(row,dict(status='blocked',reason='allowance exhausted after three attempts',next_action='Resume after allowance is restored'))
            else:finish(row,outcome)
        elif op=='recover':
            if req['pid_alive'] or req.get('session_alive'):return row
            if now-claim['heartbeat']<STALE_S and not req.get('spawn_failed'):return row
            if row['resumes']<1:
                row.update(status='queued',resumes=row['resumes']+1,placement=claim['owner'],
                           workdir=claim.get('workdir'),not_before=now,resume_phase=claim.get('phase'))
                row.pop('claim',None)
            else:finish(row,dict(status='blocked',reason='runner exited without an outcome after one recovery',next_action='Inspect retained work and resume with batch.py takeover'))
        else:raise ValueError('unknown operation '+op)
        write(p/'state.json',state);return row


def fingerprints():
    """Bind installed source bytes to pushed Git objects, not the shared checkout's dirty HEAD."""
    files=subprocess.check_output(['git','ls-tree','-rz','origin/main','--',*SOURCE_ROOTS],cwd=eq.ROOT)
    hashes={};dirty=[]
    for record in files.split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,typ,blob=meta.decode().split();name=name.decode()
        p=Path(eq.ROOT)/name
        if p.suffix not in ('.py','.json','.sh','.plist','.md','.js','.css','.html','.c') or p.name in ('scoreboard.json','review-snapshot.html'):continue
        if not p.exists():dirty.append(name+': missing');continue
        data=os.readlink(p).encode() if mode=='120000' and p.is_symlink() else p.read_bytes()
        gitsha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if gitsha!=blob:dirty.append(name)
        hashes[name]=hashlib.sha256(data).hexdigest()
    canary=read(HOME/'canary-latest.json',{})
    digest=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    launcher_ok=(canary.get('launcher_sha256')==hashlib.sha256(Path(eq.__file__).read_bytes()).hexdigest() and canary.get('executors_sha256')==hashlib.sha256(json.dumps(eq.load_config()['executors'],sort_keys=True).encode()).hexdigest())
    return dict(host=here(),launcher_ok=launcher_ok,hashes=hashes,digest=digest,dirty=dirty,canary=canary,
                commit=subprocess.check_output(['git','rev-parse','origin/main'],cwd=eq.ROOT,text=True).strip())


def preflight():
    local=fingerprints();other='m2' if here()=='m6' else 'm6'
    remote_fp=remote(other,['fingerprints'])
    problems=[]
    for fp in (local,remote_fp):
        if fp['dirty']:problems.append(fp['host']+' source differs from pushed main: '+', '.join(fp['dirty']))
        if not fp['launcher_ok'] or not fp['canary'].get('passed') or len(fp['canary'].get('rows',[]))!=4:problems.append(fp['host']+' real-session canary incomplete')
    if local['hashes']!=remote_fp['hashes']:problems.append('scheduler hashes differ between Macs')
    proof=dict(passed=not problems,at=time.time(),digest=local['digest'],problems=problems,
               hosts={f['host']:dict(commit=f['commit'],canary=f['canary'].get('id')) for f in (local,remote_fp)})
    rpc('preflight',proof=proof);return proof


def identity(pid):
    if not pid:return None
    try:
        os.kill(int(pid),0)
        p=subprocess.run(['/bin/ps','-p',str(int(pid)),'-o','lstart='],capture_output=True,text=True,timeout=3)
        return p.stdout.strip() if p.returncode==0 else None
    except (OSError,ValueError,subprocess.SubprocessError):return None


def alive(pid,birth):return bool(birth and identity(pid)==birth)


def kick(other=False):
    label='gui/'+str(os.getuid())+'/com.absbyai.edit-queue'
    subprocess.run(['launchctl','kickstart',label],capture_output=True,timeout=5)
    if other:
        target='m2' if here()=='m6' else 'm6'
        try:
            subprocess.run(['ssh','-oBatchMode=yes','-oConnectTimeout=3',target,
                            'launchctl kickstart gui/$(id -u)/com.absbyai.edit-queue'],capture_output=True,timeout=8)
        except subprocess.SubprocessError:pass


def save_snapshot(snap):
    write(HOME/'snapshot.json',snap)
    registrations={}
    ordered=sorted(((n,k,r) for n,d in snap['batches'].items() for k,r in d['jobs'].items()),key=lambda x:x[2]['queued_at'])
    for n,k,r in ordered:
        if r['status']=='taken-over':registrations.pop(r['id'],None)
        else:registrations[r['id']]=dict(batch=n,key=k,status=r['status'],token=(r.get('claim') or {}).get('token'))
    write(HOME/'registrations.json',registrations)


def guard(job):
    row=read(HOME/'registrations.json',{}).get(job)
    if row and row['status']=='claimed' and row.get('token')==os.environ.get('EDIT_BATCH_TOKEN'):return None
    return row


def flush_outbox():
    for p in sorted((HOME/'outbox').glob('*.json')):
        request=read(p)
        try:
            pending=request['outcome'].pop('pending_review',None)
            if pending:
                request['outcome']['link']=eq.sibling('batch_runner').review_link(pending)
            rpc(**request);p.unlink()
        except (OSError,RuntimeError,subprocess.SubprocessError):
            continue


def update(op, batch, k, token, **kwargs):
    request=dict(op=op,batch=batch,key=k,token=token,host=here(),**kwargs)
    try:return rpc(**request)
    except (OSError,RuntimeError,subprocess.SubprocessError):
        # Heartbeats do not queue: after reconnect the live process sends a fresh one.
        if op=='outcome':write(HOME/'outbox'/(token+'.json'),request)
        return None


def observe_local():
    reg=read(Path('/tmp/absbyai-editcap')/'registry.json',{})
    result={j:dict(state=e.get('state'),since=e.get('since')) for j,e in reg.get('edits',{}).items()}
    cap=subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'status','--json'],capture_output=True,text=True,timeout=30)
    if cap.returncode==0:
        ec=json.loads(cap.stdout);result['_capacity']=dict(free=max(0,ec['cap']-len(ec['in_use'])))
    return result


def reconcile(snap):
    for n,d in snap['batches'].items():
        for k,row in d['jobs'].items():
            if row['status']!='claimed':continue
            c=row['claim']
            if c['owner']!=here():continue
            if (HOME/'outbox'/(c['token']+'.json')).exists():continue
            local=read(HOME/'runs'/c['token']/'progress.json',{})
            if local.get('pid') and (not c.get('pid') or local['pid']==c['pid']):
                c=dict(c, **local)
            if alive(c.get('pid'),c.get('birth')):
                progress_path=HOME/'runs'/c['token']/'progress.json'
                fresh=progress_path.exists() and time.time()-progress_path.stat().st_mtime<STALE_S
                if fresh:continue
                if time.time()-c['heartbeat']<STALE_S:continue
                stopfile=HOME/'runs'/c['token']/'runner-stop.json';prior=read(stopfile,{})
                os.kill(c['pid'],signal.SIGKILL if prior.get('at') and time.time()-prior['at']>30 else signal.SIGTERM)
                if not prior:write(stopfile,dict(at=time.time()))
                continue
            if time.time()-c['heartbeat']<STALE_S:continue
            session=c.get('session',{})
            live=alive(session.get('pid'),session.get('birth'))
            if live:
                # Only the recorded orphan's exact process group, never another editor's processes.
                stopfile=HOME/'runs'/c['token']/'orphan-stop.json'
                previous=read(stopfile,{})
                force=previous.get('at') and time.time()-previous['at']>30
                try:os.killpg(session['pid'],signal.SIGKILL if force else signal.SIGTERM)
                except ProcessLookupError:pass
                if not previous:write(stopfile,dict(at=time.time(),pid=session['pid'],birth=session['birth']))
                # A following tick confirms that group exited before any recovery claim.
                continue
            rpc('recover',batch=n,key=k,token=c['token'],host=here(),pid_alive=False,session_alive=False)


def report(snap, error=None):
    """Saved on M6 every tick, including when the M2 link is down."""
    groups={x:[] for x in ('Checked','Unreviewed','Needs Dan','Blocked','Unknown (Mac unreachable)','Queued / Running')}
    now=time.time()
    for name,d in snap.get('batches',{}).items():
        for k,r in d['jobs'].items():
            if r['status']=='taken-over':continue
            owner=(r.get('claim') or {}).get('owner',r.get('placement'))
            c=r.get('claim') or {};last_tick=d.get('ticks',{}).get(owner,0)
            unknown=bool(error) or (r['status']=='claimed' and now-last_tick>STALE_S)
            group='Unknown (Mac unreachable)' if unknown else {'delivered':'Checked','delivered-unreviewed':'Unreviewed','needs-dan':'Needs Dan','blocked':'Blocked'}.get(r['status'],'Queued / Running')
            o=r.get('outcome',{});link=o.get('link','');verified=False
            if link and here()=='m6':
                try:
                    import urllib.request
                    with urllib.request.urlopen(link,timeout=3) as response:verified=response.status==200
                except Exception:pass
            item=dict(batch=name,job=r['id'],round=r['round'],title=r['title'],host=owner,status=r['status'],
                      reason='owner unreachable' if unknown else o.get('reason') or o.get('question') or c.get('phase') or ('paused-for-allowance until '+str(r['not_before']) if r['not_before']>now else 'queued'),
                      link=link,link_verified=verified,timing=r.get('timing',{}),allowance_pauses=r.get('allowance_pauses',[]),idle_slot_minutes_sampled=r.get('idle_slot_minutes',0),queue_wait_s=max(0,r.get('first_started',now)-r['queued_at']))
            if r['status']=='needs-dan':item['waiting_s']=now-r.get('ended',now)
            groups[group].append(item)
    lost=[]
    if here()=='m6':
        catalog={r['id']:r for r in read(Path(eq.ROOT)/'Handoffs/video-editing/jobs.json',{'jobs':[]})['jobs']}
        route=read(Path.home()/'.absbyai-editroute/waiting.json',{})
        obs=d.get('observations',{}) if snap.get('batches') else {}
        # Combined-line promotions are journalled even after waiting.json is popped.
        path=Path.home()/'.absbyai-editroute/decisions.jsonl'
        try:
            entries=[json.loads(line) for line in path.read_text().splitlines()[-2000:]]
            latest={e['job']:e for e in entries if not e.get('dry')}
            for j,e in latest.items():
                if catalog.get(j,{}).get('state') in ('delivered','draft_review','finalized','uploaded'):continue
                if e.get('host') in ('m2','m6') and e.get('from_line') and 600<now-e['t']<86400:
                    observed=[v.get(j) for dd in snap.get('batches',{}).values() for v in dd.get('observations',{}).values()]
                    if not any(observed):lost.append(j+' LOST: promoted without editcap entry after 10 minutes')
        except (OSError,ValueError,KeyError):pass
    doc=dict(at=now,start_block=snap.get('start_block'),enabled=snap.get('control',{}).get('enabled',False),error=error,groups=groups,lost=lost)
    write(HOME/'morning-report.json',doc)
    lines=['# Overnight edit report','',time.strftime('%Y-%m-%d %H:%M:%S %Z'),'', 'New starts: '+('enabled' if doc['enabled'] else 'disabled')]
    if error:lines+=['',error]
    if doc['start_block']:lines+=['','New starts blocked: '+doc['start_block']]
    for group,rows in groups.items():
        lines+=['','## '+group,'','| Video | Mac | State / next action | Review |','|---|---|---|---|']
        for r in rows:
            label='Open review' if r['link_verified'] else 'Link unverified'
            link='['+label+']('+r['link']+')' if r['link'] else ''
            lines.append('| '+r['title'].replace('|','/')+' ('+r['job']+' R'+str(r['round'])+') | '+str(r['host'])+' | '+str(r['reason']).replace('|','/')+' | '+link+' |')
    lines+=['',*lost]
    (HOME/'morning-report.md').write_text('\n'.join(lines)+'\n')
    return doc


def tick():
    HOME.mkdir(parents=True,exist_ok=True)
    with (HOME/'tick.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return dict(busy=True)
        try:
            flush_outbox()
            snap=rpc('tick',host=here(),observation=observe_local());save_snapshot(snap)
            reconcile(snap)
            fp=fingerprints()
            start_block=('installed source differs from pushed main: '+', '.join(fp['dirty'])) if fp['dirty'] else ('scheduler changed since preflight' if snap['control'].get('enabled') and fp['digest']!=snap['control'].get('preflight',{}).get('digest') else None)
            if not start_block:
                while True:
                    cap=subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'status','--json'],capture_output=True,text=True,timeout=30)
                    if cap.returncode:raise RuntimeError('editcap status unavailable: '+cap.stderr[-300:])
                    ec=json.loads(cap.stdout)
                    owned=rpc('claim',host=here(),digest=fp['digest'],occupied=ec['in_use'],slots=ec['cap'])
                    if not owned:break
                    snap=rpc('snapshot');save_snapshot(snap)
                    row=owned['row'];token=row['claim']['token']
                    claim_home=HOME/'runs'/token;claim_home.mkdir(parents=True,exist_ok=True)
                    write(claim_home/'claim.json',owned)
                    log=(claim_home/'runner.log').open('a')
                    try:
                        proc=subprocess.Popen([sys.executable,str(Path(eq.HERE)/'runner.py'),'--batch',str(claim_home/'claim.json')],cwd=eq.ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
                        update('heartbeat',owned['batch'],owned['key'],token,fields=dict(pid=proc.pid,birth=identity(proc.pid)))
                    except OSError:
                        rpc('recover',batch=owned['batch'],key=owned['key'],token=token,host=here(),pid_alive=False,spawn_failed=True)
                    finally:log.close()
            snap=rpc('snapshot');save_snapshot(snap)
            if start_block:snap['start_block']=start_block
            doc=report(snap)
            print('Batch tick:',here(),'new starts',snap['control'].get('enabled',False),flush=True)
            return doc
        except (OSError,RuntimeError,subprocess.SubprocessError) as exc:
            doc=report(read(HOME/'snapshot.json',{}),str(exc))
            print('Batch tick unavailable:',exc,flush=True);return doc


def enqueue(name,path):
    source=Path(path).resolve();request=json.loads(source.read_text())
    jobs=[];briefs={}
    # Source location and owner are inspected once at enqueue, before accepting the work.
    sys.path.insert(0,str(SHARED/'editroute'));import editroute
    for i,j in enumerate(request['jobs']):
        job=dict(j);job['id']=job['id'].upper()
        if not JOB.fullmatch(job['id']):raise ValueError('invalid job ID')
        if job.get('size') not in ('L','M','S') or int(job.get('round',0))<1:raise ValueError('size and positive round required')
        if job.get('executor') not in ('claude','codex'):raise ValueError('preserve an explicit editor for each job')
        if not job.get('title') or not job.get('kind') or not job.get('target'):raise ValueError('title, kind and target required')
        if float(job.get('need_gb',0))<=0:raise ValueError('honest additional storage need_gb required')
        job['order']=job.get('order',i);job['round']=int(job['round'])
        job['chroma']=bool(job.get('chroma'));job['drive_bound']=bool(job.get('drive_bound'))
        statuses=editroute.gather(job['id']);owner,_=editroute.holder(job['id'],statuses)
        if any(not st.get('reachable') for st in statuses.values()):raise ValueError('both Macs must be reachable to establish placement at enqueue')
        if any(job['id'] in st.get('editcap',{}).get('in_use',[]) for st in statuses.values()):
            raise ValueError(job['id']+' has active production; batch enqueue cannot transfer a live chat')
        if owner:placement=owner
        elif job['kind']=='LFC' or job['chroma'] or job['drive_bound']:placement='m2'
        else:placement='any'
        job['placement']=placement
        brief=Path(job.pop('brief'));brief=brief if brief.is_absolute() else source.parent/brief
        data=brief.read_bytes();job['brief_sha256']=hashlib.sha256(data).hexdigest()
        briefs[key(job)]=base64.b64encode(data).decode();jobs.append(job)
    result=rpc('enqueue',batch=name,jobs=jobs,briefs=briefs)
    kick(other=True)
    result['receipt']='registered; waiting for both Macs to log this batch'
    return result


def receipt(name):
    snap=rpc('snapshot');d=snap['batches'][name]
    observed=all(d.get('ticks',{}).get(h,0)>=d['manifest']['created'] for h in ('m2','m6'))
    return dict(batch=name,receipt='queued' if observed else 'registered; waiting for both ticks',enabled=d['enabled'],ticks=d['ticks'],jobs=list(d['jobs']))


def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('_rpc');sub.add_parser('fingerprints');sub.add_parser('preflight');sub.add_parser('tick');sub.add_parser('stop');sub.add_parser('status')
    p=sub.add_parser('enqueue');p.add_argument('batch');p.add_argument('manifest')
    p=sub.add_parser('enqueue-chat');p.add_argument('job');p.add_argument('--brief',required=True)
    p.add_argument('--round',type=int,required=True);p.add_argument('--title',required=True)
    p.add_argument('--size',choices=['S','M','L'],required=True);p.add_argument('--kind',required=True)
    p.add_argument('--executor',choices=['claude','codex'],required=True);p.add_argument('--need-gb',type=float,required=True)
    p.add_argument('--target',required=True);p.add_argument('--chroma',action='store_true')
    p=sub.add_parser('receipt');p.add_argument('batch')
    p=sub.add_parser('start');p.add_argument('batch')
    p=sub.add_parser('takeover');p.add_argument('job')
    p=sub.add_parser('guard');p.add_argument('job')
    args=ap.parse_args()
    if args.cmd=='_rpc':result=handle(json.load(sys.stdin))
    elif args.cmd=='fingerprints':result=fingerprints()
    elif args.cmd=='preflight':result=preflight()
    elif args.cmd=='tick':result=tick()
    elif args.cmd=='enqueue':result=enqueue(args.batch,args.manifest)
    elif args.cmd=='enqueue-chat':
        spec=HOME/'chat-submissions'/(args.job+'-R'+str(args.round)+'.json')
        write(spec,dict(jobs=[dict(id=args.job,round=args.round,title=args.title,size=args.size,kind=args.kind,
                                  executor=args.executor,need_gb=args.need_gb,target=args.target,chroma=args.chroma,
                                  brief=str(Path(args.brief).resolve()))]))
        result=enqueue('chat-'+args.job+'-R'+str(args.round),spec)
    elif args.cmd=='receipt':result=receipt(args.batch)
    elif args.cmd=='start':
        proof=preflight()
        if not proof['passed']:raise RuntimeError('; '.join(proof['problems']))
        result=rpc('start',batch=args.batch,digest=proof['digest']);kick(other=True)
    elif args.cmd=='stop':result=rpc('stop')
    elif args.cmd=='takeover':
        result=rpc('takeover',job=args.job,host=here());save_snapshot(rpc('snapshot'));kick(other=True)
    elif args.cmd=='guard':
        result=guard(args.job)
        if result:print(json.dumps(result));return 3
    else:result=rpc('snapshot')
    print(json.dumps(result,indent=2));return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(1)
